import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from matplotlib.widgets import Button, Slider

images_folder = "t1"
os.chdir(images_folder)
image_files = os.listdir()
RED = np.array([255,0,0])
BLUE = np.array([83,152,108])
def proccess_image(fn):

	def update_mask(color):
		deltas = np.abs(data-color)
		deltas = np.logical_and.reduce([deltas[:,:,i]<buf_slider.val for i in range(3)])
		mask = data.copy()
		mask[deltas]=RED
		im.set_data(mask)
		plt.pause(.01)

	def get_rgb_from_click(event):
		if event.inaxes: # Check if the click was within the axes
			RGB_data = data[int(event.ydata),int(event.xdata)]
			print(RGB_data)
			#update_mask(RGB_data)
			update_mask(BLUE)

	data = np.array(Image.open(fn).convert('RGB'))
	fig,ax = plt.subplots()

	# Make a horizontal slider to control the frequency.
	axbuf = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
	buf_slider = Slider(ax=axbuf,label='Buffer',valmin=10,valmax=1000,valinit=100,orientation="vertical")
	im = ax.imshow(data)
	cid = fig.canvas.mpl_connect('button_press_event', get_rgb_from_click)
	plt.show()


for image_file in image_files[2:]:
	proccess_image(image_file)