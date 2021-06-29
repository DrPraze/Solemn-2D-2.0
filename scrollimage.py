from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
import io, time, PIL, cv2
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
import tkinter.font
import numpy as np


# topx, topy, botx, boty = 0, 0, 0, 0
acts = []
past = []
class ScrollableImage(Frame):
	def __init__(self, master = None, **kw):
		self.image = kw.pop('image', None)
		self.line_width = line_width = kw.pop('line_width', None)
		sw = kw.pop('scrollbarwidth', 10)
		super(ScrollableImage, self).__init__(master = master, **kw)
		self.canvas = Canvas(self, highlightthickness = 0, **kw)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)
		# Vertical and Horizontal scrollbars
		self.v_scroll = Scrollbar(self, orient='vertical', width=sw)
		self.h_scroll = Scrollbar(self, orient='horizontal',width=sw)
		# Grid and configure weight.
		self.canvas.grid(row=0, column=0, sticky='nsew')
		self.h_scroll.grid(row=1, column=0, sticky='ew')
		self.v_scroll.grid(row=0, column=1, sticky='ns')
		self.rowconfigure(0, weight=10)
		self.columnconfigure(0, weight =10)
		# Set the scrollbars to the canvas
		self.canvas.config(xscrollcommand=self.h_scroll.set,yscrollcommand=self.v_scroll.set)
		# Set canvas view to the scrollbars
		self.v_scroll.config(command=self.canvas.yview)
		self.h_scroll.config(command=self.canvas.xview)
		# Assign the region to be scrolled
		self.canvas.config(scrollregion=self.canvas.bbox('all'))
		self.canvas.bind_class(self.canvas, "<MouseWheel>", self.mouse_scroll)

		self.count = 0
		self.mask = np.ones((490, 500))
		
	def mouse_scroll(self, evt):
		if evt.state == 0 :
			self.canvas.yview_scroll(-1*(evt.delta), 'units') # For MacOS
			self.canvas.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
		if evt.state == 1:
			self.canvas.xview_scroll(-1*(evt.delta), 'units') # For MacOS
			self.canvas.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows

	def change_image(self, img):
		self.canvas.create_rectangle(0, 0, 20000, 30000)
		self.canvas.create_image(0, 0, anchor='nw', image=img)

	def del_canvas(self):self.canvas.destroy()
	
	def clear(self):self.canvas.create_rectangle(0, 0, 2000, 2000, outline = None, fill = "white")

	def setup(self, line_width, pen, color = None):
		self.old_x = None
		self.old_y = None
		self.line_width = line_width
		self.color = "black" if color == None else color
		self.eraser_on = False
		self.active_button = pen
		self.canvas.bind('<B1-Motion>', self.paint)
		self.canvas.bind('<ButtonRelease-1>', self.reset)

	def choose_color(self):
		self.eraser_on = False
		self.color = askcolor(color=self.color)[1]

	def activate_button(self, some_button, eraser_mode=False):
		self.active_button = some_button
		self.active_button.config(relief=RAISED)
		some_button.config(relief=SUNKEN)
		self.eraser_on = eraser_mode

	def paint(self, event):
		self.line_width = self.line_width
		tag = "paint"+str(self.count)
		acts.append(tag)
		paint_color = 'white' if self.eraser_on else self.color
		if self.old_x and self.old_y:
			self.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width=self.line_width, fill=paint_color, capstyle=ROUND, smooth=TRUE, splinesteps=36, tags = tag)
		self.old_x = event.x
		self.old_y = event.y
		self.count += 1

	def reset(self, event):
		self.old_x, self.old_y = None, None

	def get_mouse_pos(self, event):
		global topy, topx
		topx, topy = event.x, event.y

	def update_selection(self, event):
		global shape_id
		global topy, topx, botx, boty
		botx, boty = event.x, event.y
		try:self.canvas.coords(shape_id, topx, topy, botx, boty)
		except:pass
		# self.count+=1

	def drawrect(self, color1, color2, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		# topx, topy, botx, boty = 0, 0, 0, 0
		tag = "rect" + str(self.count)
		acts.append(tag)
		try:
			self.canvas.bind('<Button-1>', self.get_mouse_pos)
			self.canvas.bind('<B1-Motion>', self.update_selection)
		except:pass
		shape_id = self.canvas.create_rectangle(topx, topy, topx, topy, width=linewidth, fill=color2, outline=color1, tags = tag)
		past.append(["rect", topx, topy, topx, topy, linewidth, color2, color1, tag])
		# self.canvas.create_rectangle(topx, topy, topx, topy, width=linewidth, fill=color2, outline=color1, tags = tag)
		self.count+=1
		
	def Draw_Image(self, iMg, window):
		global shape, topx, topy, botx, boty, shape_id, selectedindex
		window.config(cursor = 'crosshair')
		tag = 'img'+str(self.count)
		acts.append(tag)
		try:
			self.canvas.bind('<Button-1>', self.get_mouse_pos)
			self.canvas.bind('<B1-Motion>', self.update_selection)
		except:pass
		shape_id = self.canvas.create_image(topx, topy, anchor = 'nw', image = PIL.ImageTk.PhotoImage(Image.open(iMg)))#.resize((topx, topy), Image.ANTIALIAS))
		past.append(["img", topx, topy, botx, boty, iMg])

	def drawcircle(self, color1, color2, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		tag = "circle" + str(self.count)
		acts.append(tag)
		try:
			self.canvas.bind('<Button-1>', self.get_mouse_pos)
			self.canvas.bind('<B1-Motion>', self.update_selection)
		except:pass
		shape_id = self.canvas.create_oval(topx, topy, botx, boty, width=linewidth, fill=color2, outline=color1, tags=tag)
		# self.canvas.create_oval(topx, topy, botx, boty, width=linewidth, fill=color2, outline=color1, tags=tag)
		past.append(["circle", topx, topy, boty, boty, linewidth, color2, color1, tag])
		self.canvas.bind('<B1-Motion>', self.update_selection)
		self.count+=1

	def drawLine(self, color, linewidth, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		tag = "line" + str(self.count)
		acts.append(tag)
		self.canvas.bind('<Button-1>', self.get_mouse_pos)
		self.canvas.bind('<B1-Motion>', self.update_selection)
		shape_id = self.canvas.create_line(topx, topy, botx, boty, width=linewidth, fill=color, tags=tag)
		past.append(["line", topx, topy, botx, boty, linewidth, color, tag])
		self.count += 1
	
	def draw_text(self, color, window):
		global shape
		global topx, topy, botx, boty
		global shape_id
		global selectedindex
		selectedindex = 3
		tag = "text" + str(self.count)
		acts.append(tag)
		text = self._text_.get(0.0, END)
		font = self.font.get()
		size = self.fontsize.get()

		self.canvas.bind('<Button-1>', self.get_mouse_pos)
		shape_id = self.canvas.create_text(topx, topy, text = text, fill = color, font = (font, size))
		past.append(["text", topx, topy, text, color, font, size])
		window.destroy()
	
	def save(self):
		ps = self.canvas.postscript(colormode='color')
		img = Image.open(io.BytesIO(ps.encode('utf-8')))
		f = asksaveasfile(mode='w', defaultextension=".jpg", filetypes=[('JPG files', '*.jpg')])
		if f is None:
			return
		img.save(f, 'jpeg')
		showinfo("Successfull", "Image saved as " + str(f))

	def append_and_return(self, lst, item):
		lst.append(item)
		return item

	def _undo_(self):
		# print(self.count)
		# print(acts).,
		self.canvas.delete(self.append_and_return(past, acts.pop(self.count)))
		# self.canvas.delete(lambda lst, item:lst.append(item) or item)
		self.count -= 2

	def _redo_(self):
		redo = past.pop()
		if redo[0] == "rect":
			self.canvas.create_rectangle(redo[1], redo[2], redo[3], redo[4], redo[5], redo[6], redo[7], redo[8])
		elif redo[0] == "circle":
			self.canvas.create_oval(redo[1], redo[2], redo[3], redo[4], redo[5], redo[6], redo[7], redo[8])
		elif redo[0] == "line":
			self.canvas.create_line(redo[1], redo[2], redo[3], redo[4], redo[5], redo[6], redo[7])
		elif redo[0] == "text":
			self.canvas.create_text(redo[1], redo[2],text = redo[3],color =  redo[4], font = (redo[5], redo[6]))

	def Text_(self, color, window):
		# window.config(cursor = 'Hand')
		pop = Tk()
		pop.title('Create Text - Solemn2D')
		pop.geometry('250x150')
		pop.resizable(False, False)
		pop.wm_iconbitmap('imgs/logo.ico')
		fontLabel = ttk.LabelFrame(pop, text = "Font", width = 250, height= 50)
		fontLabel.place(x = 4, y = 3)
		self.font = StringVar()
		selectfont = ttk.Combobox(fontLabel, textvariable = self.font, width = 25)
		selectfont.place(x = 1, y =1)
		selectfont['values'] = [name for name in sorted(tkinter.font.families())]
		self.fontsize = IntVar()
		Fontspin = Spinbox(fontLabel, from_ = 1, to = 99999, width = 5, textvariable = self.fontsize)
		Fontspin.place(x = 187, y = 2)
		Tlabel = ttk.LabelFrame(pop, text = "Text")
		Tlabel.place(x = 8, y = 45)
		self._text_ = Text(Tlabel, width = 28, height = 3, foreground = color)
		self._text_.pack()
		okay = Button(pop, text = "Okay", width = 10, relief = GROOVE, command = lambda :[self.draw_text(color, pop)])
		okay.place(x = 40, y = 117)
		cancel = Button(pop, text = "Cancel", width = 10, relief = GROOVE, command = pop.destroy)
		cancel.place(x = 150, y = 117)
		pop.mainloop()

	def resize(self):
		pop = Tk()
		pop.title('resize canvas')
		pop.geometry('250x150')
		pop.resizable(False, False)
		pop.wm_iconbitmap('imgs/logo.ico')
		width_label = Label(pop, text = "width", width = 5, foreground = "white", bg = "black")
		width_label.grid(row = 2, column = 0)
		_width_ = IntVar()
		_width = Spinbox(pop, from_ = 1, to = 5000, textvariable = _width_)
		_width.grid(row = 2, column = 1)
		height_label = Label(pop, text = "height", width = 5, foreground = "white", bg = "black")
		height_label.grid(row = 4, column = 0)
		_height_ = IntVar()
		_height = Spinbox(pop, from_ = 1, to = 5000, textvariable = _height_)
		_height.grid(row = 4, column = 1)
		def _resize_():
			self.canvas.config(width = _width_.get(), height = _height_.get())
			pop.destroy()
		ok_btn = Button(pop, text = 'Ok', command = _resize_)
		ok_btn.grid(row = 3, column = 2)



	def Pass(self, event):pass 

