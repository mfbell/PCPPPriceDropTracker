"""Datebase handler for PCPPPriceDropTracker.

"""

import sqlite3
from time import time
import json
from itertools import permutations
from logging import getLogger

from errors import UnknownCountryError, FilterBuildError, UnknownPropertyError
from tools import main, Tools, Thread_tools, pdname
from dataScraper import scraper


COUNTRIES = ["au", "be", "ca", "de", "es", "fr", "in", "it", "nz", "uk", "us", None]

class Handler(Tools):
    """The database handler."""

    def __init__(self, path, country=None, *args, **kwargs):
        """Initialization.

        path - Database file path | string
        country - PCPP country code | string

        **kwargs - debug = debug object

        """
        logger = getLogger(pdname+"."+__name__+".Handler.__init__")
        logger.debug("Database handler initalization.")
        super().__init__(*args, **kwargs)
        self.path = path
        self.country = country
        if self.country not in COUNTRIES:
            raise UnknownCountryError("PCPP does not support the country {0}. Try: {1}".format(country, ", ".join(countries)))
        self.open()
        self.first_setup()
        logger.debug("Database handler setup complete.")
        return

    # DB Tools or Handling Tools
    def open(self):
        """Open a connection to a database."""
        getLogger(pdname+"."+__name__+".Handler.open").debug("Opening connection to db: {0}".format(self.path))
        self.db = sqlite3.connect(self.path)
        self.c = self.db.cursor()
        return

    def close(self, commit=True):
        """Close the connection to the database.

        commit - Do a final commit? | boolean

        """
        getLogger(pdname+"."+__name__+".Handler.close").debug("Closing connection to db, with commmit: {0}".format(commit))
        if commit:
            self.db.commit()
        self.db.close()
        return

    def updater(self, callback=None):
        """Rapper method for Updater."""
        getLogger(pdname+"."+__name__+".Handler.updater").debug("Updater rapper called.")
        updater = Updater(country=self.country, path=self.path, callback=callback, run=True)
        return

    def search(self, columns="*", filters=None, search_string=None, filter_data=None):
        """Search for offer in database and return results.

        columns - Column names of data to return | list
        filters - A list of string or list of search filters | string or list
            / E.g. "Active = 1 AND Offer_Price < 100"
            / Or ["Active = ", 1, "OR", "Displayed = 0", "AND Shop_Name = 'Amazon'"]
            / See 'Behaviour' below for more info.
        search_string - A string of text to smartly* search the database for
                        entries | string
            / See 'Behaviour' below for more info.
        filter_data - Data to include if there is '?' in filters data. | list

        --== Behaviour ==--
        Note: Any strings put into a query are not case sensitive as this part
        of SQLite.

        + Args +
        - If no args are given, this will return all columns of data for entries
          which match 'Active = 1'.
        - If columns is not given, all columns' data will be returned.
          This is the row from Offers and corresponding data from Products
        - If filters is not given or has a false/none value, filters will not be
          included. Spaces will be put around all strings in a list or around a
          given string.
        - If search_string is not give or has a false/none value, it will not be
          included in the query.

        + Smart Search +
        Smart Search starts with the string in search_string. It first splits
        the string and then strips each part.
            If over six words long, the possible combinations exceeds SQLite
            query expression limit. For now a linear search is done with the
            words reassembed in order joined, prefix and sufexed with wildcards.
            This may change in the future to use different orders.
        If there is no words the search will now neglect to include smart search.
        Now all combinations are generated from the words: This is all different
        ways the words can be arranged, then joined, prefix and sufexed with
        wildcards.
        In the search all these are listed in the query under 'Name LIKE <str>
        OR ...'. At the moment smart search is limited to Name only but I hope
        to expand to other columns, however this will reduce the possible length
        of searches as expressions will have to be spread over more conditions.
        Example:
        "Intel Core" ->
        ["Intel", "Core"] ->
        [("Intel", "Core"), ("Core", "Intel")] ->
        ["%Intel%Core%", "%Core%Intel%"] ->
        SQL: "...
              WHERE [<conditions> AND]
                  (Name LIKE '%Intel%Core%' OR Name LIKE '%Core%Intel%')" =>
        Return ...

        + Returns +
        If there is no results None is returned.
        If there is, results will be returned as: (Entry, Entry, ...)
        Where Entries are rows in Offers (with Products data) which fit
        conditions given to the SQL query.
        Entries will contrain the tuple of the column data of the entry in order
        which it was requested. See Behaviour->Args->columns for more info.

        --== Future Updates ==--
        See a doc I will create for this at some point.
            Stuff like all column smart searching, rank results by relivance eta.

        """
        logger = getLogger(pdname+"."+__name__+".Handler.search")
        logger.debug("Search method called.")
        # Smart Search
        if not search_string:
            search_string = ""
        words = [word.strip() for word in search_string.split()]
        logger.debug("Words from string: {0}".format(words))
        results = []
        if len(words) > 6:
            results.append(("Possible search combinations exceeds SQLite expression limit. Using linear search.", "ErrorMessage"))
            logger.info("Possible search combinations exceeds SQLite expression limit. Using linear search.")
            combinations = ["%" + "%".join(word for word in words) + "%"] # Could do up to so many combinations
        elif not words:
            combinations = []
            combinations_str = ""
            logger.debug("No combinations created.")
        else:
            combinations = ["%" + "%".join(order) + "%" for order in list(permutations(words))]
            logger.debug("Full search can be done.")
        if combinations:
            combinations_str = "(Name LIKE {0})".format(" OR Name LIKE ".join("?" for _ in combinations))
        # Search Filter
        if isinstance(filters, list):
            filters = " ".join(filters)
        elif not isinstance(filters, str):
            filters = "''=''"
        if combinations:
            filters += " AND "
        logger.debug("Filters are: {0}".format(filters))
        # Query
        if filter_data:
            combinations = filter_data + combinations
        results += self.query("""SELECT {0} FROM Offers
                                     JOIN Products ON Offers.ProductID = Products.ProductID
                                 WHERE {1}
                                     {2}""".format(", ".join(columns),
                                                   filters,
                                                   combinations_str),
                              combinations)
        logger.debug("Search complete.")
        return results

    def first_setup(self):
        """First time setup.

        Also run when connecting to check all tables exist eta.

        """
        logger = getLogger(pdname+"."+__name__+".Handler.first_setup")
        logger.debug("first_setup called.")
        self.query("PRAGMA foreign_keys = ON;")
        self.query("""CREATE TABLE IF NOT EXISTS Products(
                                                     ProductID integer,
                                                     Name text,
                                                     ProductTypeID integer,
                                                     PCPP_URL text,
                                                     Primary Key(ProductID),
                                                     Foreign Key(ProductTypeID) references ProductTypes(ProductTypeID));""")
        self.query("""CREATE TABLE IF NOT EXISTS ProductTypes(
                                                     ProductTypeID integer,
                                                     Description text,
                                                     Primary Key(ProductTypeID));""")
        self.query("""CREATE TABLE IF NOT EXISTS Offers(
                                                     OfferID integer,
                                                     Active integer,
                                                     Displayed integer,
                                                     ProductID integer,
                                                     Normal_Price real,
                                                     Offer_Price real,
                                                     Shop_URL text,
                                                     Shop_Name text,
                                                     Updated real,
                                                     Flames integer,
                                                     Primary Key(OfferID),
                                                     Foreign Key(ProductID) references Products(ProductID));""")
        self.query("""CREATE TABLE IF NOT EXISTS Filters(
                                                     FilterID integer,
                                                     Name text,
                                                     Filter text,
                                                     Date_Time real,
                                                     Primary Key(FilterID));""")
        self.query("""CREATE TABLE IF NOT EXISTS Properties(
                                                     ID integer,
                                                     Country text,
                                                     Primary Key(ID));""")
        self.query("""INSERT OR IGNORE INTO Properties(ID, Country) VALUES(1, ?);""", self.country)
        logger.debug("first_setup successful.")
        return

    def clean_up(self, displayed=False):
        """Remove all inactive (and displayed) offers

        displayed - Removed displayed offers | boolean

        """
        getLogger(pdname+"."+__name__+".Handler.clean_up").debug("clean_up called, removing non-active entries, removing displayed: {0}".formated(displayed))
        self.query("DELETE FROM Offers WHERE Active=0")
        if displayed:
            self.query("DELETE FROM Offers WHERE Displayed=1")
        return

    def get_product_id(self, item):
        """Get a products id from scraped offer data.

        item - all item data | dict

        """
        logger = getLogger(pdname+"."+__name__+".Handler.get_product_id")
        logger.debug("Call to get_product_id.")
        results = self.query("SELECT ProductID FROM Products WHERE Name=?", (item["name"],))
        logger.debug("Result: {0}".format(results))
        if len(results) < 1:
            logger.debug("Unknown item, adding to db.")
            self.query("INSERT INTO Products(Name, ProductTypeID, PCPP_URL) VALUES (?,?,?)",
                       (item["name"], self.get_catagorty_id(item["catagorty"]), item["pcpp url"]))
            return self.c.lastrowid
        return results[0][0]

    def get_catagorty_id(self, cat):
        """Get catagorty id.

        cat - the catagorty | sting

        """
        logger = getLogger(pdname+"."+__name__+".Handler.get_catagorty_id")
        logger.debug("Call to get_catagorty_id, get id of catagorty {0}".format(cat))
        result = self.query("SELECT ProductTypeID FROM ProductTypes WHERE Description=?", (cat,))
        logger.debug("Result: {0}".format(result))
        if len(result) < 1:
            logger.debug("Unkonwn catagorty, adding to db.")
            self.query("INSERT INTO ProductTypes(Description) VALUES (?)", (cat,))
            return self.c.lastrowid
        return result[0][0]

    def query(self, sql, data=()):
        """Send a query to the database.

        sql - SQL code to execute | string
        data - Data to provide to replace ?s | tuple
                / Not required.

        """
        if not sql.endswith(";"):
            sql += ";"
        if not isinstance(data, (tuple, list)):
            data = (data, )
        getLogger(pdname+"."+__name__+".Handler.query").debug("Querying db with '{0}' and data: {1}".format(" ".join([p.strip() for p in sql.split()]), data))
        self.c.execute(sql, data)
        self.db.commit()
        return self.c.fetchall()

    # Properties Methods
    def property_get(self, key):
        """Get property of database from Properties table.

        key - property name | string

        """
        getLogger(pdname+"."+__name__+".Handler.property_get").debug("Get property: {0}".format(key))
        # Not sqli protected but it is app-side, may change in future.
        columns = [col[1] for col in self.query("PRAGMA table_info(Properties)")]
        if not key in columns: # A bit of sqli protection as I could not get ? to work.
            raise UnknownPropertyError("Unknown property: {0}".format(key))
        return self.query("SELECT {0} FROM Properties WHERE ID=1".format(key))[0][0]

    def property_add(self, key, value=None, constraint="BLOB"):
        """Add property to database Properties table.

        key - property name | string
        value - the value to set | value to put in db
            / Not required but if given set.
        constraint - sqlite column constraint | sting
            / Defaults to any type prefered "BLOB"

        """
        # Does not really need sqli protection as it is app only facing and I can't get ? to work here.
        getLogger(pdname+"."+__name__+".Handler.property_add").debug("property_add called with key {0}, value: {1}, constraint {2}".format(key, value, constraint))
        self.query("ALTER TABLE Properties ADD COLUMN {0} {1}".format(key, constraint))
        if value:
            self.property_set(key, value)
        return

    def property_set(self, key, value):
        """Set property in database Properties table.

        key - property name | string
        value - the value to set | value to put in db
            / Not required but if given set.

        """
        getLogger(pdname+"."+__name__+".Handler.property_set").debug("Property set: key {0}, value {1}".format(key, value))
        columns = [col[1] for col in self.query("PRAGMA table_info(Properties)")]
        if not key in columns: # A bit of sqli protection as I could not get ? to work.
            raise UnknownPropertyError("Unknown property: {0}".format(key))
        self.query("UPDATE Properties SET {0} = ? WHERE ID=1".format(key), (value,))
        return

    # Filter Methods - Need reworking
    def filter_add(self, filter_, name=None):
        """Add a filter to the filter table.

        filter_ - A list of filters, ['filter', 'oporand', value], and oporands | list
                    / e.g [["OfferID", ">", 10], "AND", ["Normal_Price", "<", 100], "OR", ["Flames", "=", 3]]
                    / See do_filter() for more info on filters.
        name - Name of filter | string

        """
        getLogger(pdname+"."+__name__+".Handler.filter_add").debug("Add filter called. filter {0}, name {0}".format(filter_, name))
        self.query("INSERT INTO Filters(Name, Filter, Date_Time) VALUES (?,?,?)", (name, json.dumps(filter_), time()))
        return

    def filter_delete(self, ID):
        """Delete a filter.

        ID - Filter name or FilterID | int or string

        """
        getLogger(pdname+"."+__name__+".Handler.filter_delete").debug("Deleting filter {0}".format(ID))
        if isinstance(ID, int):
            self.query("DELETE FROM Filters WHERE FilterID=?", (ID,))
        elif isinstance(ID, str):
            self.query("DELETE FROM Filters WHERE Name=?", (ID,))
        return

    def filter_do(self, ID, filter_=None):
        """Get OfferIDs from a filter. - Needs rewriting...

        ID - FilterID or Name | int or str
        filter_ - Use if giving custom filter to give it | str
                    / Set ID = ":CUSTOM:" to run it.

        Full filtering across tables happens with:
        SELECT OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID [WHERE args]
        I think I have including all columns.
        You only get back the Offers.OfferID for simplication at the moment.

        Filters:
            "OfferID" is Offers.OfferID
            "Active" is Offers.Active
            "Displayed" is Offers.Displayed
            "ProductID" is Offers.ProductID/Products.ProductID
            "Normal_Price" is Offers.Normal_Price
            "Offer_Price" is Offers.Offer_Price
            "Shop_URL" is Offers.Shop_URL
            "Shop_Name" is Offers.Shop_Name
            "Updated" is Offers.Updated
            "Flames" is Offers.Flames
            "Name" is Products.Name
            "ProductTypeID" is Products.ProductTypeID(/ProductTypes.ProductTypeID)
            "PCPP_URL" is Products.PCPP_URL
            "ProductType" is Products.ProductTypeID(/ProductTypes.ProductTypeID) resolved from ProductTypes.Description
        Comparison OPs:
            "=", "!=", ">", "<", ">=", "<="
            Note: Some filters auto do comparison, see code.
        Value: Is the value you want to filter by.

        """
        logger = getLogger(pdname+"."+__name__+".Handler.filter_do")
        if ID == ":CUSTOM:":
            pass
        elif isinstance(ID, int):
            filter_ = json.loads(self.query("SELECT Filter FROM Filters WHERE FilterID=?", (ID,))[0][0])
        elif isinstance(ID, str):
            filter_ = json.loads(self.query("SELECT Filter FROM Filters WHERE Name=?", (ID,))[0][0])
        else:
            logging.debug("No filter can be found for ID: {0}".format(ID))
            return None
        logger.debug("Running filter: id {0}, filter {1}".format(ID, filter_))
        args = ""
        values = []
        # My sh!tty atempt to protect againest sql injection but probably failed but this does not really need it. :)
        for part in filter_:
            args += " "
            if isinstance(part, (tuple, list)):
                col, op, value = part
                # Column
                if col == "OfferID":
                    args += "OfferID "
                elif col == "Active":
                    args += "Active "
                elif col == "Displayed":
                    args += "Displayed "
                elif col == "ProductID":
                    args += "ProductID "
                elif col == "Normal_Price":
                    args += "Normal_Price "
                elif col == "Offer_Price":
                    args += "Offer_Price "
                elif col == "Shop_URL":
                    args += "Shop_URL = ?"
                    values.append(str(value))
                    continue
                elif col == "Shop_Name":
                    args += "Shop_Name = ?"
                    values.append(str(value))
                    continue
                elif col == "Updated":
                    args += "Updated "
                elif col == "Flames":
                    args += "Flames "
                elif col == "Name":
                    args += "Name = ?"
                    values.append(str(value))
                    continue
                elif col == "ProductTypeID":
                    args += "ProductTypeID "
                elif col == "PCPP_URL":
                    args += "PCPP_URL = ?"
                    values.append(str(value))
                    continue
                elif col == "ProductType":
                    args += "ProductTypeID = ?"
                    values.append(str(self.query("SELECT ProductTypeID FROM ProductTypes WHERE Description = ?", (value,))[0][0]))
                    continue
                else:
                    raise FilterBuildError("Unknown filter: {0} in {1} in {2}".format(col, part, filters))
                # Comparison Op
                if op == "=":
                    args += "= "
                elif op == "!=":
                    args += "!= "
                elif op == "<":
                    args += "< "
                elif op == ">":
                    args += "> "
                elif op == "<=":
                    args += "<= "
                elif op == ">=":
                    args += ">= "
                else:
                    raise FilterBuildError("Unknown comparision: {0} in {1} in {2}".format(op, part, filters))
                # Value
                args += "?"
                values.append(str(value))
            # Main clause ops
            elif part.upper() == "AND":
                args += "AND"
            elif part.upper() == "OR":
                args += "OR"
            else:
                raise FilterBuildError("Can not build filter from filter data: {0} in {1}".format(part, filters))
        # Call
        if args:
            args = " WHERE" + args
        sql = "SELECT OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID" + args
        logger.debug("Args are: {0}".format(args))
        return self.query(sql, values) # Needs to be corrected/reformated.


class Updater(Handler, Thread_tools):
    """Update the database to the lastest PCPP data."""

    def __init__(self, path=".\pcpp_offers.sqlite3", country="uk", *args, **kwargs):
        """Initialization.

        Same args as Handler.
        Plus callback, a function to call when done, no args.
        run - Autorun | boolean

        Was going to use Handler's but could not get it working as sqlite3
        objects but be created inside the same thread... but i did it in
        run so???
        """
        logger = getLogger(pdname+"."+__name__+".Updater.__init__")
        logger.debug("DB Updater initalization.")
        self.path = path
        countries = ["au", "be", "ca", "de", "es", "fr", "in", "it", "nz", "uk", "us"]
        if country not in countries:
            raise UnknownCountryError("PCPP does not support {0}. :\\nTry: {1}".format(country, ", ".join(countries)))
        self.country = country
        Thread_tools.__init__(self, *args, **kwargs)
        logger.debug("Updater ready.")
        return

    def run(self):
        """Run the updater."""
        logger = getLogger(pdname+"."+__name__+".Updater.run")
        logger.debug("DB Updater running.")
        self.open()
        self.first_setup()
        data = scraper(self.country)
        actives = []
        for item in data:
            # Check if offer already in offers table.
            results = self.query("SELECT OfferID, Flames FROM Offers WHERE ProductID=? AND Active=1 \
                                 AND Normal_Price=? AND Offer_Price=? AND \
                                 Shop_Name=? AND Shop_URL=?",
                                (self.get_product_id(item), item["normal price"],
                                 item["offer price"], item["shop name"], item["shop url"]))
            # Was it?
            if len(results) < 1:
                # No? Adding it.
                self.query("INSERT INTO Offers(ProductID, Active, Displayed, Normal_Price, Offer_Price, \
                            Shop_URL, Shop_Name, Updated, Flames) VALUES (?,1,0,?,?,?,?,?,?)",
                           (self.get_product_id(item), item["normal price"], item["offer price"],
                            item["shop url"], item["shop name"], item["time"], item["flames"]))
                actives.append(self.c.lastrowid)
                continue
            # Was, updating to lastest time and highest flames.
            for result in results: # Should only be one through.
                if item["flames"] > result[1]:
                    result[1] = item["flames"]
                self.query("UPDATE Offers SET Updated=?, Flames=? WHERE OfferID=?", (item["time"], result[1], result[0]))
                actives.append(result[0])
        logger.debug("Updated from website, now updating existing entries.")
        # Setup Offers not in lasest scrape to inactive.
        results = self.query("SELECT OfferID FROM Offers WHERE Active=1")
        inactives = []
        for item in results:
            if item[0] not in actives:
                inactives.append((item[0],))
        self.c.executemany("UPDATE Offers SET Active=0 WHERE OfferID=?", inactives)
        self.db.commit()
        self.close() # Must
        logger.debug("Complete updated")
        if "callback" in self.kwargs:
            logger.debug("Call back been executed.")
            self.kwargs["callback"]()
        return


if __name__ == '__main__':
    main(__doc__)
