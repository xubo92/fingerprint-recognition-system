#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from scipy.ndimage import filters



sin_table = [0,0.38,0.71,0.92,1,0.92,0.71,0.38]
cos_table = [1,0.92,0.71,0.38,0,0.38,0.71,0.92]
def Direction_Index(tuple) :
	
	if tuple == (255,0,255) :
		return 0                           # 0度
	elif tuple == (255,255,0) :
		return 22.5
	elif tuple == (0,0,255) :
		return 45
	elif tuple == (0,255,0) :
		return 67.5
	elif tuple == (255,0,0) :
		return 90
	elif tuple == (0,255,255) :
		return 112.5
	elif tuple == (255,255,255) :
		return 135
	elif tuple == (0,0,0) :
		return 157.5                          # 157.5度
def sin_index(angle) :
	if angle == 0 :
		return sin_table[0]
	elif angle == 22.5 :
		return sin_table[1]
	elif angle == 45 :
		return sin_table[2]
	elif angle == 67.5 :
		return sin_table[3]
	elif angle == 90 :
		return sin_table[4]
	elif angle == 112.5 :
		return sin_table[5]
	elif angle == 135 :
		return sin_table[6]
	elif angle == 157.5 :
		return sin_table[7]
def cos_index(angle) :
	if angle == 0 :
		return cos_table[0]
	elif angle == 22.5 :
		return cos_table[1]
	elif angle == 45 :
		return cos_table[2]
	elif angle == 67.5 :
		return cos_table[3]
	elif angle == 90 :
		return cos_table[4]
	elif angle == 112.5 :
		return cos_table[5]
	elif angle == 135 :
		return cos_table[6]
	elif angle == 157.5 :
		return cos_table[7]
def Freq(image,Direction) :
	Block_size   = 16
	Block_width  = 16
	Block_length = 32
	width  = image.size[0]
	height = image.size[1]
	iFreq  = image.copy()
	Xsig = [0] * Block_length
	out  = [0] * width * height
	a= []
	for y in range(Block_size,height-Block_size,16) :
		for x in range(Block_size,width-Block_size,16) :
			
			dir = Direction.getpixel((x+Block_size/2,y+Block_size/2))
			dir = Direction_Index(dir)
			cosdir = cos_index(dir)
			sindir = sin_index(dir)
			
			for k in range(0,Block_length,1) :
				Xsig[k] = 0
				for d in range(0,Block_width,1) :
					u = x + (d - Block_width/2) * cosdir + (k - Block_length/2) * sindir
					v = y + (d - Block_width/2) * sindir + (Block_length/2 - k) * cosdir
					u = uint8(u)
					v = uint8(v)
					# print u,v
					if u < 0 : 
						u = 0	
					elif u > width - 1 :
						u = width - 1
					if v < 0 :
						v = 0
					elif v > height - 1 :
						v = height - 1
					Xsig[k] +=  image.getpixel((int(u),int(v)))

	
			peak_count = 0
			pmax = pmin = Xsig[0]
			peak_pos = []
			for m in range(1,Block_length,1) :
				if pmin > Xsig[m] :
					pmin = Xsig[m]
				elif pmax < Xsig[m] :
					pmax = Xsig[m]
				
			if pmax - pmin > 128 :
				for m in range(1,Block_length-1,1) :
					if Xsig[m-1] < Xsig[m] and Xsig[m] >= Xsig[m+1] :
						peak_pos.append(m)
						peak_count += 1
						# print peak_count
						
			peak_freq = 0
			if peak_count >= 2 :
				for m in range(peak_count-1) :
					peak_freq += peak_pos[m+1] - peak_pos[m]
				peak_freq/= peak_count - 1 
				a.append([peak_freq,x,y])
			else :
				a.append([0,x,y])
			print peak_freq
			
			
	for each in range(len(a)) :
		if a[each][0] <=3 or a[each][0] >= 30 :
			for j in range(16) :
				for i in range(16) :
					iFreq.putpixel((a[each][1]+i,a[each][2]+j),255)
		else :
			for j in range(16) :
				for i in range(16) :
					iFreq.putpixel((a[each][1]+i,a[each][2]+j),image.getpixel((a[each][1]+i,a[each][2]+j)))

	return iFreq	
	

	
	
		
im1 = Image.open("D:\\Python27\\picture\\3.bmp")
im1 = im1.convert("L")
im2 = Image.open("D:\\Python27\\picture\\Orient.bmp")
iFreq = Freq(im1,im2)
iFreq.show()

		
		