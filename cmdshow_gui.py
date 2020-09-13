from lib import createSlideshow
import os
import re
import platform
import subprocess
import time
from tkinter import filedialog
from tkinter import *
from tkinter import ttk


class App:

    def __init__(self):
        self.root = Tk()
        self.root.title("CMDShow")
        self.root.configure(background="#d2d2c9")
        # self.root.geometry("800x500")

        self.imageDir = ""
        self.outputDir = "slideshow.mp4"
        self.audio = ""
        self.resolution = ""
        self.frameDuration = ""
        self.transitionType = ""
        self.framerate = ""
        self.transitionDuration = ""
        self.createdSlideshow = ""
        self.error = StringVar()

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=0, columnspan=6)

        self.welcome = Label(
            self.root, text="Welcome to CMDShow!", background="#d2d2c9"
        )
        self.welcome.config(fg="#6d031c", font=("Comfortaa", 40))
        self.welcome.grid(row=1, columnspan=6, sticky="NSEW")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=2, columnspan=6)

        self.imagesButton = Button(
            self.root,
            text="Choose Image Directory",
            command=self.chooseImageDir,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.imagesButton.grid(row=3, column=0, columnspan=2)

        self.audioButton = Button(
            self.root,
            text="Choose Audio File",
            command=self.chooseAudio,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.audioButton.grid(row=3, column=2, columnspan=2)

        self.output = Button(
            self.root,
            text="Choose Output Directory",
            command=self.chooseOutDir,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.output.grid(row=3, column=4, columnspan=2)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=4, columnspan=6)

        self.transition_dur = Label(
            self.root, text="Transition Duration", background="#d2d2c9"
        )
        self.transition_dur.config(fg="#673e37", font=("Comfortaa", 15))
        self.transition_dur.grid(row=5, column=0, padx=5)

        self.transition_dur_entry = Entry(self.root)
        self.transition_dur_entry.grid(row=5, column=1)
        self.transition_dur_entry.insert(0, "1")

        self.frame_dur = Label(
            self.root, text="Frame Duration", background="#d2d2c9"
        )
        self.frame_dur.config(fg="#673e37", font=("Comfortaa", 15))
        self.frame_dur.grid(row=5, column=2, padx=5)

        self.frame_dur_entry = Entry(self.root)
        self.frame_dur_entry.grid(row=5, column=3)
        self.frame_dur_entry.insert(0, "5")

        self.transition_type = Label(
            self.root, text="Transition Type", background="#d2d2c9"
        )
        self.transition_type.config(fg="#673e37", font=("Comfortaa", 15))
        self.transition_type.grid(row=5, column=4, padx=5)

        self.transition_type_entry = ttk.Combobox(
            self.root, textvariable=self.transitionType)
        self.transition_type_entry["values"] = ["random",
                                                "fade",
                                                "fadeblack",
                                                "fadewhite",
                                                "distance",
                                                "wipeleft",
                                                "wiperight",
                                                "wipeup",
                                                "wipedown",
                                                "slideleft",
                                                "slideright",
                                                "slideup",
                                                "slidedown",
                                                "smoothleft",
                                                "smoothright",
                                                "smoothup",
                                                "smoothdown",
                                                "rectcrop",
                                                "circlecrop",
                                                "circleclose",
                                                "circleopen",
                                                "horzclose",
                                                "horzopen",
                                                "vertclose",
                                                "vertopen",
                                                "diagbl",
                                                "diagbr",
                                                "diagtl",
                                                "diagtr",
                                                "hlslice",
                                                "hrslice",
                                                "vuslice",
                                                "vdslice",
                                                "dissolve",
                                                "pixelize",
                                                "radial",
                                                "hblur",
                                                "wipetl",
                                                "wipetr",
                                                "wipebl",
                                                "wipebr",
                                                "fadegrays"]
        self.transition_type_entry.current(1)
        self.transition_type_entry.grid(row=5, column=5, padx=10)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=6, columnspan=6)

        self.frame_rate = Label(
            self.root, text="Frame Rate", background="#d2d2c9"
        )
        self.frame_rate.config(fg="#673e37", font=("Comfortaa", 15))
        self.frame_rate.grid(row=7, column=0, columnspan=1)

        self.frame_rate_entry = Entry(self.root)
        self.frame_rate_entry.grid(row=7, column=1, columnspan=2)
        self.frame_rate_entry.insert(0, "10")

        self.show_resolution = Label(
            self.root, text="Resolution", background="#d2d2c9"
        )
        self.show_resolution.config(fg="#673e37", font=("Comfortaa", 15))
        self.show_resolution.grid(row=7, column=3, columnspan=1)

        self.resolution_entry = Entry(self.root)
        self.resolution_entry.grid(row=7, column=4, columnspan=2)
        self.resolution_entry.insert(0, "1920x1080")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=8, columnspan=6)

        self.content = Message(
            self.root,
            textvariable=self.error,
            bg="#d2d2c9",
            font=("Calibri"),
            fg="#673e37",
        )
        self.content.grid(row=9, columnspan=6)

        self.generateButton = Button(
            self.root,
            text="Create Slideshow",
            command=self.generateSlideshow,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.generateButton.grid(row=10, column=0, columnspan=3)

        self.playButton = Button(
            self.root,
            text="Play Slideshow",
            command=self.playSlideshow,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.playButton.grid(row=10, column=3, columnspan=3)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=11, columnspan=6)

        self.root.mainloop()

    def generateSlideshow(self):
        self.resolution = self.resolution_entry.get()
        self.frameDuration = self.frame_dur_entry.get()
        self.transitionType = self.transition_type_entry.get()
        self.framerate = self.frame_rate_entry.get()
        self.transitionDuration = self.transition_dur_entry.get()
        check = True
        if self.imageDir == "":
            self.error.set("Choose image directory.")
            check = False
            return
        if self.audio == ".!button2":
            self.audio = ""
        try:
            self.frameDuration = int(self.frameDuration)
        except:
            self.error.set("Frame Duration needs to be an INT")
            check = False
            return
        try:
            self.transitionDuration = int(self.transitionDuration)
        except:
            self.error.set("Transition Duration needs to be an INT")
            check = False
            return
        try:
            self.framerate = int(self.framerate)
        except:
            self.error.set("Frame Rate needs to be an INT")
            check = False
            return
        if not re.findall(r"[0-9]+x[0-9]+", self.resolution):
            self.error.set("Invalid format for Resolution")
            check = False
            return

        if check == True:
            self.error.set("")
        else:
            createSlideshow(self.imageDir, self.audio, self.frameDuration, self.framerate,
                            self.resolution, self.transitionDuration, self.transitionType, self.outputDir)

    def playSlideshow(self):
        try:
            if platform.system() == "Darwin":
                subprocess.call(("open", self.outputDir))
            elif platform.system() == "Windows":
                os.startfile(self.outputDir)
            else:
                subprocess.call(("xdg-open", self.outputDir))
        except:
            self.error.set("Video not found.")

    def chooseImageDir(self):
        self.imageDir = filedialog.askdirectory()

    def chooseAudio(self):
        self.audio = filedialog.askopenfile(
            mode='r', filetypes=[('Audio Files', '*.wav')]).name

    def chooseOutDir(self):
        self.outputDir = filedialog.asksaveasfile(filetypes=[(
            "Video Files", ".mp4")], defaultextension=[("Video Files", ".mp4")]).name
        os.remove(self.outputDir)
        if not self.outputDir.endswith(".mp4"):
            self.outputDir += ".mp4"


App()
