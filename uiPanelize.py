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
		parent = self.get_parent()
		if parent and(isinstance(parent, gtk.ScrolledWindow)):
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
	def Label(self, txtLabel, hFixed, posX, poxY, width, height=None, fontDesc=None, xalign=None, selectable=False):
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
			hFixed.put(hLabel, posX, poxY)
		return hLabel

	def Num(self, numTup, hFixed, posX, poxY, width, partDigits=0, height=None, fontDesc=None):
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
		hFixed.put(hSpin, posX, poxY)
		return hSpin

	def ComboBox(self, modelCb, hFixed, posX, poxY, width, height=None, fontDesc=None, wrap=None, selTxt=0):
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
		hFixed.put(hCb, posX, poxY-2)
		return hCb

	def Butt(self, txtLabel, hFixed, posX, poxY, width, height=None, fileImage=None, stockID=None, fontDesc=None):
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
		hFixed.put(hButt, posX, poxY)
		return hButt

	def TextView(self, hFixed, posX, poxY, width, height, bWrap=False, bEditable=True, tabSpace=2, fontDesc=None):
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
		hFixed.put(scrollViewTxt, posX, poxY)
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
			ui.logView.insert_end("User Interface Test...\nSo long… So long… So long… So long… long… Sooooo long… ")
			ui.uiEnter()
			gtk.main()

	def uiEnter(ui):
		ui.cLoop = 0
		if not(hasattr(ui, 'margin')):
			ui.margin = 0
		ui.numMarginMils.connect("value-changed", ui.uiUnits)
		ui.numMarginMM.connect("value-changed", ui.uiUnits)
		from gobject import timeout_add as addTick
		ui.tickHnd = addTick(500, ui.uiTick)

	def uiExit(ui):
		from gobject import source_remove as unWatch
		unWatch(ui.tickHnd)
		gtk.main_quit()

	def uiInit(ui):
		from gobject import TYPE_STRING as goStr, TYPE_INT as goInt
		apw =  ui.apw
		ui.callDir = pt.dirname(pt.abspath(__file__))
		cd(ui.callDir)
		ui.title = "pcbnew py module based Panelizator. BZR>5160"
		ui.mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
		ui.wdhMain, ui.hgtMain = (550, 300)
		ui.mainWindow.set_geometry_hints(min_width=ui.wdhMain, min_height=ui.hgtMain)
		ui.mainWindow.set_size_request(ui.wdhMain, ui.hgtMain)
		ui.mainWindow.set_title(ui.title)
		ui.mainWindow.set_border_width(5)
		accGroup = gtk.AccelGroup()
		ui.mainWindow.add_accel_group(accGroup)
		mainFrame = ui.mainFrame = gtk.Fixed()

		apw.Label("Columns:", mainFrame, 5, 5, 45)
		ui.numCols = apw.Num((1, 1, 1000, 1), mainFrame, 55, 5, 45)
		apw.Label("Rows:", mainFrame, 110, 5, 30)
		ui.numRows = apw.Num((1, 1, 1000, 1), mainFrame, 145, 5, 45)
		apw.Label("Rotate:", mainFrame, 200, 5, 35)
		ui.lsAngle = gtk.ListStore(goStr, goInt)
		for n in range(-1, 3):
			ang = n*90
			ui.lsAngle.append( ("%i°" % ang, int((ang+360)%360*10)) )
		ui.cbAngle = apw.ComboBox(ui.lsAngle, mainFrame, 240, 6, 60)
		ui.cbAngle.set_active(1)
		
		ui.numMarginMM = apw.Num((0, 0, 500, 1), mainFrame, 350, 5, 70, partDigits=4)
		apw.Label("mm=", mainFrame, 422, 5, 23)
		apw.Label("Margin:", mainFrame, 310, 5, 40)
		ui.numMarginMils = apw.Num((0, 0, 20000, 10), mainFrame, 445, 5, 70, partDigits=3)
		apw.Label("mils", mainFrame, 515, 5, 20)

		ui.labFilename = apw.Label("File:", mainFrame, 5, 35, 30)
		if __name__ == "__main__":
			ui.txtFilename = apw.Butt('Test', mainFrame, 35, 35, 0)
		else:
			ui.txtFilename = apw.Label(u'Drag file to log view or use „Open” button →', mainFrame, 35, 35, 0, xalign=0., selectable=True)
		ui.buttonFileName = ui.apw.Butt(None, mainFrame, 0, 0, 30, stockID=gtk.STOCK_OPEN)
		ui.buttonProceed = ui.apw.Butt("Proceed", mainFrame, 0, 0, 80, stockID=gtk.STOCK_MEDIA_PLAY)

		ui.logView = ui.apw.TextView(mainFrame, 5, 65, 0, 0,
			bEditable=False, tabSpace=4, fontDesc = ui.fontFixedDesc)

		ui.logoBigPixbuf = gtk.gdk.pixbuf_new_from_file(pt.realpath(pt.expanduser("pics/panelize-pcb.svg")))
		gtk.window_set_default_icon_list(ui.logoBigPixbuf, )
		ui.imageLogo = gtk.Image()
		ui.imageLogo.set_from_pixbuf(ui.logoBigPixbuf)
		mainFrame.put(ui.imageLogo, 0, 0)

		ui.buttonClear = ui.apw.Butt("Clear log view", mainFrame, 0,  0, 80)
		ui.buttonClear.connect("clicked", lambda xargs: ui.logView.clear_text())

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
			ya = 5
			yb = 35
			ui.txtFilename.set_size_request(w-170, stdH)
			ui.mainFrame.move(ui.buttonFileName, w-130, yb)
			ui.mainFrame.move(ui.buttonProceed, w-95, yb)
			ui.logView.get_parent().set_size_request(w-20, h-130)
			ui.mainFrame.move(ui.imageLogo, 0, h-57)
			yc = h-37
			ui.mainFrame.move(ui.buttonClear, w-180, yc)
			ui.mainFrame.move(ui.buttonExit, w-95, yc)
			return True

	def uiTick(ui):
		if ui.cLoop>0:
			ui.cLoop -= 1
		return True

	def uiUnits(ui, widget):
		from pcbnew import FromMils, FromMM, ToMils, ToMM
		if widget==ui.numMarginMils:
			if not(ui.cLoop):
				ui.margin = FromMils(widget.get_value())
				setV = ToMM(ui.margin)
				ui.numMarginMM.set_value(setV)
				ui.cLoop += 1
				if __name__ == "__main__":
					ui.logView.insert_end("%gmm\n" % setV)
		elif widget==ui.numMarginMM:
			if not(ui.cLoop):
				ui.margin = FromMM(widget.get_value())
				setV = ToMils(ui.margin)
				ui.numMarginMils.set_value(setV)
				ui.cLoop += 1
				if __name__ == "__main__":
					ui.logView.insert_end("%gmils\n" % setV)
		elif widget=='init':
				ui.numMarginMM.set_value(ToMM(ui.margin))
				ui.numMarginMils.set_value(ToMils(ui.margin))

# Entry point
if __name__ == "__main__":
	panelizeUI()
