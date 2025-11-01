import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from matplotlib.widgets import Button, Slider
from datetime import datetime
import re

images_folder = "Jello_hot"
os.chdir(images_folder)
image_files = [fn for fn in os.listdir() if '.jpg' in fn]
DR = 1000
CENTER = [947, 1644]
RED = np.array([255,0,0])
BLUE = np.array([83,152,108])
BUFFER =100
template = np.array(Image.open(image_files[0]).convert('RGB'))
PIXLOCS=np.array(np.meshgrid(np.arange(template.shape[0]),np.arange(template.shape[1]))).T
dt_0 = datetime(*[int(n) for n in re.split(r'[-_]+',image_files[0][8:-4])]).timestamp()
def proccess_image(fn): 
	data = np.array(Image.open(fn).convert('RGB'))
	pix = np.logical_and.reduce([data[:,:,i]<BUFFER for i in range(3)]+[PIXLOCS[:,:,0]>(CENTER[0]-DR/2),PIXLOCS[:,:,1]>(CENTER[1]-DR/2),PIXLOCS[:,:,0]<(CENTER[0]+DR/2),PIXLOCS[:,:,1]<(CENTER[1]+DR/2)])
	counts = np.sum(pix)
	print(counts)
	mask = data.copy()
	mask[pix]=RED
	
	return counts


COUNTS = []

for image_file in image_files:
	dt = datetime(*[int(n) for n in re.split(r'[-_]+',image_file[8:-4])]).timestamp()
	COUNTS.append([dt-dt_0,proccess_image(image_file)])

np.savetxt(images_folder+'_COUNTS.csv',COUNTS,delimiter=',',fmt='%f')