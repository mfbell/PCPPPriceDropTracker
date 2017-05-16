"""Interface and control for PCPPPriceDropTracker.

Including the GUI, GUI Tools and other stuff.

Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""

AUTHOR = "mtech0 | https://github.com/mtech0"
LICENSE = "GNU-GPLv3 | https://www.gnu.org/licenses/gpl.txt"
VERSION = "0.6.0"
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
        super().__init__(root, *args, **kwargs)
        self.pack()
        if not self.db_handler:
            self.db_handler = Handler(debug=self.debug)

        # Window setup
        self.root.title("PCPPScraper GUI {0}".format(VERSION))
        self.root.option_add('*tearOff', False)
            # ColName:[DisplayName, width (-1=Default)]
        self.show_columns = {"Name":["Name", 500], "OfferID":["OfferID", -1]}
        # Content
        self.title_zone = Title_Panel(self, debug=self.debug)
        self.right_bar = ttk.Separator(self, orient="vertical")
        self.search_box = Search_Box(self, debug=self.debug)
        self.results_panel = Results_Panel(self, borderwidth=2, relief="sunken", debug=self.debug)
        self.search_filters = Search_Filter_Panel(self, debug=self.debug)
        self.status_bar = Status_Bar(self, debug=self.debug)
        self.menu_bar = Menu_Bar(self)
        self.side_options = Side_Options(self, debug=self.debug)
        #self.left_bar = ttk.Separator(self, orient="vertical")
        # Packing
        self.title_zone.grid(column=8, row=0)
        self.right_bar.grid(column=9, row=2, rowspan=3, sticky="ns", padx=(6), pady=(3))
        self.side_options.grid(column=10, row=2, rowspan=3, sticky="n")
        self.search_box.grid(column=8, row=1, pady=(9,3))
        self.results_panel.grid(column=8, row=2)
        self.search_filters.grid(column=6, row=2, sticky="n", padx=(0,6), pady=(3))
        self.status_bar.grid(column=0, row=99, columnspan=32)
        #self.left_bar.grid(column=7, row=2, sticky="ns", padx=(6), pady=(3))

    def add_filter(self):
        print("add filter would go here.")

    def run_filters(self):
        print("run filters would go here.")


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
        results = []
        if len(words) > 6:
            results.append(("Possible search combinations exceeds SQLite expression limit. Using linear search.", "ErrorMessage"))
            words = ["%".join(word for word in words)]
        self.debug_msg("Words: {0}".format(words))
        if not words:
            results = self.get_all()
        else:
            combinations = ["%" + "%".join(order) + "%" for order in list(permutations(words))]
            db_results = self.root.db_handler.query("""SELECT {0} FROM Offers
                                                           JOIN Products ON Offers.ProductID = Products.ProductID
                                                       WHERE Active=1 AND
                                                           (Name LIKE {1})""".format(", ".join(self.root.show_columns),
                                                                                     " OR Name LIKE ".join("?" for _ in combinations)),
                                                    combinations)
            results += db_results
        if not results:
            return
        elif "external" in kwargs and kwargs["external"] == True:
            Results_Panel(tk.Tk(), debug=self.debug, open_search_data=[self.root.show_columns, self.search_text.get(), results])
            return self.search()
        self.root.results_panel.add(results)

    def external_open(self):
        self.search(external=True)

    def get_all(self):
        return self.root.db_handler.query("SELECT Name, OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID WHERE Active=1")

class Results_Panel(Panel):
    """Results panel."""

    def __init__(self, root, *args, **kwargs):
        data= None
        if "open_search_data" in kwargs:
            self.columns, self.search_text, data = kwargs["open_search_data"]
            del(kwargs["open_search_data"])
        super().__init__(root, *args, **kwargs)
        if not data:
            self.columns = self.root.show_columns
        self.tree = ttk.Treeview(self, column=([col for col in self.columns][1:]), height=20)
        first = True
        for col in self.columns:
            if first:
                col_ = '#0'
                first = False
            else:
                col_ = col
            self.tree.heading(col_, text=self.columns[col][0])
            if not self.columns[col][1] == -1:
                self.tree.column(col_, width=self.columns[col][1])
        self.ybar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree['yscrollcommand'] = self.ybar.set
        # Packing
        self.tree.grid(column=0, row=0)
        self.ybar.grid(column=1, row=0, sticky="ns")

        if data:
            self.root.title("Search Results: '{0}'".format(self.search_text))
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
        self.show_all = ttk.Button(self, text="Show All", command=self.root.results_panel.show_all())
        self.debug_status = tk.StringVar()
        self.debug_button = ttk.Button(self, textvariable=self.debug_status, command=self.debug_change)
        self.log_status = tk.StringVar()
        self.log_button = ttk.Button(self, textvariable=self.log_status, command=self.log_change)

        self.clear = ttk.Button(self, text="Clear", command=self.root.results_panel.clear)
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


class Status_Bar(Panel):
    """Bottom info bar."""

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.top_line = ttk.Separator(self.root, orient="horizontal")
        self.name = ttk.Label(self.root, text="PCPPScraper")
        self.bar0 = ttk.Separator(self.root, orient="vertical")
        self.results_length = ttk.Label(self.root, text="ALL")
        self.bar1 = ttk.Separator(self.root, orient="vertical")
        self.country = ttk.Label(self.root, text="UK")

        # Packing
        self.top_line.grid(column=0, row=95, columnspan=100, sticky="ew", pady=(6,2))
        self.name.grid(column=6, row=96, sticky="w")
        self.bar0.grid(column=7, row=96, sticky="ns")
        self.results_length.grid(column=8, row=96, sticky="w")
        self.bar1.grid(column=9, row=96, sticky="ns")
        self.country.grid(column=10, row=96, sticky="e")


class Menu_Bar_(tk.Menu, Tools):
    """Menu bar class."""

    def __init__(self, root, *args, **kwargs):
        self.root = root
        self.win = tk.Toplevel(self.root)
        Tools.__init__(self, *args, **kwargs)
        tk.Menu.__init__(self.win, *args, **kwargs)
        self.win["menu"] = self

        # Content
        self.file_menu = tk.Menu(self)
        self.edit_menu = tk.Menu(self)

        # Packing
        self.add_cascade(menu=menu_file, label='File')
        self.add_cascade(menu=menu_edit, label='Edit')

class Menu_Bar(Tools):
    """Menu bar class."""
    def __init__(self, root, *args, **kwargs):
        self.root = root
        Tools.__init__(self, *args, **kwargs)
        self.menu = tk.Menu(self.root.root, *args, **kwargs)
        # Could not get making this class a menu object working.
        self.root.root["menu"] = self.menu

        # Content
        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label="Open...", command=mp)
        self.file_menu.add_command(label="Close.", command=mp)
        self.edit_menu = tk.Menu(self.menu)
        self.edit_menu.add_command(label="Change country", command=mp)
        self.edit_menu.add_command(label="Another", command=mp)

        # Packing
        self.menu.add_cascade(menu=self.file_menu, label='File')
        self.menu.add_cascade(menu=self.edit_menu, label='Edit')
        self.menu.add_command(label="Update", command=mp)


def mp():
    print("A menu button was pressed")

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
