#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image
from numpy import *
from scipy.ndimage import filters

# 黑白互补翻转
"""
im = Image.open("D:\\Python27\\fingerprint\\1.bmp")
im = im.convert("L")
itemp = Image.new("L",(im.size[0],im.size[1]),0)
for i in range(im.size[0]):  #height
	for j in range(im.size[1]): #width
		tmp_grey = 255 - im.getpixel((i,j))
		itemp.putpixel((i,j), gray_scale)
im.show()
itemp.show()

"""
# 平滑 
"""
im = Image.open("D:\\Python27\\fingerprint\\1.bmp")
im = im.convert("L")
width = im.size[0]
height = im.size[1]
iFilter = Image.new("L",(width,height),255)
array = [1.0/9]*9
for i in range(height) :
	for j in range(width) :
		if i in [0,height-1] or j in [0,width-1] :
			iFilter.putpixel((j,i),im.getpixel((j,i)))
		else :
			a = [0]*9
			for k in range(3) :
				for m in range(3) :
					a[k*3+m] = im.getpixel((j-1+m,i-1+k))
			sum = 0
			for l in range(9) :
				sum = sum + array[l]*a[l]
			iFilter.putpixel((j,i),int(sum))
iFilter.show()
im.show()
"""
# 灰度均衡

a = [0] * 256
im = Image.open("D:\\Python27\\picture\\1\\1.bmp")
im = im.convert("L")
width = im.size[0]
height = im.size[1]
iEqualize = Image.new("L",(width,height),255)
for i in range(height) :
	for j in range(width) :
		iGray = int(im.getpixel((j,i)))
		a[iGray] = a[iGray] + 1
for m in range(1,256) :
	a[m] = a[m] + a[m-1]
	
sum = max(a)
for k in range(256) :
	a[k] = a[k] * 255 / sum
for i in range(height) :
	for j in range(width) :
		iEqualize.putpixel((j,i),a[int(im.getpixel((j,i)))])
iEqualize.show()
im.show()


# 画出一幅图片对应的灰度直方图
"""
a = [0] * 256
im = Image.open("D:\\Python27\\lenna.jpg")
im = im.convert("L")
width = im.size[0]
height = im.size[1]
iHist = Image.new("RGB",(256,256),"white")
iHist.show()
iHist_Draw = ImageDraw.Draw(iHist)
for i in range(height) :
	for j in range(width) :
		iGray = int (im.getpixel((j,i)))
		a[iGray] = a[iGray] + 1
sum = max(a)
for k in range(256) :
	a[k] = a[k] * 255 / sum 
	x = (k,255)
	y = (k,255-a[k])
	iHist_Draw.line((x,y),fill = (255,0,0))
iHist.show()

"""


	








