#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFilter
from numpy import *
from copy import deepcopy

def IsFeature(image1,image2) :
	width  = image1.size[0]
	height = image1.size[1]
	pix1   = image1.load()
	pix2   = image2.load()
	copy   = image1.copy()
	Draw   = ImageDraw.Draw(copy)
	dot = []
	fork = []	
	for y in range(height) :
		for x in range(width) :
			if 0 < x < width-1 and 0 < y < height-1 and pix1[x,y] == 0 :
				a = pix1[x-1,y+1] 
				b = pix1[x,y+1]
				c = pix1[x+1,y+1]
				d = pix1[x-1,y]
				f = pix1[x+1,y]
				g = pix1[x-1,y-1]
				h = pix1[x,y-1]
				i = pix1[x+1,y-1]
				sum = abs(a-b) + abs(b-c) + abs(c-f) + abs(f-i) + abs(i-h) + abs(h-g) + abs(g-d) + abs(d-a)
				if sum == 2 * 255 :
					#Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 0)
					dot.append((x,y))
				elif sum == 6 * 255 :
					#Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 0)
					fork.append((x,y))
				else :
					continue
	# 去除边缘端点 思路：根据是否靠近背景块来判断 使用了黑白分明的背景块图片1_rebuild.bmp
	flag1 = 0
	flag2 = 0
	Feature = deepcopy(dot+fork)
	for one in dot+fork :
		for n in range(32) :
			for m in range(32) :
				tempx = one[0] - 16 + m
				tempy = one[1] - 16 + n
				if ( -1<tempx<width and -1<tempy<height and pix2[tempx,tempy] == 255) :
					#Draw.ellipse((one[0]-1,one[1]-1,one[0]+1,one[1]+1),fill = 255,outline = 255)
					flag1 = 1
					Feature.remove((one[0],one[1]))
					break
				elif (tempx<0 or tempx>=width or tempy<0 or tempy>=height) :
					#Draw.ellipse((one[0]-1,one[1]-1,one[0]+1,one[1]+1),fill = 255,outline = 255)
					flag2 = 1
					Feature.remove((one[0],one[1]))
					break
				else :
					continue
			if flag1 == 1 or flag2 == 1 :
				flag1 = 0
				flag2 = 0
				break
			else :
				continue
				
	# FeatureCopy是Feature的相同副本，用于第二次遍历比较		
	FeatureCopy = deepcopy(Feature)
	
	dellist = []   # 需删除的相距太近的特征点，包含重复计算
	
	for each in Feature :
		for n in range(16) :
			for m in range(16) :
				tempx = each[0] - 8 + m
				tempy = each[1] - 8 + n 
				tuple = (tempx,tempy)
				for var in FeatureCopy :
					if var == tuple and var != each :
						dellist.append(var)
						dellist.append(each)
						break
					else :
						continue
					
	dellist_nosame = [] # 需删除的相距太近的特征点，不包含重复计算
	
	for each in dellist :
		if each not in dellist_nosame :
			dellist_nosame.append(each)
			
			
	# dot是首次检测的所有端点坐标列表 fork是首次检测的所有叉点坐标列表 dot+fork 是所有特征点
	# Feature是去掉边缘不合格端点和叉点后的列表
	# FeatureCopy是Feature的相同模板 ，仅用于遍历判断不做增减操作。
	# dellist_nosame 是所有相距太近不合格的端点和叉点的列表  Feature包含dellist_nosame
	# qualified 是所有合格的特征点集，使用元组最后一位，0表示端点，1表示叉点
	qualified = []
	for each in Feature :
		if each in dellist_nosame :
			continue
		else :
			if each in dot :
				Draw.ellipse((each[0]-2,each[1]-2,each[0]+2,each[1]+2),fill = 255,outline = 0)
				qualified.append((each[0],each[1],0))  
			elif each in fork :
				Draw.polygon([(each[0]-2,each[1]-2),(each[0]-2,each[1]+2),(each[0]+2,each[1]+2),(each[0]+2,each[1]-2)],fill = 255,outline = 0)
				qualified.append((each[0],each[1],1))
	return (copy,qualified)		







	
cell3 = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
cell5 = [(-2,-1),(-2,0),(-2,1),(-1,2),(0,2),(1,2),(2,1),(2,0),(2,-1),(1,-2),(0,-2),(-1,-2),(-2,-1)]
cell7 = [(-3,-3), (-3,-2), (-3,-1), (-3,0), (-3,1), (-3,2), (-3,3), (-2,3), (-1,3), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0),
			(3,-1), (3,-2), (3,-3), (2,-3), (1,-3), (0,-3), (-1,-3), (-2,-3)]

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
		
def get_angle(left,right,flag) :
	angle = right - left 
	if flag >= 1 :
		if angle < 0 :
			angle += 10
	elif flag <= -1 :
		if angle > 0 :
			angle -= 10
	return angle
	
# image1:细化图，image2：方向图 image3:前后背景图
def IsSingular(image1,image2,image3,flag) :
	width  = image1.size[0]
	height = image1.size[1]
	
	copy = image1.copy()
	Draw = ImageDraw.Draw(copy)
	
	pix1 = image1.load()
	pix2 = image2.load()
	pix3 = image3.load()
	
	singular = []
	fg = False
	for y in range(3,height-3) :
		for x in range(3,width-3) :
		
			if pix3[x,y] == 255 :
				continue
			fg = False
			for i in range(24) :
				if pix3[cell7[i][0]+x,cell7[i][1]+y] == 255 :
					fg = True 
					break
			if fg :
				continue
			sum1 = 0
			for i in range(8) :
				a1 = pix2[cell3[i][0]+x,cell3[i][1]+y]/24
				a2 = pix2[cell3[(i+1)%8][0]+x,cell3[(i+1)%8][1]+y]/24
				d  = get_angle(a1,a2,flag)
				if abs(d) > 5 :
					break
				sum1 += d
			sum2 = 0
			for i in range(12) :	
				a1 = pix2[cell5[i][0]+x,cell5[i][1]+y]/24
				a2 = pix2[cell5[(i+1)%12][0]+x,cell5[(i+1)%12][1]+y]/24 
				d  = get_angle(a1,a2,flag)
				if abs(d) > 5 :
					break
				sum2 += d
			if flag == -1 :
				value = -10
			elif flag == 1 :
				value = 10 
			if sum2 == value and sum1 == value :
				Draw.ellipse((x-2,y-2,x+2,y+2),fill = 255,outline = 0)
		
	'''		
	# 去除靠近边缘的奇异点
	flag = 0
	N_singular = deepcopy(singular)
	for one in singular :
		for n in range(-16,17) :
			for m in range(-16,17) :
				tempx = one[0] + m 
				tempy = one[1] + n
				if (-1<tempx<width and -1<tempy<height and pix3[tempx,tempy] == 255) :
					flag = 1
					N_singular.remove((one[0],one[1]))
					break
				elif (tempx<0 or tempx>=width or tempy<0 or tempy>=height) :
					flag == 2
					N_singular.remove((one[0],one[1]))
				else :
					continue
			if flag == 1 or flag == 2 :
				flag = 0 
				break
			else :
				continue
			
	for one in N_singular :
		Draw.ellipse((one[0]-2,one[1]-2,one[0]+2,one[1]+2),fill = 255,outline = 0)
	print len(N_singular)		
	'''
					
	return copy


	
im1 = Image.open("D:\\Python2.7\\picture\\1\\1_ThinPro.bmp")
im1 = im1.convert("L")
im2 = Image.open("D:\\Python2.7\\picture\\1\\1_rebuild.bmp")
im2 = im2.convert("L")
im3 = Image.open("D:\\Python2.7\\picture\\b.bmp")
iStart = IsSingular(im1,im3,im2,1)
iStart.show()
		
				