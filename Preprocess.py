# #!/usr/bin/python
# -*- coding: utf-8 -*-
# 基本成型
import wx,os,Image
path = [0] 

def OnLoad(event) :
	dialog = wx.FileDialog(None,'items',style = wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK :
		img = wx.Image(name = dialog.GetPath(),type = wx.BITMAP_TYPE_ANY,index = -1)
		bmp.SetBitmap(wx.BitmapFromImage(img))
		img.Destroy()
	dialog.Destroy()
	path[0] = dialog.GetPath()
def OnGrad(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\grad.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()

def OnDirection(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\dir.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()

def OnEqualization(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\equ.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
def OnConvergence(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\conv.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
def OnEnhance(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\enhance.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
def OnBinary(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\binary.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
def OnThin(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\thin.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()

def OnFeature(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\feature.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
	
def OnSingular(event) :
	fpath = path[0]
	p,f   = os.path.split(fpath)
	img  = wx.Image(name = p + '\\singular.bmp',type = wx.BITMAP_TYPE_ANY, index = -1)
	bmp.SetBitmap(wx.BitmapFromImage(img))
	img.Destroy()
	
app = wx.App()
win = wx.Frame(None,title = "预处理".decode('utf-8','ignore').encode('gbk'),size = (582,605))
bkg = wx.Panel(win)

loadbutton = wx.Button(bkg,label = '打开'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,25))
loadbutton.Bind(wx.EVT_BUTTON,OnLoad)


gradbutton = wx.Button(bkg,label = '梯度图'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,75))
gradbutton.Bind(wx.EVT_BUTTON,OnGrad)

direbutton = wx.Button(bkg,label = '方向图'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,125))
direbutton.Bind(wx.EVT_BUTTON,OnDirection)

equabutton = wx.Button(bkg,label = '均衡'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,175))
equabutton.Bind(wx.EVT_BUTTON,OnEqualization)

convbutton = wx.Button(bkg,label = '高斯收敛'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,225))
convbutton.Bind(wx.EVT_BUTTON,OnConvergence)

enhabutton = wx.Button(bkg,label = 'Gabor增强'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,275))
enhabutton.Bind(wx.EVT_BUTTON,OnEnhance)

binabutton = wx.Button(bkg,label = '二值化'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,325))
binabutton.Bind(wx.EVT_BUTTON,OnBinary)

thinbutton = wx.Button(bkg,label = '细化'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,375))
thinbutton.Bind(wx.EVT_BUTTON,OnThin)

feabutton  = wx.Button(bkg,label = '特征点'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,425))
feabutton.Bind(wx.EVT_BUTTON,OnFeature)

sigubutton = wx.Button(bkg,label = '奇异点'.decode('utf-8','ignore').encode('gbk'),size = (80,25),pos = (50,475))
sigubutton.Bind(wx.EVT_BUTTON,OnSingular)

bmp = wx.StaticBitmap(bkg,pos = (250,83), size = (256,360))
win.Show()
app.MainLoop()