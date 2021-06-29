class Sound:
    """class for sound editing"""
    def __init__(self):
        pass
    def initiate(self): 
        try:
            self.track = AudioSegment.from_mp3(self.images[0])
        except:pass
        # stack and queue are arrays used for the undo/redo functionality. 
        self.queue = []
        self.stack = []
    def save(self):
        save_path = asksaveasfilename(initialdir = "/home/", title = "save the modified file", filetypes = (("mp3 files","*.mp3"), ("all files","*.*")))
        self.track.export(save_path, bitrate = "320k",format = "mp3")
        
    def reverse(self):
        self.stack.append(self.track)
        self.track = self.track.reverse()
        self.images[0] = self.track

    def checkLength(self):return self.track.duration_seconds

    def mergeTracks(self):
        self.stack.append(self.track)
        self.filePath = askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
        self.mergeTrack = AudioSegment.from_mp3(self.filePath)
        self.track = self.track + self.mergeTrack

    def gapMerge(self):
        self.stack.append(self.track)
        self.filePath = tkFileDialog.askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
        self.mergeTrack = AudioSegment.from_mp3(self.filePath)
        self.track = self.track + AudioSegment.silent(duration = 10000) + self.mergeTrack

    def repeat(self):
        self.stack.append(self.track)
        self.track = self.track*2
        
    def overlay(self):
        self.stack.append(self.track)
        self.filePath = askopenfilename(initialdir = "/home/", title = "What file do you want to import?", filetypes = (("mp3 files","*.mp3"),("all files","*.*")))
        self.overlayTrack = AudioSegment.from_mp3(self.filePath)
        self.track = self.track.overlay(self.overlayTrack)

    def undo(self):
        self.queue.insert(0, self.track)
        self.track = self.stack.pop()
    
    def redo(self):
        self.stack.append(self.track)
        self.track = self.queue[0]
        self.queue.pop(0)
        