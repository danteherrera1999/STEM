import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from matplotlib.widgets import Button, Slider

images_folder = "jello_blue"
os.chdir(images_folder)
image_files = os.listdir()
DR = 300
CENTER = [699, 1972]
RED = np.array([255,0,0])
BLUE = np.array([83,152,108])
BUFFER =149
def proccess_image(fn):

	def update_mask(self,center=CENTER):
		pixlocs=np.array(np.meshgrid(np.arange(data.shape[0]),np.arange(data.shape[1]))).T
		pix = np.logical_and.reduce([data[:,:,i]<buf_slider.val for i in range(3)]+[pixlocs[:,:,0]>(center[0]-DR/2),pixlocs[:,:,1]>(center[1]-DR/2),pixlocs[:,:,0]<(center[0]+DR/2),pixlocs[:,:,1]<(center[1]+DR/2)])
		# pix = np.logical_and.reduce([pixlocs[:,:,0]>(center[0]-DR/2),pixlocs[:,:,1]>(center[1]-DR/2),pixlocs[:,:,0]<(center[0]+DR/2),pixlocs[:,:,1]<(center[1]+DR/2)])
		counts = np.sum(pix)
		print(counts)
		mask = data.copy()
		mask[pix]=RED
		im.set_data(mask)

	def get_rgb_from_click(event):
		if event.inaxes: # Check if the click was within the axes
			RGB_data = data[int(event.ydata),int(event.xdata)]
			print([int(event.ydata),int(event.xdata)])

	data = np.array(Image.open(fn).convert('RGB'))
	fig,ax = plt.subplots()

	axbuf = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
	buf_slider = Slider(ax=axbuf,label='Buffer',valmin=10,valmax=200,valinit=110,orientation="vertical")
	buf_slider.on_changed(update_mask)
	im = ax.imshow(data)
	update_mask(None)
	cid = fig.canvas.mpl_connect('button_press_event', get_rgb_from_click)
	plt.show()


for image_file in image_files[:1]:
	proccess_image(image_file)