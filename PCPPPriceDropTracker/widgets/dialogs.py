"""Dialog boxes for PCPPPriceDropTracker."""

import tkinter as tk
from tkinter import ttk
from logging import getLogger

from tools import pdname, main
from .customWidgets import Panel, FilePathEntry, FileList


__all__ = ["OpenDB", "CreateDB"]


class _DialogTools(Panel):
    """General dialog tools."""
    def callback(self, *a, **kw):
        if self.destroy_:
            self.master.destroy()
        self.callback_(*a, **kw)

    def cancel(self, *a, **kw):
        self.master.destroy()
        self.callback(event = self.cancel, *a, **kw)


class _PathDialog(_DialogTools):
    def cancel(self, *a, **kw):
        super().cancel(path = "", *a, **kw)


class CreateDB(_PathDialog):
    """Create a new database dialog."""

    def __init__(self, callback, master = None, destroy = True, *args, **kwargs):
        logger = getLogger(pdname + "." + __name__ + ".CreateDB.__init__")
        logger.debug("CreateDB initalization.")
        if master is None:
            master = tk.Toplevel()
        super().__init__(master, *args, **kwargs)
        self.grid()
        self.callback_ = callback
        self.destroy_ = destroy
        try:
            self.master.title("Create database...")
        except AttributeError:
            pass

        self.text = ttk.Label(self, text = "Create a database...")
        self.entrybox = FilePathEntry(self, callback = self.callback, action_text = "Create", finder = "getsavefile", padding = (12, 6))
        self.text.grid(column = 0, row = 1)
        self.entrybox.grid(column = 0, row = 2, sticky = "we")
        self.grid_columnconfigure(0, weight = 1)

        # Side options
        self.options = ttk.Frame(self, padding=3)
        self.options.create = ttk.Button(self.options, text = "Open", command = self.change_to_open_dialog)
        self.options.cancel = ttk.Button(self.options, text = "Cancel", command = self.cancel)
        self.options.create.grid(column = 0, row = 0, pady = (3, 0))
        self.options.cancel.grid(column = 0, row = 1, pady = (3, 0))
        self.options.grid(column = 1, row = 0, rowspan = 99, sticky = "nw")

        self.focus_set()
        self.grab_set()

    def change_to_open_dialog(self):
        self.master.destroy()
        OpenDB(self.callback_)


class OpenDB(_PathDialog):
    """Open database dialog."""

    def __init__(self, callback, master = None, resent = [], destroy = True, *args, **kwargs):
        """Initialization."""
        logger = getLogger(pdname + "." + __name__ + ".OpenDB.__init__")
        logger.debug("OpenDB initalization.")
        if master is None:
            self.master = tk.Toplevel()
        else:
            self.master = master
        super().__init__(self.master, *args, **kwargs)
        self.grid()
        self.callback_ = callback
        self.destroy_ = destroy
        try:
            self.master.title("Open database...")
        except AttributeError:
            pass

        self.text = ttk.Label(self, text = "Open a database")
        self.entrybox = FilePathEntry(self, callback = self.callback, action_text = "Open", finder = "getopenfile", padding = (12, 6))
        self.text.grid(column = 0, row = 1)
        self.entrybox.grid(column = 0, row = 2, sticky = "we")

        if resent:
            self.resent_title = ttk.Label(self, text = "Resent databases")
            self.list = FileList(self, paths = resent, callback = self.callback, padding = 3)
            self.resent_title.grid(column = 0, row = 4)
            self.list.grid(column = 0, row = 5)

        # Side options
        self.options = ttk.Frame(self, padding=3)
        self.options.create = ttk.Button(self.options, text = "New", command = self.change_to_create_dialog)
        self.options.cancel = ttk.Button(self.options, text = "Cancel", command = self.cancel)
        self.options.create.grid(column = 0, row = 0, pady = (3, 0))
        self.options.cancel.grid(column = 0, row = 1, pady = (3, 0))
        self.options.grid(column = 1, row = 0, rowspan = 99, sticky = "nw")

        self.focus_set()
        self.grab_set()

        logger.debug("OpenDB setup complete.")
        return

    def change_to_create_dialog(self):
        self.master.destroy()
        CreateDB(self.callback_)

if __name__ == '__main__':
    main(__doc__)
