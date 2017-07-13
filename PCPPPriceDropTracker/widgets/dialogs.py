"""Dialog boxes for PCPPPriceDropTracker."""

import tkinter as tk
import tkinter.ttk as ttk
from logging import getLogger
from os.path import basename

from tools import Tools, pdname, main
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

        self.list = FileList(self, paths=resent)

        self.list.grid(column=0, row=2)

        logger.debug("OpenDB setup complete.")
        return


class FileList(Panel):
    """"""

    def __init__(self, root, paths=[], *args, **kwargs):
        """"""
        logger = getLogger(pdname+"."+__name__+".FileList")
        logger.debug("FileList initalization.")
        super().__init__(root, *args, **kwargs)
        self.scrollable_panel = ScrollablePanel(self.root)
        self.grid()



        s = ttk.Style()
        s.configure('mouseover.TFrame',
                    background='black',)
        s.map('mouseover.TFrame',
              foreground=[('disabled', 'yellow'),
                          ('pressed', 'red'),
                          ('active', 'blue')],
              background=[('disabled', 'magenta'),
                          ('pressed', '!focus', 'cyan'),
                          ('active', 'green')],
              relief=[('pressed', 'groove'),
                      ('!pressed', 'ridge')])

        s.configure('mouseover.TLabel',
                    background='black',
                    foreground='white',
                    highlightthickness='20',
                    font=('Helvetica', 10))
        s.map('mouseover.TLabel',
              foreground=[('disabled', 'yellow'),
                          ('pressed', 'red'),
                          ('active', 'blue')],
              background=[('disabled', 'magenta'),
                          ('pressed', '!focus', 'cyan'),
                          ('active', 'green')],
              highlightcolor=[('focus', 'green'),
                              ('!focus', 'red')],
              relief=[('pressed', 'groove'),
                      ('!pressed', 'ridge')])

        self.entries = []
        for path in paths:
            self.add(path)

        # Temp for development
        if not self.entries:
            self.add("No entries")

        logger.debug("Filelist setup complete.")
        return

    def add(self, path):
        """Add an entry to entries."""
        entry = {}
        entry["path"] = path
        entry["frame"] = ttk.Frame(self.scrollable_panel.scrollwindow,
                                   padding=(6),
                                   style="mouseover.TFrame")
        entry["lname"] = ttk.Label(entry["frame"], text=basename(path), style="mouseover.TLabel")
        entry["lpath"] = ttk.Label(entry["frame"], text=path, style="mouseover.TLabel")

        entry["frame"].grid(column=0, row=len(self.entries), sticky="enw")
        entry["lname"].grid(column=0, row=0, sticky="nw")
        entry["lpath"].grid(column=0, row=1, sticky="nw")

        self.entries.append(entry)
        return

    def grid(self, *args, **kwargs):
        self.scrollable_panel.grid(*args, **kwargs)


if __name__ == '__main__':
    main(__doc__)
