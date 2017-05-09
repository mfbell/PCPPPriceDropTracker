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
from DBHandler import Handler

class App(ttk.Frame):
    """The main window."""

    def __init__(self, root=tk.Tk(), db_handler=Handler()):
        self.root = root
        super().__init__(self.root, padding=(12, 6, 6, 6))
        self.pack()
        self.db_handler = db_handler

        # Window setup
        self.root.title("PCPPScrapper GUI {0}".format(VERSION))
        # Content
        self.main = Title_Panel(self)
        self.sep = ttk.Separator(self, orient="vertical")
        self.left = Side_Options(self)
        self.search_box = Search_Box(self)
        self.results_panel = Results_Panel(self, borderwidth=2, relief="sunken")
        # Packing
        self.main.grid(column=0, row=0)
        self.sep.grid(column=1, row=0, rowspan=3, sticky="ns", padx=(6), pady=(3))
        self.left.grid(column=2, row=0, rowspan=3, sticky="n")
        self.search_box.grid(column=0, row=1, pady=(9,3))
        self.results_panel.grid(column=0, row=2)


    def add_filter(self):
        print("add filter would go here.")

    def run_filters(self):
        print("run filters would go here.")


class Title_Panel(ttk.Frame):
    """Title panel."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)
        self.text = ttk.Label(self, text="PCPPScrapper\nWriten by mtech0")
        # Packing
        self.text.grid(row=0)

class Search_Box(ttk.Frame):
    """Search Box."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)
        self.search_text = tk.StringVar()
        self.search_box = ttk.Entry(self, textvariable=self.search_text)
        self.search_button = ttk.Button(self, text="Search")

        # Packing
        self.search_box.grid(column=0, row=0)
        self.search_button.grid(column=1, row=0)

class Results_Panel(ttk.Frame):
    """Results panel."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)
        self.text = ttk.Label(self, text="Results will go here...", padding=(100,200,100,200))
        # Packing
        self.text.pack()


class Side_Options(ttk.Frame):
    """Side option bar."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.update = ttk.Button(self, text="Update", command=self.root.db_handler.updater)
        self.add_filter = ttk.Button(self, text="Add Filter", command=self.root.add_filter)
        self.run_filter = ttk.Button(self, text="Run Filters", command=self.root.run_filters)
        self.clear_db = ttk.Button(self, text="Clean DB", command=self.root.db_handler.clean_up())

        self.clear = ttk.Button(self, text="Clear", command=cbp)
        self.exit = ttk.Button(self, text="Exit", command=self.root.quit)

        # Packing
        self.update.grid(row=0, pady=(3,0))
        self.add_filter.grid(row=1, pady=(3,0))
        self.clear_db.grid(row=2, pady=(3,0))

        self.clear.grid(row=98, pady=(3,0))
        self.exit.grid(row=99, pady=(3,0), sticky="s")


def ubp():
    print("Update button pressed")
def cbp():
    print("Clear button pressed")

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
