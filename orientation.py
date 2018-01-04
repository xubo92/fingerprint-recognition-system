#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
from numpy import *
from scipy.ndimage import filters
import math
# sobel算子求梯度图像 基本实现 但是和scipy中的sobel函数有较大差距 建议使用官方
'''
im = Image.open("D:\\Python27\\fingerprint\\1.bmp")
im = im.convert("L")
width = im.size[0]
height = im.size[1]
iGradx = Image.new("L",(width,height),0)
iGrady = Image.new("L",(width,height),0)
iGrad  = Image.new("L",(width,height),0)
for i in range(height) :
	for j in range(width) :
		if i in [0,height-1] or j in [0,width-1] :
			continue
		else :
			sumx = pix1((j+1,i+1)) + 2*pix1((j+1,i))+pix1((j+1,i-1))
			-pix1((j-1,i+1)) - 2*pix1((j-1,i)) -pix1((j-1,i-1))
			sumy = pix1((j-1,i-1)) + 2*pix1((j,i-1))+pix1((j+1,i-1))
			-pix1((j-1,i+1))-2*pix1((j,i+1))-pix1((j+1,i+1))
			sumx = abs(sumx)
			sumy = abs(sumy)
			magnitude = sqrt(sumx**2 + sumy**2)
			iGradx.putpixel((j,i),uint8(sumx))
			iGrady.putpixel((j,i),uint8(sumy))
			iGrad.putpixel((j,i) ,uint8(magnitude))
im.show()
iGradx.show()
iGrady.show()
iGrad.show()
'''




'''
# 成功实现连续分布方向图 但是经过研究 这并不是分块思想 而是对每个点进行了方向分析处理 所以运算量超级大 
# 效果很好 就是速度慢
nBlockSize = 15
im = Image.open("D:\\Python27\\1.BMP")
im = im.convert("L")
width = im.size[0]
height = im.size[1]
iOrient  = Image.new("L",(width,height),0)

vx = [0] * ((nBlockSize*2+1)**2)
vy = [0] * ((nBlockSize*2+1)**2)
radian = 0.0
for y in range(nBlockSize+1,height-nBlockSize-1,1) :
	for x in range(nBlockSize+1,width-nBlockSize-1,1) :
		for j in range(nBlockSize*2+1) :
			for i in range(nBlockSize*2+1) :
				vx[j*(nBlockSize*2+1)+i] = pix1((x+i-nBlockSize,y+j-nBlockSize)) - pix1((x+i-nBlockSize-1,y+j-nBlockSize))
				vy[j*(nBlockSize*2+1)+i] = pix1((x+i-nBlockSize,y+j-nBlockSize)) - pix1((x+i-nBlockSize,y+j-nBlockSize-1))
		nx = 0.0
		ny = 0.0	
		for v in range(nBlockSize*2+1) :
			for u in range(nBlockSize*2+1) :
				nx += 2 * vx[v*(nBlockSize*2+1)+u] * vy[v*(nBlockSize*2+1)+u]
				ny += vx[v*(nBlockSize*2+1)+u]**2 - vy[v*(nBlockSize*2+1)+u]**2
		
		radian = math.atan2(ny,nx)
		#print radian
		if (radian<0): radian = radian + 2 * math.pi
		radian = radian * 180 / math.pi *0.5 + 0.5
		angle = int(radian)
		angel = angle - 135
		if (angle <=0): angle = angle + 180
		angle = 180 - angle
		# print angle
		pix2((y,x),uint8(angle))
iOrient.show()
iOrient.save("D:\\Python27\\1_Orient.bmp")
'''




# 新的改进的方法求取连续分布方向图 速度有了一定提升，准确度也很好 可以采用
# 先求点方向图，然后对点方向图进行平滑滤波，得到连续分布方向图

im1 = Image.open("D:\\Python27\\picture\\1.bmp") # 原图
im1 = im1.convert("L")
im2 = Image.open("D:\\Python27\\picture\\1_rebuild.bmp") # 分割后的黑白图
im2 = im2.convert("L") 
width  = im1.size[0]
height = im1.size[1]
iOrient = Image.new("RGB",(width,height),'white')   # 点方向图 彩色
iOrient_succession = Image.new("RGB",(width,height),"white")  # 连续分布方向图 彩色
array1 = im1.load()
array2 = im2.load()
array3 = iOrient.load()
array4 = iOrient_succession.load()

for y in range(5,height-4) :
	for x in range(5,width-4) :
		if array2[x,y] == 255 :                                                                                                                               
			array3[x,y] = (255,255,255)
			continue
		aver_grey_d1 = sum([array1[x,y],array1[x,y-4],array1[x,y-2],array1[x,y+2],array1[x,y+4]]) / 5   # 90度
		aver_grey_d2 = sum([array1[x,y],array1[x-2,y-4],array1[x-1,y-2],array1[x+1,y+2],array1[x+2,y+4]]) / 5 # 67.5度
		aver_grey_d3 = sum([array1[x,y],array1[x-4,y-4],array1[x-2,y-2],array1[x+2,y+2],array1[x+4,y+4]]) / 5 # 45度
		aver_grey_d4 = sum([array1[x,y],array1[x-4,y-2],array1[x-2,y-1],array1[x+2,y+1],array1[x+4,y+2]]) / 5 # 22.5度
		aver_grey_d5 = sum([array1[x,y],array1[x-4,y],array1[x-2,y],array1[x+2,y],array1[x+4,y]]) / 5         # 0 度
		aver_grey_d6 = sum([array1[x,y],array1[x+4,y-2],array1[x+2,y-1],array1[x-2,y+1],array1[x-4,y+2]]) / 5 # 112.5度
		aver_grey_d7 = sum([array1[x,y],array1[x+4,y-4],array1[x+2,y-2],array1[x-2,y+2],array1[x-4,y+4]]) / 5 # 135度
		aver_grey_d8 = sum([array1[x,y],array1[x+2,y-4],array1[x+1,y-2],array1[x-1,y+2],array1[x-2,y+4]]) / 5 # 157.5度
		aver_diff1 = abs(aver_grey_d1-aver_grey_d5) # 90度和0度
		aver_diff2 = abs(aver_grey_d2-aver_grey_d8) # 67.5度和157.5度
		aver_diff3 = abs(aver_grey_d3-aver_grey_d7) # 45度和135度
		aver_diff4 = abs(aver_grey_d4-aver_grey_d6) # 22.5度和112.5度
		list_diff  = [aver_diff1,aver_diff2,aver_diff3,aver_diff4]
		Max_Diff = max(list_diff)
		perhap_direction = list_diff.index(Max_Diff)
		
		if perhap_direction == 0 :
			if abs(aver_grey_d1-array1[x,y]) < abs(aver_grey_d5-array1[x,y]) :
				array3[x,y] = (255,0,0)  # 90度
			else :
				array3[x,y] = (255,0,255) # 0度
		elif perhap_direction == 1 :
			if abs(aver_grey_d2-array1[x,y]) < abs(aver_grey_d8-array1[x,y]) :
				array3[x,y] = (0,255,0)  #67.5度
			else :
				array3[x,y] = (0,0,0)   #157.5度
		elif perhap_direction == 2 :
			if abs(aver_grey_d3-array1[x,y]) < abs(aver_grey_d7-array1[x,y]) :
				array3[x,y] = (0,0,255)  # 45度
			else :
				array3[x,y] = (255,255,255) #135度
		elif perhap_direction == 3 :
			if abs(aver_grey_d4-array1[x,y]) < abs(aver_grey_d6-array1[x,y]) :
				array3[x,y] = (255,255,0) #22.5度
			else :
				array3[x,y] = (0,255,255) #112.5度


for j in range(5,height-4) :
	for i in range(5,width-4) :
		if array2[i,j] == 255 :
			array4[i,j] = (255,255,255)
			continue
		a = [0] * 8
		for n in range(-8,9) :  # 变成17*17的平滑模板 时间增加 效果非常不错 想想怎么快一点
			for m in range(-8,9) :
				if -1 < i-m < width and -1 < j-n < height :
					if 	 array3[i-m,j-n] == (255,0,255) :
						a[0] += 1
					elif array3[i-m,j-n] == (255,255,0) :
						a[1] += 1
					elif array3[i-m,j-n] == (0,0,255) :
						a[2] += 1
					elif array3[i-m,j-n] == (0,255,0) :
						a[3] += 1
					elif array3[i-m,j-n] == (255,0,0) :
						a[4] += 1
					elif array3[i-m,j-n] == (0,255,255) :
						a[5] += 1
					elif array3[i-m,j-n] == (255,255,255) :
						a[6] += 1
					elif array3[i-m,j-n] == (0,0,0) :
						a[7] += 1
		Max = max(a)
		
		dot_direction = a.index(Max)
		
		if dot_direction == 0 :
			array4[i,j] = (255,0,255)
		elif dot_direction == 1 :
			array4[i,j] = (255,255,0)
		elif dot_direction == 2 :
			array4[i,j] = (0,0,255)
		elif dot_direction == 3 :
			array4[i,j] = (0,255,0)
		elif dot_direction == 4 :
			array4[i,j] = (255,0,0)
		elif dot_direction == 5 :
			array4[i,j] = (0,255,255)
		elif dot_direction == 6 :
			array4[i,j] = (255,255,255)
		elif dot_direction == 7 :
			array4[i,j] = (0,0,0)

#iOrient.show()
iOrient_succession.show()	
