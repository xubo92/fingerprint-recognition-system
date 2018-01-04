#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw
from numpy import *
from scipy.ndimage import filters
from copy import deepcopy

cell3 = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
cell5 = [(-2,-1),(-2,0),(-2,1),(-1,2),(0,2),(1,2),(2,1),(2,0),(2,-1),(1,-2),(0,-2),(-1,-2),(-2,-1)]
cell7 = [(-3,-3), (-3,-2), (-3,-1), (-3,0), (-3,1), (-3,2), (-3,3), (-2,3), (-1,3), (0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0),
		(3,-1), (3,-2), (3,-3), (2,-3), (1,-3), (0,-3), (-1,-3), (-2,-3)]
		
def get_angle(left,right,flag) :
	angle = right - left 
	if flag >= 1 :
		if angle < 0 :
			angle += 10
	elif flag <= -1 :
		if angle > 0 :
			angle -= 10
	return angle
	
# ************************************************************#
# 求梯度函数 返回值包含x方向，y方向以及总梯度矢量的图像, 后续也用于分割算法
def Magnitude(image) :
	im = array(image)
	imx = zeros(im.shape)
	filters.sobel(im,1,imx)
	imy = zeros(im.shape)
	filters.sobel(im,0,imy)
	magnitude = sqrt(imx ** 2 + imy ** 2)
	x_gradient = Image.fromarray(imx)
	y_gradient = Image.fromarray(imy)
	mag = Image.fromarray(magnitude)
	return (mag,x_gradient,y_gradient)
# ************************************************************#
# 方向图算法，效果平滑，但是速度还是有些慢，需要加速改进
# image1 : 分割后的正常图 image12 : 分割后的黑白图
def Direction(image1,image2) :
	width  = image1.size[0]
	height = image1.size[1]
	iDirection_Dot 		   = Image.new("RGB",(width,height),'white')    # 点方向图 彩色
	iDirection_succession  = Image.new("RGB",(width,height),"white")    # 连续分布方向图 彩色
	array1 = image1.load()
	array2 = image2.load()
	array3 = iDirection_Dot.load()
	array4 = iDirection_succession.load()
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
	return (iDirection_Dot,iDirection_succession)
# *********************************************************** #
# 分割算法：包含三个阶段 
# 1. 对原图按轮廓进行形态学处理，得到黑白二值的轮廓图
# 2. 对上一步的结果依据x方向梯度、y方向梯度进行横纵切，有效去掉一些杂乱噪声
# 3. 按照最后的轮廓进行还原

# 用于平滑图像的高斯算子，实现图像收敛处理
gauess_filter_operator = [0.0000,0.0001,0.0010,0.0016,0.0010,0.0001,0.0000,
 0.0001,0.0027,0.0129,0.0214,0.0129,0.0027,0.0001,
 0.0010,0.0129,0.0582,0.0960,0.0582,0.0129,0.0010,
 0.0016,0.0214,0.0960,0.1586,0.0960,0.0214,0.0016,
 0.0010,0.0129,0.0582,0.0960,0.0582,0.0129,0.0010,
 0.0001,0.0027,0.0129,0.0214,0.0129,0.0027,0.0001,
 0.0000,0.0001,0.0010,0.0016,0.0010,0.0001,0.0000]
 
# 用于进行形态学运算的结构矩阵，共有三个，第二个效果比较好
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
# 形态学腐蚀函数				  
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
# 形态学膨胀函数
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
# 形态学闭运算
def Close(image,structure_data,radius) :
	iExpand = Expand(image,structure_data,radius) 
	iCorrode = Corrode(iExpand,structure_data,radius) 
	iClose = iCorrode
	return iClose
# 形态学开运算
def Open(image,structure_data,radius) :
	iCorrode = Corrode(image,structure_data,radius)
	iExpand = Expand(iCorrode,structure_data,radius) 
	iOpen = iExpand
	return iOpen
# 用于实现高斯收敛的卷积运算，也适用于其他进行卷积的地方 但是速度较慢 后期取消之后影响不大
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
# 普通二值化函数，将灰度图像变为二值图像，仅用在分割函数内，后面还有智能二值化函数
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


# 分割第一步  输入：原图，形态学结构算子，结构算子半径
def Segment_First(image,structure_data,radius1) :
	(iMag,X_Grad,Y_Grad) = Magnitude(image)
	# iConvolution = Convolution(iMagnitude,operator,radius2)
	iBinary = Binary(iMag)
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
# 分割第二步 输入： 原图，梯度总矢量图，梯度x分量图，梯度y分量图
def Segment_Second(image,image0,image1,image2) :
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
# 分割第三步 输入 ：原图，分割第一步的返回值，分割第二步返回值 ,返回二值化的分割结果和正常分割结果
def Segment_Final(image,image1,image2) :
	width  = image1.size[0]
	height = image1.size[1]
	iFinal_Binary = Image.new("L",(width,height),255)
	iFinal = Image.new("L",(width,height),255)
	pix1 = image.load()
	pix2 = iFinal.load()
	for y in range(height) :
		for x in range(width) :
			temp1 = image1.getpixel((x,y))
			temp2 = image2.getpixel((x,y))
			if temp1 == temp2 and temp1 != 255 :
				iFinal_Binary.putpixel((x,y),0)
				pix2[x,y] = pix1[x,y]
			elif temp1 != temp2 :
				iFinal_Binary.putpixel((x,y),255)
	 			pix2[x,y] = 255
	return (iFinal_Binary,iFinal)
	
# 分割主程序 综合前三步骤，得到分割后的图像 输入：原图
def Segment(image) :
	(iMag,x_Grad,y_Grad) = Magnitude(image)
	iMag    = iMag.convert("L")
	x_Grad  = x_Grad.convert("L")
	y_Grad  = y_Grad.convert("L")
	iRebuild = Segment_First(image,structure_data_two,3) 
	iResult  = Segment_Second(image,iMag,x_Grad,y_Grad)
	iRebuild = iRebuild.convert("L")
	iResult  = iResult.convert("L")
	(iFinal_Binary,iFinal) = Segment_Final(image,iRebuild,iResult)
	return (iFinal_Binary,iFinal)
# ******************************************************************* #
# ******************************************************************* #
# 灰度均衡算法，使指纹图像对比更强烈 输入：分割后的正常图 有点问题
def Equalize(image) :
	a = [0] * 256
	width  = image.size[0]
	height = image.size[1]
	iEqualize = Image.new("L",(width,height),255)
	pix1 = image.load()
	pix2 = iEqualize.load()
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
	return iEqualize

# *************************************************************** #
# 指纹平滑算法，运用一些平滑算子对图像进行平滑处理  这里用的是[1.0/9] * 9
def Smooth(image) :
	width  = image.size[0]
	height = image.size[1]
	iSmooth = Image.new("L",(width,height),255)
	array = [1.0/9]*9
	for i in range(height) :
		for j in range(width) :
			if i in [0,height-1] or j in [0,width-1] :
				iSmooth.putpixel((j,i),image.getpixel((j,i)))
			else :
				a = [0] * 9
				for k in range(3) :
					for m in range(3) :
						a[k*3+m] = image.getpixel((j-1+m,i-1+k))
				sum = 0
				for l in range(9) :
					sum = sum + array[l]*a[l]
				iSmooth.putpixel((j,i),int(sum))
	return iSmooth

# ******************************************************************** #
# ******************************************************************** #
# 智能增强函数，第一步使用Gabor滤波器使纹线黑的更黑，白的更白。
# 但是需要一个预处理，对方向图进行编码输出
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
		
def Gabor_Enhance(image,image_Dir) :
	width = image.size[0]
	height = image.size[1]
	iGabor = Image.new("L",(width,height),255)
	iTemp  = Image.new("L",(width,height),255)
	
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
				iTemp.putpixel((x,y),uint8(sum/hsum))
			else :
				iTemp.putpixel((x,y),255)
				
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
					sum += Vw[k] * iTemp.getpixel((x + Direction_Block[d * Direction_Block_Width + k][0],y + Direction_Block[d * Direction_Block_Width + k][1]))
					vsum += Vw[k]
			if vsum > 0 :
				sum /= vsum
				if sum >255 :
					iGabor.putpixel((x,y),255)
				elif sum < 0 :
					iGabor.putpixel((x,y),0)
				else :
					iGabor.putpixel((x,y),uint8(sum))
			else :
				iGabor.putpixel((x,y),255)
	return iGabor
	
# 第二步：智能二值化，噪声比较多，需要继续去噪，输入：Gabor滤波后的图片
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
# 第三步：去噪 ，去掉二值化后的噪声 输入：上一步得到的智能二值化图片		
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
# 最后一个综合函数，实现增强以及后处理，输入：分割后的正常图，分割后的方向图
def Enhance(image,direction) :
	width  = image.size[0]
	height = image.size[1]
	iGabor = Image.new("L",(width,height),255)
	iBinary  = Image.new("L",(width,height),255)
	iEnhance = Image.new("L",(width,height),255)
	iGabor = Gabor_Enhance(image,direction)
	iBinary = AI_Binary(iGabor,direction)
	iEnhance = Denoising(iBinary)
	return iEnhance
	
# ************************************************************************* #
# ************************************************************************* #
# 指纹细化。这是处理中的最后一步，细化完了同样需要去噪
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


# 上面是细化表，这里是细化算法，仅保留每条纹线的一个像素。 输入：Gabor增强后的图片
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
# 指纹细化后的去噪算法 !!! we are done 后续处理很好 加了一层新的循环 去掉前一次得到的孤立点
# 输入 ： 细化后的图片，len是想要清除的短棒的长度，自定义
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
# 同理，来一个综合函数，直接得到最终结果
def Thinning(image,len) :
	width = image.size[0]
	height = image.size[1]
	iThin = Image.new("L",(width,height),255)
	iThin = Thin(image)
	iThin = Thin_Pro(iThin,len)
	return iThin
	

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
	
	print singular
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

def ColorToGrey(image) :
	width  = image.size[0]
	height = image.size[1]
	grey   = Image.new("L",(width,height),'white')
	pix1   = image.load()
	pix2   = grey.load()
	for y in range(height) :
		for x in range(width) :
			if pix1[x,y] == (255,0,255) :
				pix2[x,y] = 0 
			elif pix1[x,y] == (255,255,0) :
				pix2[x,y] = 23
			elif pix1[x,y] == (0,0,255) :
				pix2[x,y] = 45 
			elif pix1[x,y] == (0,255,0) :
				pix2[x,y] = 68
			elif pix1[x,y] == (255,0,0) :
				pix2[x,y] = 90 
			elif pix1[x,y] == (0,255,255) :
				pix2[x,y] = 113
			elif pix1[x,y] == (255,255,255) :
				pix2[x,y] = 135
			elif pix1[x,y] == (0,0,0) :
				pix2[x,y] = 158
	return grey
	
im = Image.open("D:\\Python2.7\\image\\sample2\\9.bmp").convert("L")

d = Image.open("D:\\Python2.7\\image\\sample2\\c.bmp")

divide = Image.open("D:\\Python2.7\\image\\sample2\\Divide.bmp").convert("L")

thin = Image.open("D:\\Python2.7\\image\\sample2\\Thin.bmp").convert("L")


IsSingular(thin,ColorToGrey(d),divide,1)


#iDirection_Dot,iDirection_succession  = Direction(im,divide)
#iDirection_succession.show()
#g = Enhance(im,d)
#g.show()



'''
# ************************************************************************* #
# ************************************************************************* #
# 这里进入第二部分，识别特征点和奇异点。特征点主要包括：端点、叉点；奇异点包括：core，delta，whorl
# 该函数用于识别端点和叉点，并且去掉不符合条件的端点和叉点，端点已调好，叉点还没加上
# image1 : 细化图 image2 ： 分割后的黑白图
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
					Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 255)
					dot.append((x,y))
				elif sum == 6 * 255 :
					Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 255)
					fork.append((x,y))
				else :
					continue
	
	# 去除边缘端点 思路：根据是否靠近背景块来判断 使用了黑白分明的背景块图片1_rebuild.bmp
	flag1 = 0
	flag2 = 0
	dot1 = deepcopy(dot)
	for one in dot :
		for n in range(32) :
			for m in range(32) :
				tempx = one[0] - 16 + m
				tempy = one[1] - 16 + n
				if (-1<tempx<width and -1<tempy<height and pix2[tempx,tempy] == 255) :
					Draw.ellipse((one[0]-1,one[1]-1,one[0]+1,one[1]+1),fill = 255,outline = 255)
					flag1 = 1
					dot1.remove((one[0],one[1]))
					break
				elif (tempx<0 or tempx>=width or tempy<0 or tempy>=height) :
					Draw.ellipse((one[0]-1,one[1]-1,one[0]+1,one[1]+1),fill = 255,outline = 255)
					flag2 = 1
					dot1.remove((one[0],one[1]))
					break
				else :
					continue
			if flag1 == 1 or flag2 == 1 :
				flag1 = 0
				flag2 = 0
				break
			else :
				continue
				
	# dot2是dot1的相同副本，用于第二次遍历比较		
	dot2 = deepcopy(dot1)
	dellist = []
	for each in dot1 :
		for n in range(16) :
			for m in range(16) :
				tempx = each[0] - 8 + m
				tempy = each[1] - 8 + n 
				tuple = (tempx,tempy)
				for var in dot2 :
					if var == tuple and var != each :
						dellist.append(var)
						dellist.append(each)
						break
					else :
						continue
					
	dellist_nosame = []
	# 去掉列表中重复的元素，仅保留一个
	for each in dellist :
		if each not in dellist_nosame :
			dellist_nosame.append(each)
	# 去掉图片上距离太近的伪端点
	# dot是首次检测的所有端点坐标列表总和
	# dot1是去掉边缘不合格端点后的列表
	# dot2是在dot1基础上再次去掉距离太近的端点的列表
	for each in dellist_nosame :
		Draw.ellipse((each[0]-1,each[1]-1,each[0]+1,each[1]+1),fill = 255,outline = 255)
		dot2.remove(each)
	return copy				

# 下面的函数用于检测并识别出奇异点 	
cell3 = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
cell5 = [(-2,-1),(-2,0),(-2,1),(-1,2),(0,2),(1,2),(2,1),(2,0),(2,-1),(1,-2),(0,-2),(-1,-2),(-2,-1)]

signum = lambda x: -1 if x < 0 else 1

def get_angle(left,right) :
	angle = left - right 
	if abs(angle) > 180 :
		angle = -1 * signum(angle) * (360 - abs(angle))
	return angle
	
# image1:细化图，image2：方向图 image3:前后背景图 tolerance：容错阈值
def IsCore(image1,image2,image3,tolerance) :
	width  = image1.size[0]
	height = image1.size[1]
	
	copy = image1.copy()
	Draw = ImageDraw.Draw(copy)
	
	pix1 = image1.load()
	pix2 = image2.load()
	pix3 = image3.load()
	
	singular = []
	
	for y in range(3,height-3) :
		for x in range(3,width-3) :
		
			if pix3[x,y] == 255 :
				continue
				
			sum1 = 0
			angle_list_in = [Direction_Index(pix2[x+i,y+j]) % 180  for i,j in cell3]
			sum2 = 0
			angle_list_out = [Direction_Index(pix2[x+i,y+j]) % 180 for i,j in cell5]
			
			for k in range(8) :
				if abs(get_angle(angle_list_in[k],angle_list_in[k+1])) > 90 :
					angle_list_in[k+1] += 180
				sum1 += get_angle(angle_list_in[k],angle_list_in[k+1])
			for k in range(12) :
				if abs(get_angle(angle_list_out[k],angle_list_out[k+1])) > 90 :
					angle_list_out[k+1] += 180
				sum2 += get_angle(angle_list_out[k],angle_list_out[k+1])
			if 180 - tolerance <= sum1 and sum1 <= 180 + tolerance and 180 - tolerance <= sum2 and sum2 <= 180 + tolerance :
				print "loop"
				#Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 0)
				singular.append((x,y))
				
			elif -180 - tolerance <= sum1 and sum1 <= -180 + tolerance and -180 - tolerance <= sum2 and sum2 <= -180 + tolerance :
				print "delta"
				#Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 0)
				singular.append((x,y))
				
			elif 360 - tolerance <= sum1 and sum1 <= 360 + tolerance and 360 - tolerance <= sum2 and sum2 <= 360 + tolerance:
				print "whorl"
				#Draw.ellipse((x-1,y-1,x+1,y+1),fill = 255,outline = 0)
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
	return copy	
'''