#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from scipy.ndimage import filters

def final_pro(image1,image2) :
	width = image1.size[0]
	height = image1.size[1]
	iFinal = Image.new("L",(width,height),255)
	for y in range(height) :
		for x in range(width) :
			temp1 = image1.getpixel((x,y))
			temp2 = image2.getpixel((x,y))
			if temp1 == temp2 and temp1 != 255 :
				iFinal.putpixel((x,y),temp1)
			elif temp1 != temp2 :
				iFinal.putpixel((x,y),255)
	return iFinal
	
im1 = Image.open("D:\\Python27\\picture\\1_rebuild.bmp")
im2 = Image.open("D:\\Python27\\picture\\1_result.bmp")
im1 = im1.convert("L")
im2 = im2.convert("L")
iFinal = final_pro(im1,im2)
iFinal.save("D:\\Python27\\picture\\1_seg.bmp","BMP")
				