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

import tkinter as tk
import tkinter.ttk as ttk

class App(ttk.Frame):
    """The main window."""

    def __init__(self, root=tk.Tk()):
        self.root = root
        super().__init__(self.root, padding=(12, 6, 6, 6))
        self.pack()

        # Window setup
        self.root.title("PCPPScrapper GUI {0}".format(VERSION))
        # Content
        self.main = Main_Panel(self, padding=(0, 0, 3, 0))
        self.main.grid(column=0, row=1)
        self.left = Side_Options(self, padding=(3, 0, 0, 0))
        self.left.grid(column=1, row=1)
        # Packing


class Main_Panel(ttk.Frame):
    """Main panel."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.text = ttk.Label(self, text="This is the main bar.\nThere is some text.\nIt is me :)")

        # Packing
        self.text.pack()


class Side_Options(ttk.Frame):
    """Side option bar."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.update = ttk.Button(self, text="Update", command=ubp)
        self.clear = ttk.Button(self, text="Clear", command=cbp)
        self.exit = ttk.Button(self, text="Exit", command=self.root.quit)

        # Packing
        self.update.grid(row=0)
        self.clear.grid(row=1)
        self.exit.grid(row=2)


def ubp():
    print("Update button pressed")
def cbp():
    print("Clear button pressed")

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
