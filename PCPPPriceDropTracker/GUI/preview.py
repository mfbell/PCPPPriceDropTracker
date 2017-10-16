class PreviewTabs():
    """Multi-tab database results preview."""

    def __init__(self, master, *args, **kwargs):
        """Initialization."""
        logger = getLogger(__name__ + "PreviewTabs.__init__")
        logger.debug("PreviewTabs initalization.")
        super().__init__(master, *args, **kwargs)

        self.tabs = ttk.Notepad(self)



        self.tabs.grid()

    def add(self):
        pass



class PreviewPanel():
    """Preview Panel."""

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
        logger = getLogger(__name__ + ".PreviewPanel.__init__")
        logger.debug("PreviewPanel initalization.")
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
        logger.debug("PreviewPanel setup complete.")
        return

    def clear(self):
        """Clear the Treeview/results."""
        getLogger(__name__ + ".PreviewPanel.clear").debug("Clear panel")
        return self.tree.delete(*self.tree.get_children())

    def show_all_w_filters(self):
        """Show all <conditions -only active=1 at the moment> offers."""
        getLogger(__name__ + ".PreviewPanel.show_all_w_filters").debug("Showing all entries with filters applied to results panel.")
        self.clear()
        results = self.searchdb(self.columns, self.get_search_filters(), None)
        return self.add(results)

    def add(self, data):
        """Add data to Treeview/results.

        data - Results to add | [[col1, col2, ...], ...] or tuplised
        """
        getLogger(__name__ + ".PreviewPanel.add").debug("Adding results to Treeview")
        for item in data:
            self.tree.insert('', "end", text = item[0], values = (item[1:]))
        return

    def input(self, data):
        self.clear()
        self.add(data)
