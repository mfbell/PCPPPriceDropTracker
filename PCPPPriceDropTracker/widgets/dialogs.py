"""Dialog boxes for PCPPPriceDropTracker."""

import tkinter as tk
from tkinter import ttk
from logging import getLogger

from tools import pdname, main
from .customWidgets import Panel, FilePathEntry, FileList


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
            pass

        self.text = ttk.Label(self, text="Open a database...")
        self.entrybox = FilePathEntry(self, self.cb, padding=(12, 6))
        self.text.grid(column=0, row=1)
        self.entrybox.grid(column=0, row=2, sticky="we")

        self.resent_title = ttk.Label(self, text="Resent databases")
        self.list = FileList(self, paths=resent, callback=self.cb, padding=3)
        self.resent_title.grid(column=0, row=4)
        self.list.grid(column=0, row=5)
        self.focus_set()
        self.grab_set()

        logger.debug("OpenDB setup complete.")
        return

    def cb(self, path, event=None):
        print("open "+path)



if __name__ == '__main__':
    main(__doc__)
