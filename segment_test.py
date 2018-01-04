#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from scipy.ndimage import filters

# 打算使用一种光滑轮廓的分割方法 但先要解决几个形态学计算问题
# 这个程序是利用半径为5的结构元素对图像进行腐蚀

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


structure_data_four = [1,1,1,
				  1,1,1,
				  1,1,1]

				  
def binary(image) :
	width = image.size[0]
	height = image.size[1]
	iBinary = Image.new("L",(width,height),255)
	for j in range(height) :	
		for i in range(width) :
			if image.getpixel((i,j)) < 220 :
				iBinary.putpixel((i,j),0)
			else :
				iBinary.putpixel((i,j),255)
	return iBinary
	


			  
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
				iCorrode.putpixel((x,y),255)
			elif image.getpixel((x,y)) == 255 :
				iCorrode.putpixel((x,y),255)
			else :
				flag = 0                       # 要始终记得变量清零
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
			for n in range(2 * radius + 1) :
				for m in range(2 * radius + 1) :
					if -1 < x - radius + m < width and -1 < y - radius + n < height and structure_data[(structure_num - 1) - (n*(2*radius+1) + m)]  == 1 and image.getpixel((x-radius+m,y-radius+n)) == 0 :
						iExpand.putpixel((x,y),0)
						break
				break
	return iExpand
			
				
im = Image.open("D:\\Python27\\picture\\character.gif")
im = im.convert("L")
iBinary = binary(im)
#iCorrode = Corrode(iBinary,structure_data,2)
iExpand = Expand(iBinary,structure_data_two,3)
im.show()

#iCorrode.show()
iExpand.show()


				