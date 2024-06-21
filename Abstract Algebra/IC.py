import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

loan_term_years = 30
loan_term_months = loan_term_years * 12
tax_rate = 24+4.7
principal = 300000


M = lambda n,r_l: principal * (r_l/100/12)*(1+r_l/100/12)**n / ((1+r_l/100/12)**n-1)
total_paid = lambda n,r_l: M(n,r_l)*n
interest_paid= lambda n,r_l: total_paid(n,r_l) - principal
total_gained = lambda n,r_g: principal * (1 + r_g/12/100)**n
interest_gained = lambda n,r_l,r_g: ( total_gained(n,r_g) - principal - mpil(n,r_l,r_g) ) * (1-tax_rate/100)

def mpil(n,r_l,r_g):
	m = M(n,r_l)
	tg = np.zeros(n.size)
	for i in range(n[-1]+1):
		tg *= np.where(n>i,1+r_g/100/12,1)
		tg += np.where(n>i,m,0)
	return tg - m*n

d = np.arange(1,loan_term_years*12)

fig,ax = plt.subplots()

# Make a horizontal slider to control the investment APR
ax_r_g = fig.add_axes([0.25, 0.02, 0.65, 0.03])
r_g_slider = Slider(ax=ax_r_g,label='Investment APR',valmin=1,valmax=10,valinit=4.6)

# Make a horizontal slider to control the investment APR
ax_r_l = fig.add_axes([0.25, 0.04, 0.65, 0.03])
r_l_slider = Slider(ax=ax_r_l,label='Loan APR',valmin=1,valmax=10,valinit=5.5)

ax.set_xlabel('Loan Term (years)')
ax.set_ylabel('Dollars')
ax.ticklabel_format(useOffset=False,style="plain")

ln_l, = ax.plot(d/12,interest_paid(d,5.5),c='r',label=f"Net Interest Paid")
ln_g, = ax.plot(d/12,interest_gained(d,5.5,4.6),c='g',label=f"Net Investment Profits")
ax.legend(loc='upper left')
def update(i):
		ln_l.set_ydata(interest_paid(d,r_l_slider.val))
		ln_g.set_ydata(interest_gained(d,r_l_slider.val,r_g_slider.val))

r_l_slider.on_changed(update)
r_g_slider.on_changed(update)

plt.show()





