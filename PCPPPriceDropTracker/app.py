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
VERSION = "0.7.0"
STATUS = "Development"
URL = ""
__doc__ = __doc__.format(AUTHOR, VERSION, STATUS, LICENSE, URL)

import tkinter as tk
import tkinter.ttk as ttk
from .DBHandler import Handler
from .tools import Tools
from .customWidgets import Panel, MessageBox



class App(Panel):
    """The main window."""

    def __init__(self, root=tk.Tk(), *args, **kwargs):
        """Initialization.

        Args as of Panel
        + kwargs:
        db_handler - Database handler object | object

        """
        if "db_handler" in kwargs:
            self.db_handler = kwargs["db_handler"]
            del(kwargs["db_handler"])
        else:
            self.db_handler = False
        if not "padding" in kwargs:
            kwargs["padding"] = (12, 6, 6, 6)
        super().__init__(root, *args, **kwargs)
        #self.debug(True)
        self.pack()
        if not self.db_handler:
            self.db_handler = Handler(debug=self.debug)

        # Window setup
        self.root.title("PCPPPriceDropTracker {0}".format(VERSION))
        self.root.option_add('*tearOff', False)
            # ColName:[DisplayName, width (-1=Default)]
        self.show_columns = {"Name":["Name", 450],
                             "Normal_Price":["Normal Price", -1],
                             "Offer_Price":["Offer Price", -1],
                             "Flames": ["Flames", 75],
                             "Active": ["Active", 100]
                             }
        # Content
        self.title_zone = Title_Panel(self, debug=self.debug)
        self.search_filters = Search_Filter_Panel(self, debug=self.debug)
        self.right_bar = ttk.Separator(self, orient="vertical")
        self.search_box = Search_Box(self, debug=self.debug)
        self.results_panel = Results_Panel(self, borderwidth=2, relief="sunken", debug=self.debug)
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
        self.status_bar.grid(column=0, row=99, columnspan=32, sticky="s")
        #self.left_bar.grid(column=7, row=2, sticky="ns", padx=(6), pady=(3))
        return None

    def add_filter(self):
        print("add filter would go here.")
        return None

    def run_filters(self):
        print("run filters would go here.")
        return None


class Title_Panel(Panel):
    """Title panel."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel."""
        super().__init__(root, *args, **kwargs)
        self.text = ttk.Label(self, text="PCPPScraper\nWriten by mtech0")
        # Packing
        self.text.grid(row=0)
        return None


class Search_Box(Panel):
    """Search Box Panel."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel."""
        super().__init__(root, *args, **kwargs)
        self.search_text = tk.StringVar()
        self.search_text.trace("w", self.search)
        self.search_box = ttk.Entry(self, textvariable=self.search_text, width=100)
        self.search_button = ttk.Button(self, text="Search", command=self.external_open)
        # Packing
        self.search_box.grid(column=0, row=0)
        self.search_button.grid(column=1, row=0)
        return None

    def search(self, *args, **kwargs):
        """Search for offer in database and display results."""
        self.debug_msg("Search in Search_Box called")
        string = self.search_text.get()
        self.debug_msg("Search string is: "+string)
        if not string or string == "":
            self.debug_msg("Nothing in string, showing all with filters")
            return self.root.results_panel.show_all_w_filters()
        results = self.root.db_handler.search(self.root.show_columns, self.root.search_filters.get(), string)
        if not results:
            return None
        elif "external" in kwargs and kwargs["external"]:
            Results_Panel(tk.Tk(), debug=self.debug, open_search_data=[self.root.show_columns, self.search_text.get(), results])
            return None
        self.root.results_panel.clear()
        return self.root.results_panel.add(results)

    def external_open(self):
        """Search external open rapper method."""
        return self.search(external=True)


class Results_Panel(Panel):
    """Results Panel."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel.

        + kwargs
        open_search_data - Open data from this | [show_columns, search_text, [search data, ...]]
            / I have only tested using this to open stuff in new window.
            / root must be tk.Tk() for this as it also sets a title to root.

        """
        data = None
        if "open_search_data" in kwargs:
            self.columns, self.search_text, data = kwargs["open_search_data"]
            del(kwargs["open_search_data"])
        super().__init__(root, *args, **kwargs)
        if not data:
            self.columns = self.root.show_columns
        self.tree = ttk.Treeview(self, column=([col for col in self.columns][1:]), height=25)
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
            self.show_all_w_filters() # Remember this is done on first creation.
        return None

    def clear(self):
        """Clear the Treeview/results."""
        return self.tree.delete(*self.tree.get_children())

    def show_all_w_filters(self):
        """Show all <conditions -only active=1 at the moment> offers."""
        self.clear()
        results = self.root.db_handler.search(self.root.show_columns, self.root.search_filters.get(), None)
        return self.add(results)

    def add_by_id(self, ids):
        """Add offer to the Treeview by OfferID.

        ids - A list/tuple of OfferIDs | list/tuple
            / Can be [(id,), ...] as got from query.
        """
        if isinstance(ids[0], tuple):
            wasIds = ids
            ids = [id[0] for id in wasIds]
        results = self.root.db_handler.search(self.root.show_columns, "(OfferID = {0})".format(" OR OfferID = ".join("?")), None, ids)
        return self.add(results)

    def add(self, data):
        """Add data to Treeview/results.

        data - Results to add | [[col1, col2, ...], ...] or tuplised
        """
        for item in data:
            self.tree.insert('', "end", text=item[0], values=(item[1:]))
        return None


class Side_Options(Panel):
    """Side options bar."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel."""
        super().__init__(root, *args, **kwargs)

        self.update = ttk.Button(self, text="Update", command=lambda: Update_Hanlder(self.root))
        self.add_filter = ttk.Button(self, text="Add Filter", command=self.root.add_filter)
        self.run_filter = ttk.Button(self, text="Run Filters", command=self.root.run_filters)
        self.clear_db = ttk.Button(self, text="Clean DB", command=self.root.db_handler.clean_up)
        self.show_all = ttk.Button(self, text="Show All", command=self.root.results_panel.show_all_w_filters)
        self.debug_status = tk.StringVar()
        self.debug_button = ttk.Button(self, textvariable=self.debug_status, command=self.debug_change)
        self.log_status = tk.StringVar()
        self.log_button = ttk.Button(self, textvariable=self.log_status, command=self.log_change)

        self.clear = ttk.Button(self, text="Clear", command=self.root.results_panel.clear)
        self.exit = ttk.Button(self, text="Exit", command=self.root.quit)

        self.set_textvars()

        # Packing
        self.update.grid(row=0, pady=(3,0))
        self.show_all.grid(row=1, pady=(3,0))
        self.add_filter.grid(row=2, pady=(3,0))
        self.run_filter.grid(row=3, pady=(3,0))
        self.clear_db.grid(row=4, pady=(3,0))
        self.debug_button.grid(row=5, pady=(3,0))
        self.log_button.grid(row=6, pady=(3,0))

        self.clear.grid(row=98, pady=(3,0))
        self.exit.grid(row=99, pady=(3,0), sticky="s")
        return None

    def debug_change(self):
        """Change debug status and update GUI."""
        if self.debug():
            self.debug(False)
        else:
            self.debug(True)
        return self.set_textvars()

    def log_change(self):
        """Change log status and update GUI."""
        if self.debug(log="get"):
            self.debug(log=False)
        else:
            self.debug(log=True)
        return self.set_textvars()

    def set_textvars(self):
        """Update GUI to match debug and log status."""
        if self.debug():
            self.debug_status.set("Debugging")
        else:
            self.debug_status.set("Debug")
        if self.debug(log="get"):
            self.log_status.set("Logging")
        else:
            self.log_status.set("Log")
        return None


class Search_Filter_Panel(Panel):
    """Search Filter Panel and elements."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel."""
        super().__init__(root, *args, **kwargs)

        self.text = ttk.Label(self, text="Search Filters\nwill go here")
        # Packing
        self.text.grid(column=0, row=0)
        return None

    def get(self):
        """Get a formated filter string."""
        return "Active = 1"


class Status_Bar(Panel):
    """Bottom info bar. Needs to be rewriten into own frame."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Panel."""
        super().__init__(root, *args, **kwargs)

        self.top_line = ttk.Separator(self.root, orient="horizontal")
        self.name = ttk.Label(self.root, text="PCPPScraper")
        self.bar0 = ttk.Separator(self.root, orient="vertical")
        self.results_length = ttk.Label(self.root, text="ALL")
        self.bar1 = ttk.Separator(self.root, orient="vertical")
        self.country = ttk.Label(self.root, text="UK") # needs to be dynamic to db.
        # Packing
        self.top_line.grid(column=0, row=95, columnspan=100, sticky="ew", pady=(6,2))
        self.name.grid(column=6, row=96, sticky="w")
        self.bar0.grid(column=7, row=96, sticky="ns")
        self.results_length.grid(column=8, row=96, sticky="w")
        self.bar1.grid(column=9, row=96, sticky="ns")
        self.country.grid(column=10, row=96, sticky="e")
        return None


class Menu_Bar(Tools):
    """Menu bar class."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Args as of Tools."""
        self.root = root
        Tools.__init__(self, *args, **kwargs)
        self.menu = tk.Menu(self.root.root, *args, **kwargs)
        # Could not get making this class a menu object working.
        self.root.root["menu"] = self.menu

        # Drop downs
        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label="Open...", command=mp)
        self.file_menu.add_command(label="Close.", command=mp)
        #
        self.edit_menu = tk.Menu(self.menu)
        self.edit_menu.add_command(label="Change country", command=mp)
        self.edit_menu.add_command(label="Another", command=mp)
        # On bar
        self.menu.add_cascade(menu=self.file_menu, label='File')
        self.menu.add_cascade(menu=self.edit_menu, label='Edit')
        self.menu.add_command(label="Update", command=lambda: Update_Hanlder(self.root))
        return None


class Update_Hanlder(Tools):
    """Database updater handler."""

    def __init__(self, root):
        """Initialization."""
        self.root = root
        self.create_popup()
        self.root.db_handler.updater(self.popup_updater)
        return None

    def create_popup(self):
        self.text = tk.StringVar()
        self.button = tk.StringVar()
        self.text.set("Updating local database...")
        self.button.set("Hide")
        self.msg_box = MessageBox(msg=self.text,
                                  buttons={"1":[self.button, "WITHDRAW"]},
                                  title="Updating",
                                  icon=".\imgs\info_icon.png")
        return None

    def popup_updater(self):
        self.text.set("Updated local database")
        self.button.set("Close")
        self.msg_box.buttons["1"]["command"] = self.update_and_close
        self.msg_box.deiconify()
        return None

    def update_and_close(self):
        self.msg_box.destroy()
        self.root.search_box.search()
        return None


def mp():
    """Placeholder functions."""
    return print("A menu button was pressed")

def main():
    """"""
    app = App()
    app.mainloop()
    return None

if __name__ == '__main__':
    main()
