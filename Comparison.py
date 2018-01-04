#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFilter
from numpy import *
from copy import deepcopy 
import operator

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
		
# image1: 细化图 image2: 分割后的黑白图 image3: 方向图
def IsFeature(image1,image2,image3) :
	width  = image1.size[0]
	height = image1.size[1]
	pix1   = image1.load()
	pix2   = image2.load()
	pix3   = image3.load()
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
					
					dot.append((x,y))
				elif sum == 6 * 255 :
					
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
					
					flag1 = 1
					Feature.remove((one[0],one[1]))
					break
				elif (tempx<0 or tempx>=width or tempy<0 or tempy>=height) :
					
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
				angle = 22.5 * Direction_Index(pix3(each[0],each[1]))
				Draw.ellipse((each[0]-2,each[1]-2,each[0]+2,each[1]+2),fill = 255,outline = 0)
				qualified.append((each[0],each[1],angle,'dot'))  
			elif each in fork :
				angle = 22.5 * Direction_Index(pix3(each[0],each[1]))
				Draw.polygon([(each[0]-2,each[1]-2),(each[0]-2,each[1]+2),(each[0]+2,each[1]+2),(each[0]+2,each[1]-2)],fill = 255,outline = 0)
				qualified.append((each[0],each[1],angle,'fork'))
	return (copy,qualified)	

class Point_Info() :
	def __init__(self) :
		self.PointType = 'default'
		self.X_axis     = 0 
		self.Y_axis	    = 0
		self.Angle      = 0
		self.FivePoints = [(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default')]
		self.triangles  = [(0,0,0,0,0,'default',0,'default')] * 10
		
def Get_Distance(pointA,pointB) :
	distance = (pointA[0]-pointB[0]) ** 2 + (pointA[1]-pointB[1]) ** 2
	return distance
def GetAngle(x0,y0,x1,y1,x2,y2) :
	angle1 = arctan2(float(y1-y0),float(x1-x0))
	angle2 = arctan2(float(y2-y0),float(x2-x0))
	
	
	angle = abs(angle1 - angle2)
	return int16(angle * EPI + 0.5)	
	
# A_feature : 第一幅标识特征点的细化图 A_qualified : 第一幅图的合格特征点集
# B_feature : 第二幅标识特征点的细化图 B_qualified : 第二幅图的合格特征点集
def Compare(A_qualified) :
	
	A_copy = deepcopy(A_qualified)
	B_copy = deepcopy(B_qualified)
	Distance = []
	Struct_Array = []
	for i in A_qualified :
		Temp = Point_Info()
		Temp.PointType = i[3]
		Temp.X_axis    = i[0]
		Temp.Y_axis    = i[1]
		Temp.Angle     = i[2]
		for j in A_copy :
			if i != j :
				Distance.append((Get_Distance(i,j),j))
			else :
				continue
		Distance.sort(key = operator.itemgetter(0))
		for k in range(5) :
			Temp.FivePoints[k] = (A_copy[Distance[k][1]]) 
		for m in range(len(Temp.FivePoints)) :
			for n in range(m+1,len(Temp.FivePoints)) :
				num = 0 
				d1 = Get_Distance(i,Temp.FivePoints[m]) 
				d2 = Get_Distance(i,Temp.FivePoints[n])
				angle = GetAngle(i[0],i[1],m[0],m[1],n[0],n[1])
				
				if d1 >= d2 :
					Temp.triangles[num][0] = d1 
					Temp.triangles[num][1] = d2 
					Temp.triangles[num][2] = angle 
					Temp.triangles[num][4] = Temp.FivePoints[m][2]
					Temp.triangles[num][5] = Temp.FivePoints[m][3]
					Temp.triangles[num][6] = Temp.FivePoints[n][2]
					Temp.triangles[num][7] = Temp.FivePoints[n][3]
				elif d1 < d2 :
					Temp.triangles[num][0] = d2 
					Temp.triangles[num][1] = d1 
					Temp.triangles[num][2] = angle 
					Temp.triangles[num][4] = Temp.FivePoints[n][2]
					Temp.triangles[num][5] = Temp.FivePoints[n][3]
					Temp.triangles[num][6] = Temp.FivePoints[m][2]
					Temp.triangles[num][7] = Temp.FivePoints[m][3]
					
					
				
		Struct_Array.append(Temp)
		
	print 'collected'

im1 = Image.open("D:\\Python27\\picture\\1\\1_ThinPro.bmp")	
im2 = Image.open("D:\\Python27\\picture\\1\\1_Rebuild.bmp")


