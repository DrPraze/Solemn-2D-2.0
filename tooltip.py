from tkinter import *

class Tooltip(object):
	def __init__(self, widget):
		self.widget = widget
		self.tip_window = None

	def show(self, tip):
		if self.tip_window or not tip:
			return
		x, y, _cx, cy = self.widget.bbox(INSERT)
		x = x +self.widget.winfo_rootx()+25
		y = y+cy+self.widget.winfo_rooty()+25
		self.tip_window = tw = Toplevel(self.widget)
		tw.wm_overrideredirect(True)
		tw.wm_geometry("+%d+%d"%(x, y))
		label = Label(tw, text = tip, justify = LEFT,background = "#ffffe0", relief = SOLID, borderwidth = 1,font = ("tahoma", "8", "normal"))
		label.pack(ipadx = 1)

	def hide(self):
		tw = self.tip_window
		self.tip_window = None
		if tw:
			tw.destroy()

def create_Tip(widget, text):
	toolTip = Tooltip(widget)
	def enter(event):toolTip.show(text)
	def leave(event):toolTip.hide()
	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)
