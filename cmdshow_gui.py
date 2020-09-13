import os
import platform
import re
import subprocess
import time
from pathlib import Path
from tkinter import *
from tkinter import filedialog, ttk
from lib.utils import getImagesFromPath, orderImages
from lib import createSlideshow

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("CMDShow")
        self.root.configure(background="#d2d2c9")

        self.imageDir = StringVar()
        self.imageOrderType = ""
        self.imageOrder = None
        self.outputDir = StringVar()
        self.audio = StringVar()
        self.resolution = ""
        self.frameDuration = ""
        self.transitionType = ""
        self.framerate = ""
        self.transitionDuration = ""
        self.createdSlideshow = ""
        self.error = StringVar()
        self.imageDir.set("No image directory chosen")
        self.outputDir.set("slideshow.mp4")
        self.audio.set("No audio file chosen")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=0, columnspan=6)

        self.welcome = Label(
            self.root, text="CMDShow!", background="#d2d2c9"
        )
        self.welcome.config(fg="#6d031c", font=("Roboto", 40))
        self.welcome.grid(row=1, columnspan=6, sticky="NSEW", padx = 200)

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
        self.imagesButton.grid(row=3, column=0, columnspan=3)

        self.imgdir_content = Message(
            self.root,
            textvariable=self.imageDir,
            bg="#d2d2c9",
            font=("Calibri"),
            fg="#673e37",
        )
        self.imgdir_content.grid(row=3, column = 3, columnspan=3, sticky = "WE")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=4, columnspan=6)

        self.audioButton = Button(
            self.root,
            text="Choose Audio File",
            command=self.chooseAudio,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.audioButton.grid(row=5, column=0, columnspan=3)

        self.audiodir_content = Message(
            self.root,
            textvariable=self.audio,
            bg="#d2d2c9",
            font=("Calibri"),
            fg="#673e37",
        )
        self.audiodir_content.grid(row=5, column = 3, columnspan=3)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=6, columnspan=6)

        self.output = Button(
            self.root,
            text="Choose Output Directory",
            command=self.chooseOutDir,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.output.grid(row=7, column=0, columnspan=3)

        self.opdir_content = Message(
            self.root,
            textvariable=self.outputDir,
            bg="#d2d2c9",
            font=("Calibri"),
            fg="#673e37"
        )
        self.opdir_content.grid(row=7, column = 3, columnspan=3)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=8, columnspan=6)

        self.config = Label(
            self.root, text="SETTINGS", background="#d2d2c9"
        )
        self.config.config(fg="#6d031c", font=("Comfortaa", 15))
        self.config.grid(row=9, column = 2, columnspan=2, sticky="NSEW")

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=10, columnspan=6)

        self.transition_dur = Label(
            self.root, text="Transition Duration", background="#d2d2c9"
        )
        self.transition_dur.config(fg="#673e37", font=("Comfortaa", 15))
        self.transition_dur.grid(row=11, column=0, columnspan = 3, padx=5)

        self.transition_dur_entry = Entry(self.root)
        self.transition_dur_entry.grid(row=11, column=3, columnspan = 3)
        self.transition_dur_entry.insert(0, "2")

        self.frame_dur = Label(
            self.root, text="Frame Duration", background="#d2d2c9")
        self.frame_dur.config(fg="#673e37", font=("Comfortaa", 15))
        self.frame_dur.grid(row=12, column=0, columnspan = 3, padx=5)

        self.frame_dur_entry = Entry(self.root)
        self.frame_dur_entry.grid(row=12, column=3, columnspan = 3)
        self.frame_dur_entry.insert(0, "5")

        self.transition_type = Label(
            self.root, text="Transition Type", background="#d2d2c9"
        )
        self.transition_type.config(fg="#673e37", font=("Comfortaa", 15))
        self.transition_type.grid(row=13, column=0, columnspan = 3, padx=5)

        self.transition_type_entry = ttk.Combobox(
            self.root, textvariable=self.transitionType
        )
        self.transition_type_entry["values"] = [
            "random",
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
            "fadegrays",
        ]
        self.transition_type_entry.current(1)
        self.transition_type_entry.grid(row=13, column=3, columnspan=3, padx=10)


        self.frame_rate = Label(
            self.root, text="Frame Rate", background="#d2d2c9")
        self.frame_rate.config(fg="#673e37", font=("Comfortaa", 15))
        self.frame_rate.grid(row=14, column=0, columnspan=3)

        self.frame_rate_entry = Entry(self.root)
        self.frame_rate_entry.grid(row=14, column=3, columnspan=3)
        self.frame_rate_entry.insert(0, "15")

        self.show_resolution = Label(
            self.root, text="Resolution", background="#d2d2c9")
        self.show_resolution.config(fg="#673e37", font=("Comfortaa", 15))
        self.show_resolution.grid(row=15, column=0, columnspan=3)

        self.resolution_entry = Entry(self.root)
        self.resolution_entry.grid(row=15, column=3, columnspan=3)
        self.resolution_entry.insert(0, "1920x1080")

        self.show_order = Label(
            self.root, text="Order Image by", background="#d2d2c9")
        self.show_order.config(fg="#673e37", font=("Comfortaa", 15))
        self.show_order.grid(row=16, column=0, columnspan=3)

        self.order_type_entry = ttk.Combobox(
            self.root, textvariable=self.transitionType
        )
        self.order_type_entry["values"] = ["Similarity", "Name", "Custom"]
        self.order_type_entry.current(1)
        self.order_type_entry.grid(row=16, column=3, columnspan=3, padx=10)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=17, columnspan=6)

        self.content = Message(
            self.root,
            textvariable=self.error,
            bg="#d2d2c9",
            font=("Calibri"),
            fg="#673e37",
        )
        self.content.grid(row=18, columnspan=6)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=19, columnspan=6)

        self.generateButton = Button(
            self.root,
            text="Create Slideshow",
            command=self.generateSlideshow,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.generateButton.grid(row=20, column=0, columnspan=3)

        self.playButton = Button(
            self.root,
            text="Play Slideshow",
            command=self.playSlideshow,
            bg="#6d031c",
            fg="white",
            font=("Comfortaa", 15),
        )
        self.playButton.grid(row=20, column=3, columnspan=3)

        self.blank = Label(self.root, bg="#d2d2c9")
        self.blank.grid(row=21, columnspan=6)

        self.root.mainloop()

    def generateSlideshow(self):
        self.resolution = self.resolution_entry.get()
        self.frameDuration = self.frame_dur_entry.get()
        self.transitionType = self.transition_type_entry.get()
        self.framerate = self.frame_rate_entry.get()
        self.transitionDuration = self.transition_dur_entry.get()
        self.imageOrderType = self.order_type_entry.get()

        check = True
        if self.imageDir.get() == "No image directory chosen":
            self.error.set("Choose image directory.")
            check = False
            return
        else:
            images = getImagesFromPath(self.imageDir.get())
            if self.imageOrderType == "Custom":
                self.slave = Tk()
                self.slave.title("Choose Image Order")
                self.slave.configure(background="#d2d2c9")
                listbox = DragDropListbox(self.slave)
                btn = Button(self.slave, text="Submit", command=lambda : self.getImageOrder(listbox))
                for name in self.imageOrder:
                    listbox.insert(END, name)
                listbox.pack(fill=BOTH, expand=True)
                btn.pack(fill=BOTH)
            elif self.imageOrderType == "Name":
                self.imageOrder = orderImages(images, "name")
            else:
                self.imageOrder = orderImages(images, "sim")
            self.imageOrder = [Path(i) for i in self.imageOrder]
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
        else:
            self.resolution = tuple(map(int, self.resolution.split("x")))

        if check == False:
            pass
        else:
            self.error.set("")
            createSlideshow(
                self.imageOrder,
                self.audio.get(),
                self.frameDuration,
                self.framerate,
                self.resolution,
                self.transitionDuration,
                self.transitionType,
                self.outputDir.get(),
            )

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
        self.imageDir.set(filedialog.askdirectory())


    def chooseAudio(self):
        self.audio.set(filedialog.askopenfile(
            mode="r", filetypes=[("Audio Files", "*.wav")]
        ).name)

    def chooseOutDir(self):
        self.outputDir.set(filedialog.asksaveasfile(
            filetypes=[("Video Files", ".mp4"), ("Video Files", ".avi"), ("Video Files", ".flv"), (
                "Video Files", ".m4a"), ("Video Files", ".mov"), ("Video Files", ".ogg"), ("Video Files", ".webm")],
        ).name)
        os.remove(self.outputDir)

    def getImageOrder(self, listbox):
        self.imageOrder = listbox.show()

class DragDropListbox(Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw["selectmode"] = SINGLE
        Listbox.__init__(self, master, kw)
        self.bind("<Button-1>", self.setCurrent)
        self.bind("<B1-Motion>", self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i

    def show(self):
        order = self.get(0,'end')
        self.master.destroy()
        print(order)
        return order


App()
