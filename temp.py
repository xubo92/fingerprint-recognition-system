#  #!/usr/bin/python
# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFilter
from numpy import *
from ctypes import *

class tagMinutiae(Structure) :
	__field__ = [('x',c_int),('y',c_int),('Direction',c_int),('Triangle',c_int*3),('Type',c_int)]
	
'''		
class tagFeature(Structure) :
	__field__ = [('MinutiaNum',c_int),('MinutiaArr',tagMinutiae*60)]
'''
Minutiae = tagMinutiae(x=1,y=6,Direction=135,Triangle=[4,5,6],Type=0)

Feature =  tagMinutiae * 3
f = Feature(Minutiae)

print f[0]