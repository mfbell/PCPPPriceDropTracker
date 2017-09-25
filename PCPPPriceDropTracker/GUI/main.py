"""PCPPPriceDropTracker main GUI widgets."""

import tkinter as tk
from tkinter import ttk
from logging import getLogger

from tools import PD, config
from DBHandler import DBHandler
from .customWidgets import Panel, MessageBox, ScrollablePanel
from .dialogs import OpenDB, CreateDB


__all__ = ["GUI"]

class GUI(tk.Tk):

    def __init__(self):
        getLogger(__name__ + ".GUI.__init__").debug("GUI initialized.")
        super().__init__()
        self.withdraw()
        self.toplevel = None

    def launch(self, *a):
        logger = getLogger(__name__ + ".GUI.launch")
        if self.toplevel is None:
            logger.debug("GUI launch called, no existing: launching.")
            self.toplevel = tk.Toplevel(self)
            self.toplevel.protocol('WM_DELETE_WINDOW', self.close)
            self.main = Main(self.toplevel, self.close)
        else:
            logger.debug("GUI launch called, existing: bring to front.")
            self.toplevel.attributes('-topmost', True)
            self.toplevel.attributes('-topmost', False)

    def close(self, *a):
        logger = getLogger(__name__ + ".GUI.close")
        if self.toplevel is not None:
            logger.debug("GUI close called, existing: closing.")
            self.toplevel.destroy()
            self.toplevel = None
        else:
            logger.debug("GUI close called, no existing: pass")

    def destroy(self, *a):
        getLogger(__name__ + ".GUI.quit").debug("GUI quitting.")
        super().destroy()
        self.toplevel = None


class Main(Panel):
    """The main window."""

    def __init__(self, master, close):
        """Initialization."""
        logger = getLogger(__name__ + ".Main.__init__")
        logger.debug("GUI main window initalization.")
        super().__init__(master, padding = (12, 6, 6, 6))
        self.close = close
        self.grid()
        self.master.withdraw()
        OpenDB(resent = config["databases"]["resent"], callback = self.finish_setup)

    def finish_setup(self, path, *a, **kw):
        logger = getLogger(__name__ + ".Main.finish_setup")
        logger.debug("Finish setup...")
        self.db_handler = DBHandler(path = path, country = "uk")
        # Window setup
        self.master.title("PCPPPriceDropTracker")
        self.master.option_add('*tearOff', False)
            # ColName:[DisplayName, width (-1: Default)]
        self.columns = {"Name": ["Name", 450],
                             "Normal_Price": ["Normal Price", 100],
                             "Offer_Price": ["Offer Price", 100],
                             "Flames": ["Flames", 75],
                             "Active": ["Active", 100]}
        # Content
        self.title_panel = TitlePanel(self)
        self.right_sep = ttk.Separator(self, orient = "vertical")
        self.results_panel = ResultsPanel(self, borderwidth = 2, relief = "sunken",
                                          columns = self.columns,
                                          searchdb = self.db_handler.search,
                                          get_search_filters = self.get_search_filters)
        #
        self.search_filters = SearchFilterPanel(self,
                                                max_height = self.get_main_row_height,
                                                min_height = self.get_main_row_height,
                                                max_width = 200,
                                                padding = (0, 0, 6, 0))
        self.search_box = SearchBox(master = self,
                                     showall = self.results_panel.show_all_w_filters,
                                     search = self.db_handler.search,
                                     columns = self.columns,
                                     get_search_filters = self.search_filters.get,
                                     clear_results = self.results_panel.clear,
                                     add_results = self.results_panel.add)

        self.results_panel.grid(column = 8, row = 2, sticky = "new")
        self.menu_bar = MenuBar(self)
        self.side_options = SideOptions(self, self.close)
        # Packing
        self.title_panel.grid(column = 8, row = 0)
        #self.right_sep.grid(column = 9, row = 2, rowspan = 3, sticky = "ns", padx = 6, pady = 6)
        self.side_options.grid(column = 10, row = 2, rowspan = 3, sticky = "nwe")
        self.search_box.grid(column = 8, row = 1, pady = (9, 3))
        self.search_filters.grid(column = 6, row = 2, sticky = "nwse")
        self.master.deiconify()
        logger.debug("App setup complete.")
        logger.info("PCPPPriceDropTracker GUI is running")
        return

    def add_filter(self):
        print("add filter would go here.")
        return

    def run_filters(self):
        print("run filters would go here.")
        return

    def get_main_row_height(self):
        a = self.results_panel.winfo_height()
        getLogger(__name__ + ".Main.get_main_row_height").debug("Height is "+str(a))
        if a is 0:
            return 32
        else:
            return a

    def mainloop(self, *args, **kw):
        self.master.mainloop(*args, **kw)

    def quit(self):
        self.master.quit()

    def get_search_filters(self):
        try:
            a = self.search_filters.get()
        except AttributeError as e:
            getLogger(__name__ + ".Main.get_search_filters").exception(e)
            return "Active = 1"
        return a


class TitlePanel(Panel):
    """Title panel."""

    def __init__(self, master, *args, **kwargs):
        """Initialization. Args as of Panel."""
        logger = getLogger(__name__ + ".TitlePanel.__init__")
        logger.debug("TitlePanel initalization.")
        super().__init__(master, *args, **kwargs)
        self.text = ttk.Label(self, text = "PCPPPriceDropTracker - writen by mtech0")

        self.text.grid(row = 0)
        logger.debug("TitlePanel setup complete.")
        return


class SearchBox(Panel):
    """Search Box Panel."""

    def __init__(self, master, showall, search, columns, get_search_filters,
                 clear_results, add_results, *args, **kwargs):
        """Initialization. Args as of Panel.

        Plus:
        showall - Function to show all entries with filters | Function
            / ResultsPanel.show_all_w_filters
        search - Database handler search function | Function
            / DBHandler.search
        columns - Show columns dictionary | Dictionary
            / columns
        get_search_filters - Get all search filters to pass to dbhandler search
                                | Function
            / SearchFilterPanel.get
        clear_results - Function to clear results | Function
            / ResultsPanel.clear
        add_results - Function to add results | Function
            / ResultsPanel.add

        """
        logger = getLogger(__name__ + ".SearchBox.__init__")
        logger.debug("SearchBox initalization.")
        super().__init__(master, *args, **kwargs)
        self.showall = showall
        self.searchdb = search
        self.columns = columns
        self.get_search_filters = get_search_filters
        self.clear_results = clear_results
        self.add_results = add_results
        self.search_text = tk.StringVar()
        self.search_text.trace("w", self.search)
        self.SearchBox = ttk.Entry(self, textvariable = self.search_text, width = 100)
        self.search_button = ttk.Button(self, text = "Search", command = self.external_open)
        # Packing
        self.SearchBox.grid(column = 0, row = 0)
        self.search_button.grid(column = 1, row = 0)
        logger.debug("SearchBox setup complete.")
        return

    def search(self, *args, **kwargs):
        """Search for offer in database and display results."""
        logger = getLogger(__name__ + ".SearchBox.search")
        string = self.search_text.get()
        logger.debug("All to search with string: '%s'.", string)
        if not string or string == "":
            logger.debug("No value in string, showing all with filters applied.")
            return self.showall()
        results = self.searchdb(self.columns, self.get_search_filters(), string)
        if not results:
            logger.debug("No result from search query.")
            return
        elif "external" in kwargs and kwargs["external"]:
            logger.debug("Search results been opened external.")
            ResultsPanel(tk.Toplevel(self), self.columns, self.searchdb, self.search_text.get(), self.get_search_filters, string, results)
            return
        self.clear_results()
        logger.debug("Search results sent to be added to results panel.")
        return self.add_results(results)

    def external_open(self):
        """Search external open rapper method."""
        getLogger(__name__ + ".SearchBox.external_open").debug("External open called.")
        return self.search(external = True)


class ResultsPanel(Panel):
    """Results Panel."""

    def __init__(self, master, columns, searchdb, get_search_filters, search = None, open_results = None, *args, **kwargs):
        """Initialization. Args as of Panel.

        Plus:
        columns - Columns to show | Dictionary
            / master.columns
        searchdb - Database handler search function | Function
            / DBHandler.search
        get_search_filters - Get search filters for search call | Function
            / SearchFilterPanel.get
        open_results - Open data from this | [search data, ...]
            / I have only tested using this to open stuff in new window.
            / master must be tk.Tk() for this as it also sets a title to master.


        """
        logger = getLogger(__name__ + ".ResultsPanel.__init__")
        logger.debug("ResultsPanel initalization.")
        self.columns = columns
        self.searchdb = searchdb
        self.get_search_filters = get_search_filters
        self.search = search
        self.rows = 20
        super().__init__(master, *args, **kwargs)
        self.tree = ttk.Treeview(self, column = ([col for col in self.columns][1:]), height = self.rows)
        first = True
        for col in self.columns:
            if first:
                col_ = '#0'
                first = False
            else:
                col_ = col
            self.tree.heading(col_, text = self.columns[col][0])
            if not self.columns[col][1] == -1:
                self.tree.column(col_, width = self.columns[col][1])
        self.ybar = ttk.Scrollbar(self, orient = "vertical", command = self.tree.yview)
        self.tree['yscrollcommand'] = self.ybar.set
        # Packing
        self.tree.grid(column = 0, row = 0)
        self.ybar.grid(column = 1, row = 0, sticky = "ns")
        if open_results:
            self.master.title("Search Results: '{0}'".format(self.search))
            self.grid()
            self.add(data)
        else:
            self.show_all_w_filters() # Only done on first creation.
        logger.debug("ResultsPanel setup complete.")
        return

    def clear(self):
        """Clear the Treeview/results."""
        getLogger(__name__ + ".ResultsPanel.clear").debug("Clear panel")
        return self.tree.delete(*self.tree.get_children())

    def show_all_w_filters(self):
        """Show all <conditions -only active=1 at the moment> offers."""
        getLogger(__name__ + ".ResultsPanel.show_all_w_filters").debug("Showing all entries with filters applied to results panel.")
        self.clear()
        results = self.searchdb(self.columns, self.get_search_filters(), None)
        return self.add(results)

    def add(self, data):
        """Add data to Treeview/results.

        data - Results to add | [[col1, col2, ...], ...] or tuplised
        """
        getLogger(__name__ + ".ResultsPanel.add").debug("Adding results to Treeview")
        for item in data:
            self.tree.insert('', "end", text = item[0], values = (item[1:]))
        return

    def input(self, data):
        self.clear()
        self.add(data)


class SideOptions(Panel):
    """Side options bar."""

    def __init__(self, master, close, *args, **kwargs):
        """Initialization. Args as of Panel."""
        logger = getLogger(__name__ + ".SideOptions.__init__")
        logger.debug("SideOptions initialization.")
        super().__init__(master, *args, **kwargs)

        self.update = ttk.Button(self, text = "Update", command = lambda: UpdateHanlder(self.master))
        self.add_filter = ttk.Button(self, text = "Add Filter", command = self.master.add_filter)
        self.run_filter = ttk.Button(self, text = "Run Filters", command = self.master.run_filters)
        self.show_all = ttk.Button(self, text = "Show All", command = self.master.results_panel.show_all_w_filters)

        self.clear = ttk.Button(self, text = "Clear", command = self.master.results_panel.clear)
        self.exit = ttk.Button(self, text = "Exit", command = close)
        # Packing
        self.update.grid(row = 0, pady = (3, 0))
        self.show_all.grid(row = 1, pady = (3, 0))
        self.add_filter.grid(row = 2, pady = (3, 0))
        self.run_filter.grid(row = 3, pady = (3, 0))

        self.clear.grid(row = 98, pady = (3, 0))
        self.exit.grid(row = 99, pady = (3, 0), sticky = "s")
        logger.debug("SideOptions setup complete.")
        return


class SearchFilterPanel(ScrollablePanel):
    """Search Filter Panel and elements."""

    def __init__(self, master, *args, **kwargs):
        """Initialization. Args as of Panel."""
        logger = getLogger(__name__ + ".SearchFilterPanel.__init__")
        logger.debug("SearchFilterPanel initialization.")
        super().__init__(master, *args, **kwargs)
        # Build filters here:
        win = self.scrollwindow
        win.title = ttk.Label(win, text = "Search filters:\nComing soon.")
        win.title.grid(column = 0, row = 0)
        logger.debug("SearchFilterPanel setup complete.")
        return

    def get(self):
        """Get a formated filter string."""
        logger = getLogger(__name__ + ".SearchFilterPanel.get")
        logger.debug("SearchFilterPanel.get called, returning filters")
        logger.warning("Filters not supported yet, only Active = 1. To be added in future update.")
        return "Active = 1"


class StatusBar(Panel):
    """Bottom debug bar. Needs to be rewriten into own frame."""

    def __init__(self, master, *args, **kwargs):
        """Initialization. Args as of Panel."""
        logger = getLogger(__name__ + ".StatusBar.__init__")
        logger.debug("StatusBar initialization.")
        super().__init__(master, *args, **kwargs)

        self.top_line = ttk.Separator(self.master, orient = "horizontal")
        self.name = ttk.Label(self.master, text = "PCPPScraper")
        self.bar0 = ttk.Separator(self.master, orient = "vertical")
        self.results_length = ttk.Label(self.master, text = "ALL")
        self.bar1 = ttk.Separator(self.master, orient = "vertical")
        self.country = ttk.Label(self.master, text = "UK") # needs to be dynamic to db.
        # Packing
        self.top_line.grid(column = 0, row = 95, columnspan = 100, sticky = "ew", pady = (6, 2))
        self.name.grid(column = 6, row = 96, sticky = "w")
        self.bar0.grid(column = 7, row = 96, sticky = "ns")
        self.results_length.grid(column = 8, row = 96, sticky = "w")
        self.bar1.grid(column = 9, row = 96, sticky = "ns")
        self.country.grid(column = 10, row = 96, sticky = "e")
        logger.debug("StatusBar setup complete.")
        return


class MenuBar():
    """Menu bar class."""

    def __init__(self, master):
        """Initialization."""
        logger = getLogger(__name__ + ".MenuBar.__init__")
        logger.debug("MenuBar initialization.")
        self.master = master
        self.menu = tk.Menu(self.master.master)
        # Could not get making this class a menu object working.
        self.master.master["menu"] = self.menu

        # Drop downs
        self.file_menu = tk.Menu(self.menu)
        self.file_menu.add_command(label = "Open database", command = mp)
        self.file_menu.add_command(label = "Close", command = mp)
        #
        self.edit_menu = tk.Menu(self.menu)
        self.edit_menu.add_command(label = "Change country", command = mp)
        self.edit_menu.add_command(label = "Another", command = mp)
        # On bar
        self.menu.add_cascade(menu = self.file_menu, label = 'File')
        self.menu.add_cascade(menu = self.edit_menu, label = 'Edit')
        self.menu.add_command(label = "Update", command = lambda: UpdateHanlder(self.master))
        logger.debug("MenuBar setup complete.")
        return


class UpdateHanlder():
    """Database updater handler."""

    def __init__(self, master):
        """Initialization."""
        logger = getLogger(__name__ + ".UpdateHanlder.__init__")
        logger.debug("UpdateHanlder initialization.")
        self.master = master
        self.create_popup()
        self.master.db_handler.updater(self.popup_updater)
        logger.debug("UpdateHanlder setup complete")
        return

    def create_popup(self):
        logger = getLogger(__name__ + ".UpdateHanlder.create_popup")
        logger.debug("Creating popup.")
        self.text = tk.StringVar()
        self.button = tk.StringVar()
        self.text.set("Updating local database...")
        self.button.set("Hide")
        self.msg_box = MessageBox(msg = self.text,
                                  buttons = {"1": [self.button, "WITHDRAW"]},
                                  title = "Updating",
                                  icon = ".\PCPPPriceDropTracker\imgs\info.png")
        logger.debug("Popup created.")
        return

    def popup_updater(self):
        logger = getLogger(__name__ + ".UpdateHanlder.popup_updater")
        logger.debug("popup_updater called")
        self.text.set("Updated local database")
        self.button.set("Close")
        self.msg_box.buttons["1"]["command"] = self.update_and_close
        self.msg_box.deiconify()
        self.msg_box.grab_set()
        logger.debug("Popup updated")
        return

    def update_and_close(self):
        getLogger(__name__ + ".UpdateHanlder.update_and_close").debug("Close and update pressed.")
        self.msg_box.destroy()
        self.master.search_box.search()
        return


def mp():
    """Placeholder functions."""
    return print("A menu button was pressed")

def main():
    """Main."""
    logger = getLogger(__name__ + ".main")
    logger.debug("Main called, calling and running App")
    app = App()
    app.mainloop()
    logger.debug("App closed.")
    return

def run_as_main():
    import log_setup
    log_setup.setup()
    getLogger(__name__).debug("Run as main.")
    main()

if __name__ == '__main__':
    run_as_main()
