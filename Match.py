# #!/usr/bin/python
# -*- coding: utf-8 -*-
# 基本成型
import wx,os,Image
from Restart import *
pathlist = [0]*2 

def OnOpen1(event) :
	dialog = wx.FileDialog(None,'items',style = wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK :
		# filename.SetValue(dialog.GetPath())
		img = wx.Image(name = dialog.GetPath(),type = wx.BITMAP_TYPE_ANY,index = -1)
		bmp1.SetBitmap(wx.BitmapFromImage(img))
		img.Destroy()
	dialog.Destroy()
	pathlist[0] = dialog.GetPath()
def OnOpen2(event) :
	dialog = wx.FileDialog(None,'items',style = wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK :
		img = wx.Image(name = dialog.GetPath(),type = wx.BITMAP_TYPE_ANY,index = -1)
		bmp2.SetBitmap(wx.BitmapFromImage(img))
		img.Destroy()
	dialog.Destroy()
	pathlist[1] = dialog.GetPath()
		
def PatternMatch(event) :
	fpath1 = pathlist[0]
	fpath2 = pathlist[1]
	p1,f1  = os.path.split(fpath1)
	p2,f2  = os.path.split(fpath2)
	#print p1+'\a.bmp',f1,p2,f2
	thin1  = Image.open(p1+'\\thin.bmp').convert("L")
	dir1   = Image.open(p1+'\\dir.bmp').convert("L")
	divide1= Image.open(p1+'\\divide.bmp').convert("L")
	thin2  = Image.open(p2+'\\thin.bmp').convert("L")
	dir2   = Image.open(p2+'\\dir.bmp').convert("L")
	divide2= Image.open(p2+'\\divide.bmp').convert("L")
	A_copy,A_qualified = IsFeature(thin1,divide1,dir1)
	B_copy,B_qualified = IsFeature(thin2,divide2,dir2)
	A_Struct_Array = Compare(A_qualified)
	B_Struct_Array = Compare(B_qualified)
	result_str = ShowResult(A_Struct_Array,B_Struct_Array,A_qualified,B_qualified)
	#thin1.show()
	dialog = wx.MessageDialog(None,result_str,'Message',style = wx.OK|wx.CANCEL)
	if dialog.ShowModal() == wx.ID_OK :
		dialog.Destroy()
		
app = wx.App()
win = wx.Frame(None,title = "指纹匹配".decode('utf-8','ignore').encode('gbk'),size = (582,505))
bkg = wx.Panel(win)

# 创建组件
openbutton1 = wx.Button(bkg,label = '打开'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (85,20))
openbutton1.Bind(wx.EVT_BUTTON,OnOpen1)

openbutton2 = wx.Button(bkg,label = '打开'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (405,20))
openbutton2.Bind(wx.EVT_BUTTON,OnOpen2)

matchbutton = wx.Button(bkg,label = '匹配'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (245,20))
matchbutton.Bind(wx.EVT_BUTTON,PatternMatch) 
# filename = wx.TextCtrl(bkg)
bmp1 = wx.StaticBitmap(bkg,pos = (20,95), size = (256,360))
bmp2 = wx.StaticBitmap(bkg,pos = (306,95),size = (256,360))
# 生成布局管理器 使组件随着鼠标更改
'''
hbox = wx.BoxSizer()
hbox.Add(filename,proportion = 1,flag = wx.EXPAND)
hbox.Add(openbutton,proportion = 0,flag = wx.LEFT,border = 5)

vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 5) 
vbox.Add(bmp,proportion = 1,flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,border = 5)

bkg.SetSizer(vbox)
'''
win.Show()




app.MainLoop()



