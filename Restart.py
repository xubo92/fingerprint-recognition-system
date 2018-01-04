#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
from numpy import *
from copy import deepcopy
from ctypes import *
import operator
EPI     = 57.29578
CENTRALRADIUS = 60 
OFFSITE = [(-3,0 ),(-2,0 ),(-1,0 ),(0,0),(1,0 ),(2,0 ),(3,0 ),
		   (-3,-1),(-2,-1),(-1,0 ),(0,0),(1,0 ),(2,1 ),(3,1 ),
		   (-3,-2),(-2,-1),(-1,-1),(0,0),(1,1 ),(2,1 ),(3,2 ),
		   (-3,-3),(-2,-2),(-1,-1),(0,0),(1,1 ),(2,2 ),(3,3 ),
		   (-2,-3),(-1,-2),(-1,-1),(0,0),(1,1 ),(1,2 ),(2,3 ),
		   (-1,-3),(-1,-2),(0,-1 ),(0,0),(0,1 ),(1,2 ),(1,3 ),
		   (0,-3 ),(0,-2 ),(0,-1 ),(0,0),(0,1 ),(0,2 ),(0,3 ),
		   (-1,3 ),(-1,2 ),(0,1  ),(0,0),(0,-1),(1,-2),(1,-3),
		   (-2,3 ),(-1,2 ),(-1,1 ),(0,0),(1,-1),(1,-2),(2,-3),
		   (-3,3 ),(-2,2 ),(-1,1 ),(0,0),(1,-1),(2,-2),(3,-3),
		   (-3,2 ),(-2,1 ),(-1,1 ),(0,0),(1,-1),(2,-1),(3,-2),
		   (-3,1 ),(-2,1 ),(-1,0 ),(0,0),(1,0 ),(2,-1),(3,-1)]

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

cell3 = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
cell5 = [(-2,-1),(-2,0),(-2,1),(-1,2),(0,2),(1,2),(2,1),(2,0),(2,-1),(1,-2),(0,-2),(-1,-2),(-2,-1)]
cell7 = [(-3,-3), (-3,-2), (-3,-1), (-3,0), (-3,1), (-3,2), (-3,3), (-2,3), (-1,3), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0),
		(3,-1), (3,-2), (3,-3), (2,-3), (1,-3), (0,-3), (-1,-3), (-2,-3)]
		
DisTable = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
			1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
			2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 
			3, 3, 3, 4, 5, 5, 6, 7, 8, 9, 
			4, 4, 4, 5, 5, 6, 7, 8, 8, 9, 
			5, 5, 5, 5, 6, 7, 7, 8, 9, 10, 
			6, 6, 6, 6, 7, 7, 8, 9, 10, 10, 
			7, 7, 7, 7, 8, 8, 9, 9, 10, 11, 
			8, 8, 8, 8, 8, 9, 10, 10, 11, 12, 
			9, 9, 9, 9, 9, 10, 10, 11, 12, 12]

SiteR5 = [(-5,0),(-5,1),(-5,2),(-4,3),(-3,4),(-2,5),(-1,5),(0,5),(1,5),
		  (2,5),(3,4),(4,3),(5,2),(5,1),(5,0),(5,-1),(5,-2),(4,-3),(3,-4),
		  (2,-5),(1,-5),(0,-5),(-1,-5),(-2,-5),(-3,-4),(-4,-3),(-5,-2),(-5,-1)]
	

def Zoom(image) :
	width  = image.size[0]
	height = image.size[1]
	pix1   = image.load()
	iZoom  = Image.new("L",(width/2,height/2),'white')
	pix2   = iZoom.load()
	for y in range(0,height,2) :
		pix2[0,y/2] = pix1[0,y]  
		pix2[width/2-1,y/2] = pix1[width-1,y]
	for x in range(0,width,2) :
		pix2[x/2,0] = pix1[x,0]
		pix2[x/2,height/2-1] = pix1[x,height-1]
		
	for y in range(2,height-2,2) :
		for x in range(2,width-2,2) :
			sum = pix1[x,y] * 4 + pix1[x-1,y+1] + pix1[x+1,y+1] + pix1[x-1,y-1]
			+ pix1[x+1,y-1] + pix1[x-1,y] * 2 + pix1[x+1,y] * 2 + pix1[x,y-1] * 2
			+ pix1[x,y+1] * 2
			pix2[x/2,y/2] = sum >> 4
	return iZoom

def GetOrientMap(image,r) :
	width   = image.size[0]
	height  = image.size[1]
	iOrient = Image.new("L",(2*width,2*height),'white')
	iGrad   = Image.new("L",(2*width,2*height),'white')
	pix1    = image.load()
	pix2    = iOrient.load()
	pix3    = iGrad.load()
	
	for y in range(height) :
		for x in range(width) :
			lvx = 0
			lvy = 0
			num = 0
			gradsum = 0
			for j in range(-r,r+1,1) :
				if y + j - 1 < 1 or y + j + 1 >= height - 1 :
					continue 
				for i in range(-r,r+1,1) :
					if x + i - 1 < 1 or x + i + 1 >= width -1 :
						continue
					vx = pix1[x+i+1,y+j+1] - pix1[x+i-1,y+j+1] + pix1[x+i+1,y+j] * 2 - pix1[x+i-1,y+j] * 2 
					+ pix1[x+i+1,y+j-1] - pix1[x+i-1,y+j-1]
					
					vy = pix1[x+i-1,y+j+1] - pix1[x+i-1,y+j-1] + pix1[x+i,y+j+1] * 2 - pix1[x+i,y+j-1] * 2 
					+ pix1[x+i+1,y+j+1] - pix1[x+i+1,y+j-1] 
					
					gradsum += abs(vx) + abs(vy)
					lvx += vx * vy * 2
					lvy += vx ** 2 - vy ** 2 
					num += 1
			if num == 0 : 
				num = 1
			grad = gradsum / num 
			
			if(grad > 255) :
				grad = 255
			pix3[2*x,2*y] = uint8(grad)
			pix3[2*x+1,2*y] = uint8(grad)
			pix3[2*x+1,2*y+1] = uint8(grad)
			pix3[2*x,2*y+1]   = uint8(grad)
			
			fAngle = arctan2(lvy,lvx)
			if fAngle < 0 :
				fAngle += 2 * pi
			fAngle = fAngle * EPI * 0.5 + 0.5 
			angle  = int16(fAngle)
			angle  -= 135
			if angle <= 0 :
				angle += 180 
			angle = 180 - angle 
			pix2[2*x,2*y] = uint8(angle) 
			pix2[2*x,2*y+1] = uint8(angle)
			pix2[2*x+1,2*y] = uint8(angle)
			pix2[2*x+1,2*y+1] = uint8(angle)
			
	return (iOrient,iGrad)

def Smooth(image,r,d) :
	width   = image.size[0]
	height  = image.size[1]
	iSmooth = Image.new("L",(width,height),'white')
	pix1    = image.load()
	pix2    = iSmooth.load()
	sum     = 0
	num     = 0
	for y in range(height) :
		for x in range(width) :
			sum = 0
			num = 0
			for j in range(-r,r+1,d) :
				if y + j < 1 or y + j >= height-1 :
					continue
				for i in range(-r,r+1,d) :
					if x + i < 1 or x + i >= width-1 :
						continue 
					sum += pix1[x+i,y+j] 
					num += 1 
			pix2[x,y] = uint8(sum/num)
	return iSmooth
					
def Segment(image,iGrad,r,threshold) :
	width  = image.size[0]
	height = image.size[1]
	iSegment = image.copy()
	pix1   = image.load()
	pix2   = iSegment.load()
	iDivide  = Smooth(iGrad,r,2)
	pix3   = iDivide.load()
	num    = 0
	
	for y in range(height) :
		pix3[0,y] = 0
		pix3[width-1,y] = 0 
	for x in range(width) :
		pix3[x,0] = 0 
		pix3[x,height-1] = 0 
	for y in range(1,height-1) :
		for x in range(1,width-1) :
			if pix3[x,y] < threshold :
				pix3[x,y] = 255
				pix2[x,y] = 0
			else :
				pix3[x,y] = 0
				num += 1
	if num < height * width / 10 :
		print "Image not qualified"
	else :
		print "Image effective"
	return (iDivide,iSegment)		

def Equalize(image,iDivide) :
	a = [0] * 256
	width  = image.size[0]
	height = image.size[1]
	iEqualize = Image.new("L",(width,height),255)
	pix1 = image.load()
	pix2 = iEqualize.load()
	pix3 = iDivide.load()
	for y in range(height) :
		for x in range(width) :
			iGray = int(pix1[x,y])
			a[iGray] = a[iGray] + 1
	for m in range(1,256) :
		a[m] = a[m] + a[m-1]
		
	sum = max(a)
	for k in range(256) :
		a[k] = a[k] * 255 / sum
	for y in range(height) :
		for x in range(width) :
			pix2[x,y] = a[int(pix1[x,y])]
	for y in range(height) :
		for x in range(width) :
			if pix3[x,y] == 0 :
				pix2[x,y] = 255
			
	return iEqualize

def GaussFilter(image,sigma) :
	(Kernel,WindowSize) = MakeGauss(sigma)
	HalfSize = WindowSize / 2
	width  = image.size[0]
	height = image.size[1]
	iGauss = Image.new("L",(width,height),'white')
	pix1   = image.load()
	pix2   = iGauss.load()
	temp   = zeros([width,height])
	# print Kernel
	for y in range(height) :
		for x in range(width) :
			DotMul    = 0.0
			WeightSum = 0.0
			for i in range(-HalfSize,HalfSize+1,1) :
				if x+i >= 0 and x+i < width :
					DotMul    += float(pix1[x+i,y]) * Kernel[HalfSize + i]
					WeightSum += Kernel[HalfSize + i]
			
			temp[x,y] = DotMul / WeightSum 

	for x in range(width) :
		for y in range(height) :
			DotMul    = 0.0
			WeightSum = 0.0
			for i in range(-HalfSize,HalfSize+1,1) :
				if y+i >= 0 and y+i < height :
					DotMul    += (temp[x,y+i]) * Kernel[HalfSize + i]
					WeightSum += Kernel[HalfSize + i]
			pix2[x,y] = uint8(int16(DotMul / WeightSum))
	
	return iGauss
	
def MakeGauss(sigma) :
	WindowSize = int16(1 + 2 * ceil(3 * sigma))
	Center     = WindowSize / 2 
	Kernel     = []
	Sum        = 0
	for i in range(WindowSize) :
		Dis = i - Center
		#print Dis
		Value = exp(-(1.0/2) * Dis * Dis / (sigma ** 2)) / (sqrt(2 * pi) * sigma)
		#print Value
		Kernel.append(Value) 
		Sum += Value
	for i in range(WindowSize) :
		Kernel[i] /= Sum
	print Kernel
	return (Kernel,WindowSize)

def Index(angle) :
	if angle >= 173 or angle < 8 :
		return 0 
	else :
		return (angle - 8) / 15 + 1


def Enhance(image,iOrient) :
	width  = image.size[0]
	height = image.size[1] 
	Hw = [1,1,1,1,1,1,1]
	Vw = [-3,-1,3,9,3,-1,-3]
	hsum = 0
	vsum = 0 
	pix1 = image.load()
	pix2 = iOrient.load()
	iEnhance = Image.new("L",(width,height),'white')
	temp     = Image.new("L",(width,height),'white')
	pix3 = iEnhance.load()
	pix4 = temp.load()
	
	for y in range(height) :
		for x in range(width) :
			index = Index(pix2[x,y])
			sum   = 0 
			hsum  = 0 
			for i in range(7) :
				if y + OFFSITE[7*index+i][1] < 0 or y + OFFSITE[7*index+i][1] >= height or x + OFFSITE[7*index+i][0] < 0 or x + OFFSITE[7*index+i][0] >= width :
					continue
				else :
					sum  += Hw[i] * pix1[x+OFFSITE[7*index+i][0],y+OFFSITE[7*index+i][1]]
					hsum += Hw[i]
			if hsum != 0 :
				pix4[x,y] = uint8(sum/hsum)
			else :
				pix4[x,y] = 255
		
	for y in range(height) :
		for x in range(width) :
			index = (Index(pix2[x,y]) + 4) % 8
			sum   = 0
			vsum  = 0 
			for i in range(7) :
				if y + OFFSITE[7*index+i][1] < 0 or y + OFFSITE[7*index+i][1] >= height or x + OFFSITE[7*index+i][0] < 0 or x + OFFSITE[7*index+i][0] >= width :
					continue 
				else :
				
					sum  += Vw[i] * pix4[x+OFFSITE[7*index+i][0],y+OFFSITE[7*index+i][1]]
					vsum += Vw[i]
			if vsum > 0 :
				sum /= vsum
				if sum > 255 :
					pix3[x,y] = 255 
				elif sum < 0 :
					pix3[x,y] = 0
				else :
					pix3[x,y] = uint8(sum)
			else :
				pix3[x,y] = 255 
	 
	
	return iEnhance

def Binary(image,iOrient) :
	Hw = [2,2,3,4,3,2,2]
	Vw = [1,1,1,1,1,1,1]
	hsum  = 0
	vsum  = 0 
	havr  = 0
	vavr  = 0 
	width  = image.size[0]
	height = image.size[1] 
	iBinary_temp  = Image.new("L",(width,height),'white')
	pix1   = image.load()
	pix2   = iOrient.load()
	pix3   = iBinary_temp.load()
	
	for y in range(height) :
		for x in range(width) :
			if pix1[x,y] < 4 :
				pix3[x,y] = 0 
				continue 
			index = Index(pix2[x,y])
			sum  = 0
			hsum = 0
			for i in range(7) :
				if y + OFFSITE[7*index+i][1] < 0 or y + OFFSITE[7*index+i][1] >= height or x + OFFSITE[7*index+i][0] < 0 or x + OFFSITE[7*index+i][0] >= width :
					continue 
				sum  += Hw[i] * pix1[x+OFFSITE[7*index+i][0],y+OFFSITE[7*index+i][1]]
				hsum += Hw[i]
			if hsum != 0 :
				havr = sum / hsum 
			else :
				havr = 255 
				
			index = (index + 6) % 12 
			
			sum  = 0
			vsum = 0
			for i in range(7) :
				if y + OFFSITE[7*index+i][1] < 0 or y + OFFSITE[7*index+i][1] >= height or x + OFFSITE[7*index+i][0] < 0 or x + OFFSITE[7*index+i][0] >= width :
					continue 
				sum  += Vw[i] * pix1[x+OFFSITE[7*index+i][0],y+OFFSITE[7*index+i][1]]
				vsum += Vw[i]
			if vsum != 0 :
				vavr = sum / vsum 
			else :
				vavr = 255 
			
			
			if havr < vavr :
				pix3[x,y] = 0 
			else :
				pix3[x,y] = 255 
	
					
	return iBinary_temp
	
def Binary_Clear(image,iDivide) :
	pix1   = image.load()
	pix2   = iDivide.load()
	flag   = True
	n      = 0
	width  = image.size[0]
	height = image.size[1] 
	iBinary = image.copy()
	pix3    = iBinary.load()
	while (flag and n < 8) :
		flag = False 
		n += 1 
		for y in range(1,height-1,1) :
			for x in range(1,width-1,1) :
				if pix2[x,y] == 0 :
					pix3[x,y] = 255 
					continue 
				num = 0 
				for i in [-1,0,1] :
					for j in [-1,0,1] :	
						if pix1[x,y] == pix1[x+i,y+j] and not(i==0 and j == 0) :
							num += 1 
				if num < 2 :
					pix3[x,y] = 255 - pix1[x,y]
					flag = True
				else :
					pix3[x,y] = pix1[x,y]
	return iBinary
	
def Thin(image) :
	width  = image.size[0]
	height = image.size[1]
	iThin  = Image.new("L",(width,height),'white')
	pix1    = image.load()
	pix2    = iThin.load()
	for y in range(height) :
		for x in range(width) :
			if pix1[x,y] == 0 :
				a = [1] * 9
				for j in range(3) :
					for i in range(3) :
						if -1 < y-1+j < height and -1 < x-1+i < width and pix1[x-1+i,y-1+j] == 0 :
							a[j*3+i] = 0
				sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
				pix2[x,y] = Thin_Table[sum] * 255
	return iThin
# image1:细化图 image2：黑白分割图 image3：方向图
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
				angle = pix3[each[0],each[1]]
				Draw.ellipse((each[0]-2,each[1]-2,each[0]+2,each[1]+2),fill = 255,outline = 0)
				qualified.append((each[0],each[1],angle,'dot'))  
			elif each in fork :
				angle = pix3[each[0],each[1]]
				Draw.polygon([(each[0]-2,each[1]-2),(each[0]-2,each[1]+2),(each[0]+2,each[1]+2),(each[0]+2,each[1]-2)],fill = 255,outline = 0)
				qualified.append((each[0],each[1],angle,'fork'))
	return (copy,qualified)		
	
def get_angle(left,right,flag) :
	angle = right - left 
	if flag >= 1 :
		if angle < 0 :
			angle += 10
	elif flag <= -1 :
		if angle > 0 :
			angle -= 10
	return angle

# image1:细化图，image2：方向图 image3:前后背景图 mode: 检测模式（奇异点类型）
def IsSingular(image1,image2,image3,mode) :
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
				d  = get_angle(a1,a2,mode)
				if abs(d) > 5 :
					break
				sum1 += d
			sum2 = 0
			for i in range(12) :	
				a1 = pix2[cell5[i][0]+x,cell5[i][1]+y]/24
				a2 = pix2[cell5[(i+1)%12][0]+x,cell5[(i+1)%12][1]+y]/24 
				d  = get_angle(a1,a2,mode)
				if abs(d) > 5 :
					break
				sum2 += d
			if mode == -1 :
				value = -10
			elif mode == 1 :
				value = 10 
			if sum2 == value and sum1 == value :
				singular.append((x,y))
	
	
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
					N_singular.remove(one)
					break
				elif (tempx<0 or tempx>=width or tempy<0 or tempy>=height) :
					flag == 2
					N_singular.remove(one)
				else :
					continue
			if flag == 1 or flag == 2 :
				flag = 0 
				break
			else :
				continue
	
	for one in N_singular :
		Draw.ellipse((one[0]-2,one[1]-2,one[0]+2,one[1]+2),fill = 255,outline = 0)	
	
	return copy,len(N_singular)


	
	

class Point_Info() :
	def __init__(self) :
		self.PointType = 'default'
		self.X_axis     = 0 
		self.Y_axis	    = 0
		self.Angle      = 0
		#self.FivePoints = [(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default'),(0,0,0,'default')]
		self.FivePoints = []
		#self.triangles  = [(0,0,0,0,0,'default',0,'default')] * 10
		#顺序分别是 长边 短边 夹角 纹线条数 长边对应点角度 类型 短边对应点角度 类型   
		#            0    1    2      3          4          5       6           7
		self.triangles = []
		
def Get_Distance(pointA,pointB) :
	distance = (pointA[0]-pointB[0]) ** 2 + (pointA[1]-pointB[1]) ** 2
	return distance
# 两两点连线夹角
def GetAngle(x0,y0,x1,y1,x2,y2) :
	angle1 = arctan2(float(y1-y0),float(x1-x0))
	angle2 = arctan2(float(y2-y0),float(x2-x0))
	
	
	angle = abs(angle1 - angle2)
	return int16(angle * EPI + 0.5)	
	
# A_feature : 第一幅标识特征点的细化图 A_qualified : 第一幅图的合格特征点集
# B_feature : 第二幅标识特征点的细化图 B_qualified : 第二幅图的合格特征点集
def Compare(A_qualified) :
	
	#A_copy = deepcopy(A_qualified)
	#B_copy = deepcopy(B_qualified)
	Distance = []
	Struct_Array = []
	dis = 0
	for i in range(len(A_qualified)) :
		Distance = []
		Temp = Point_Info()
		Temp.PointType = A_qualified[i][3]
		Temp.X_axis    = A_qualified[i][0]
		Temp.Y_axis    = A_qualified[i][1]
		Temp.Angle     = A_qualified[i][2]
		for j in range(len(A_qualified)) :
			if A_qualified[i] != A_qualified[j] :
				dis = Get_Distance(A_qualified[i],A_qualified[j])
				Distance.append((dis,j))
			else :
				continue
		Distance.sort(key = operator.itemgetter(0))
		for k in range(5) :
			Temp.FivePoints.append(A_qualified[Distance[k][1]]) 
		num = 0 
		for m in range(len(Temp.FivePoints)) :
			for n in range(m+1,len(Temp.FivePoints)) :
				
				d1 = Get_Distance(A_qualified[i],Temp.FivePoints[m]) 
				d2 = Get_Distance(A_qualified[i],Temp.FivePoints[n])
				angle = GetAngle(A_qualified[i][0],A_qualified[i][1],Temp.FivePoints[m][0],Temp.FivePoints[m][1],Temp.FivePoints[n][0],Temp.FivePoints[n][1])
				
				if d1 >= d2 :
					Temp.triangles.append((d1,d2,angle,0,Temp.FivePoints[m][2],Temp.FivePoints[m][3],Temp.FivePoints[n][2],Temp.FivePoints[n][3]))
					
				elif d1 < d2 :
					Temp.triangles.append((d2,d1,angle,0,Temp.FivePoints[n][2],Temp.FivePoints[n][3],Temp.FivePoints[m][2],Temp.FivePoints[m][3]))
				
				num += 1
					
		#print num		
		Struct_Array.append(Temp)
	return Struct_Array	
	#print 'collected',Struct_Array[1].triangles
# Struct_Array 整幅图像的所有特征点以及拓扑信息 qualified：整幅图像各点基本信息
def ShowResult(A_Struct_Array,B_Struct_Array,A_qualified,B_qualified)	:
	TD = 5 
	TW = 5
	TQ1 = 5
	TQ2 = 5
	SCORE_THRESHOLD = 9
	score = zeros([len(A_qualified),len(B_qualified)],int16)
	num_compare = 0
	RADIO = 0
	
	for i in range(len(A_qualified)) :
		for j in range(len(B_qualified)) :
			if A_Struct_Array[i].PointType ==  B_Struct_Array[j].PointType :
				score[i][j] += 1 
			else :
				continue 
			for k in range(10) : 
				for l in range(10) :
					if abs(A_Struct_Array[i].triangles[k][0]-B_Struct_Array[j].triangles[l][0]+A_Struct_Array[i].triangles[k][1]-B_Struct_Array[j].triangles[l][1]) < TD and \
						abs(A_Struct_Array[i].triangles[k][2]-B_Struct_Array[j].triangles[l][2]) < TW and \
						A_Struct_Array[i].triangles[k][5] == B_Struct_Array[j].triangles[l][5] and \
						A_Struct_Array[i].triangles[k][7] == B_Struct_Array[j].triangles[l][7] and \
						abs((A_Struct_Array[i].triangles[k][4]-A_Struct_Array[i].Angle)-(B_Struct_Array[j].triangles[l][4]-B_Struct_Array[j].Angle)) < TQ1 and \
						abs((A_Struct_Array[i].triangles[k][6]-A_Struct_Array[i].Angle)-(B_Struct_Array[j].triangles[l][6]-B_Struct_Array[j].Angle)) < TQ2 :
						score[i][j] += 2 
	row_max = score.max(axis = 1)
	column_max = score.max(axis = 0)
	score_compare = (row_max.sum()+column_max.sum())/(len(A_qualified)+len(B_qualified))
	for i in range(len(A_qualified)) :
		for j in range(len(B_qualified)) :
			if score[i][j] >= SCORE_THRESHOLD :
				num_compare += 1 
	RADIO =  int16 ((num_compare * 1.0 / score.shape[0]) * 100 + (num_compare * 1.0 / score.shape[1]) * 100) / 2
	RADIO =   (num_compare * 1.0 / score.shape[1]) * 100
	#print RADIO
	#print score
	if score_compare <= score.min() or RADIO < 80 :
		return  ("相似度为 %f %%，匹配失败".decode('utf-8','ignore').encode('gbk') %uint8(RADIO))
	elif score_compare >= score.max() or RADIO >= 80:
		return  ("相似度为 %f %%，匹配成功".decode('utf-8','ignore').encode('gbk') %uint8(RADIO))
	else :
		return  ("相似度为 %f %%，需进一步识别".decode('utf-8','ignore').encode('gbk') %uint8(RADIO))
		
		

					
					
'''					 
img = Image.open("D:\\Python2.7\\image\\615\\9\\9.bmp").convert("L")
iD = Image.open("D:\\Python2.7\\image\\615\\9\\dir.bmp")
iD = iD.convert("L")
iDS = Image.open("D:\\Python2.7\\image\\615\\9r\\dir.bmp")
iDS = iDS.convert("L")

iDivide = Image.open("D:\\Python2.7\\image\\615\\9\\divide.bmp")
iDivide = iDivide.convert("L")
iDivideS = Image.open("D:\\Python2.7\\image\\615\\9r\\divide.bmp")
iDivideS = iDivideS.convert("L")

iThin = Image.open("D:\\Python2.7\\image\\615\\9\\thin.bmp")
iThin = iThin.convert("L")
iThinS = Image.open("D:\\Python2.7\\image\\615\\9r\\thin.bmp")
iThinS = iThinS.convert("L")




A_copy,A_qualified = IsFeature(iThin,iDivide,iD)
#A_copy.show()

B_copy,B_qualified = IsFeature(iThinS,iDivideS,iDS)
A_Struct_Array = Compare(A_qualified)
B_Struct_Array = Compare(B_qualified)
str = ShowResult(A_Struct_Array,B_Struct_Array,A_qualified,B_qualified)
print str
#B_copy.show()
'''




'''
# 两点之间连线与x轴的角度	
def GetAngle(x0,y0,x1,y1) :
	angle = arctan2(float(y1-y0),float(x1-x0))
	if angle < 0 :
		angle += 2 * pi 
	return int16(angle * EPI + 0.5)
# 求两个角度的夹角(0~180)	
# angle1 ，angle2 ： 0~360
def AngleAbs360(angle1,angle2) :	
	a = abs(angle1 - angle2) 
	if a > 180 :
		return 360 - a 
	else :
		return a 
# 求两点间距离
def Dist(x0,y0,x1,y1) :
	return int16 sqrt((x0-x1) * (x0-x1) + (y0-y1) * (y0-y1))
#　求两个角度的夹角	(0~90)
#  angle1,angle2 : 0~180
def GetJiaJiao(angle1,angle2) :
	a = abs(angle1-angle2)
	if a > 90 :
		a = 180 - a 
	return a
def GetAngleDis(angleBegin,angleEnd) :
	a = angleEnd - angleBegin
	if a < 0 : 
		a += 360 
	return a 
		
# Feature:要变换的图像特征集合 数组类型 内含字典
# AlignedFeature：变换后的图像特征集合 数组类型 内含字典
# FeatureCore：旋转变换的中心点 字典类型 属于特征点结构体
# rotation：旋转角度
# transx：水平偏移
# transy：竖直偏移

def align(Feature,AlignedFeature,FeatureCore,rotation,transx,transy) :
	AlignedFeature = deepcopy(Feature)
	cx = FeatureCore['x']
	cy = FeatureCore['y']
	rota = rotation / EPI
	sinv = sin(rota)
	cosv = cos(rota)
	for i in range(Feature[60]) :
		x = Feature[i]['x']
		y = Feature[i]['y']
		AlignedFeature[i]['x'] = int16(cx + cosv*(x-cx) - sinv*(y-cy) + transx + 0.5)
		AlignedFeature[i]['y'] = int16(cy + sinv*(x-cx) + cosv*(y-cy) + transy + 0.5)
		AlignedFeature[i]['Direction'] = (Feature[i]['Direction'] + rotation ) % 360
		
def alignmatch(AlignedFeature,Template,MatchResult,MatchMode) :
	flagA = [0] * 60 
	flagT = [0] * 60 
	num1  = AlignedFeature[60]
	num2  = Template[60]
	
	score = 0 
	matchnum = 0
	
	for i in range(Template[60]) :
		if flagT[i] :
			continue 
		for j in range(AlignedFeature[60]) :
			if flagA[j] :
				continue 
			if Template[i]['Type'] != AlignedFeature[j]['Type'] :
					continue
			angle = AngleAbs360(Template[i]['Direction'],AlignedFeature[j]['Direction'])
			if angle >= 10 :
				continue
			x1 = Template[i]['x']
			y1 = Template[i]['y']
			x2 = AlignedFeature[j]['x']
			y2 = AlignedFeature[j]['y']
			
			if abs(x1-x2) >= 10 :
				continue 
			if abs(y1-y2) >= 10 :
				continue
			dis = DisTable[10 * abs(y1-y2) + abs(x1-x2)]
			if dis >= 10 :
				continue 
			flagA[j] = 1 
			flagT[i] = 1 
			score += 10 - angle 
			score += 10 - dis 
			matchnum += 1
			if MatchMode == 'FAST_MODE' and matchnum >= 8 :
				s = 4 * score * matchnum * 60 / (num1 + num2) ** 2)
				if s > 100 :
					MatchResult['MMcount'] = matchnum 
					MatchResult['Rotation'] = 0 
					MatchResult['Similarity'] = s 
					MatchResult['TransX'] = 0 
					MatchResult['TransY'] = 0 
					return 
					
	if MatchMode != 'FAST_MODE' :
		for i in range(Template[60]) :
			if flagT[i] :
				continue 
			for j in range(AlignedFeature[60]) :
				if flagA[j] :
					continue 
				if Template[i]['Type'] == AlignedFeature[j]['Type'] :
					continue 
				angle = AngleAbs360(Template[i]['Direction'],AlignedFeature[j]['Direction'])
				if angle >= 10 :
					continue
				x1 = Template[i]['x']
				y1 = Template[i]['y']
				x2 = AlignedFeature[j]['x']
				y2 = AlignedFeature[j]['y']
				
				if abs(x1-x2) >= 10 :
					continue 
				if abs(y1-y2) >= 10 :
					continue
				dis = DisTable[10 * abs(y1-y2) + abs(x1-x2)]
				if dis >= 10 :
					continue 
				flagA[j] = 1 
				flagT[i] = 1
				score += ((10-angle)/2)
				score += ((10-dis)/2)
				matchnum += 1 
	s = 4 * score * matchnum * 60 / (num1 + num2) ** 2)
	MatchResult['MMcount'] = matchnum 
	MatchResult['Rotation'] = 0 
	MatchResult['Similarity'] = s 
	MatchResult['TransX'] = 0 
	MatchResult['TransY'] = 0 
				
				
	
# Feature 待匹配的图像特征集合 数组类型 内含字典
# Template 模板图像特征集合 数组类型 内含字典
# MatchResult 匹配结果信息 字典类型
def CoreMatch(Feature,Template，MatchResult，MatchMode,n,m) :
	alignMax = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	globalMatchResult = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	agate = 8 
	num = 0
	alignFeature = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * 60,0]
	
	transx = Template[n]['x'] - Feature[m]['x']
	transy = Template[n]['y'] - Feature[m]['y']
	
	for i in range(Feature[60]) :
		for j in range(Template[60]) :
			alignFeature[60] = 0 
			 
			if Feature[i]['Type'] == 'CORE' or Template[j]['Type'] == 'CORE' :
				continue
			if Feature[i]['Type'] == 'DELTA' or Template[j]['Type'] == 'DELTA' :
				continue
			
			rotation = GetAngle(Feature[i]['x'],Feature[i]['y'],Template[j]['x'],Template[j]['y'])
			
			align(Feature,alignFeature,Feature[i],rotation,transx,transy)
			alignmatch(alignFeature,Template,globalMatchResult,MatchMode)
			if globalMatchResult['Similarity'] > alignMax['Similarity'] :
				alignMax['MMcount'] = globalMatchResult['MMcount']
				alignMax['Similarity'] = globalMatchResult['Similarity']
				alignMax['Rotation'] = rotation
				alignMax['TransX'] = transx
				alignMax['TransY'] = transy
				
				if MatchMode == 'FAST_MODE' and alignMax['MMcount'] >= 8 :
					alignMax['Similarity'] > 100 :
						MatchResult = alignMax
						return 
	
	MatchResult = alignMax

# n_delta,m_delta : 数组类型 
def DeltaMatch(Feature,Template,MatchResult,MatchMode,n_delta,m_delta) :
	alignMax = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	globalMatchResult = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	agate = 8 
	num = 0
	alignFeature = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * 60,0]
	
	for nn in range(len(n_delta)) : 
		for mm in range(len(m_delta)) :
			n = int16 (n_delta[nn])
			m = int16 (m_delta[mm])
			transx = Template[n]['x'] - Feature[m]['x']
			transy = Template[n]['y'] - Feature[m]['y']
			for i in range(Feature[60]) :
				for j in range(Template[60]) :
					alignFeature[60] = 0 
					 
					if Feature[i]['Type'] == 'CORE' or Template[j]['Type'] == 'CORE' :
						continue
					if Feature[i]['Type'] == 'DELTA' or Template[j]['Type'] == 'DELTA' :
						continue
					
					rotation = GetAngle(Feature[i]['x'],Feature[i]['y'],Template[j]['x'],Template[j]['y'])
					
					align(Feature,alignFeature,Feature[i],rotation,transx,transy)
					alignmatch(alignFeature,Template,globalMatchResult,MatchMode)
					if globalMatchResult['Similarity'] > alignMax['Similarity'] :
						alignMax['MMcount'] = globalMatchResult['MMcount']
						alignMax['Similarity'] = globalMatchResult['Similarity']
						alignMax['Rotation'] = rotation
						alignMax['TransX'] = transx
						alignMax['TransY'] = transy
						
						if MatchMode == 'FAST_MODE' and alignMax['MMcount'] >= 8 :
							alignMax['Similarity'] > 100 :
								MatchResult = alignMax
								return 
			
	MatchResult = alignMax

def CentralMatch(Feature,Template,MatchResult,MatchMode) :
	alignMax = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	globalMatchResult = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	agate = 8 
	num = 0
	alignFeature = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * 60,0]
	
	nx = 0
	ny = 0 
	for n in range(Template[60]) :
		nx += Template[n]['x']
		ny += Template[n]['y']
	nx = nx / Template[60]
	ny = ny / Template[60]
	
	mx = 0 
	my = 0 
	for m in range(Feature[60]) :
		mx += Feature[m]['x']
		my += Feature[m]['y']
	mx = mx / Feature[60]
	my = my / Feature[60]
	
	counter = 0 
	for n in range(Template[60]) :
		if Dist(nx,ny,Template[n]['x'],Template[n]['y']) > CENTRALRADIUS :
			continue 
		for m in range(Feature[60]) :
			if Feature[m]['Type'] != Template[n]['Type'] :
				continue 
			if Dist(mx,my,Feature[m]['x'],Feature[m]['y']) > CENTRALRADIUS :
				counter += 1 
			if MatchMode == 'FAST_MODE' :
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Direction'] % 180) 
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Direction'] % 180) 
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 and 
				Feature[m]['Triangle'][1] != 255 and Template[n]['Triangle'][1] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Triangle'][1]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Triangle'][1]) 
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][2] != 255 and Template[n]['Triangle'][2] != 255 and 
				Feature[m]['Triangle'][1] != 255 and Template[n]['Triangle'][1] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][1],Feature[m]['Triangle'][2]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][1],Template[n]['Triangle'][2]) 
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 and 
				Feature[m]['Triangle'][2] != 255 and Template[n]['Triangle'][2] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Triangle'][2]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Triangle'][2]) 
					if abs(a1-a2) > agate :
						continue
			alignFeature[60] = 0 
			rotation = GetAngleDis(Feature[m]['Direction'],Template[n]['Direction'])
			
			transx = Template[n]['x'] - Feature[m]['x']
			transy = Template[n]['y'] - Feature[m]['y']
			
			align(Feature,alignFeature,Feature[m],rotation,transx,transy)
			alignmatch(alignFeature,Template，globalMatchResult，MatchMode)
			if globalMatchResult['Similarity'] > alignMax['Similarity'] :
				alignMax['MMcount'] = globalMatchResult['MMcount']
				alignMax['Similarity'] = globalMatchResult['Similarity']
				alignMax['Rotation'] = rotation
				alignMax['TransX'] = transx
				alignMax['TransY'] = transy
				if MatchMode == 'FAST_MODE' and alignMax['MMcount'] >= 8 :
					if alignMax['Similarity'] > 100 :
						MatchResult = alignMax
						return 
	MatchResult = alignMax

def GlobalMatch(Feature,Template,MatchResult,MatchMode) :
	alignFeature = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * 60,0]
	alignMax = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	globalMatchResult = {'Similarity':0,'Rotation':0,'TranX':0,'TranY':0,'MMcount':0}
	agate = 8
	num = 0
	
	for n in range(Template[60]) :
		for m in range(Feature[60]) :
			if Feature[m]['Type'] != Template[n]['Type'] :
				continue 
			if MatchMode == 'FAST_MODE' :
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Direction'] % 180)
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Direction'] % 180)
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 and 
				Feature[m]['Triangle'][1] != 255 and Template[n]['Triangle'][1] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Triangle'][1]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Triangle'][1]) 
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][2] != 255 and Template[n]['Triangle'][2] != 255 and 
				Feature[m]['Triangle'][1] != 255 and Template[n]['Triangle'][1] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][1],Feature[m]['Triangle'][2]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][1],Template[n]['Triangle'][2]) 
					if abs(a1-a2) > agate :
						continue 
				if Feature[m]['Triangle'][0] != 255 and Template[n]['Triangle'][0] != 255 and 
				Feature[m]['Triangle'][2] != 255 and Template[n]['Triangle'][2] != 255 :
					a1 = GetJiaJiao(Feature[m]['Triangle'][0],Feature[m]['Triangle'][2]) 
					a2 = GetJiaJiao(Template[n]['Triangle'][0],Template[n]['Triangle'][2]) 
					if abs(a1-a2) > agate :
						continue
			alignFeature[60] = 0 
			rotation = GetAngleDis(Feature[m]['Direction'],Template[n]['Direction'])
			transx = Template[n]['x'] - Feature[m]['x']
			transy = Template[n]['y'] - Feature[m]['y']
			align(Feature,alignFeature,Feature[m],rotation,transx,transy)
			alignmatch(alignFeature,Template,globalMatchResult,MatchMode)
			if globalMatchResult['Similarity'] > alignMax['Similarity'] :
				alignMax['MMCount'] = globalMatchResult['MMCount']
				alignMax['Similarity'] = globalMatchResult['Similarity']
				alignMax['Rotation'] = rotation
				alignMax['TransX'] = transx
				alignMax['TransY'] = transy
				if MatchMode == 'FAST_MODE' and alignMax['MMCount'] >= 8 :
					if alignMax['Similarity'] > 100 :
						MatchResult = alignMax
						return 
	MatchResult = alignMax
def PatternMatch(Feature,Template,MatchResult,MatchMode) :
	n_core = []
	m_core = []
	n_delta = []
	m_delta = []
	
	for n in range(Feature[60]) :
		if Feature[n]['Type'] == 'CORE' :
			n_core.append(n)
	for m in range(Template[60]) :
		if Template[m]['Type'] == 'CORE' :
			m_core.append(m)
			
			
	if len(n_core) > 0 and len(m_core) > 0 :
		for i in range(len(n_core)) :
			for j in range(len(m_core)) :
				n = n_core[i]
				m = m_core[j]
				CoreMatch(Feature,Template,MatchResult,MatchMode,n,m) 
				if MatchMode == 'FAST_MODE' and MatchResult['MMcount'] >= 8 :
					if MatchResult['Similarity'] > 100 :
						return 
						
	if len(n_delta) > 0 and len(m_delta) > 0 :
		DeltaMatch(Feature,Template,MatchResult,MatchMode,n_delta,m_delta)
		if MatchMode == 'FAST_MODE' and MatchResult['MMcount'] >= 8 :
			if MatchResult['Similarity'] > 100 :
				return 
	
	CentralMatch(Feature,Template,MatchResult,MatchMode)
	if MatchMode == 'FAST_MODE' and MatchResult['MMcount'] >= 8 :
		if MatchResult['Similarity'] > 100 :
			return 
	GlobalMatch(Feature,Template,MatchResult,MatchMode)
'''	



