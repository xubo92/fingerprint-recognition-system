# #!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

def OnOpen(event) :
	dialog = wx.FileDialog(None,'items',style = wx.OPEN)
	if dialog.ShowModal() == wx.ID_OK :
		filename.SetValue(dialog.GetPath())
		file = open(dialog.GetPath())
		contents.SetValue(file.read().decode('utf-8','ignore').encode('gbk'))
		file.close()
	dialog.Destroy()
	

app = wx.App()
win = wx.Frame(None,title = "lvxubo's notepad",size = (410,335))
bkg = wx.Panel(win)

# 创建组件
openbutton = wx.Button(bkg,label = 'Open')
openbutton.Bind(wx.EVT_BUTTON,OnOpen)

savebutton = wx.Button(bkg,label = 'Save')

filename = wx.TextCtrl(bkg)
contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE|wx.HSCROLL)


# 生成布局管理器 使组件随着鼠标更改
hbox = wx.BoxSizer()
hbox.Add(filename,proportion = 1,flag = wx.EXPAND)
hbox.Add(openbutton,proportion = 0,flag = wx.LEFT,border = 5)
hbox.Add(savebutton,proportion = 0,flag = wx.LEFT,border = 5)

# 一个布局管理器可以包含另一个管理器
vbox = wx.BoxSizer(wx.VERTICAL)
vbox.Add(hbox,proportion = 0,flag = wx.EXPAND|wx.ALL,border = 5) 
vbox.Add(contents,proportion = 1,flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,border = 5) 

bkg.SetSizer(vbox)
win.Show()




app.MainLoop()