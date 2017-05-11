"""GUI for PCPPScraper.



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
        self.root.title("PCPPScraper GUI {0}".format(VERSION))
        # Content
        self.title_zone = Title_Panel(self)
        self.right_bar = ttk.Separator(self, orient="vertical")
        self.side_options = Side_Options(self)
        self.search_box = Search_Box(self)
        self.results_panel = Results_Panel(self, borderwidth=2, relief="sunken")
        self.search_filters = Search_Filter_Panel(self)
        #self.left_bar = ttk.Separator(self, orient="vertical")
        # Packing
        self.title_zone.grid(column=8, row=0)
        self.right_bar.grid(column=9, row=2, rowspan=3, sticky="ns", padx=(6), pady=(3))
        self.side_options.grid(column=10, row=2, rowspan=3, sticky="n")
        self.search_box.grid(column=8, row=1, pady=(9,3))
        self.results_panel.grid(column=8, row=2)
        self.search_filters.grid(column=6, row=2, sticky="n", padx=(0,6), pady=(3))
        #self.left_bar.grid(column=7, row=2, sticky="ns", padx=(6), pady=(3))


    def add_filter(self):
        print("add filter would go here.")

    def run_filters(self):
        print("run filters would go here.")

    def clear_results(self):
        self.results_panel.clear()

    def show_all(self):
        self.results_panel.fill()


class Title_Panel(ttk.Frame):
    """Title panel."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)
        self.text = ttk.Label(self, text="PCPPScraper\nWriten by mtech0")
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

        self.tree = ttk.Treeview(self, column=("OfferID"), height=20)
        self.tree.heading("#0", text="Name")
        self.tree.column('#0', width=500)
        self.tree.heading("OfferID", text="Offer ID")
        # Packing
        self.tree.pack()
        self.fill()

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def fill(self):
        results = self.root.db_handler.query("SELECT Name, OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID WHERE Active=1")
        for item in results:
            self.tree.insert('', 'end', text=item[0], values=(item[1]))


class Side_Options(ttk.Frame):
    """Side option bar."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.update = ttk.Button(self, text="Update", command=self.root.db_handler.updater)
        self.add_filter = ttk.Button(self, text="Add Filter", command=self.root.add_filter)
        self.run_filter = ttk.Button(self, text="Run Filters", command=self.root.run_filters)
        self.clear_db = ttk.Button(self, text="Clean DB", command=self.root.db_handler.clean_up())
        self.show_all = ttk.Button(self, text="Show All", command=self.root.show_all)

        self.clear = ttk.Button(self, text="Clear", command=self.root.clear_results)
        self.exit = ttk.Button(self, text="Exit", command=self.root.quit)

        # Packing
        self.update.grid(row=0, pady=(3,0))
        self.add_filter.grid(row=2, pady=(3,0))
        self.clear_db.grid(row=3, pady=(3,0))
        self.show_all.grid(row=1, pady=(3,0))

        self.clear.grid(row=98, pady=(3,0))
        self.exit.grid(row=99, pady=(3,0), sticky="s")

class Search_Filter_Panel(ttk.Frame):
    """Search Filter Panel and elements."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        super().__init__(self.root, *args, **kwargs)

        self.text = ttk.Label(self, text="Search Filters\nwill go here")

        # Packing
        self.text.grid(column=0, row=0)


def ubp():
    print("Update button pressed")
def cbp():
    print("Clear button pressed")

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
