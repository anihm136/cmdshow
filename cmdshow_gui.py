from lib import createSlideshow
import os
import platform
import subprocess
import time
from tkinter import filedialog
from tkinter import *
'''Directory of images
		- [x] Music file
		- [ ] Frame duration
		- [ ] Transition duration
		- [ ] Transition type
		- [ ] Resolution'''

class App:

    def __init__(self):
        self.root = Tk()
        self.root.title("CMDShow")
        self.root.configure(background="#121212")
        self.root.geometry("800x500")
        self.imageDir = ""
        self.audio = ""
        self.blank = Label(self.root, bg="#121212")
        self.blank.grid(row = 0, columnspan = 2)
        self.welcome = Label(
            self.root, text="Welcome to CMDShow!", background="#121212"
        )
        self.welcome.config(fg="#3b54ce", font=("Comfortaa", 40))
        self.welcome.grid(row = 1, columnspan = 2)
        self.blank = Label(self.root, bg="#121212")
        self.blank.grid(row = 2, columnspan = 2)
        self.imagesButton = Button(
            self.root,
            text="Choose Image Directory",
            command=self.chooseImageDir,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.imagesButton.grid(row = 3, column = 0)
        self.audio = Button(
            self.root,
            text="Choose Audio File",
            command=self.chooseAudio,
            bg="#4759b8",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.audio.grid(row = 3, column = 1)
        self.blank = Label(self.root, bg="#121212")
        self.blank.grid(row = 4, columnspan = 2)
        self.welcome = Label(
            self.root, text="Welcome to CMDShow!", background="#121212"
        )
        self.welcome.config(fg="#3b54ce", font=("Comfortaa", 40))
        self.welcome.grid(row = 1, columnspan = 2)
        self.root.mainloop()

    def chooseImageDir(self):
        self.imageDir = filedialog.askdirectory()
        #print(self.imageDir)

    def chooseAudio(self):
        self.audio = filedialog.askopenfile(mode ='r', filetypes =[('Audio Files', '*.wav')])
        if self.audio!=None:
            self.audio = self.audio.name 
        #print(self.audio.name)
App()