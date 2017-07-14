"""Dialog boxes for PCPPPriceDropTracker."""

import tkinter as tk
import tkinter.ttk as ttk
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

        self.list = FileList(self, paths=resent)

        self.text.grid(column=0, row=1)
        self.list.grid(column=0, row=2)

        logger.debug("OpenDB setup complete.")
        return

class EntryPressCB(CallbackWithArgs):
    def call(self, event):
        print("pressed "+self.kwargs["path"])


class FileList(Panel):
    """"""

    def __init__(self, root, paths=[], *args, **kwargs):
        """"""
        logger = getLogger(pdname+"."+__name__+".FileList")
        logger.debug("FileList initalization.")
        super().__init__(root, *args, **kwargs)
        self.scrollable_panel = ScrollablePanel(self.root)
        self.build(paths)

        logger.debug("Filelist setup complete.")
        return

    def build(self, paths):
        s = ttk.Style()
        s.map("FileEntry.TFrame",
              foreground=[("pressed", "red"), ("active", "blue")],
              background=[("pressed", "!disabled", "black"), ("active", "white")]
              )
        self.entries = []
        for path in paths:
            e = FileEntry(self, path, EntryPressCB(path=path), padding=6, style="FileEntry.TFrame")
            e.grid(column=0, row=len(self.entries), sticky="nsw")
            self.entries.append(e)
        return

    def grid(self, *args, **kwargs):
        super().grid()
        self.scrollable_panel.grid(*args, **kwargs)


class FileEntry(Panel):
    """"""

    def __init__(self, root, path, callback, name_style="TLabel",
                 path_style="TLabel", *args, **kwargs):
        """Return a file entry panel."""
        super().__init__(root, *args, **kwargs)
        self.path = path
        self.callback = callback
        self.name_style = name_style
        self.path_style = path_style
        self.lname = ttk.Label(self, text=basename(path), style=self.name_style)
        self.lpath = ttk.Label(self, text=path, style=self.path_style)

        self.lname.grid(column=0, row=0, sticky="nw")
        self.lpath.grid(column=0, row=1, sticky="nw")

        self.bind("<Button-1>", self.callback)
        self.lname.bind("<Button-1>", self.callback)
        self.lpath.bind("<Button-1>", self.callback)
        return






if __name__ == '__main__':
    main(__doc__)
