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
from itertools import permutations
from DBHandler import Handler
from tools import Tools

class Panel(ttk.Frame, Tools):
    """Inherited class."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        Tools.__init__(self, *args, **kwargs)
        ttk.Frame.__init__(self, self.root, *self.args, **self.kwargs)

class App(Panel):
    """The main window."""

    def __init__(self, root=tk.Tk(), *args, **kwargs):
        if "db_handler" in kwargs:
            self.db_handler = kwargs["db_handler"]
            del(kwargs["db_handler"])
        else:
            self.db_handler = False
        if not "padding" in kwargs:
            kwargs["padding"] = (12, 6, 6, 6)
        #kwargs["debug"] = True # Override
        #kwargs["log"] = True # ^
        super().__init__(root, *args, **kwargs)
        self.pack()
        if not self.db_handler:
            self.db_handler = Handler(debug=self.debug)

        # Window setup
        self.root.title("PCPPScraper GUI {0}".format(VERSION))
        # Content
        self.title_zone = Title_Panel(self, debug=self.debug)
        self.right_bar = ttk.Separator(self, orient="vertical")
        self.side_options = Side_Options(self, debug=self.debug)
        self.search_box = Search_Box(self, debug=self.debug)
        self.results_panel = Results_Panel(self, borderwidth=2, relief="sunken", debug=self.debug)
        self.search_filters = Search_Filter_Panel(self, debug=self.debug)
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
        self.results_panel.show_all()


class Title_Panel(Panel):
    """Title panel."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.text = ttk.Label(self, text="PCPPScraper\nWriten by mtech0")
        # Packing
        self.text.grid(row=0)

class Search_Box(Panel):
    """Search Box."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.search_text = tk.StringVar()
        self.search_text.trace("w", self.search)
        self.search_box = ttk.Entry(self, textvariable=self.search_text, width=100)
        self.search_button = ttk.Button(self, text="Search", command=self.external_open)

        # Packing
        self.search_box.grid(column=0, row=0)
        self.search_button.grid(column=1, row=0)

    def search(self, *args, **kwargs):
        self.root.results_panel.clear()
        words = [word.strip() for word in self.search_text.get().split()]
        if not words:
            return self.root.show_all()
        orders = list(permutations(words))
        combinations = []
        for order in orders:
            combinations.append("%" + "%".join(order) + "%")
        results = self.root.db_handler.query("""SELECT Name, OfferID FROM Offers
                                                    JOIN Products ON Offers.ProductID = Products.ProductID
                                                WHERE Active=1 AND
                                                    (Name LIKE {0})""".format(" OR Name LIKE ".join("?" for _ in combinations)), combinations)
        if not results:
            return
        if "return_" in kwargs and kwargs["return_"] == True:
            return results
        self.root.results_panel.add(results)

    def external_open(self):
        Results_Panel(tk.Tk(), debug=self.debug, open_search_data=self.search(return_=True))
        self.search()

class Results_Panel(Panel):
    """Results panel."""

    def __init__(self, root, *args, **kwargs):
        data = None
        if "open_search_data" in kwargs:
            data = kwargs["open_search_data"]
            del(kwargs["open_search_data"])
        super().__init__(root, *args, **kwargs)

        self.tree = ttk.Treeview(self, column=("OfferID"), height=20)
        self.tree.heading("#0", text="Name")
        self.tree.column('#0', width=500)
        self.tree.heading("OfferID", text="Offer ID")
        # Packing
        self.tree.pack()

        if data:
            self.root.title("Search Results")
            self.pack()
            self.add(data)
        else:
            self.show_all()

    def clear(self):
        self.tree.delete(*self.tree.get_children())

    def show_all(self):
        self.clear()
        results = self.root.db_handler.query("SELECT Name, OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID WHERE Active=1")
        for item in results:
            self.tree.insert('', 'end', text=item[0], values=(item[1]))

    def add_by_id(self, ids):
        if isinstance(ids[0], tuple):
            wasIds = ids
            ids = []
            for id in wasIds:
                ids.append(id[0])
        results = self.root.db_handler.query("SELECT Name, OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID \
                                              WHERE OfferID in ({0})".format(", ".join("?" for _ in ids)), ids)
        for item in results:
            self.tree.insert('', "end", text=item[0], values=(item[1]))

    def add(self, data):
        for item in data:
            self.tree.insert('', "end", text=item[0], values=(item[1]))

class Side_Options(Panel):
    """Side option bar."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.update = ttk.Button(self, text="Update", command=self.root.db_handler.updater)
        self.add_filter = ttk.Button(self, text="Add Filter", command=self.root.add_filter)
        self.run_filter = ttk.Button(self, text="Run Filters", command=self.root.run_filters)
        self.clear_db = ttk.Button(self, text="Clean DB", command=self.root.db_handler.clean_up)
        self.show_all = ttk.Button(self, text="Show All", command=self.root.show_all)
        self.debug_status = tk.StringVar()
        self.debug_button = ttk.Button(self, textvariable=self.debug_status, command=self.debug_change)
        self.log_status = tk.StringVar()
        self.log_button = ttk.Button(self, textvariable=self.log_status, command=self.log_change)

        self.clear = ttk.Button(self, text="Clear", command=self.root.clear_results)
        self.exit = ttk.Button(self, text="Exit", command=self.root.quit)

        self.set_textvars()

        # Packing
        self.update.grid(row=0, pady=(3,0))
        self.add_filter.grid(row=2, pady=(3,0))
        self.clear_db.grid(row=3, pady=(3,0))
        self.show_all.grid(row=1, pady=(3,0))
        self.debug_button.grid(row=4, pady=(3,0))
        self.log_button.grid(row=5, pady=(3,0))

        self.clear.grid(row=98, pady=(3,0))
        self.exit.grid(row=99, pady=(3,0), sticky="s")

    def debug_change(self):
        if self.debug():
            self.debug(False)
        else:
            self.debug(True)
        self.set_textvars()

    def log_change(self):
        if self.debug(log="get"):
            self.debug(log=False)
        else:
            self.debug(log=True)
        self.set_textvars()

    def set_textvars(self):
        if self.debug():
            self.debug_status.set("Debugging")
        else:
            self.debug_status.set("Debug")
        if self.debug(log="get"):
            self.log_status.set("Logging")
        else:
            self.log_status.set("Log")


class Search_Filter_Panel(Panel):
    """Search Filter Panel and elements."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

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
