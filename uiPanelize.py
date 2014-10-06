#!/usr/bin/python2
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

import gtk, pango
from os import path as pt, chdir as cd

class EasyTextView(gtk.TextView):
	def __init__(self):
		super(EasyTextView, self).__init__()
		self.autoscroll = True

	def clear_text(self):
		self.get_buffer().set_text('')

	def set_size_request(self, x, y):
		try:
			parent = self.get_parent()
			bPass = True
		except AttributeError, e:
			bPass = False
		if bPass and(isinstance(parent, gtk.ScrolledWindow)):
			parent.set_size_request(x, y)
		else:
			super(EasyTextView, self).set_size_request(x, y)

	def get_text(self):
		tBuff = self.get_buffer()
		return tBuff.get_text(tBuff.get_start_iter(), tBuff.get_end_iter())

	set_text = lambda self, txt: self.get_buffer().set_text(txt)

	def insert_end(self, txt, tag=None):
		buff = self.get_buffer()
		end = buff.get_end_iter()
		text = txt.encode('utf-8', errors='replace')
		if tag:
			buff.insert_with_tags(end, text, tag)
		else:
			buff.insert(end, text)
		del(end)

	def reScrollV(self, adjV, scrollV):
		"""Scroll to the bottom of the TextView when the adjustment changes."""
		if self.autoscroll:
			adjV.set_value(adjV.upper - adjV.page_size)
			scrollV.set_vadjustment(adjV)
		return

	def setTabSpace(self, spaces, fontDesc=None):
		pangoTabSpc = self.getTabPixelWidth(spaces, fontDesc=fontDesc)
		tabArray =  pango.TabArray(1, True)
		tabArray.set_tab(0, pango.TAB_LEFT, pangoTabSpc)
		self.set_tabs(tabArray)
		return pangoTabSpc

	def getTabPixelWidth(self, spaces, fontDesc=None):
		txtTab = ' ' * spaces
		pangoLayout = self.create_pango_layout(txtTab)
		if fontDesc:
			pangoLayout.set_font_description(fontDesc)
		pangoTabSpc = pangoLayout.get_pixel_size()[0]
		del(pangoLayout)
		return pangoTabSpc

class apw:
	def Label(self, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None, xalign=None, selectable=False):
		if not height:
			height=self.Height
		hLabel = gtk.Label(txtLabel)
		if fontDesc:
			hLabel.modify_font(fontDesc)
		if type(xalign)==float and(0.<=xalign<=1.):
			yalign = hLabel.get_alignment()[1]
			hLabel.set_alignment(xalign, yalign)
		if type(selectable)==bool:
			hLabel.set_selectable(selectable)
		hLabel.show()
		hLabel.set_size_request(width, height)
		if hFixed:
			hFixed.put(hLabel, posX, posY)
		return hLabel

	def Num(self, numTup, hFixed, posX, posY, width, partDigits=0, height=None, fontDesc=None):
		if not height:
			height=self.Height
		numInit, numMin, numMax, numStep = numTup
		hAdj =  gtk.Adjustment(value=numInit, lower=numMin, upper=numMax, step_incr=numStep,
			page_incr=0, page_size=0)
		hSpin = gtk.SpinButton(hAdj, 0, partDigits)
		hSpin.set_numeric(True)
		if fontDesc:
			hSpin.modify_font(fontDesc)
		hSpin.set_size_request(width, height)
		hSpin.set_update_policy(gtk.UPDATE_IF_VALID)
		hFixed.put(hSpin, posX, posY)
		return hSpin

	def ComboBox(self, modelCb, hFixed, posX, posY, width, height=None, fontDesc=None, wrap=None, selTxt=0):
		if not height:
			height=self.Height
		hCb = gtk.ComboBox()
		crtCb = gtk.CellRendererText()
		if fontDesc:
			crtCb.set_property('font-desc', fontDesc)
		hCb.pack_start(crtCb)
		hCb.set_attributes(crtCb, text=selTxt)
		if wrap:
			hCb.set_wrap_width(wrap)
		else:
			crtCb.set_property('ellipsize', pango.ELLIPSIZE_END)
		hCb.set_model(modelCb)
		hCb.set_size_request(width, height+4)
		hFixed.put(hCb, posX, posY-2)
		return hCb

	def Butt(self, txtLabel, hFixed, posX, posY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
		"""If stockID is set, txtLabel set as True means full stock button,
		non-null string - own Label for stock image,
		in other case - button with only stock image"""
		if not height:
			height=self.Height
		if stockID == None and fileImage == None:
			hButt = gtk.Button(label=txtLabel, use_underline=False)
			if fontDesc:
				hLabel = hButt.child
				hLabel.modify_font(fontDesc)
		else:
			if type(txtLabel)==int or type(txtLabel)==float or type(txtLabel)==type(None) or (type(txtLabel)==str and txtLabel==''):
				txtLabel = bool(txtLabel)
			if type(txtLabel)==bool and txtLabel==True or type(txtLabel)==str:
				if stockID:
					hButt = gtk.Button(stock=stockID)
				elif fileImage:
					image = gtk.Image()
					image.set_from_file(fileImage)
					hButt = gtk.Button()
					hButt.add(image)
				if type(txtLabel)==str:
					hLabel = hButt.get_children()[0].get_children()[0].get_children()[1]
					hLabel.set_text(txtLabel)
					if fontDesc:
						hLabel.modify_font(fontDesc)
			else:
				image = gtk.Image()
				if stockID:
					image.set_from_stock(stockID, gtk.ICON_SIZE_BUTTON)
				elif fileImage:
					image.set_from_file(fileImage)
				hButt = gtk.Button()
				hButt.add(image)
		hButt.set_size_request(width, height)
		hFixed.put(hButt, posX, posY)
		return hButt

	def Check(self, txtLabel, hFixed, posX, posY, width, height=None, fontDesc=None):
		if not height:
			height=self.Height
		hCheck = gtk.CheckButton(label=txtLabel, use_underline=False)
		hLabel=hCheck.child
		hCheck.set_size_request(width, height)
		hFixed.put(hCheck, posX, posY)
		return hCheck

	def TextView(self, hFixed, posX, posY, width, height, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
		hTextView = EasyTextView()
		hTextView.set_property("editable", bEditable)
		if fontDesc:
			hTextView.modify_font(fontDesc)
			hTextView.setTabSpace(tabSpace, fontDesc=fontDesc)
		if bWrap:
			hTextView.set_wrap_mode(gtk.WRAP_WORD)
		scrollViewTxt = gtk.ScrolledWindow()
		vadj = scrollViewTxt.get_vadjustment()
		vadj.connect('changed', hTextView.reScrollV, scrollViewTxt)
		scrollViewTxt.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrollViewTxt.add(hTextView)
		scrollViewTxt.set_size_request(width, height)
		hFixed.put(scrollViewTxt, posX, posY)
		return hTextView

	def dialogChooseFile(self, parent=None, startDir=None, startFile=None, title='Select a file...', act='file_open', bShowHidden=False):
		action = {
			'file_open': gtk.FILE_CHOOSER_ACTION_OPEN,
			'file_save': gtk.FILE_CHOOSER_ACTION_SAVE,
			'dir_open': gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			'dir_create': gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
			}[act]
		hDialog = gtk.FileChooserDialog(title=title, parent=parent, action=action,
			buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK) )
		hDialog.set_default_response(gtk.RESPONSE_OK)
		hDialog.set_show_hidden(bShowHidden)
		if startDir:
			hDialog.set_current_folder(startDir)
		if startFile:
			if act=='file_save':
				hDialog.set_current_name(startFile)
			elif act=='file_open':
				hDialog.set_filename(startFile)
		respFileName = hDialog.run()
		fileName = None
		if respFileName==gtk.RESPONSE_OK:
			fileName = hDialog.get_filename()
		hDialog.destroy()
		return fileName

def getTxtPixelWidth(widget, txt, fontDesc=None):
	pangoLayout = widget.create_pango_layout(txt)
	if fontDesc:
		pangoLayout.set_font_description(fontDesc)
	pangoTxtSpc = pangoLayout.get_pixel_size()[0]
	del(pangoLayout)
	return pangoTxtSpc

class radioFrame(gtk.Frame):
	def __init__(frame, txtLabel, parentFixed, lsVal, x, y, row_height, active=0, wrap=0, fontDesc=None):
		super(gtk.Frame, frame).__init__(label=txtLabel)
		items = len(lsVal)
		frame.fixed = gtk.Fixed()
		frame.lsRet = map(lambda row: row[1], lsVal)
		if type(wrap) is not int or(wrap<0):
			wrap = 0
		frameW = 5
		maxColW = 0
		posX = 2
		for idx, (radioTxt, radioValue) in enumerate(lsVal):
			if idx:
				hRadio = gtk.RadioButton(group=hMainRadio, label=radioTxt)
			else:
				hRadio = hMainRadio = gtk.RadioButton(group=None, label=radioTxt)
			if fontDesc:
				hRadio.modify_font(fontDesc)
			radioW = getTxtPixelWidth(hRadio, radioTxt, fontDesc=fontDesc)+20
			if wrap:
				maxColW = max(maxColW, radioW)
				if not(idx%wrap) or(idx==items-1) and(items%wrap):
					frameW += maxColW+2
				if idx and(not(idx%wrap)):
					posX += maxColW+2
					maxColW = 0
				posY = (idx%wrap)*row_height
				if idx==items-1: frameW += 3
			else:
				posY = idx*row_height
				frameW = max(frameW, radioW)
				if idx==items-1: frameW += 5
			hRadio.set_size_request(radioW, row_height-2)
			frame.fixed.put(hRadio, posX, posY)
			hRadio.connect("toggled", frame.callBack, radioValue)
		frameH = (wrap+1)*row_height if wrap else (items+1)*row_height
		frame.add(frame.fixed)
		frame.set_size_request(frameW, frameH)
		parentFixed.put(frame, x, y)
		frame.group = tuple(reversed(hMainRadio.get_group()))
		if type(active) is not int or(active>=items):
			frame.value = None
			return
		frame.set_active(active)

	def callBack(frame, radio, value):
		if radio.get_active():
			frame.value = value
			frame.active = frame.group.index(radio)

	get_active = lambda frame: frame.active
	set_active = lambda frame, active: frame.group[active].set_active(True) 
	get_value = lambda frame: frame.value

class rasterMetricMils(gtk.Fixed):
	def __init__(fixed, txtLabel, parentFixed, apw, x, y, fontDesc=None):
		super(gtk.Fixed, fixed).__init__()
		fixed.Check = apw.Check(txtLabel, fixed, 0, 0, 40)
		cw = getTxtPixelWidth(fixed.Check, txtLabel, fontDesc=fontDesc)+15
		fixed.Check.set_size_request(cw, apw.Height)
		fixed.MM = apw.Num((0, 0, 500, 1), fixed, cw, 0, 70, partDigits=4)
		apw.Label("mm=", fixed, cw+72, 0, 23)
		fixed.Mils = apw.Num((0, 0, 20000, 10), fixed, cw+95, 0, 70, partDigits=3)
		apw.Label("mils", fixed, cw+165, 0, 20)
		parentFixed.put(fixed, x, y)
		fixed.MM.connect("value-changed", fixed.units)
		fixed.Mils.connect("value-changed", fixed.units)
		fixed.Check.connect("toggled", fixed.toggled)
		fixed.set_checked(False)
		fixed.set_value(0)

	def units(fixed, intOrWidget):
		from pcbnew import FromMils, FromMM, ToMils, ToMM
		if intOrWidget==fixed.MM:
			fixed.value = FromMM(intOrWidget.get_value())
			testVal =  FromMils(fixed.Mils.get_value())
			if fixed.value != testVal:
				setV = ToMils(fixed.value)
				fixed.Mils.set_value(setV)
				if __name__ == "__main__":
					fixed.logView.insert_end("%gmils\n" % setV)
		elif intOrWidget==fixed.Mils:
			fixed.value = FromMils(intOrWidget.get_value())
			testVal =  FromMM(fixed.MM.get_value())
			if fixed.value != testVal:
				setV = ToMM(fixed.value)
				fixed.MM.set_value(setV)
				if __name__ == "__main__":
					fixed.logView.insert_end("%gmm\n" % setV)
		elif type(intOrWidget)==int:
			fixed.value = intOrWidget
			fixed.MM.set_value(ToMM(intOrWidget))
			fixed.Mils.set_value(ToMils(intOrWidget))

	def toggled(fixed, widget):
		bCheck = widget.get_active()
		fixed.Mils.set_sensitive(bCheck)
		fixed.MM.set_sensitive(bCheck)

	def set_checked(fixed, bCheck):
		fixed.Check.set_active(bCheck)
		fixed.Mils.set_sensitive(bCheck)
		fixed.MM.set_sensitive(bCheck)

	get_checked = lambda fixed: fixed.Check.get_active()
	set_value = lambda fixed, value: fixed.units(value)
	get_value = lambda fixed: fixed.value

class panelizeUI:
	def __init__(ui):
		from sys import path as ptSys
		ui.apw = apw()
		ui.gtk = gtk
		ui.fontDesc = pango.FontDescription('Univers,Sans Condensed 8')
		ui.fontFixedDesc = pango.FontDescription('Terminus,Monospace Bold 7')
		ui.apw.Height = 25
		ui.uiInit()
		if __name__ == "__main__":
			ui.mainWindow.connect("destroy", lambda w: ui.uiExit())
			ui.buttonExit.connect("clicked", lambda w: ui.uiExit())
			ui.buttonProceed.connect("clicked",
				lambda w: ui.logView.insert_end("Angle: %0.1f°\n" % (ui.rfAngle.get_value()/10)))
			ui.logView.insert_end("User Interface Test...\nSo long… So long… So long… So long… long… Sooooo long…\n")
			ui.uiEnter()

	uiEnter = lambda ui: gtk.main()
	uiExit = lambda ui: gtk.main_quit()

	def uiInit(ui):
		from gobject import TYPE_STRING as goStr, TYPE_INT as goInt
		apw =  ui.apw
		ui.callDir = pt.dirname(pt.abspath(__file__))
		cd(ui.callDir)
		ui.title = "pcbnew py module based Panelizator v.0.7. For BZR>5161"
		ui.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		ui.wdhMain, ui.hgtMain = (580, 300)
		ui.mainWindow.set_geometry_hints(min_width=ui.wdhMain, min_height=ui.hgtMain)
		ui.mainWindow.set_size_request(ui.wdhMain, ui.hgtMain)
		ui.mainWindow.set_title(ui.title)
		ui.mainWindow.set_border_width(5)
		accGroup = gtk.AccelGroup()
		ui.mainWindow.add_accel_group(accGroup)
		mainFrame = ui.mainFrame = gtk.Fixed()

		ui.logView = ui.apw.TextView(mainFrame, 5, 5, 0, 0,
			bEditable=False, tabSpace=4, fontDesc = ui.fontFixedDesc)

		lsAngle = map(lambda n: ((u"{}°".format(n*90)), (int((n*90+360)%360*10))), (range(-1, 3)))
		ui.rfAngle = radioFrame("Rotate:", mainFrame, lsAngle, 0, 0, 20,
			active=1, wrap=2, fontDesc=ui.fontDesc)

		ui.labFilename = apw.Label("File:", mainFrame, 0, 0, 30)
		if __name__ == "__main__":
			ui.txtFilename = apw.Butt('Test', mainFrame, 0, 0, 0)
		else:
			ui.txtFilename = apw.Label(u'Drag file to log view or use „Open” button →',
				mainFrame, 0, 0, 0, xalign=0., selectable=True)
		ui.buttonFileName = ui.apw.Butt(None, mainFrame, 0, 0, 30, stockID=gtk.STOCK_OPEN)

		ui.Margin = rasterMetricMils("Margin:", mainFrame, apw, 0, 0)
		ui.SpaceX = rasterMetricMils("SpaceX:", mainFrame, apw, 0, 0)
		ui.SpaceY = rasterMetricMils("SpaceY:", mainFrame, apw, 0, 0)

		ui.buttonProceed = ui.apw.Butt("Proceed", mainFrame, 0, 0, 80, stockID=gtk.STOCK_MEDIA_PLAY)

		ui.logoBigPixbuf = gtk.gdk.pixbuf_new_from_file(pt.realpath(pt.expanduser("pics/panelize-pcb.svg")))
		gtk.window_set_default_icon_list(ui.logoBigPixbuf, )
		ui.imageLogo = gtk.Image()
		ui.imageLogo.set_from_pixbuf(ui.logoBigPixbuf)
		mainFrame.put(ui.imageLogo, 0, 0)

		ui.labCols = apw.Label("Columns:", mainFrame, 0, 0, 45)
		ui.Cols = apw.Num((1, 1, 999, 1), mainFrame, 0, 0, 37)

		ui.buttonClear = ui.apw.Butt("Clear log view", mainFrame, 0,  0, 80)
		ui.buttonClear.connect("clicked", lambda xargs: ui.logView.clear_text())

		ui.labRows = apw.Label("Rows:", mainFrame, 0, 0, 30)
		ui.Rows = apw.Num((1, 1, 999, 1), mainFrame, 0, 0, 37)

		ui.buttonExit = ui.apw.Butt("Exit (Ctrl+Q)", mainFrame, 0, 0, 80)
		ui.buttonExit.add_accelerator("clicked", accGroup, ord('Q'),
			gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE)

		ui.mainWindow.add(mainFrame)
		ui.mainWindow.show_all()
		ui.mainWindow.set_keep_above(True)
		ui.lastWinSize = None
		ui.mainWindow.connect("configure-event", ui.uiSize)

	def uiSize(ui, window, event):
		if event.type==gtk.gdk.CONFIGURE:
			w, h = event.width, event.height
			if ui.lastWinSize==(w, h):
				return True
			stdH = ui.apw.Height
			ui.lastWinSize = w, h
			if __name__ == "__main__":
				ui.logView.get_parent().set_size_request(w-20, h-200)
			else:
				ui.logView.get_parent().set_size_request(w-20, h-110)
			#y1 = h-130
			y1 = h-240
			y2 = h-100
			ui.mainFrame.move(ui.labFilename, 5, y2)
			ui.mainFrame.move(ui.txtFilename, 35, y2)
			ui.txtFilename.set_size_request(w-170, stdH)
			ui.mainFrame.move(ui.buttonFileName, w-130, y2)
			ui.mainFrame.move(ui.buttonProceed, w-95, y2)
			ui.mainFrame.move(ui.imageLogo, 0, h-57)
			x1, x2, y3 = 50, 445, h-70
			ui.mainFrame.move(ui.Margin, x1, h-80)
			ui.mainFrame.move(ui.SpaceX, x1, h-55)
			ui.mainFrame.move(ui.SpaceY, x1, h-30)
			ui.mainFrame.move(ui.rfAngle, 290, y3-3)
			ui.mainFrame.move(ui.labCols, x2-47, y3)
			ui.mainFrame.move(ui.Cols,  x2, y3)
			ui.mainFrame.move(ui.buttonClear, w-95, y3)
			y4 = h-40
			ui.mainFrame.move(ui.labRows, x2-32, y4)
			ui.mainFrame.move(ui.Rows, x2, y4)
			ui.mainFrame.move(ui.buttonExit, w-95, y4)
			return True

	def uiTick(ui):
		return True

# Entry point
if __name__ == "__main__":
	panelizeUI()
