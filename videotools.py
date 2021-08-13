import cv2
from moviepy.video.tools.drawing import circle
# from moviepy.video.fx.all import blink, even_size, time_symmetrize
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.time_symmetrize import time_symmetrize

from tkinter import *
from tooltip import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import ttk
# from moviepy.editor import VideoFileClip, concatenate_videoclips
# from moviepy.video.io.VideoFileClip import VideoFileClip
# from moviepy.video.VideoClip import ImageClip
# from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
# from moviepy.video import fx

def merge_videos():
	def open_clip():
		clip = askopenfilename(title = "Open - Solemn2D 2.0")
		clip1_path.delete(0, END)
		clip1_path.insert(END, clip)
	def open_clip2():
		clip2 = askopenfilename(title = "Open - Solemn2D 2.0")
		clip2_path.delete(0, END)
		clip2_path.insert(END, clip2)
	pop = Tk()
	pop.title('Merge Videos')
	pop.geometry('230x145')
	pop.resizable(False, False)
	clip1_label = ttk.LabelFrame(pop, text = "First clip", width = 100,height = 25)
	clip1_label.place(x = 1, y = 2)
	clip1_path = Entry(clip1_label, width = 25)
	clip1_path.grid(row = 0, column = 0)
	clip1_btn = Button(clip1_label, text = 'browse', command= open_clip)
	clip1_btn.grid(row = 0, column = 1)
	clip2_label = ttk.LabelFrame(pop, text = "Second clip", width= 100, height = 25)
	clip2_label.place(x = 1, y = 50)
	clip2_path = Entry(clip2_label, width = 25)
	clip2_path.grid(row = 0, column = 0)
	clip2_btn = Button(clip2_label, text = "browse", command = open_clip2)
	clip2_btn.grid(row = 0, column = 1)
	progress_bar = ttk.Progressbar(pop, orient = HORIZONTAL, length = 80, mode = 'indeterminate')
	progress_bar.place(x = 10, y = 120)
	progress_bar['maximum']=100
	def _merge_():
		try:
			clip1 = VideoFileClip(clip1_path.get())
			clip2 = VideoFileClip(clip2_path.get())
			final_clip = concatenate_videoclips([clip1, clip2])
			final_clip.write_videofile("output.mp4")
		except Exception as e:
			showerror("Error", e) 
	Buttn = Button(pop, text = "Submit", command = _merge_)
	Buttn.place(x = 70, y = 117)

def cut_video(): 
	def open_():
		file = askopenfilename(title = "Open - Solemn2D 2.0")
		file_path.delete(0, END)
		file_path.insert(END, clip2)
	pop = Tk()
	pop.title('Merge Videos')
	pop.geometry('230x145')
	pop.resizable(False, False)
	file_label = ttk.LabelFrame(pop, text = "First clip", width = 100, height = 25)
	file_label.place(x = 1, y = 2)
	file_path = Entry(file_label, width = 25)
	file_path.grid(row = 0, column = 0)
	file_btn = Buttodn(file_label, text = 'browse', command= open_)
	file_btn.grid(row = 0, column = 1)
	cut_label = ttk.LabelFrame(pop, text = "Cut video", width= 100, height = 25)
	cut_label.place(x = 1, y = 50)
	startvar = IntVar()
	stopvar = IntVar()
	start = Spinbox(cut_label, from_ = 1, to = 20000, width = 5, textvariable = startvar)
	start.grid(row = 0, column = 0)
	stop = Spinbox(cut_label, from_ = 1, to = 20000,width = 5, textvariable = stopvar)
	stop.grid(row = 0, column = 1)
	create_Tip(start, 'Start cutting from here (seconds)')
	create_Tip(stop, 'Stop the cut here (seconds)')

	def _cut_():
		clip = VideoFileClip(file).subclip(start, stop)
		clip.write_videofile(asksaveasfilename(title = 'Save Cut - Solemn2D', initialfile = file+f'{start}-{stop}'))

	bttn = Button(pop, text = "Cut", command = _cut_)
	bttn.place(x = 65, y = 95)

def add_text():
	def text():
		vcodec = 'libx264'
		txt = Textclip(text, font = font, fontsize = size, color = Color, bg_color = Color_)
		txt = txt.set_position((location, num), relative = True)
		txt = txt.set_duration(n)
		txt = txt.set_crossfadein(fade)
		txt = txt.set_crossfadeout(fadeout)
		outclip = CompositeVideoClip(clip, txt)
		outclip.write_videofile(asksaveasfilename(title = 'Save - Solemn2D', threads = 4, codec = vcodec, preset = compression, ffmpeg_params = ["-crf", videoquality]))
		video.close()

def fade_in():
	def open_():
		file = askopenfilename(title = "Open - Solemn2D 2.0")
		file_path.delete(0, END)
		file_path.insert(END, file)
	pop = Tk()
	pop.title('Fade in Video')
	pop.geometry('230x145')
	pop.resizable(False, False)
	file_label = ttk.LabelFrame(pop, text = "Video clip", width = 100, height = 25)
	file_label.place(x = 1, y = 2)
	file_path = Entry(file_label, width = 25)
	file_path.grid(row = 0, column = 0)
	file_btn = Button(file_label, text = 'browse', command= open_)
	file_btn.grid(row = 0, column = 1)
	Rate = IntVar()
	rate_ = Spinbox(pop, from_ = 3, to = 5000, width = 15, textvariable = Rate)
	rate_.place(x = 3, y = 50)
	create_Tip(rate_, "Set the fade-in rate, 15 is good")
	def faden():
		clip = VideoFileClip(file_path.get())
		clipColorx = clip.fx(vfx.fadein, Rate.get())
		clipColorx.write_videofile(file)
	btn = Button(pop, text = "Okay", relief = GROOVE, command = faden)
	btn.place(x = 50, y = 80)
	pop.mainloop()

def fade_out():
	def open_():
		file = askopenfilename(title = "Open - Solemn2D 2.0")
		file_path.delete(0, END)
		file_path.insert(END, file)
	pop = Tk()
	pop.title('Fade out Video')
	pop.geometry('230x145')
	pop.resizable(False, False)
	file_label = ttk.LabelFrame(pop, text = "Video clip", width = 100, height = 25)
	file_label.place(x = 1, y = 2)
	file_path = Entry(file_label, width = 25)
	file_path.grid(row = 0, column = 0)
	file_btn = Button(file_label, text = 'browse', command = open_)
	file_btn.grid(row = 0, column = 1)
	Rate = IntVar()
	rate_ = Spinbox(pop, from_ = 3, to = 5000, width = 15, textvariable = Rate)
	rate_.place(x = 3, y = 50)
	create_Tip(rate_, "Set the fade-out rate, 15 is good")
	def fadet():
		clip = VideoFileClip(file_path.get()).fx(vfx.fadein, rate)
		clip.write_videofile(outfile)
	Btn = Button(pop, text = "Okay", relief = GROOVE, command = fadet)
	Btn.place(x = 50, y = 80)
	pop.mainloop()

def black_and_white():
	clip = cv2.VideoCapture(askopenfilename(title = "Open - Solemn 2D"))
	if askokcancel('Black and white', 'Are you sure you want to turn this clip into black\n and white? beware that this cannot be reversed.'):
		blackwhite(clip, RBG = None, preserve_luminoscity = True)
		showinfo('Success', 'Clip has been successfully converted to black and white')

def TheEndEffect():
	try:
		clip = VideoFileClip(askopenfilename(title = "Open - Solemn2D")).add_mask()
		w, h = clip.size
		clip.mask.get_frame = lambda t: circle(screensize = (clip.w, clip.h),
			center = (clip.w/2, clip.h/4),
			radius=max(0,int(800-200*t)),
			col1=1, col2=0, blur=4)
		the_end = Textclip("The End", font = "Amiri-bold", color = "white", fontsize = 70).set_duration(clip.duration)
		final = CompositeVideoClip([the_end.set_pos('center'),clip], size =clip.size)
		final.write_videofile('endeffected.avi')
	except Exception as e:
		showerror("Error", e)

def EditSpeed():
	try:
		pop = Tk()
		pop.title('Edit speed of Video')
		pop.geometry('230x145')
		pop.resizable(False, False)
		speed = IntVar()
		speedlabel = ttk.LabelFrame(pop, text = "Video Speed", width = 50, height = 20)
		speedlabel.place(x = 1, y = 2)
		speed_ = Spinbox(speedlabel, from_ = 1, to = 30, textvariable = speed, width = 7)
		speed_.place(x = 3, y = 2)
		clip = VideoFileClip(askopenfilename(title = "Open - Solemn2D"))
		final = clip.fx(vfx.speedx, speed)
		final.write_videofile('SpeedEdited.avi')
	except Exception as e:
		showerror("Error", e)

def video_drop(self):
    """Video silent"""
    if askokcancel("Are You sure", "Muting this video would replace this video with a silent\n one, if you don't want that, duplicate the video"):
    	try:
    		video = VideoFileClip(askopenfilename(title = "Open - Solemn2D"))
    		video = video.without_audio()
    		video.write_videofile('muted.avi')
    	except:
    		showerror("An error occured", "Make sure there isn't a file already muted\n if so, rename it")

def audio_concat_vedio(self):
    """Audio Video Synthesis"""
    if askokcancel('Warning', "This act cannot be reversed, you're advised to have backup"):
    	try:
    		video = VideoFileClip(askopenfilename(title = "Open the video - Solemn2D"))
    		audio = AudioFileClip(askopenfilename(title = "Open the Audio file - Solemn2D"))
    		video = video.set_audio(audio)
    		video.write_videofile(self.path2)
    	except Exception as e:
    		showerror("Error",e)

def _blink_(self):
	pop = Tk()
	pop.title('Edit speed of Video')
	pop.geometry('230x145')
	pop.resizable(False, False)
	start = IntVar()
	startlabel = ttk.LabelFrame(pop, text = "Start blink here (secs)", width = 50, height = 20)
	startlabel.place(x = 1, y = 2)
	start_ = Spinbox(startlabel, from_ = 1, textvariable = start, width = 7)
	start_.place(x = 3, y = 2)
	create_Tip(start_, "Start the blink from this point in the video, (in seconds)")
	stop = IntVar()
	stop_ = Spinbox(startlabel, from_ = 1, textvariable = stop, width = 7)
	stop_.place(x = 3, y = 10)
	create_Tip(stop_, "Where to stop the blinki in the video, (in seconds)s")
	clip = VideoFileClip(askopenfilename(title = "Open - Solemn2D"))
	blink(clip, start, stop)

def even_video_size(self):
	clip = VideoFileClip(askopenfilename(title = "Open - Solemn2D"))
	even_size(clip)

def time_symm(self):
	clip = VideoFileClip(askopenfilename(title = "Open - Solemn2D"))
	time_symmetrize(clip)

# fade_in()
# fade_out()
