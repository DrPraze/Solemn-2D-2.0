from tkinter import *
from TkinterDnD2 import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import ttk
from pydub import  AudioSegment
import PIL.Image, PIL.ImageTk, PIL.ImageOps, PIL.ImageDraw, PIL.ImageGrab
from scrollimage import ScrollableImage
import os, cv2, time, shutil, pygame, smtplib, ssl, subprocess, threading, io
import videotools
from tooltip import *
from tkinter.colorchooser import askcolor
from Sound import Sound
import sounddevice as sd 
from scipy.io.wavfile import write, read
import numpy as np
from samplerate_plot import Samplerate
# import soundfile as sf
from animator import anime
from glob import glob
from AudioLib import AudioEffect

class Main(TkinterDnD.Tk):
	images = ['imgs/skeleton.jpg']
	File = ''
	def __init__(self):
		super().__init__()
		self.menuBar = Menu(self)
		self.FileMenu = Menu(self.menuBar, tearoff = 0)
		self.ToolMenu = Menu(self.menuBar, tearoff = 0)
		self.HelpMenu = Menu(self.menuBar, tearoff = 0)
		self.title('Solemn 2D 2.0')
		self.geometry('900x650')
		self.config(bg = "white")
		try:self.wm_iconbitmap("imgs\\logo.ico")
		except:pass
		self.FileMenu.add_command(label = "Open", command = self.Open)
		self.FileMenu.add_command(label = "Import Sound", command = self.FetchSound)
		self.FileMenu.add_command(label = "New project     Ctrl+N", command = self.New)
		self.FileMenu.add_command(label = "Save Project     Ctrl+S", command = self.save)
		# self.FileMenu.add_command(label = "SaveAs", command = self.SaveAs)
		# self.FileMenu.add_command(label = "Export", command = self.export)
		self.FileMenu.add_command(label = "Exit                    Ctrl+Q", command = self._quit_)

		self.ToolMenu.add_command(label = "clear color 1   Ctrl+F", command = self.clear_color1)
		self.ToolMenu.add_command(label = "clear color 2   Ctrl+G", command = self.clear_color2)

		self.HelpMenu.add_command(label = "About ", command = self.About)
		self.HelpMenu.add_command(label = "How to use  F1", command = self.Use)
		self.HelpMenu.add_command(label = "Version ", command = self.version)
		self.HelpMenu.add_command(label = "Send Feedback", command = self.feedback)

		self.menuBar.add_cascade(label = "File", menu = self.FileMenu)
		self.menuBar.add_cascade(label = "Tools", menu = self.ToolMenu)
		self.menuBar.add_cascade(label = "Help", menu = self.HelpMenu)
		self.config(menu = self.menuBar)

		self.n = 0
		self.SoundTrack = None
		self.widgets()

		self.protocol('WM_DELETE_WINDOW', self._quit_)
		self.bind('<F1>', lambda x:[self.Use()])

		self.bind('<Control-q>', lambda x:[self._quit_()])
		self.bind('<Control-n>', lambda x:[self.New()])
		self.bind('<Control-s>', lambda x:[self.save()])
		self.bind('<Control-o>', lambda x:[self.Open()])
		self.bind('<Control-f>', lambda x:[self.clear_color1()])
		self.bind('<Control-g>', lambda x:[self.clear_color2()])

	def widgets(self):
		global _img, play_img, pause_img, stop_img

		self.TabControl = ttk.Notebook(self)
		self.tab1 = ttk.Frame(self.TabControl)
		self.tab2 = ttk.Frame(self.TabControl)
		self.tab3 = ttk.Frame(self.TabControl)
		self.TabControl.add(self.tab1, text = "Draw")
		self.TabControl.add(self.tab2, text = "Sound")
		self.TabControl.add(self.tab3, text = "Animation")
		self.TabControl.pack(fill = "both", expand = 1)

		#=================Tab1 region===================
		toolbar = Canvas(self.tab1, width = 400000, height = 80).pack()

		self.Brush = Button(self.tab1, text = "Brush", width = 5, command = self.brush)
		self.Brush.place(x =12, y = 2)
		self.Eraser = Button(self.tab1, text = "Erase", width = 5, command = self.erase)
		self.Eraser.place(x = 12, y = 30)
		self.shape = StringVar()
		self.shapes = ttk.Combobox(self.tab1, textvariable = self.shape, width = 12, state = 'readonly')
		self.shapes['values'] = ['Circle', 'Rect', 'Line']
		self.shapes.set('shape')
		self.shapes.place(x = 60, y = 5)
		create_Tip(self.shapes, "Select object")
		self.Object = Button(self.tab1, text = "Object", command = self.draw_shape)
		self.Object.place(x = 163, y = 5)
		create_Tip(self.Object, 'Draw selected object')

		self.color = "Black"
		self.color2 = "White"
		self.color_button = Button(self.tab1, text = "color", width = 12, relief = GROOVE, command = self.Color)
		self.color_button.place(x = 330, y = 2)
		self.color_btn2 = Button(self.tab1, text = "Color2", width = 12, relief = GROOVE, command = self.Color2)
		self.color_btn2.place(x = 330, y = 30)

		try:
			img = PIL.Image.open('imgs/skeleton.jpg')
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab1, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
		except ImportError:
			showerror('An Error occured', e)
		
		self.new_blank = Button(self.tab1, width = 14, text = "New blank frame", relief = GROOVE, command = self.NewBlankFrame)
		self.new_blank.place(x = 213, y = 5)
		create_Tip(self.new_blank, "Create a new blank frame")
		# self.clear_btn = Button(self.tab1, width = 14, text = "clear frame", relief = GROOVE, command = self.img_win.clear)
		# self.clear_btn.place(x = 155, y = 5)
		# create_Tip(self.clear_btn, "Clear the current frame to blank white")

		effects = ttk.LabelFrame(self.tab1, text = "Effects", width = 320, height = 60)
		effects.place(x = 430, y = 2)
		Sketch = Button(effects, text = "Sketch", width = 9, relief = GROOVE, command = self.drawimage)
		Sketch.place(x = 2)
		create_Tip(Sketch, "Turn current frame image into sketch")
		Blur = Button(effects, text = "Blur", width = 9, relief = GROOVE, command = self.blurimage)
		Blur.place(x = 82)
		create_Tip(Blur, "Blur the current image")
		Invert = Button(effects, text = "Invert", width = 9, relief = GROOVE, command = self.invert)
		Invert.place(x = 162)
		create_Tip(Invert, "Invert the colors of the current image")
		Mirror = Button(effects, text = "Mirror", width = 9, relief = GROOVE, command = self.mirror)
		Mirror.place(x = 242)
		create_Tip(Mirror, "Mirror the current frame")

		undo_btn = Button(self.tab1, text = "undo", relief = GROOVE, command = self.img_win._undo_)
		undo_btn.place(x = 67, y = 30)
		redo_btn = Button(self.tab1, text = "redo", relief = GROOVE, command = self.img_win._redo_)
		redo_btn.place(x = 115, y = 30)
		self.choose_size_button = Scale(self.tab1, from_=0, to=10, orient=HORIZONTAL)
		self.choose_size_button.place(x = 760, y = 10)
		self.line_width = self.choose_size_button.get()

		Nav_frame = ttk.LabelFrame(self.tab1, text = "Navigate", width = 120, height = 100)
		Nav_frame.place(x = 5, y = 100)
		prev = Button(Nav_frame, text = "Prev", width = 5, font = ('Calibri', 12), bg = '#000', foreground = '#FFF', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.prev_frame)
		prev.place(x = 4, y = 1)
		Next = Button(Nav_frame, text = "Next", width = 5, font = ('Calibri', 12), bg = "black", foreground = "white", activebackground = 'grey', highlightbackground = '#bce8f1', highlightthickness = 0.5, borderwidth = "2", command = self.next_frame)
		Next.place(x = 60, y = 1)
		del_frame = Button(Nav_frame, text = "Delete Frame", width = 10, font = ('Calibri', 12), bg = "black", foreground = "white", activebackground = "grey", highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.Del_frame)
		del_frame.place(x = 12, y = 40)
		create_Tip(prev, "Go back to the previous frame")
		create_Tip(Next, "Go to the next frame")
		create_Tip(del_frame, "Delete the current frame")

		ComicFrame = ttk.LabelFrame(self.tab1, text = "Comic", width = 120, height = 300)
		ComicFrame.place(x = 5, y = 200)
		self.act = StringVar()
		self.acts = ttk.Combobox(ComicFrame, textvariable = self.act, width = 12, state = 'readonly')
		self.acts['values'] = ['aargh', 'bang', 'boom', 'kapow', 'poof', 'pow', 'whoosh']
		self.acts.set('Acts Banner')
		self.acts.place(x = 10, y = 3)
		create_Tip(self.acts, "Select acts banner")
		try:
			# self.draw_act = Button(ComicFrame, text = "Draw act", width= 13, relief = GROOVE, command = lambda :[self.img_win.Draw_Image(str(r'imgs/'+self.acts.get()+'.png'), self)])
			self.draw_act = Button(ComicFrame, text = "Draw act", width= 13, relief = GROOVE, command = self.comingsoon)
			self.draw_act.place(x = 8, y = 44)
		except:pass

		self.text = Button(ComicFrame, text = "Text", width = 13, relief = GROOVE, command = lambda:[self.img_win.Text_(self.color, self)])
		self.text.place(x = 8, y = 67)
		create_Tip(self.text, 'Create text')
		resize = Button(ComicFrame, text = "Resize", width = 13, relief = GROOVE, command = self.img_win.resize)
		resize.place(x = 8, y = 90)
		create_Tip(resize, 'Resize the canvas')
		paint = Button(ComicFrame, text = "Paint", width = 13, relief = GROOVE, command = self.Paint)
		paint.place(x = 8, y = 113)
		create_Tip(paint, "Open mspaint if you're running on windows")
		save = Button(ComicFrame, text = "Save", width = 13, relief = GROOVE, command = self.img_win.save)
		save.place(x = 8, y = 136)
		export_ = Button(ComicFrame, text = 'export', width = 13, relief = GROOVE, command = self.export2comic)
		export_.place(x = 8, y = 182)
		create_Tip(save, "Save image in drawing canvas")
		create_Tip(export_, "Export comic to PDF")
		# select_ = Button(ComicFrame, text = "Select", width = 13, relief = GROOVE, command = self.select_area)
		# select_.place(x = 8, y = 136)
		self.progress_bar_ = ttk.Progressbar(self.tab3, orient = HORIZONTAL, length = 800, mode = 'determinate')
		self.progress_bar_.place(x = 100, y = 640)

		_explore = ttk.LabelFrame(self.tab1, text = "Image files", width = 30, height = 540)
		_explore.place(x = 860, y = 100)
		self.img_list = Listbox(_explore, bg = 'black', foreground = 'white', width = 25, height = 30)
		self.img_list.pack(fill = Y, expand = 1)
		self.find_pics()

		self.tab1.drop_target_register(DND_FILES)
		self.tab1.dnd_bind('<<Drop>>', self.pic_in)
		#============END OF REGION================
		
		#=================Tab2 region==================
		Sound.initiate
		self.sound_frame = ttk.LabelFrame(self.tab2, text = "Sound", width = 180, height = 500)
		self.sound_frame.place(x = 18, y = 10)

		self.reverse = Button(self.sound_frame, text="Reverse Track", width = 16, command = lambda: Sound.reverse(self.SoundTrack), relief = GROOVE)
		self.reverse.place(x=2,y=2)
		create_Tip(self.reverse, "Reverse the track(rewrite the\ntrack backwards)")
		self.merge = Button(self.sound_frame, text="Gapless Merge", width = 16, command = Sound.mergeTracks, relief = GROOVE)
		self.merge.place(x = 2, y=32)
		create_Tip(self.merge, "Merge two audio files with a gap")
		self.gapMerge = Button(self.sound_frame, text = "Merge with Gap", width = 16, command = Sound.gapMerge, relief = GROOVE)
		self.gapMerge.place(x=2,y=62)
		create_Tip(self.gapMerge, "Merge two audio files together with a gap between them")
		self.repeat = Button(self.sound_frame, text = "Repeat", width = 16, command = Sound.repeat)
		self.repeat.place(x=2,y=92)
		create_Tip(self.repeat, "Repeat track once again")

		self.overlay = Button(self.sound_frame, text = "Overlay", width = 16, command = lambda: self.overlayTrack())
		self.overlay.place(x=2,y=122)
		create_Tip(self.overlay, "Overlay two tracks together")

		self.savesound = Button(self.sound_frame, text="Save changes", width = 16, command = lambda: Sound.save(self.SoundTrack), relief = GROOVE) 
		self.savesound.place(x=2,y=152)
		create_Tip(self.savesound, "Save current changes\n made on sound")

		self.undo = Button(self.sound_frame, text = "Undo", command = lambda: Sound.undo(self.SoundTrack), relief = GROOVE)
		self.undo.place(x=22, y=182)
		create_Tip(self.undo, "Undo changes made on sound")
		self.redo = Button(self.sound_frame, text = "Redo", command = lambda: Sound.redo(self.SoundTrack), relief = GROOVE)
		self.redo.place(x=65, y=182)
		create_Tip(self.redo, "Redo changes made on sound")
		self.maxtempo = Button(self.sound_frame, text = "Max tempo", width = 16, command = self.Max_tempo, relief = GROOVE)
		self.maxtempo.place(x=2, y=242)
		# self.play = Button(self.sound_frame, text = "Play", command = self.play, relief=GROOVE)
		# self.play.place(x=22, y=212)
		# self.stop = Button(self.sound_frame, text = "Stop", command = self.stop, relief = GROOVE)
		# self.stop.place(x =65, y=212)

		# self.change_voice_label = ttk.LabelFrame(self.sound_frame, text = "Change voice", width = 140, height = 55)
		# self.change_voice_label.place(x = 2, y = 272)
		# self.shift = IntVar()
		# self.change = Spinbox(self.change_voice_label, from_ = -150, to = 150, width  = 5, bd= 2, textvariable = self.shift)
		# self.change.place(x = 2, y = 2)
		# create_Tip(self.change, "Set the change rate of the voice")
		# self.Change_voice = Button(self.change_voice_label, text = "Change", command = lambda :self.change_voice(self.shift))
		# self.Change_voice.place(x = 70, y =2)

		self.reduce_noise = Button(self.sound_frame, text = "Reduce noise", width = 16, command = self.ReduceNoise)
		self.reduce_noise.place(x = 2, y = 272)
		self.min_tempo = Button(self.sound_frame, text = "Min tempo", width = 16, command = self.Min_tempo)
		self.min_tempo.place(x = 2, y = 302)
		self.durLabel = Label(self.sound_frame, text = "Track duration: 0")

		self.record_frame = ttk.LabelFrame(self.sound_frame, text = "Record", width = 140, height = 100)
		self.record_frame.place(x=2, y = 330)
		self.frequency = IntVar()
		self.freq = Spinbox(self.record_frame, width = 5, from_ = 0, to = 99000, textvariable = self.frequency)
		self.freq.place(x = 1, y = 2)
		self.frequency.set("44100")
		create_Tip(self.freq, "Enter the frequency, don't\n change if you don't understand")
		self.duration = IntVar()
		self.dur = Spinbox(self.record_frame, width = 5, from_ = 0, to = 90000, textvariable = self.duration)
		self.dur.place(x = 61, y = 2)
		self.duration.set('50')
		create_Tip(self.dur, "Set the duration\n of record, IN SECONDS")
		self.saveaudio = Entry(self.record_frame, width = 18)
		self.saveaudio.place(x =3, y = 30)
		create_Tip(self.saveaudio, "Write the name of the\n file for saving here")
		self.record = Button(self.record_frame, text = "record", width = 15, command = self.rec_sound)
		self.record.place(x = 2, y = 55)
		self.del_sound = Button(self.sound_frame, text = "Delete Sound", width = 16, command = self.delete_sound)
		self.del_sound.place(x = 2, y = 435)

		self.effect_frame = ttk.LabelFrame(self.tab2, text = "Audio effects", width = 230, height = 130)
		self.effect_frame.place(x = 200, y = 10)
		i = 0
		def inc_i():i+=1
		self.echo_btn = Button(self.effect_frame, text = 'Echo', relief = GROOVE, command = lambda :[AudioEffect.echo(AudioSegment.from_mp3(self.SoundTrack), 'output'+str(i)), inc_i()])
		self.echo_btn.place(x = 2, y = 2)
		self.radio_btn = Button(self.effect_frame, text = 'Radio', relief = GROOVE, command = lambda :[AudioEffect.radio(AudioSegment.from_mp3(self.SoundTrack), 'output'+str(i)), inc_i()])
		self.radio_btn.place(x = 44, y = 2)
		self.robot_btn = Button(self.effect_frame, text = 'Robot', relief = GROOVE, command = lambda :[AudioEffect.robotic(AudioSegment.from_mp3(self.SoundTrack), 'output'+str(i)), inc_i()])
		self.robot_btn.place(x = 90, y = 2)
		self.ghost_btn = Button(self.effect_frame, text = "Ghost", relief = GROOVE, command = lambda :[AudioEffect.ghost(AudioSegment.from_mp3(self.SoundTrack), 'output'+str(i)), inc_i()])
		self.ghost_btn.place(x = 138, y = 2)
		self.darth_btn = Button(self.effect_frame, text = "Darth", relief = GROOVE, command = lambda :[AudioEffect.darth_vader(AudioSegment.from_mp3(self.SoundTrack), 'output'+str(i)), inc_i()])
		self.darth_btn.place(x = 186, y = 2)
		create_Tip(self.echo_btn, "Add echo effect to imported sound")
		create_Tip(self.radio_btn, "Add radio effect to imported sound")
		create_Tip(self.robot_btn, "Add robotic effect to imported sound")
		create_Tip(self.ghost_btn, "Add ghost effect to imported sound")
		create_Tip(self.darth_btn, "Add darth vader's (from star wars) voice effect to imported sound")

		_img = PIL.Image.open('imgs/disk.png')
		# _img = _img.convert('RGB')
		_img = PIL.ImageTk.PhotoImage(_img)
		label = Label(self.tab2, image = _img)
		label.place(x = 208, y = 65)

		play_img = PIL.ImageTk.PhotoImage(PIL.Image.open('imgs/play.png'))
		pause_img = PIL.ImageTk.PhotoImage(PIL.Image.open('imgs/pause.png'))
		stop_img = PIL.ImageTk.PhotoImage(PIL.Image.open('imgs/stop.png'))

		self.play_btn = Button(self.tab2, text = "Play", image = play_img, command = self.play)
		self.play_btn.place(x = 400, y = 500)
		self.stop_btn = Button(self.tab2, text = "Stop", image = stop_img, command = self.stop)
		self.stop_btn.place(x = 460, y = 500)

		explore = ttk.LabelFrame(self.tab2, text = "Audio files", width = 150, height = 540)
		explore.place(x = 680, y = 20)
		self.audio_list = Listbox(explore, bg = 'black', foreground = 'white', width = 40, height = 30)
		self.audio_list.pack(fill = Y, expand = 1)
		# subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
		self.find_audio()

		self.tab2.drop_target_register(DND_FILES)
		self.tab2.dnd_bind('<<Drop>>', self.sound_in)
		self.audio_list.bind('<Double-Button>', lambda x:[self.SoundFromList(self.audio_list)])
		# self.update_sound_editing_tools()
		#===============END OF REGION============
		#============Tab3 region===========
		navframe = ttk.LabelFrame(self.tab3, text = "Navigate", width = 310, height = 53)
		navframe.place(x = 50, y = 7)
		prev_ = Button(navframe, text = "Prev", width = 5, font = ('Calibri', 12), bg = '#000', foreground = '#FFF', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.prev_frame_anime)
		prev_.place(x = 4, y = 1)
		Next_ = Button(navframe, text = "Next", width = 5, font = ('Calibri', 12), bg = "black", foreground = "white", activebackground = 'grey', highlightbackground = '#bce8f1', highlightthickness = 0.5, borderwidth = "2", command = self.next_frame_anime)
		Next_.place(x = 60, y = 1)
		del_frame_ = Button(navframe, text = "Delete Frame", width = 10, font = ('Calibri', 12), bg = "black", foreground = "white", activebackground = "grey", highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = "2", command = self.Del_frame)
		del_frame_.place(x = 116, y = 1)
		dup_frame = Button(navframe, text = "Dup Frame", width = 10, font = ('Calibri', 12), bg = 'black', foreground = 'white', activebackground = 'grey', highlightbackground = "#bce8f1", highlightthickness = 0.5, borderwidth = '2', command = self.duplicate)
		dup_frame.place(x = 212, y = 1)
		create_Tip(prev_, "Go back to the previous frame")
		create_Tip(Next_, "Go to the next frame")
		create_Tip(del_frame_, "Delete the current frame")
		create_Tip(dup_frame, "Duplicate the current frame")
		self.FPS = IntVar()
		fps_label = ttk.LabelFrame(self.tab3, text = "fps", width = 100, height = 53)
		fps_label.place(x = 375, y = 7)
		self.fps = Spinbox(fps_label, from_ = 1, to = 150, width  = 10, bd= 2, textvariable = self.FPS)
		self.fps.place(x = 10, y = 2)
		anim_label = ttk.LabelFrame(self.tab3, text = "Animate", width = 300, height = 53)
		anim_label.place(x = 490, y = 7)
		preview = Button(anim_label, text = "preview", relief = GROOVE, command = self.Animate)
		preview.place(x = 10, y = 2)
		export = Button(anim_label, text = "export", relief = GROOVE, command = self.export)
		export.place(x = 70, y = 2)
		vid_label = ttk.LabelFrame(self.tab3, text = "Edit Video", width = 100, height = 400)
		vid_label.place(x = 10, y = 70)
		Merge_Vid = Button(vid_label, text = "Merge Videos", relief = GROOVE, width = 10, command = videotools.merge_videos)
		Merge_Vid.place(x = 6, y = 2)
		cut_vid = Button(vid_label, text = "Cut Video", relief = GROOVE, width = 10, command = videotools.cut_video)
		cut_vid.place(x = 6, y = 30)
		fadeIn = Button(vid_label, text = "Fade In", relief = GROOVE, width = 10, command = videotools.fade_in)
		fadeIn.place(x = 6,y = 58)
		fadeOut = Button(vid_label, text = "Fade Out", relief =GROOVE, width = 10, command= videotools.fade_out)
		fadeOut.place(x = 6, y = 86)
		BnW = Button(vid_label, text = "BnW", relief = GROOVE, width = 10, command = videotools.black_and_white)
		BnW.place(x = 6, y = 112)
		EndEffect = Button(vid_label, text = "The End", relief = GROOVE, width = 10, command = videotools.TheEndEffect)
		EndEffect.place(x = 6, y = 138)
		Editspeed = Button(vid_label, text = "Edit Speed", relief = GROOVE, width = 10, command = videotools.EditSpeed)
		Editspeed.place(x = 6, y = 164)
		Mute = Button(vid_label, text = "Mute Video", relief = GROOVE, width = 10, command = videotools.video_drop)
		Mute.place(x = 6, y = 216)
		Concat = Button(vid_label, text = "Audio+video", relief = GROOVE, width = 10, command=videotools.audio_concat_vedio)
		Concat.place(x = 6, y = 242)
		blink_ = Button(vid_label, text = "Blink", relief = GROOVE, width = 10, command = videotools._blink_)
		blink_.place(x = 6, y = 268)
		even = Button(vid_label, text = "Even size", relief = GROOVE, width = 10, command = videotools.even_video_size)
		even.place(x = 6, y = 294)
		time_s = Button(vid_label, text = "time symm", relief = GROOVE, width = 10, command = videotools.time_symm)
		time_s.place(x = 6, y = 320)

		create_Tip(Merge_Vid, 'Merge/concatenate 2 videos together')
		create_Tip(preview, 'Preview the animation   F5')
		create_Tip(export, 'Export the animation to a video')
		create_Tip(cut_vid, 'Cut out segments from a video')
		create_Tip(self.fps, "Set the frames per second")
		create_Tip(fadeIn, "add fade-in effect to a video")
		create_Tip(fadeOut, "add fade-out effect to a video")
		create_Tip(BnW, "Black and White (turn video into black and white)")
		create_Tip(EndEffect, "Apply 'The End' effect at the ending of a video")
		create_Tip(Mute, "Remove sound from video into oblivion")
		create_Tip(Concat, "Apply a sound to a video")
		create_Tip(blink_, "apply blink to video clip")
		create_Tip(even, "Crop video clip to make dimensions even")
		create_Tip(time_s, "Time symmetrize video, play a video once forward and once backwards")
		try:
			img = PIL.Image.open('imgs/skeleton.jpg')
			img = PIL.ImageTk.PhotoImage(img)
			self.anim_win = ScrollableImage(self.tab3, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.anim_win.place(x = 130, y = 100)
		except Exception as e:
			showerror('An Error occured', e)

		self.progress_bar = ttk.Progressbar(self.tab3, orient = HORIZONTAL, length = 800, mode = 'determinate')
		self.progress_bar.place(x = 100, y = 640)
		explore_ = ttk.LabelFrame(self.tab3, text = "Solemn files", width = 30, height = 540)
		explore_.place(x = 860, y = 100)
		self.anime_list = Listbox(explore_, bg = 'black', foreground = 'white', width = 25, height = 30)
		self.anime_list.pack(fill = Y, expand = 1)
		self.find_animes()

		self.tab3.bind('<F5>', lambda x:[self.Animate()])
		#===========END OF REGION==========
		self.tab3.drop_target_register(DND_FILES)
		self.tab3.dnd_bind('<<Drop>>', self.file_in)

	def export2comic(self):
		from fpdf import FPDF
		pdf = FPDF()
		for image in self.images:
			pdf.add_page()
			pdf.image(image, 5,5,100,150)
		pdf.output('comic' + '.pdf', "F")

		
	def find_audio(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.mp3') or file.endswith('.wav'):
					self.audio_list.insert(END, file)

	def find_pics(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.bmp') or file.endswith('.gif'):
					self.img_list.insert(END, file)

	def find_animes(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				if file.endswith('.solemn'):
					self.anime_list.append(END, file)

	def stop(self):
		pygame.mixer.music.stop()
		self.play_btn.config(image = play_img, command = self.play)
	def resume(self):
		pygame.mixer.music.unpause()
		self.play_btn.config(image = pause_img, command = self.pause)
	def pause(self):
		pygame.mixer.music.pause()
		self.play_btn.config(image = play_img, command = self.resume)
	def play(self):
		try:
			pygame.mixer.music.load(self.SoundTrack)
			pygame.mixer.music.play(-1)
			self.play_btn.config(text = "Pause", command = self.pause)
		except Exception as e:
			showerror("An error occured", e)

	def Paint(self):
		try:subprocess.Popen('CMD /K mspaint')
		except:showerror('An error occured', 'This feature is only available for windows operating\n system, it seems your PC is otherwise')

	def clear_color1(self):
		self.color = None
		self.color_button.config(bg = None)
	def clear_color2(self):
		self.color2 = None
		self.color_btn2.config(bg = None)

	def update_sound_editing_tools(self):
		if self.SoundTrack==None:
			self.reverse.config(state=DISABLED)
			self.savesound.config(state = DISABLED)
			self.undo.config(state=DISABLED)
			self.redo.config(state = DISABLED)
			self.repeat.config(state = DISABLED)
			self.overlay.config(state = DISABLED)
			self.gapMerge.config(state = DISABLED)
			self.merge.config(state = DISABLED)
			self.play_btn.config(state = DISABLED)
			self.stop_btn.config(state = DISABLED)
			self.maxtempo.config(state = DISABLED)
			self.del_sound.config(state = DISABLED)
			self.reduce_noise.config(state = DISABLED)
			self.min_tempo.config(state = DISABLED)
		else:
			self.reverse.config(state=NORMAL)
			self.savesound.config(state = NORMAL)
			self.undo.config(state=NORMAL)
			self.redo.config(state = NORMAL)
			self.repeat.config(state = NORMAL)
			self.overlay.config(state = NORMAL)
			self.gapMerge.config(state = NORMAL)
			self.merge.config(state = NORMAL)
			self.play_btn.config(state = NORMAL)
			self.stop.config(state = NORMAL)
			self.maxtempo.config(state = NORMAL)
			self.del_sound.config(state = NORMAL)
			self.reduce_noise.config(state = NORMAL)
			self.min_tempo.config(state = NORMAL)

	def SoundFromList(self, box):self.SoundTrack = box.get('active')

	def Max_tempo(self):
		dst = 'out.wav'
		sound = self.SoundTrack
		sound.export(dst, format = 'mp3')
		data, samplerate = sf.read(self.SoundTrack)
		# print(data.shape)
		# print(samplerate)
		# plt.plot(data)
		# plt.show()
		samplerate = int(samplerate*1.5)
		self.progressing()

		sf.write("output.wav", data, samplerate)
		os.system("output.wav")

	def Min_tempo(self):
		dst = 'out.wav'
		sound = self.SoundTrack
		sound.export(dst, format = 'mp3')
		data, samplerate = sf.read(self.SoundTrack)
		# print(data.shape)
		# print(samplerate)
		# plt.plot(data)
		# plt.show()
		samplerate = int(samplerate/1.5)
		# self.progressing()
		sf.write("output.wav", data, samplerate)
		os.system("output.wav")

	def ReduceNoise(self):
		import noisereduce as nr
		import wavfile
		rate, data = wavfile.read(self.SoundTrack)
		noisy_part = data[10000:15000]
		reduced_noise = nr.reduce_noise(audio_clip=data, noise_clip=noisy_part, verbose=True)
		self.SoundTrack = reduced_noise

	def rec_sound(self):
		record_thread = threading.Thread(target= self.record_sound, daemon = True)
		record_thread.start()
	
	def record_sound(self):
		try:
			self.status_bar = Canvas(self.tab2, width= 4000, height = 50)
			self.status_bar.pack(side="bottom", fill="both", expand=False)
			frequency = self.frequency.get()
			duration = self.duration.get()
			file = self.saveaudio.get()
			self.record.config(text = 'recording')
			self.status_bar.create_text(350, 10, fill = "black", font = "Times 15 italic bold", text = "recording... Note that a record can't be terminated")
			self.status_bar.update()
			recording =sd.rec(int(duration * frequency), samplerate = frequency, channels = 2)
			sd.wait()
			write(file +'.mp3', frequency, recording)
			self.status_bar.create_rectangle(0, 0, 600, 120, fill = self.status_bar.cget('background'), outline = "")
			self.record.config(text = "record")
			showinfo('Record was succesfull', "record exported at "+file+'.mp3')
		except Exception as e:
			showerror("An error occured", "the file field is meant to be filled"+str(e))

	def delete_sound(self):self.SoundTrack=None
	
	def pic_in(self, e):
		try:
			e = self.tk.splitlist(e.data)[0]
			self.images.append(e)
			self.n = self.images.index(e)
			self.img_win.del_canvas()
			img = PIL.Image.open(e)
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab1, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
			# self.update_nav()
		except Exception as E:
			showerror("An Error Occured", E)

	def sound_in(self, e):
		try:
			e = self.tk.splitlist(e.data)[0]
			self.SoundTrack = e
		except Exception as Err:
			showerror("An error occured", Err) 

	def file_in(self, e):
		# try:
		e = self.tk.splitlist(e.data)[0]
		with open(e, 'r') as f:
			data = eval(f.read())
			self.images = data['Images']
			self.SoundTrack = data['Sound']
			f.close()
		# except Exception as Err:
			# showerror("Error", Err)

	def Del_frame(self):
		if askokcancel('Delete', 'Are you sure you want to delete the current frame?'):
			try:
				self.images.pop(self.n)
			except IndexError:pass
			self.prev_frame()
	
	def invert(self):
		try:
			img = PIL.Image.open(self.images[self.n])
			image = PIL.ImageOps.invert(img)
			im = self.images[self.n].replace('.png', '').replace('.jpg', '').replace('.bmp', '') + '.jpg'  
			image = image.save(im)
			self.images.append(im)
		except Exception as e:
			showerror('Error', e)

	def blurimage(self):
		img = self.images[self.n]
		if askyesno("Warning", "Are you sure about this? \nThis would replace the image with the blurred\n one, if you want to keep it, you have to duplicate\n it, click prev and next to refresh and see the image", icon = 'warning'):
			blur = cv2.blur(cv2.imread(img), (10, 10))
			os.remove(img)
			cv2.imwrite(img, blur)
			self.images[self.n] = img

	def duplicate(self):
		try:
			src = self.images[self.n]
			new = src[:4] + '(copy)' + '.jpg'
			try:
				shutil.copy(src, new)
			except PermissionError:
				showerror("An error occured", "access is denied, try running Solemn 2D\n as administrator, your pc is restricting the access\n if this doesn't work, try changing the path of your image to somewhere\n that doesn't require admin privileges")
			self.images.append(new)
			self.n = self.images.index(new)
			self.img_win.del_canvas()
			img = Image.open(new)
			img = ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(root, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
		except IndexError:
			pass
	
	def drawimage(self):
		img = self.images[self.n]
		if askyesno("Warning", "Are you sure about this? \nThis would replace the image with the sketched\n one, if you want to keep it, you have to duplicate\n it, click prev and next to refresh and see the image", icon = 'warning'):
			gray = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
			smoothing = cv2.GaussianBlur(cv2.bitwise_not(gray), (21, 21), sigmaX = 0, sigmaY = 0)
			image = cv2.divide(gray, 255 - smoothing, scale = 256)
			os.remove(img)
			cv2.imwrite(img, image)
			self.images[self.n] = img

	def mirror(self):
		try:
			img = Image.open(self.images[self.n])
		except:pass
		image = ImageOps.mirror(img)
		im = self.images[self.n].replace('.png', '').replace('.jpg', '').replace('.bmp', '') + '.jpg'  
		image = image.save(im)
		self.images.append(im)
 
	def Color(self):
		self.color = askcolor(title = "select a color")[1]
		self.eraser_on = False
		self.color_button.config(bg = self.color)

	def Color2(self):
		self.color2 = askcolor(title = "Select another color")[1]
		self.eraser_on = False
		self.color_btn2.config(bg = self.color2)
	
	def draw_shape(self):
		self.Object.config(relief = SUNKEN)
		self.Brush.config(relief = RAISED)
		self.Eraser.config(relief = RAISED)
		self.line_width = self.choose_size_button.get()
		self.img_win.activate_button(self.Object, eraser_mode = False)
		self.tab1.config(cursor = "crosshair")
		if self.shape.get() == 'Circle':
			self.bind('<Button-1>', lambda x:[self.set4shape, self.img_win.drawcircle(self.color, self.color2, self.line_width, self)])
		elif self.shape.get() == 'Rect':
			self.bind('<Button-1>', lambda x:[self.set4shape, self.img_win.drawrect(self.color, self.color2, self.line_width, self)])
		elif self.shape.get() == 'Line':
			self.bind('<Button-1>', lambda x:[self.set4shape, self.img_win.drawLine(self.color, self.line_width, self)])
		else:	
			print(self.shape)

	def set4shape(self):
		self.line_width = self.choose_size_button.get()
		color = self.color

	def set(self):
		try:
			self.line_width = self.choose_size_button.get()
			self.img_win.setup(self.line_width, self.Brush, color=self.color)
		except Exception as e:
			showerror("Error", e)

	def brush(self):
		self.tab1.config(cursor="dot")
		self.line_width = self.choose_size_button.get()
		self.Brush.config(relief = SUNKEN)
		self.img_win.activate_button(self.Brush, eraser_mode = False)
		self.bind('<Button-1>', lambda x:[self.set()])
		self.Eraser.config(relief = RAISED)
		self.Object.config(relief = RAISED)
	
	def erase(self):
		self.tab1.config(cursor="circle")
		self.line_width = self.choose_size_button.get()
		self.color = 'white'
		self.img_win.activate_button(self.Eraser, eraser_mode = True)
		self.Brush.config(relief = RAISED)
		self.Object.config(relief = RAISED)
		self.bind('<Button-1>', lambda x:[self.set()])
	
	def create_rect(self):
		self.tab1.bind('<Button-1>', lambda x:[self.img_win.drawrect(self.color, self.color2, self.line_width, self)])
	def create_circle(self):
		self.tab1.bind('<Button-1>', lambda x:[self.img_win.drawcircle(self.color, self.color2, self.line_width, self)])
	def create_line(self):
		self.tab1.bind('<Button-1>', lambda x:[self.img_win.drawLine(self.color, self.line_width, self)])

	def NewBlankFrame(self):self.img_win.clear()
	
	def _quit_(self):
		if askokcancel("Exit", "Are you sure you want to quit?"):
			self.destroy()

	def Plot(self, data):
		frame = Frame(self.tab2, width = 700, height = 300)
		frame.place(x = 200, y = 400)
		samp = Samplerate(frame)
		samp._plot_(data)

	def Open(self):
		try:
			self.file = askopenfilename(title = "Open - Solemn2D 2.0", filetypes = [("All Files", "*.*")])
		except FileNotFoundError:pass
		if self.file == '':
			self.file = None
		else:
			if self.file[:3] == 'jpg' or 'png' or 'bmp' or 'gif':
				try:
					self.images.append(self.file)
					self.n = self.images.index(self.file)
					img = PIL.Image.open(self.file)
					self.img_win.change_image(img)
				except Exception as e:
					pass
			if self.file[:4] == '.mp3' or '.wav':
				self.SoundTrack = self.file
				try:
					self.SoundTrack = AudioSegment.from_mp3(self.file)
					self.SoundTrack = self.SoundTrack.export(f'{self.file}', format = 'wav')
				except:pass

			if self.file[:7] == '.solemn':
				with open(self.File, 'r') as f:
					data = eval(f.read())
					self.images = data['Images']
					self.SoundTrack = data['Sound']
					f.close()

	def FetchSound(self):
		self.SoundTrack = askopenfilename(title = "Open Sound Track - Solemn2D 2.0")
		self.SoundTrack = AudioSegment.from_mp3(self.SoundTrack)
		self.update_sound_editing_tools()

	def comingsoon(self):showinfo("Very Sorry", "This feature is not available for this version of the app,\n you can check for the latest verison with the\n version button in the help menu")

	def next_frame(self):
		self.n += 1
		self.img_win.del_canvas()
		try:
			img = PIL.Image.open(self.images[self.n])
		except:
			pass
		try:
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab1, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
			self.line_width = self.choose_size_button.get()
		except UnboundLocalError:
			pass
		self.progress_bar_['maximum'] = len(self.images)
		self.progress_bar_['value'] = self.n
		self.progress_bar_.update()

	def prev_frame(self):
		self.n -=1
		try:
			img = PIL.Image.open(self.images[self.n])
		except:
			pass
		try:
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab1, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
			self.line_width = self.choose_size_button.get()
		except UnboundLocalError:
			pass
		self.progress_bar_['maximum'] = len(self.images)
		self.progress_bar_['value'] = self.n
		self.progress_bar_.update()

	def next_frame_anime(self):
		self.n+=1
		try:
			img = PIL.Image.open(self.images[self.n])
		except:
			pass
		try:
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab3, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
		except UnboundLocalError:
			pass
		self.progress_bar['maximum'] = len(self.images)
		self.progress_bar['value'] = self.n
		self.progress_bar.update()

	def prev_frame_anime(self):
		self.n-=1
		try:
			img = PIL.Image.open(self.images[self.n])
		except:
			pass
		try:
			img = PIL.ImageTk.PhotoImage(img)
			self.img_win = ScrollableImage(self.tab3, image = img, scrollbarwidth = 16, width = 700, height = 480, line_width = 10)
			self.img_win.place(x = 130, y = 100)
		except UnboundLocalError:
			pass
		self.progress_bar['maximum'] = len(self.images)
		self.progress_bar['value'] = self.n
		self.progress_bar.update()

	def New(self):
		self.title("Untitled - Solemn2D 2.0")
		self.file = ''
		self.images = ['imgs/skeleton.jpg']
		self.img_win.del_canvas()
		img = PIL.Image.open('imgs/skeleton.jpg')
		img = PIL.ImageTk.PhotoImage(img)
		self.img_win.change_image(img)

	def save(self):         
		if not os.path.exists(self.File):
			self.File = asksaveasfilename(title = "Save Project - Solemn2D 2.0", initialfile = 'Untitled.solemn', defaultextension = " .solemn", filetypes = [("Solemn 2D files", "* .solemn")])
			if self.File == '':
				self.File == "Untitled"
			else:
				self.title(os.path.basename(self.File).replace('.solemn', '') + "- Solemn2D 2.0")
				with open(self.File, 'w+') as f:
					data = str({"Images":self.images, "Sound":self.SoundTrack})
					f.write(data)                                                                                                                                                                                                                           
					f.close()
		else:
			with open(self.File, 'w+') as f:
				f.truncate()
				f.write(str({"Images":self.images, "Sound":self.SoundTrack}))
				f.close()

	def Animate(self):
		pygame.init()
		# self.progressing()
		showinfo("", "Your animation is ready for preview")
		fps_ = self.FPS.get()
		images = self.images
		anime.animate(images, float(1/fps_))

	def About(self):showinfo('About Solemn2D', '''Solemn 2d is a simple beginner oriented animating 
and comic creating app that is simple and fast for 
amazing projects with wonderful features to help 
your animation skills at its best.
It is created by Praise James but the developer would
 like to thank pixabay.com for the Solemn ghoul image
 Icon was gotten from icons8 >>> https://icons8.com"
 it was built in 100% python code, and several libraries
 such as: tkinter, pygame, shutil, opencv, smtplib, ssl,
  subprocess, threading, time, os, pillow, pydub, scipy,
  TkinterDnD2, moviepy, AudioLib, numpy, and io.
Send Feedback with the 'send feedback' button to help us
 improve Solemn2D :)''')

	def Use(self):
		file = open('how.txt', 'r')
		showinfo("How to use", file.read())

	def version(self):
		showinfo("Version", "Solemn2D version 2.0")
		pop = Tk()
		pop.title('check for latest version')
		pop.geometry('150x50')
		pop.resizable(False, False)
		pop.wm_iconbitmap('imgs/logo.ico')

		def checklatest():
			import webbrowser
			pop.destroy()
			webbrowser.open('https://sourceforge.net/projects/solemn2d/')
		button = Button(pop, text = "check latest version", command = checklatest).pack()

	def feedback(self):
		pop = Tk()
		pop.title('Send Feedback')
		pop.geometry('400x200')
		pop.wm_iconbitmap('imgs/logo.ico')

		email = Entry(pop, width = 30)
		email.place(x = 100, y = 25)
		password = Entry(pop, width = 30, show = '*')
		password.place(x = 100, y = 60)
		message = Entry(pop, width = 50)
		message.place(x = 50, y = 100)

		def send():
			port = 465
			email_ = email.get()
			password_ = password.get()
			message_ = message.get()
			context = ssl.create_default_context()
			pop.destroy()
			try:
				with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
					server.login(email_, password_)
					for i in file.readlines():
						server.send_mail(email_, 'praisejames011@gmail.com', message_) 
			except Exception as e:showerror("An Error Occured", e)

		btn = Button(pop, text = 'Send', command = send)
		btn.place(x = 170, y = 150)

		create_Tip(email, 'Enter your email here')
		create_Tip(password, 'Enter your password here')
		create_Tip(message, 'Enter your feedback')

	def Use(self):
		file = open('how.txt', 'r')
		showinfo("How to use", file.read())

	def createVid(self, images, fps, title, audio):
		imgs = []
		for i in images:
			img = cv2.imread(i)
			height, width, layer = img.shape
			size = (width, height)
			imgs.append(img)
		Title = title.replace('.solemn', '')
		# print(Title)
		output = cv2.VideoWriter(Title, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
		for i in range(len(imgs)):
			output.write(imgs[i])
		output.release()
		if self.SoundTrack is not None:
			os.popen(f'CMD /K ffmpeg -i ' + Title + ' -i ' + audio +' -map 0:0 -map 1:0 -c:v copy -c:a copy ' + title)

	def export(self):
		images = self.images
		fps = self.FPS.get()
		self.progressing()
		title = self.File.replace('.avi', '') + '.avi'
		try:
			self.createVid(images, fps, title, audio = self.images[0])
		except TypeError:
			showerror("An Error Occured", "You'll need to import an audio to export the project")
		showinfo("Success", "Your animation was exported succesfully exported to "+title)

if __name__=='__main__':
	Main().mainloop()
