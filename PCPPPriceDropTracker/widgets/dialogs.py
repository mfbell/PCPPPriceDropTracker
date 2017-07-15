"""Dialog boxes for PCPPPriceDropTracker."""

import tkinter as tk
from tkinter import ttk, filedialog
from logging import getLogger
from os.path import basename

from tools import Tools, pdname, main, CallbackWithArgs
from .customWidgets import Panel, ScrollablePanel


__all__ = ["OpenDB"]


class OpenDB(Panel):
    """Open database dialog."""

    def __init__(self, root=None, resent=[], *args, **kwargs):
        """Initialization."""
        logger = getLogger(pdname+"."+__name__+".OpenDB.__init__")
        logger.debug("OpenDB initalization.")
        if root is None:
            root = tk.Toplevel()
        super().__init__(root, *args, **kwargs)
        self.grid()
        try:
            self.root.title("Open database...")
        except AttributeError:
            self.info_title = ttk.Label(self, text="Open database...")
            self.info_title.grid(column=0, row=0)

        self.text = ttk.Label(self, text="Open a database...")
        self.entrybox = FilePathEntry(self, self.cb, relief="groove")

        self.resent_title = ttk.Label(self, text="Resent databases")
        self.list = FileList(self, paths=resent, padding=6)

        self.text.grid(column=0, row=1)
        self.entrybox.grid(column=0, row=2, sticky="we")

        self.resent_title.grid(column=0, row=4)
        self.list.grid(column=0, row=5)

        logger.debug("OpenDB setup complete.")
        return

    def cb(self, path):
        print("open "+path)



class EntryPressCB(CallbackWithArgs):
    def call(self, *a, **k):
        print("pressed "+self.kwargs["path"])


class FileList(ScrollablePanel):
    """"""

    def __init__(self, root, paths=[], *args, **kwargs):
        """"""
        logger = getLogger(pdname+"."+__name__+".FileList")
        logger.debug("FileList initalization.")
        super().__init__(root, *args, **kwargs)
        self.scrollwindow
        self.build(paths)

        logger.debug("Filelist setup complete.")
        return

    def build(self, paths):
        s = ttk.Style()
        s.map("FileEntry.TButton",
              background=[("pressed", "#4262f4"), ("active", "#3ba4f9"), ("!disabled", "#3af9c6")],
              highlightcolor=[("pressed", "#4262f4"), ("active", "#3ba4f9"), ("!disabled", "#3af9c6")])
        self.scrollwindow.entries = []
        for path in paths:
            e = FileEntry(self.scrollwindow, path, callback=EntryPressCB(path=path), padding=6, style="FileEntry.TButton", takefocus=True)
            e.grid(column=0, row=len(self.scrollwindow.entries), sticky="new", pady=2, padx=6)
            self.scrollwindow.entries.append(e)
        return

class FileEntry(Panel):
    """"""

    def __init__(self, root, path, callback, name_style="TLabel",
                 path_style="TLabel", *args, **kwargs):
        """Return a file entry panel."""
        super().__init__(root, *args, **kwargs)
        self.path = path
        self.name_style = name_style
        self.path_style = path_style
        self.callback = callback
        self.lname = ttk.Label(self, text=basename(path), style=self.name_style)
        self.lpath = ttk.Label(self, text=path, style=self.path_style)

        self.lname.grid(column=0, row=0, sticky="nw")
        self.lpath.grid(column=0, row=1, sticky="nw")
        self.add_binds()

    def add_binds(self):
        widgets = self.get_all_children(self)
        widgets.append(self)
        for widget in widgets:
            widget.bind("<Button-1>", self.on_click)
            widget.bind("<ButtonRelease-1>", self.on_click_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_exit)
        self.bind("<FocusIn>", self.on_enter)
        self.bind("<FocusOut>", self.on_exit)


    def on_click(self, event):
        s = ttk.Style()
        s.configure(self["style"],
                    background="blue")
        self.update()
        self.callback()

    def on_click_release(self, event):
        s = ttk.Style()
        s.configure(self["style"],
                    background="green")
        self.update()

    def on_enter(self, event):
        s = ttk.Style()
        s.configure(self["style"],
                    background="green")
        self.update()

    def on_exit(self, event):
        s = ttk.Style()
        s.configure(self["style"],
                    background="pink")
        self.update()



    def get_all_children(self, wid, nested=False):
        if nested:
            nest = {}
        children = wid.winfo_children()
        for child in children:
            method = getattr(child, "winfo_children", None)
            if callable(method):
                if nested:
                    nest[child] = self.get_all_children(child, True)
                else:
                    children.extend(self.get_all_children(child))
        return nest if nested else children


class _1FileEntry(Tools, ttk.Button):
    """"""

    def __init__(self, root, path, name_style="TLabel",
                 path_style="TLabel", *args, **kwargs):
        """Return a file entry panel."""
        Tools.__init__(self, *args, **kwargs)
        self.root = root
        self.path = path
        self.kwargs["text"] = basename(self.path) + "\n" + self.path
        ttk.Button.__init__(self, self.root, *self.args, **self.kwargs)

        #self.name_style = name_style
        #self.path_style = path_style
        #self.lname = ttk.Label(self, text=basename(path))#, style=self.name_style)
        #self.lpath = ttk.Label(self, text=path)#, style=self.path_style)

        #self.lname.grid(column=0, row=0, sticky="nw")
        #self.lpath.grid(column=0, row=1, sticky="nw")

        """self.bind("<Button-1>", self.callback)
        self.lname.bind("<Button-1>", self.callback)
        self.lpath.bind("<Button-1>", self.callback)"""
        return


class FilePathEntry(Panel):
    """"""

    def __init__(self, root, callback, *args, **kwargs):
        """"""
        super().__init__(root, *args, **kwargs)
        self.callback_ = callback
        self.path = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.path)
        self.find_button = ttk.Button(self, text="...", command=self.askopenfilename)
        self.open_button = ttk.Button(self, text="Open", command=self.callback)

        self.entry.grid(column=0, row=0, sticky="we")
        self.find_button.grid(column=1, row=0)
        self.open_button.grid(column=2, row=0)

        self.grid_columnconfigure(0, weight=1)

        return


    def askopenfilename(self):
        path = filedialog.askopenfilename()
        if not path:
            return
        else:
            self.callback(path)


    def callback(self, path=None):
        if path is not None:
            self.path.set(path)
        self.callback_(self.path.get())






if __name__ == '__main__':
    main(__doc__)
