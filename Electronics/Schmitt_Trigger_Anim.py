from manim import *
import os 
import re 
from ast import literal_eval

"""
This is my first project with manim,
I built a custom "WirePath" class which allows me to easily animate current flow over existing manim circuit infrastructure through LaTeX's circuitikz module.
This is a simple demo with an RC schmitt trigger circuit operating as a bistable multivibrator to create a sawtooth wave.
"""

vlen = lambda vec: np.sqrt(np.sum(vec**2))
sf = .705
class WirePath:
    def __init__(self,path_str,aux_str='',dot_offsets=(0,0),dots=0, dot_velocity=0,dot_color=WHITE,vt=None,vg_shift=(0,0),vg_scale=1,dot_phase_function=None):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")
        self.vg_shift =vg_shift
        self.vg_scale = vg_scale
        self.vertices = np.array([literal_eval(point) for point in re.findall(r'\([0-9,.]+\)',path_str)]).astype(float)*self.vg_scale
        self.dVs = self.vertices[1:]-self.vertices[:-1]
        self.Mags = np.sqrt(np.sum(self.dVs**2,axis=1))
        self.norm_dVS=np.array([self.dVs[i]/self.Mags[i] for i in range(len(self.Mags))])
        self.segments = np.cumsum(np.concatenate(([0],self.Mags)))
        self.L = sum(self.Mags)
        self.N = dots
        self.dl = self.L/self.N
        self.dot_velocity=dot_velocity
        self.dot_color = dot_color
        self.vt = vt
        self.dot_phase_function = dot_phase_function
        dummywire = self.wire = MathTex(r"\draw "+f"{'--'.join([str(tuple(point)) for point in self.vertices])};",stroke_width=3,stroke_opacity=1,tex_environment="circuitikz",tex_template=template).scale(sf)
        self.dims=np.array([dummywire.width,dummywire.height])
        self.offsets = dot_offsets
        self.wire = MathTex(
            r"\draw "+f"{path_str};",
            aux_str,
            stroke_width=3,
            stroke_opacity=1,
            tex_environment="circuitikz",
            tex_template=template
            )

        self.wire.scale(sf).scale(self.vg_scale) # Scale to match manim grid
        self.dots = always_redraw(self.update_dots)
        self.VGroup = VGroup()
        self.VGroup.add(self.wire.shift((*self.vg_shift,0)),self.dots)

    def update_dots(self):
        dot_phase,dot_color = self.dot_phase_function(self.vt.get_value())
        dots = []
        for i in range(self.N):
            l = self.dl*(i+dot_phase)%self.L
            start_point = np.argwhere(l>=self.segments)[-1,0]
            dot_pos = self.vertices[start_point]+(l-self.segments[start_point])*self.norm_dVS[start_point]
            dots.append(Dot(point=(*dot_pos,0),color=dot_color,radius=.06))
        return VGroup(*dots).shift((*(self.dims/-2+self.offsets),0)).shift((*self.vg_shift,0))


class ST_animation(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")
        t = ValueTracker(0)
        V_s = 5 # ST Rail Voltage
        V_upper_thresh = 4 # Upper Voltage Threshold
        V_lower_thresh = 1 # Lower Voltage Threshold
        tau = 1 # Time constant in seconds
        t_L = tau*np.log(V_s/(V_s-V_lower_thresh)) # Time at Lower Threshold
        t_U = tau*np.log(V_s/V_upper_thresh) # Time at Upper Threshold
        axes = Axes(x_range=(0,10,1),y_range=(0,10,1),y_length=5)
        labels=axes.get_axis_labels(Text('Time (s)').scale(.6),Tex(r"$V_c$ (V)"))
        C = 100e-9 # Capaitance in Farad
        R = tau/C # Resistance in Ohms
        dt_up= tau * np.log((V_s-V_lower_thresh)/(V_s-V_upper_thresh)) # Ascending Period
        dt_down = tau * np.log(V_upper_thresh/V_lower_thresh) # Descending Period
        T = dt_up+dt_down # Full Cycle Period

        def V_arr(t):
            tp = t%(T)
            return np.where(tp<=dt_up,V_s * (1 - np.exp(-(tp+t_L)/tau)),V_s * np.exp(-(tp+t_U-dt_up)/tau))
        def V_str():
            tp = t.get_value()%(T)
            ascending = tp<=dt_up
            V_p = V_s * (1 - np.exp(-(tp+t_L)/tau)) if ascending else V_s * np.exp(-(tp+t_U-dt_up)/tau)
            V_p = "{:.2f}".format(V_p) + " V"
            return Text(V_p,font="Times New Roman",font_size=20,color=GREEN if ascending else RED).set_x(1.15).set_y(-.16)
        def dot_phase(t):
            tp = t%(T)
            ascending = tp<=dt_up
            V_p = V_s * (1 - np.exp(-(tp+t_L)/tau)) if ascending else V_s * np.exp(-(tp+t_U-dt_up)/tau)
            phi_max = 5
            #dot_phase = phi_max * (tp/dt_up if ascending else (1- (tp-dt_up)/dt_down))
            dot_phase = phi_max * (1-(V_s-V_p)/(V_s-V_lower_thresh) if ascending else (V_p-V_lower_thresh)/(V_upper_thresh-V_lower_thresh))
            return dot_phase,GREEN if ascending else RED
        Voltage_plot = always_redraw(lambda: axes.plot(V_arr, x_range=(0,t.get_value(),.001),color=TEAL,use_smoothing=False))
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage[siunitx, RPvoltages, american]{circuitikz}")

        #Build Circuit
        circuit= WirePath(r"(6.45,3)--(9,3)--(9,6) to[resistor] (3,6) -- (3,3) to[capacitor,v=$V_c$] (3,0);",
            aux_str=r"""\draw (6,3) node[invschmitt](ST){} (3,3) -- (ST.in) (ST.out) -- (9,3) (3,0) node[ground]{};""",
            dot_offsets=(-1.255,.08),
            dots=15,
            dot_velocity=2,
            dot_color=GREEN,
            vt=t,
            vg_shift=(4.5,1.5),
            vg_scale=.5,
            dot_phase_function=dot_phase
        )


        #Begin Animation
        self.play(Write(axes),Write(Voltage_plot),Write(labels),Write(circuit.VGroup))
        self.wait(2)

        #Run time set
        self.play(t.animate.set_value(10),rate_func=linear,run_time=20)
        #End Animation
        self.play(FadeOut(axes,Voltage_plot,circuit.VGroup,labels))

if __name__ == "__main__":
    os.system("manim Schmitt_Trigger_Anim.py -pql ST_animation")