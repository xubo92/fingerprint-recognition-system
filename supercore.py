#  #!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw
import numpy as np
from scipy.ndimage import filters

def ComplexFilter(image,variance,order) :
	x = range(-200,201,1)
	y = range(-200,201,1)
	width  = len(x)
	height = len(y)
	SD     = np.sqrt(variance) # 标准差
	gamma  = 2                 # 参数伽马
    iCore  = np.zeros((width,height))
	
	for m in range(1,width) :
		for n in range(1,height) :
			exponent = np.exp(-(x[m]**2+y[n]**2) /(2*(SD**2)))
			factor = x[m] + j * y[n]
			iCore[m,n] = exponent * (factor ** order) 
			
	img = np.array(image)
	gx  = np.zeros((img.shape))
	gy  = np.zeros((img.shape))
	
	z   = np.zeros((img.shape))
	filters.sobel(img,1,gx)
	filters.sobel(img,0,gy)
	num = (gx + i * gy) ** 2
	den = abs((gx + i * gy) ** 2)
	pos = np.nonzero(den)
	for i in range(len(pos[0])) :
		temp1 = pos[0][i]
		temp2 = pos[1][i]
		num[temp1][temp2] = num[temp1][temp2] / den[tem1][temp2]
		z[temp1][temp2]   = num[temp1][temp2]
	pos = np.nonzero(den == 0)
	for i in range(len(pos[0])) :
		temp1 = pos[0][i]
		temp2 = pos[1][i]
		z[temp1][temp2] = 1
	
	
	
	
			
	