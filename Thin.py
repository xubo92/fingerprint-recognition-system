#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *

Thin_Table = [
0,0,1,1,0,0,1,1,       1,1,0,1,1,1,0,1,
1,1,0,0,1,1,1,1,       0,0,0,0,0,0,0,1,
0,0,1,1,0,0,1,1,       1,1,0,1,1,1,0,1,
1,1,0,0,1,1,1,1,       0,0,0,0,0,0,0,1,
1,1,0,0,1,1,0,0,       0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,       0,0,0,0,0,0,0,0,
1,1,0,0,1,1,0,0,       1,1,0,1,1,1,0,1,
0,0,0,0,0,0,0,0,       0,0,0,0,0,0,0,0,
0,0,1,1,0,0,1,1,       1,1,0,1,1,1,0,1,
1,1,0,0,1,1,1,1,       0,0,0,0,0,0,0,1,
0,0,1,1,0,0,1,1,       1,1,0,1,1,1,0,1,
1,1,0,0,1,1,1,1,       0,0,0,0,0,0,0,0,
1,1,0,0,1,1,0,0,       0,0,0,0,0,0,0,0,
1,1,0,0,1,1,1,1,       0,0,0,0,0,0,0,0,
1,1,0,0,1,1,0,0,       1,1,0,1,1,1,0,0,
1,1,0,0,1,1,1,0,       1,1,0,0,1,0,0,0]


# good! 需要搞清楚基本原理
def Thin(image) :
	height = image.size[1]
	width  = image.size[0]
	iThin  = Image.new("L",(width,height),255)
	iThin  = image.copy()
	for y in range(height) :
		for x in range(width) :
			if image.getpixel((x,y)) == 0 :
				a = [1] * 9
				for j in range(3) :
					for i in range(3) :
						if -1 < y-1+j < height and -1 < x-1+i < width and iThin.getpixel((x-1+i,y-1+j)) == 0 :
							a[j*3+i] = 0
				sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
				iThin.putpixel((x,y),Thin_Table[sum] * 255)
	return iThin
# !!! we are done 后续处理很好 加了一层新的循环 去掉前一次得到的孤立点
def Thin_Pro(image,len) :
	width  = image.size[0]
	height = image.size[1]
	iThin_Pro = image.copy()
	for y in range(height) :
		for x in range(width) :
			if image.getpixel((x,y)) != 0 :
				continue
			else :
				num = 0
				a = []
				for n in range(3) :
					for m in range(3) :
						if m == 1 and n == 1 :
							continue 
						else :
							if -1<y-1+n<height and -1<x-1+m<width and image.getpixel((x-1+m,y-1+n)) == 0 :
								tuple = (x-1+m,y-1+n)                      # 记录可能的周边点坐标 为后来清除短棒做准备
								a.append(tuple)
								num += 1
				if num == 0 :
					iThin_Pro.putpixel((x,y),255)
					continue
				elif num == 1 :
					for k in range(1,len,1) :
						temp_1 = (k*(a[0][0]-x),k*(a[0][1]-y))
						if image.getpixel((a[0][0]+temp_1[0],a[0][1]+temp_1[1])) == 0 :
							n += 1
							continue 
						else :
							break
					if n <= len  :
						for i in range(n) :
							temp_2 = (i*(a[0][0]-x),i*(a[0][1]-y))
							iThin_Pro.putpixel((a[0][0]+temp_2[0],a[0][1]+temp_2[1]),255)
	for y in range(height) :
		for x in range(width) :
			if iThin_Pro.getpixel((x,y)) == 0 :
				if  (iThin_Pro.getpixel((x-1,y)) and iThin_Pro.getpixel((x+1,y)) and iThin_Pro.getpixel((x,y-1)) and iThin_Pro.getpixel((x,y+1)) and iThin_Pro.getpixel((x-1,y-1)) and iThin_Pro.getpixel((x+1,y-1)) and iThin_Pro.getpixel((x-1,y+1)) and iThin_Pro.getpixel((x+1,y+1))) == 0 :
					continue
				else : iThin_Pro.putpixel((x,y),255)
			else :
				continue
	return iThin_Pro
					
'''						
def No_lonely(image) :
	width = image.size[0]
	height = image.size[1]
	iNo_lonely = image.copy()
	for y in range(height) :
		for x in range(width) :
			if image.getpixel((x,y)) == 0 :
				if  (image.getpixel((x-1,y)) and image.getpixel((x+1,y)) and image.getpixel((x,y-1)) and image.getpixel((x,y+1)) and image.getpixel((x-1,y-1)) and image.getpixel((x+1,y-1)) and image.getpixel((x-1,y+1)) and image.getpixel((x+1,y+1))) == 0 :
					continue
				else : iNo_lonely.putpixel((x,y),255)
			else :
				continue
	return iNo_lonely		
'''					
	
							
	
im = Image.open("D:\\Python27\\picture\\Denoising.bmp")
im = im.convert("L")
iThin = Thin(im)
iThin_Pro = Thin_Pro(iThin,8)
iThin_Pro.show()
iThin_Pro.save("D:\\Python27\\picture\\Thin_Pro.bmp","BMP")




					