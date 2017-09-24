"""Datebase handler for PCPPPriceDropTracker.

"""

import sqlite3
from time import time
import json
from logging import getLogger

from exception import CustomException
from tools import main, ThreadTools, pdname, countries
from dataScraper import scraper


class Handler():
    """PCPPPriceDropTracker Database Handler."""

    def __init__(self):
        """Initialization."""
        logger = getLogger(pdname + "." + __name__ + ".Handler.__init__")
        logger.debug("Database handler initalization.")

    # DB Tools or Handling Tools
    def create(self, path, country):
        """Database creation method.

        path - File path | string
        country - Country code | string

        """
        logger = getLogger(pdname + "." + __name__ + ".Handler.create")
        logger.debug("Creating db {0}, {1}".format(path, country))
        self.path = path
        if country not in countries:
            raise UnknownCountryError("PCPP does not support the country {0}. Try: {1}".format(country, ", ".join(countries)), country = country)
        self.country = country
        self.open(self.path)
        logger.debug("Building database.")
        self.query("PRAGMA foreign_keys = ON;")
        self.query("""CREATE TABLE IF NOT EXISTS Products(
                                                     ProductID integer,
                                                     Name text,
                                                     ProductType text,
                                                     PCPP_URL text,
                                                     Primary Key(ProductID));""")
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
        logger.debug("Build Complete.")

    def open(self, path):
        """Database connection opening method.

        path - File path | string

        """
        getLogger(pdname + "." + __name__ + ".Handler.open").debug("Opening connection to db: {0}".format(path))
        self.db = sqlite3.connect(path)
        self.c = self.db.cursor()

    def close(self, commit = True):
        """Database connection termination method.

        commit - Do a final commit? | boolean

        """
        getLogger(pdname + "." + __name__ + ".Handler.close").debug("Closing connection to db, with commmit?: {0}".format(commit))
        if commit:
            self.db.commit()
        self.db.close()

    def updater(self, callback = None):
        """Database updater method.

        Needs rewriting...

        callback - Function to call on completion | Function

        """
        getLogger(pdname + "." + __name__ + ".Handler.updater").debug("Updater rapper called.")
        updater = Updater(country = self.country, path = self.path, callback = callback, run = True)

    def clean(self, inactive = True, displayed = False):
        """Remove all inactive and/or displayed offers from the database.

        inactive - Remove inactive offers | boolean
            / Defaults to True
        displayed - Removed displayed offers | boolean
            / Defaults to False

        """
        logger = getLogger(pdname + "." + __name__ + ".Handler.clean")
        logger.debug("Removing inactive: {} and displayed: {} entries from database offers tablle".format(inactive, displayed))
        if inactive:
            self.query("DELETE FROM Offers WHERE Active = 0")
        if displayed:
            self.query("DELETE FROM Offers WHERE Displayed = 1")

    """def get_product_id(self, item):
        ""/"Get a products id from scraped offer data.

        item - all item data | dict

        ""/"
        logger = getLogger(pdname + "." + __name__ + ".Handler.get_product_id")
        logger.debug("Call to get_product_id.")
        results = self.query("SELECT ProductID FROM Products WHERE Name = ?", (item["name"],))
        logger.debug("Result: {0}".format(results))
        if len(results) < 1:
            logger.debug("Unknown item, adding to db.")
            self.query("INSERT INTO Products(Name, ProductTypeID, PCPP_URL) VALUES (?, ?, ?)",
                       (item["name"], self.get_catagorty_id(item["catagorty"]), item["pcpp url"]))
            return self.c.lastrowid
        return results[0][0]""""

    def get_product_id(self, name):
        """Get product ID by name.

        name - Name value of the product | String
        Returns the ID as a integer.

        UnknownProductWarning will be raised if no entry is found.
        ProductNameClashWarning will be raised if multiple entries are found.
            IDs can be frond in the error under results.

        """
        logger = getLogger(pdname + "." + __name__ + ".Handler.get_product_id")
        logger.debug("Get product ID of {}".format(name))
        result = self.query("SELECT ProductID FROM Products WHERE Name = ?", (item,))
        if not result:
            raise UnknownProductWarning("Name: {}".format(name), name = name)
        elif result > 1:
            results = [id for id in result]
            raise ProductNameClashWarning("Name: {}, ProductIDs: {}".format(name, results),
                                          name = name, results = results)
        else:
            return result[0][0]

    def query(self, sql, *data, commit = True):
        """Send a query to the database.

        sql - SQL code to execute | String
        data - Data to provide to replace ?s | Tuple
            / Not required.
        commit - Whether to commit | Boolean
            / Defaults to True
        Returns cursor.fetchall

        """
        logger = getLogger(pdname + "." + __name__ + ".Handler.query")
        logger.debug("Querying DB: '{}' with {}".format(" ".join([p.strip() for p in sql.split()]), data))
        self.c.execute(sql, data)
        if commit:
            self.db.commit()
        return self.c.fetchall()

    # Properties Methods
    def property_get(self, key):
        """Get property of database from Properties table.

        key - property name | string

        """
        getLogger(pdname + "." + __name__ + ".Handler.property_get").debug("Get property: {0}".format(key))
        # Not sqli protected but it is app-side, may change in future.
        columns = [col[1] for col in self.query("PRAGMA table_info(Properties)")]
        if not key in columns: # A bit of sqli protection as I could not get ? to work.
            raise UnknownPropertyError("Unknown property: {0}".format(key), key = key)
        return self.query("SELECT {0} FROM Properties WHERE ID = 1".format(key))[0][0]

    def property_add(self, key, value = None, constraint = "BLOB"):
        """Add property to database Properties table.

        key - property name | string
        value - the value to set | value to put in db
            / Not required but if given set.
        constraint - sqlite column constraint | sting
            / Defaults to any type prefered "BLOB"

        """
        # Does not really need sqli protection as it is app only facing and I can't get ? to work here.
        getLogger(pdname + "." + __name__ + ".Handler.property_add").debug("property_add called with key {0}, value: {1}, constraint {2}".format(key, value, constraint))
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
        getLogger(pdname + "." + __name__ + ".Handler.property_set").debug("Property set: key {0}, value {1}".format(key, value))
        columns = [col[1] for col in self.query("PRAGMA table_info(Properties)")]
        if not key in columns: # A bit of sqli protection as I could not get ? to work.
            raise UnknownPropertyError("Unknown property: {0}".format(key), key = key)
        self.query("UPDATE Properties SET {0} = ? WHERE ID = 1".format(key), (value,))
        return

    # Filter Methods - Need reworking
    def filter_add(self, filter_, name = None):
        """Add a filter to the filter table.

        filter_ - A list of filters, ['filter', 'oporand', value], and oporands | list
                    / e.g [["OfferID", ">", 10], "AND", ["Normal_Price", "<", 100], "OR", ["Flames", "=", 3]]
                    / See do_filter() for more info on filters.
        name - Name of filter | string

        """
        getLogger(pdname + "." + __name__ + ".Handler.filter_add").debug("Add filter called. filter {0}, name {0}".format(filter_, name))
        self.query("INSERT INTO Filters(Name, Filter, Date_Time) VALUES (?, ?, ?)", (name, json.dumps(filter_), time()))
        return

    def filter_delete(self, ID):
        """Delete a filter.

        ID - Filter name or FilterID | int or string

        """
        getLogger(pdname + "." + __name__ + ".Handler.filter_delete").debug("Deleting filter {0}".format(ID))
        if isinstance(ID, int):
            self.query("DELETE FROM Filters WHERE FilterID = ?", (ID,))
        elif isinstance(ID, str):
            self.query("DELETE FROM Filters WHERE Name = ?", (ID,))
        return

    def filter_do(self, ID, filter_ = None):
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
        logger = getLogger(pdname + "." + __name__ + ".Handler.filter_do")
        if ID == ":CUSTOM:":
            pass
        elif isinstance(ID, int):
            filter_ = json.loads(self.query("SELECT Filter FROM Filters WHERE FilterID = ?", (ID,))[0][0])
        elif isinstance(ID, str):
            filter_ = json.loads(self.query("SELECT Filter FROM Filters WHERE Name = ?", (ID,))[0][0])
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
                    raise FilterBuildError("Unknown filter: {0} in {1} in {2}".format(col, part, filters), col = col, part = part, filters = filters)
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
                    raise FilterBuildError("Unknown comparision: {0} in {1} in {2}".format(op, part, filters), op = op, part = part, filters = filters)
                # Value
                args += "?"
                values.append(str(value))
            # Main clause ops
            elif part.upper() == "AND":
                args += "AND"
            elif part.upper() == "OR":
                args += "OR"
            else:
                raise FilterBuildError("Can not build filter from filter data: {0} in {1}".format(part, filters), part = part, filters = filters)
        # Call
        if args:
            args = " WHERE" + args
        sql = "SELECT OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID" + args
        logger.debug("Args are: {0}".format(args))
        return self.query(sql, values) # Needs to be corrected/reformated.


class Updater(Handler, ThreadTools):
    """Update the database to the lastest PCPP data."""

    def __init__(self, path, country, callback = None, *args, **kwargs):
        """Initialization.

        Same args as Handler.
        Plus callback, a function to call when done, no args.
        run - Autorun | boolean

        args/kwargs are passed to ThreadTools

        Was going to use Handler's but could not get it working as sqlite3
        objects but be created inside the same thread... but i did it in
        run so???
        """
        logger = getLogger(pdname + "." + __name__ + ".Updater.__init__")
        logger.debug("DB Updater initalization.")
        self.path = path
        self.callback = callback
        if country not in countries:
            raise UnknownCountryError("PCPP does not support {0}. :\\nTry: {1}".format(country, ", ".join(countries)), county = county)
        self.country = country
        ThreadTools.__init__(self, *args, **kwargs)
        logger.debug("Updater ready.")
        return

    def run(self):
        """Run the updater."""
        logger = getLogger(pdname + "." + __name__ + ".Updater.run")
        logger.debug("DB Updater running.")
        self.open()
        self.first_setup()
        data = scraper(self.country)
        actives = []
        for item in data:
            # Check if offer already in offers table.
            results = self.query("SELECT OfferID, Flames FROM Offers WHERE ProductID = ? AND Active = 1 \
                                 AND Normal_Price = ? AND Offer_Price = ? AND \
                                 Shop_Name = ? AND Shop_URL = ?",
                                (self.get_product_id(item), item["normal price"],
                                 item["offer price"], item["shop name"], item["shop url"]))
            # Was it?
            if len(results) < 1:
                # No? Adding it.
                self.query("INSERT INTO Offers(ProductID, Active, Displayed, Normal_Price, Offer_Price, \
                            Shop_URL, Shop_Name, Updated, Flames) VALUES (? , 1, 0, ?, ?, ?, ?, ?, ?)",
                           (self.get_product_id(item), item["normal price"], item["offer price"],
                            item["shop url"], item["shop name"], item["time"], item["flames"]))
                actives.append(self.c.lastrowid)
                continue
            # Was, updating to lastest time and highest flames.
            for result in results: # Should only be one through.
                if item["flames"] > result[1]:
                    result[1] = item["flames"]
                self.query("UPDATE Offers SET Updated = ?, Flames = ? WHERE OfferID = ?", (item["time"], result[1], result[0]))
                actives.append(result[0])
        logger.debug("Updated from website, now updating existing entries.")
        # Setup Offers not in lasest scrape to inactive.
        results = self.query("SELECT OfferID FROM Offers WHERE Active = 1")
        inactives = []
        for item in results:
            if item[0] not in actives:
                inactives.append((item[0],))
        self.c.executemany("UPDATE Offers SET Active = 0 WHERE OfferID = ?", inactives)
        self.db.commit()
        self.close() # Must
        logger.debug("Complete updated")
        if self.callback:
            logger.debug("Callback been executed.")
            self.callback()
        return


# Exceptions
class UnknownCountryError(CustomException):
    """General unknown country error."""

class FilterError(CustomException):
    """General filter error."""

class FilterBuildError(FilterError):
    """General filter build error."""

class UnknownPropertyError(CustomException):
    """General unknown property error."""

class UnknownProductWarning(CustomException):
    """General unknown product warning."""

class ProductNameClashWarning(CustomException):
    """General product name clash warning."""

if __name__ == '__main__':
    main(__doc__)
