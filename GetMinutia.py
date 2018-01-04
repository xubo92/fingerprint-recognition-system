# #!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw
from numpy import *
from copy import deepcopy

SiteR5 = [(-5,0),(-5,1),(-5,2),(-4,3),(-3,4),(-2,5),(-1,5),(0,5),(1,5),
		  (2,5),(3,4),(4,3),(5,2),(5,1),(5,0),(5,-1),(5,-2),(4,-3),(3,-4),
		  (2,-5),(1,-5),(0,-5),(-1,-5),(-2,-5),(-3,-4),(-4,-3),(-5,-2),(-5,-1)]
SiteD8 = [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
		  
MAXRAWMINUTIANUM = 100 
MAXMINUTIANUM    = 60	

def IsFork(image) :
	
#　求两个角度的夹角	(0~90)
#  angle1,angle2 : 0~180
def GetJiaJiao(angle1,angle2) :
	a = abs(angle1-angle2)
	if a > 90 :
		a = 180 - a 
	return a
# now,last,next 都是表示坐标的元组
def GetNext(image,now,last) :
	pix = image.load()
	n = 0 
	save = []
	for i in range(8) :
		temp = (now[0]+SiteD8[i][0],now[1]+SiteD8[i][1])
		if pix[temp[0],temp[1]] == 0 and temp != last :
			n+= 1 
			save.append(temp)
	if n == 0 :
		return 1 
	elif n == 1 :
		
			
	return next
def GetMinutia(iThin,iDivide,iDirection) :
	r = 16 
	dGate = 16 
	bGood = False 
	densD = 7 
	ForkNum = 0 
	EndNum  = 0
	tempForkNum = 0
	tempEndNum  = 0 
	ForkArr =  [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * MAXRAWMINUTIANUM]
	EndArr  =  [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * MAXRAWMINUTIANUM]
	tempFork = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * MAXRAWMINUTIANUM]
	tempEnd  = [{'x':0,'y':0,'Direction':0,'Triangle':[0]*3,'Type':0} * MAXRAWMINUTIANUM]
	width  = iThin.size[0]
	height = iThin.size[1]
	pix1   = iThin.load()
	pix2   = iDivide.load()
	pix3   = iDirection.load()
	
	for y in range(17,height-17) :
		for x in range(17,width-17) :
			if  pix1[x,y] != 0 :
				continue 
			
			a = pix1[x-1,y+1] 
			b = pix1[x,y+1]
			c = pix1[x+1,y+1]
			d = pix1[x-1,y]
			f = pix1[x+1,y]
			g = pix1[x-1,y-1]
			h = pix1[x,y-1]
			i = pix1[x+1,y-1]
			sum = abs(a-b) + abs(b-c) + abs(c-f) + abs(f-i) + abs(i-h) + abs(h-g) + abs(g-d) + abs(d-a)
			if sum == 6 * 255 :
				flag = True 
				for i in range(-r,r+1) :
					for j in range(-r,r+1) :
						if y+i<0 or y+i>=height or x+j<0 or x+j>width :
							continue
						if pix3[x+j,y+i] == 255 :
							flag = False 
							break 
				anglesum = 0
				for i in range(28) :
					anglesum += GetJiaJiao(pix3[x+SiteR5[(i+1)%28][0],y+SiteR5[(i+1)%28][1]],pix3[x+SiteR5[i][0],y+SiteR5[i][1]])
				if anglesum > 96 :
					flag = False 
				if flag :
					ForkArr[ForkNum]['x'] = x 
					ForkArr[ForkNum]['y'] = y 
					ForkNum += 1 
					if ForkNum >= MAXRAWMINUTIANUM :
						ForkNum = 0 
						return 1 
			if sum == 2 * 256 :
				flag = True 
				for i in range(-r,r+1) :
					for j in range(-r,r+1) :
						if y+i<0 or y+i>=height or x+j<0 or x+j>=width :
							continue 
						if pix3[x+j,y+i] == 255 :
							flag = False 
							break
							
				anglesum = 0 
				for i in range(28) :
					anglesum += GetJiaJiao(pix3[x+SiteR5[(i+1)%28][0],y+SiteR5[(i+1)%28][1]],pix3[x+SiteR5[i][0],y+SiteR5[i][1]])
				if anglesum > 96 :
					flag = False 
				
				if flag :
					EndArr[EndNum]['x'] = x 
					EndArr[EndNum]['y'] = y 
					EndNum += 1 
					if EndNum >= MAXRAWMINUTIANUM :
						EndNum = 0 
						return 1 
	for i in range(MAXRAWMINUTIANUM) :
		tempEnd[i] = EndArr[i]
	for i in range(MAXRAWMINUTIANUM) :
		tempFork[i] = ForkArr[i]
	tempForkNum = ForkNum
	tempEndNum  = EndNum 
	
	bGood = False 
	loopnum = 0 
	while(!bGood and loopnum < 32) :
		loopnum += 1 
		for i in range(MAXRAWMINUTIANUM) :
			EndArr[i] = tempEnd[i]
			
		for i in range(MAXRAWMINUTIANUM) :
			ForkArr[i] = tempFork[i]
		ForkNum = tempForkNum
		EndNum  = tempEndNum
		
		bGood = True 
		for i in range(EndNum-1) :
			flag = False 
			for j in range(i+1,EndNum) :
				d = sqrt((EndArr[i]['x']-EndArr[j]['x']) ** 2 + (EndArr[i]['y']-EndArr[j]['y']) ** 2)
				if d > dGate and d > densD :
					continue 
				if d <= densD:
					EndArr[j]['x'] = 0
					EndArr[j]['y'] = 0 
					flag = True 
					continue 
				
		
	
						
					
			
			
			
			