"""GUI for PCPPScrapper.



Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""

AUTHOR = "mtech0 | https://github.com/mtech0"
LICENSE = "GNU-GPLv3 | https://www.gnu.org/licenses/gpl.txt"
VERSION = "0.0.0"
STATUS = "Development"
URL = ""
__doc__ = __doc__.format(AUTHOR, VERSION, STATUS, LICENSE, URL)

from tkinter import *
from tkinter.ttk import *

class App(Frame):
    """The GUI."""

    def __init__(self):
        self.root = Tk()
        super().__init__(self.root)
        self.pack()

        # setup
        # window
        self.root.title("PCPPScrapper GUI {0}".format(VERSION))

        # Content
        self.frame = Frame(self.root)
        self.frame["padding"] = (12, 3, 12, 3)
        self.frame.pack()
        self.main_text = Label(self.frame, text="PCPPScrapper Interface...").pack()




app = App()
app.mainloop()
