#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
from numpy import *
from scipy.ndimage import filters

# 求梯度函数
def Magnitude(image) :
	im  = array(image)
	imx = zeros(im.shape)
	filters.sobel(im,1,imx)
	imy = zeros(im.shape)
	filters.sobel(im,0,imy)
	magnitude = sqrt(imx ** 2 + imy ** 2)
	imag = Image.fromarray(magnitude)
	imx = Image.fromarray(imx)
	imy = Image.fromarray(imy)
	return (imag,imx,imy)
	
def First_Pro(image,image0,image1,image2) :
	width   = image.size[0]
	height  = image.size[1]
	#iFirst = Image.new("L",(width,height),255)
	#Draw   = ImageDraw.Draw(iFirst)
	iResult = Image.new("L",(width,height),255)
	a = []
	b = []
	temp = 0
	num  = 0
	
	for each in range(3) :
		if each == 0 :
			a = []
			b = []
			iTemp = image0.copy()
			# 梯度垂直
			for x in range(width) :
				for y in range(height) :
					temp += iTemp.getpixel((x,y))
				a.append(temp)
				temp = 0
			MeanH = sum(a) / width
			for one in range(len(a)) :
				if a[one] < MeanH :
					num += 1
					temp += a[one]
			Lower_MeanH = temp / num
			temp = 0
			num  = 0
			for i in range(len(a)) :
				if a[i] > Lower_MeanH :
					left0 = i
					break
			for i in range(len(a)) :
				if a[len(a)-i-1] > Lower_MeanH :
					right0 = len(a) - i - 1
					break
			# 梯度水平
			for y in range(height) :
				for x in range(width) :
					temp += iTemp.getpixel((x,y))
				b.append(temp)
				temp = 0
			MeanV = sum(b) / height
			for one in range(len(b)) :
				if b[one] < MeanV :
					num  += 1 
					temp += b[one]
			Lower_MeanV = temp / num
			temp = 0
			num  = 0
			for j in range(len(b)) :
				if b[j] > Lower_MeanV :
					top0 = j 
					break
			for j in range(len(b)) :
				if b[len(b)-j-1] > Lower_MeanV :
					bottom0 = len(b) - j - 1
					break
		elif each == 1 :
			a = []
			b = []
			iTemp = image1.copy()
			# 梯度x分量垂直
			for x in range(width) :
				for y in range(height) :
					temp += iTemp.getpixel((x,y))
				a.append(temp)
				temp = 0
			MeanH = sum(a) / width
			for one in range(len(a)) :
				if a[one] < MeanH :
					num += 1
					temp += a[one]
			Lower_MeanH = temp / num
			temp = 0
			num  = 0
			for i in range(len(a)) :
				if a[i] > Lower_MeanH :
					left1 = i
					break
			for i in range(len(a)) :
				if a[len(a)-i-1] > Lower_MeanH :
					right1 = len(a) - i - 1
					break
			# 梯度x分量水平
			for y in range(height) :
				for x in range(width) :
					temp += iTemp.getpixel((x,y))
				b.append(temp)
				temp = 0
			MeanV = sum(b) / height
			for one in range(len(b)) :
				if b[one] < MeanV :
					num  += 1 
					temp += b[one]
			Lower_MeanV = temp / num
			temp = 0
			num  = 0
			for j in range(len(b)) :
				if b[j] > Lower_MeanV :
					top1 = j 
					break
			for j in range(len(b)) :
				if b[len(b)-j-1] > Lower_MeanV :
					bottom1 = len(b) - j - 1
					break
		elif each == 2 :
			a = []
			b = []
			iTemp = image2.copy()
			# 梯度y分量垂直
			for x in range(width) :
				for y in range(height) :
					temp += iTemp.getpixel((x,y))
				a.append(temp)
				temp = 0
			MeanH = sum(a) / width
			for one in range(len(a)) :
				if a[one] < MeanH :
					num += 1
					temp += a[one]
			Lower_MeanH = temp / num
			temp = 0
			num  = 0
			for i in range(len(a)) :
				if a[i] > Lower_MeanH :
					left2 = i
					break
			for i in range(len(a)) :
				if a[len(a)-i-1] > Lower_MeanH :
					right2 = len(a) - i - 1
					break
			# 梯度y分量水平
			for y in range(height) :
				for x in range(width) :
					temp += iTemp.getpixel((x,y))
				b.append(temp)
				temp = 0
			MeanV = sum(b) / height
			for one in range(len(b)) :
				if b[one] < MeanV :
					num  += 1 
					temp += b[one]
			Lower_MeanV = temp / num
			temp = 0
			num  = 0
			for j in range(len(b)) :
				if b[j] > Lower_MeanV :
					top2 = j 
					break
			for j in range(len(b)) :
				if b[len(b)-j-1] > Lower_MeanV :
					bottom2 = len(b) - j - 1
					break
	'''
	for k in range(width) :
		a[k] = a[k]/height  
		x = (k,255)
		y = (k,255-a[k])
		Draw.line((x,y),fill = 20)
	'''
	left   = [left0,left1,left2]
	right  = [right0,right1,right2]
	top    = [top0,top1,top2]
	bottom = [bottom0,bottom1,bottom2]
	final_left = max(left)
	final_right = min(right)
	final_top = max(top)
	final_bottom = min(bottom)
	print final_left,final_right,final_top,final_bottom
	
	for y in range(height) :
		for x in range(width) :
			if y in range(final_top,final_bottom) and x in range(final_left,final_right) :
				iResult.putpixel((x,y),0)
			else :
				iResult.putpixel((x,y),255)
			
			
	
	
	
	return iResult
	

	
	

	
'''	
# 基于灰度图的开闭运算
def Change(image,flag,radius) :
	width = image.size[0]
	height = image.size[1]
	iChange = Image.new("L",(width,height),255)
	for y in range(height) :
		for x in range(width) :
			a = []
			for n in range(2 * radius + 1) :
				for m in range(2 * radius + 1) :
					if -1 < y-radius+n < height and -1 < x-radius+m < width :
						a.append(image.getpixel((x-radius+m,y-radius+n)))
			if flag == 0 :
				k = max(a)       # 腐蚀操作
			else :
				k = min(a)       # 膨胀操作
			iChange.putpixel((x,y),k)
	return iChange
'''				
im = Image.open("D:\\Python27\\picture\\1.bmp")
im = im.convert("L")
(iMag,imx,imy) = Magnitude(im)
iMag = iMag.convert("L")
imx  = imx.convert("L")
imy  = imy.convert("L")  # !!!
iResult = First_Pro(im,iMag,imx,imy)
iResult.save("D:\\Python27\\picture\\1_result.bmp","BMP")



