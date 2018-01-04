#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *

Direction_Block = [(-4,0),(-2,0),(-1,0),(0,0),(1,0),(2,0),(4,0),   
				   (-4,-2),(-2,-1),(-1,-1),(0,0),(1,1),(2,1),(4,2),    
			       (-4,-4),(-2,-2),(-1,-1),(0,0),(1,1),(2,2),(4,4),    
			       (-2,-4),(-1,-2),(0,-1),(0,0),(0,1),(1,2),(2,4),     
			       (0,-4),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,4),       
			       (-4,2),(-2,1),(-1,1),(0,0),(1,-1),(2,-1),(4,-2),    
			       (-4,4),(-2,2),(-1,1),(0,0),(1,-1),(2,-2),(4,-4),    
			       (-2,4),(-1,2),(0,1),(0,0),(0,-1),(1,-2),(2,-4)]   

Hw = [1,1,1,1,1,1,1]           # Gabor 平行模板
Vw = [-3,-1,3,9,3,-1,-3]	   # Gabor 垂直模板

Wh = [2,2,3,4,3,2,3]	       # 智能二值化水平权值
Wv = [1,1,1,1,1,1,1]		   # 智能二值化垂直权值
			   
def Direction_Index(tuple) :
	
	if tuple == (255,0,255) :
		return 0                           # 0度
	elif tuple == (255,255,0) :
		return 1
	elif tuple == (0,0,255) :
		return 2
	elif tuple == (0,255,0) :
		return 3
	elif tuple == (255,0,0) :
		return 4
	elif tuple == (0,255,255) :
		return 5
	elif tuple == (255,255,255) :
		return 6
	elif tuple == (0,0,0) :
		return 7                          # 157.5度

def Orientation(image) :
	width  = image.size[0]
	height = image.size[1]
	iOrient = Image.new("RGB",(width,height),'white')
	for y in range(5,height-4) :
		for x in range(5,width-4) :
			aver_grey_d1 = sum([image.getpixel((x,y)),image.getpixel((x,y-4)),image.getpixel((x,y-2)),image.getpixel((x,y+2)),image.getpixel((x,y+4))]) / 5   # 90度
			aver_grey_d2 = sum([image.getpixel((x,y)),image.getpixel((x-2,y-4)),image.getpixel((x-1,y-2)),image.getpixel((x+1,y+2)),image.getpixel((x+2,y+4))]) / 5 # 67.5度
			aver_grey_d3 = sum([image.getpixel((x,y)),image.getpixel((x-4,y-4)),image.getpixel((x-2,y-2)),image.getpixel((x+2,y+2)),image.getpixel((x+4,y+4))]) / 5 # 45度
			aver_grey_d4 = sum([image.getpixel((x,y)),image.getpixel((x-4,y-2)),image.getpixel((x-2,y-1)),image.getpixel((x+2,y+1)),image.getpixel((x+4,y+2))]) / 5 # 22.5度
			aver_grey_d5 = sum([image.getpixel((x,y)),image.getpixel((x-4,y)),image.getpixel((x-2,y)),image.getpixel((x+2,y)),image.getpixel((x+4,y))]) / 5         # 0 度
			aver_grey_d6 = sum([image.getpixel((x,y)),image.getpixel((x+4,y-2)),image.getpixel((x+2,y-1)),image.getpixel((x-2,y+1)),image.getpixel((x-4,y+2))]) / 5 # 112.5度
			aver_grey_d7 = sum([image.getpixel((x,y)),image.getpixel((x+4,y-4)),image.getpixel((x+2,y-2)),image.getpixel((x-2,y+2)),image.getpixel((x-4,y+4))]) / 5 # 135度
			aver_grey_d8 = sum([image.getpixel((x,y)),image.getpixel((x+2,y-4)),image.getpixel((x+1,y-2)),image.getpixel((x-1,y+2)),image.getpixel((x-2,y+4))]) / 5 # 157.5度
			aver_diff1 = abs(aver_grey_d1-aver_grey_d5) # 90度和0度
			aver_diff2 = abs(aver_grey_d2-aver_grey_d8) # 67.5度和157.5度
			aver_diff3 = abs(aver_grey_d3-aver_grey_d7) # 45度和135度
			aver_diff4 = abs(aver_grey_d4-aver_grey_d6) # 22.5度和112.5度
			list_diff  = [aver_diff1,aver_diff2,aver_diff3,aver_diff4]
			Max_Diff = max(list_diff)
			perhap_direction = list_diff.index(Max_Diff)
			if perhap_direction == 0 :
				if abs(aver_grey_d1-image.getpixel((x,y))) < abs(aver_grey_d5-image.getpixel((x,y))) :
					iOrient.putpixel((x,y),(255,0,0))  # 90度
				else :
					iOrient.putpixel((x,y),(255,0,255)) # 0度
			elif perhap_direction == 1 :
				if abs(aver_grey_d2-image.getpixel((x,y))) < abs(aver_grey_d8-image.getpixel((x,y))) :
					iOrient.putpixel((x,y),(0,255,0))  #67.5度
				else :
					iOrient.putpixel((x,y),(0,0,0))   #157.5度
			elif perhap_direction == 2 :
				if abs(aver_grey_d3-image.getpixel((x,y))) < abs(aver_grey_d7-image.getpixel((x,y))) :
					iOrient.putpixel((x,y),(0,0,255))  # 45度
				else :
					iOrient.putpixel((x,y),(255,255,255)) #135度
			elif perhap_direction == 3 :
				if abs(aver_grey_d4-image.getpixel((x,y))) < abs(aver_grey_d6-image.getpixel((x,y))) :
					iOrient.putpixel((x,y),(255,255,0)) #22.5度
				else :
					iOrient.putpixel((x,y),(0,255,255)) #112.5度

	iOrient_succession = Image.new("RGB",(width,height),"white")
	for j in range(5,height-4) :
		for i in range(5,width-4) :
			a = [0] * 8
			for n in range(-4,4) :
				for m in range(-4,4) :
					if 	 iOrient.getpixel((i-m,j-n)) == (255,0,255) :
						a[0] += 1
					elif iOrient.getpixel((i-m,j-n)) == (255,255,0) :
						a[1] += 1
					elif iOrient.getpixel((i-m,j-n)) == (0,0,255) :
						a[2] += 1
					elif iOrient.getpixel((i-m,j-n)) == (0,255,0) :
						a[3] += 1
					elif iOrient.getpixel((i-m,j-n)) == (255,0,0) :
						a[4] += 1
					elif iOrient.getpixel((i-m,j-n)) == (0,255,255) :
						a[5] += 1
					elif iOrient.getpixel((i-m,j-n)) == (255,255,255) :
						a[6] += 1
					elif iOrient.getpixel((i-m,j-n)) == (0,0,0) :
						a[7] += 1
			Max = max(a)
			dot_direction = a.index(Max)
			if dot_direction == 0 :
				iOrient_succession.putpixel((i,j),(255,0,255))
			elif dot_direction == 1 :
				iOrient_succession.putpixel((i,j),(255,255,0))
			elif dot_direction == 2 :
				iOrient_succession.putpixel((i,j),(0,0,255))
			elif dot_direction == 3 :
				iOrient_succession.putpixel((i,j),(0,255,0))
			elif dot_direction == 4 :
				iOrient_succession.putpixel((i,j),(255,0,0))
			elif dot_direction == 5 :
				iOrient_succession.putpixel((i,j),(0,255,255))
			elif dot_direction == 6 :
				iOrient_succession.putpixel((i,j),(255,255,255))
			elif dot_direction == 7 :
				iOrient_succession.putpixel((i,j),(0,0,0))
	return iOrient_succession
	
# Gabor 增强     成功！	
def Gabor_Enhance(image,image_Dir) :
	width = image.size[0]
	height = image.size[1]
	iEnhance = Image.new("L",(width,height),255)
	Direction_Block_Width = 7
	
	for y in range(height) :
		for x in range(width) :
			h_tuple = image_Dir.getpixel((x,y))
			d = Direction_Index(h_tuple)
			sum = 0
			hsum = 0
			for k in range(7) :
				if (y + Direction_Block[d * Direction_Block_Width + k][1] < 0 or y + Direction_Block[d * Direction_Block_Width + k][1] >= height 
					or x + Direction_Block[d * Direction_Block_Width + k][0] < 0 or x + Direction_Block[d * Direction_Block_Width + k][0] >= width) :
					continue 
				else :
					sum += Hw[k] * image.getpixel((x + Direction_Block[d * Direction_Block_Width + k][0],y + Direction_Block[d * Direction_Block_Width + k][1]))
					hsum += Hw[k]
			if (hsum != 0) :
				iEnhance.putpixel((x,y),uint8(sum/hsum))
			else :
				iEnhance.putpixel((x,y),255)
				
	for y in range(height) :
		for x in range(width) :
			v_tuple = image_Dir.getpixel((x,y))
			d = (Direction_Index(v_tuple) + 4) % 8
			sum = 0
			vsum = 0
			for k in range(7) :
				if(y + Direction_Block[d * Direction_Block_Width + k][1] < 0 or y + Direction_Block[d * Direction_Block_Width + k][1] >= height 
					or x + Direction_Block[d * Direction_Block_Width + k][0] < 0 or x + Direction_Block[d * Direction_Block_Width + k][0] >= width) :
					continue
				else :
					sum += Vw[k] * image.getpixel((x + Direction_Block[d * Direction_Block_Width + k][0],y + Direction_Block[d * Direction_Block_Width + k][1]))
					vsum += Vw[k]
			if vsum > 0 :
				sum /= vsum
				if sum >255 :
					iEnhance.putpixel((x,y),255)
				elif sum < 0 :
					iEnhance.putpixel((x,y),0)
				else :
					iEnhance.putpixel((x,y),uint8(sum))
			else :
				iEnhance.putpixel((x,y),255)
	return iEnhance
	

# 智能二值化    噪声比较多
def AI_Binary(image,image_Dir) :
	width  = image.size[0]
	height = image.size[1]
	iBinary = Image.new("L",(width,height),255)
	Direction_Block_Width = 7
	avrH = 0
	avrV = 0
	for y in range(height) :
		for x in range(width) :
			if image.getpixel((x,y)) < 4 :
				iBinary.putpixel((x,y),0)
				continue
			h_tuple = image_Dir.getpixel((x,y))
			d = Direction_Index(h_tuple)
			sum = 0
			hsum = 0
			for k in range(7) :
				if (y + Direction_Block[d * Direction_Block_Width + k][1] < 0 or y + Direction_Block[d * Direction_Block_Width + k][1] >= height 
					or x + Direction_Block[d * Direction_Block_Width + k][0] < 0 or x + Direction_Block[d * Direction_Block_Width + k][0] >= width) :
					continue 
				else : 
					sum  += Wh[k] * image.getpixel((x + Direction_Block[d * Direction_Block_Width + k][0],y + Direction_Block[d * Direction_Block_Width + k][1]))
					hsum += Wh[k]
			if hsum != 0 :
				avrH = uint8(sum / hsum) 
			else :
				avrH = 255
			
			d = (d + 4) % 8
			sum = 0
			vsum = 0
			for k in range(7) :
				if (y + Direction_Block[d * Direction_Block_Width + k][1] < 0 or y + Direction_Block[d * Direction_Block_Width + k][1] >= height 
					or x + Direction_Block[d * Direction_Block_Width + k][0] < 0 or x + Direction_Block[d * Direction_Block_Width + k][0] >= width) :
					continue 
				else : 
					sum  += Wv[k] * image.getpixel((x + Direction_Block[d * Direction_Block_Width + k][0],y + Direction_Block[d * Direction_Block_Width + k][1]))
					vsum += Wv[k]
			if vsum != 0 :
				avrV = sum / vsum
				if avrV > 255 :
					avrV = 255
				elif avrV < 0 :
					avrV = 0
				else :
					avrV = uint8(avrV)
			else :
				avrV = 255
				
			
			if avrH < avrV :
				iBinary.putpixel((x,y),0)
			else :
				iBinary.putpixel((x,y),255)
	return iBinary
			
def Denoising(image) :
	width  = image.size[0]
	height = image.size[1]
	a = [-1,0,1]
	iDenoising = Image.new("L",(width,height),255)
	for y in range(height - 1) :
		for x in range(width - 1) :
			if image.getpixel((x,y)) == 255 :
				continue
			else :
				num = 0
				for n in range(3) :
					for m in range(3) :
						if n != 0 and m != 0 :
							if image.getpixel((x+a[m],y+a[n])) == image.getpixel((x,y)) :
								num += 1
						else :
							continue
				if num < 3 :
					iDenoising.putpixel((x,y),255-image.getpixel((x,y)))
				else :
					iDenoising.putpixel((x,y),image.getpixel((x,y)))
				
	return iDenoising
'''
im1 = Image.open("D:\\Python27\\picture\\segment_1.bmp")				
im2 = Image.open("D:\\Python27\\picture\\Orient.bmp")	
iEnhance = Gabor_Enhance(im1,im2)
iEnhance.save("D:\\Python27\\picture\\Enhance.bmp","BMP")
im3 = Image.open("D:\\Python27\\picture\\Enhance.bmp")
iBinary = AI_Binary(im3,im2)
iBinary.save("D:\\Python27\\picture\\Binary.bmp","BMP")
'''
iBinary = Image.open("D:\\Python27\\picture\\Binary.bmp")
iDenoising = Denoising(iBinary)
iDenoising.save("D:\\Python27\\picture\\Denoising.bmp","BMP")




