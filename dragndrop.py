import tkinter


class DragDropListbox(tkinter.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw["selectmode"] = tkinter.SINGLE
        tkinter.Listbox.__init__(self, master, kw)
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
        print(self.get(0,'end'))


root = tkinter.Tk()
listbox = DragDropListbox(root)
btn = tkinter.Button(root, text="Hello", command=listbox.show)
for i, name in enumerate(["name" + str(i) for i in range(10)]):
    listbox.insert(tkinter.END, name)
    if i % 2 == 0:
        listbox.selection_set(i)
listbox.pack(fill=tkinter.BOTH, expand=True)
btn.pack(fill=tkinter.BOTH)
root.mainloop()
