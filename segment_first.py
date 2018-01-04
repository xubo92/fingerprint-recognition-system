#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from scipy.ndimage import filters

gauess_filter_operator = [0.0000,0.0001,0.0010,0.0016,0.0010,0.0001,0.0000,
 0.0001,0.0027,0.0129,0.0214,0.0129,0.0027,0.0001,
 0.0010,0.0129,0.0582,0.0960,0.0582,0.0129,0.0010,
 0.0016,0.0214,0.0960,0.1586,0.0960,0.0214,0.0016,
 0.0010,0.0129,0.0582,0.0960,0.0582,0.0129,0.0010,
 0.0001,0.0027,0.0129,0.0214,0.0129,0.0027,0.0001,
 0.0000,0.0001,0.0010,0.0016,0.0010,0.0001,0.0000]
 
 
structure_data_one = [0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 , 
				      0 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,
				      0 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,0 ,
				      0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0]
structure_data_two = [0,0,0,1,0,0,0,
				      0,0,1,1,1,0,0,
				      0,1,1,1,1,1,0,
				      0,1,1,1,1,1,0,
				      0,1,1,1,1,1,0,
				      0,0,1,1,1,0,0,
				      0,0,0,1,0,0,0]
structure_data_three = [1,1,1,1,1,
						1,1,1,1,1,
						1,1,1,1,1,
						1,1,1,1,1,
						1,1,1,1,1]
				  
def Corrode(image,structure_data,radius) :
	structure_num = (2 * radius + 1) ** 2
	flag = 0
	valid_data = 0
	width = image.size[0]
	height = image.size[1]
	iCorrode = Image.new("L",(width,height),255)
	KH = range(radius) + range(height-radius,height)
	KL = range(radius) + range(width-radius,width)
	for k in range(structure_num) :
		if structure_data[k] == 1 :
			valid_data += 1
	for y in range(height) :
		for x in range(width) :
			if y in KH or x in KL :
				iCorrode.putpixel((x,y),0)
			elif image.getpixel((x,y)) == 255 :
				iCorrode.putpixel((x,y),255)
			else :
				flag = 0                       															# 要始终记得变量清零
				for n in range(2 * radius + 1) :
					for m in range(2 * radius + 1) :
						if structure_data[(structure_num - 1) - (n*(2*radius+1) + m)]  == 1 and image.getpixel((x-radius+m,y-radius+n)) == 0 :
							flag += 1
						else :
							continue
				if flag == valid_data :
					iCorrode.putpixel((x,y),0)
				else :
					iCorrode.putpixel((x,y),255)
	return iCorrode

def Expand(image,structure_data,radius) :
	structure_num = (2 * radius + 1) ** 2
	width = image.size[0]
	height = image.size[1]
	KH = range(radius) + range(height-radius,height)
	KL = range(radius) + range(width-radius,width)
	iExpand = Image.new("L",(width,height),255)
	for y in range(height) :
		for x in range(width) :
			if y in KH or x in KL :
				iExpand.putpixel((x,y),0)
			else :
				for n in range(2 * radius + 1) :
					for m in range(2 * radius + 1) :
						if -1 < x - radius + m < width and -1 < y - radius + n < height and structure_data[(structure_num - 1) - (n*(2*radius+1) + m)]  == 1 and image.getpixel((x-radius+m,y-radius+n)) == 0 :
							iExpand.putpixel((x,y),0)
							break
					break
	return iExpand
def Close(image,structure_data,radius) :
	iExpand = Expand(image,structure_data,radius) 
	iCorrode = Corrode(iExpand,structure_data,radius) 
	iClose = iCorrode
	return iClose
def Open(image,structure_data,radius) :
	iCorrode = Corrode(image,structure_data,radius)
	iExpand = Expand(iCorrode,structure_data,radius) 
	iOpen = iExpand
	return iOpen
def Convolution(image,operator,radius) :
	operator_num = (2 * radius + 1) ** 2
	width = image.size[0]
	height = image.size[1]
	iConvolution = Image.new("L",(width,height),255)
	for y in range(height) :
		for x in range(width) :
			sum = 0.0
			for n in range(2 * radius + 1) :
				for m in range(2 * radius + 1) :
					if -1 < x - radius + m < width and -1 < y - radius + n < height :
						sum += operator[(operator_num - 1) - (n*(2*radius+1) + m)] * image.getpixel((x-radius+m,y-radius+n))
					else :
						continue
			iConvolution.putpixel((x,y),int(sum))
	return iConvolution
			
# 求梯度函数
def Magnitude(image) :
	im = array(image)
	imx = zeros(im.shape)
	filters.sobel(im,1,imx)
	imy = zeros(im.shape)
	filters.sobel(im,0,imy)
	magnitude = sqrt(imx ** 2 + imy ** 2)
	mag = Image.fromarray(magnitude)
	return mag

def Binary(image) :
	width = image.size[0]
	height = image.size[1]
	iBinary = Image.new("L",(width,height),255)
	sum = 0
	for y in range(height) :
		for x in range(width) :
			sum += image.getpixel((x,y))
	Threshold = sum / (height * width)
	for y in range(height) :
		for x in range(width) :
			if image.getpixel((x,y)) > Threshold :
				iBinary.putpixel((x,y),255)
			else :
				iBinary.putpixel((x,y),0)
	return iBinary


	
def Segment(image,structure_data,radius1) :
	iMagnitude = Magnitude(image)
	# iConvolution = Convolution(iMagnitude,operator,radius2)
	iBinary = Binary(iMagnitude)
	iClose = Close(iBinary,structure_data,radius1)
	iOpen = Open(iClose,structure_data,radius1)
	height = image.size[1]
	width  = image.size[0]
	iRebuild = Image.new("L",(width,height),255)
	for y in range(height) :
		for x in range(width) :
			if iOpen.getpixel((x,y)) == 0 :
				iRebuild.putpixel((x,y),255)
			else :
				iRebuild.putpixel((x,y),0)
	return iRebuild

im = Image.open("D:\\Python27\\picture\\1.bmp")
im = im.convert("L")
iSegment = Segment(im,structure_data_two,3)
iSegment.save("D:\\Python27\\picture\\1_rebuild.bmp","BMP")
