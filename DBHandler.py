"""Datebase handler for PCPPScraper.



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

import sqlite3
from time import time
import json
from errors import UnknownCountryError, FilterBuildError
from tools import main, Tools
from dataScraper import Scraper

class Handler(Tools):
    """The database handler."""

    def __init__(self, path=".\pcpp_offers.sqlite3", country="uk", debug=False):
        """Initialization.

        path - Database file path | string

        """
        self.path = path
        if country not in ["au", "be", "ca", "de", "es", "fr",
                           "in", "it", "nz", "uk", "us"]:
            raise UnknownCountryError("PCPP does not support {0}. :\\".format(country))
        self.debug = debug
        self.country = country
        self.open()
        self.first_setup()

    def updater(self):
        """Update the db to the lastest PCPP data."""
        data = Scraper(self.country)
        actives = []
        for item in data:
            # Check if offer already in offers table.
            result = self.query("SELECT OfferID FROM Offers WHERE ProductID=? AND Active=1 \
                                 AND Normal_Price=? AND Offer_Price=? AND \
                                 Shop_Name=? AND Shop_URL=?",
                                (self.get_product_id(item), item["normal price"],
                                 item["offer price"], item["shop name"], item["shop url"]))
            # Was it?
            if len(result) < 1:
                # No? Adding it.
                self.query("INSERT INTO Offers(ProductID, Active, Displayed, Normal_Price, Offer_Price, \
                            Shop_URL, Shop_Name, Updated, Flames) VALUES (?,1,0,?,?,?,?,?,?)",
                           (self.get_product_id(item), item["normal price"], item["offer price"],
                            item["shop url"], item["shop name"], item["time"], item["flames"]))
                actives.append(self.c.lastrowid)
                continue
            # Was, updating to lastest time and highest flames.
            result = result[0][0]
            flames = self.query("SELECT Flames FROM Offers WHERE OfferID=?", (result,))[0][0]
            if item["flames"] > flames:
                flames = item["flames"]
            self.query("UPDATE Offers SET Updated=?, Flames=? WHERE OfferID=?", (item["time"], flames, result))
            actives.append(result)
        # Setup Offers not in lasest scrap to Inactive.
        results = self.query("SELECT OfferID FROM Offers WHERE Active=1")
        inactives = []
        for item in results:
            if item[0] not in actives:
                inactives.append((item[0],))
        self.c.executemany("UPDATE Offers SET Active=0 WHERE OfferID=?", inactives)
        self.db.commit()

    def add_filter(self, filters, name=None):
        """Add a filter to the filter table.

        filters - A list of filters, ['filter', 'oporand', value] and oporands | list
                    / e.g [["OfferID", ">", 10], "AND", ["Normal_Price", "<", 100], "OR", ["Flames", "=", 3]]
                    / See do_filter() for more info on filters.
        name - Name of filter | string

        """
        self.query("INSERT INTO Filters(Name, Filter, Date_Time) VALUES (?,?,?)", (name, json.dumps(filters), time()))

    def del_filter(self, ID):
        """Delete a filter.

        ID - Filter name or FilterID | int or string

        """
        if isinstance(ID, int):
            self.query("DELETE FROM Filters WHERE FilterID=?", (ID,))
        elif isinstance(ID, str):
            self.query("DELETE FROM Filters WHERE Name=?", (ID,))

    def do_filter(self, ID, filters=None):
        """Get OfferIDs from a filter.

        ID - FilterID or Name | int or str
        filters - Use if giving custom filter to give it | str
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
        if ID == ":CUSTOM:":
            con = True
        elif isinstance(ID, int):
            filters = json.loads(self.query("SELECT Filter FROM Filters WHERE FilterID=?", (ID,))[0][0])
        elif isinstance(ID, str):
            filters = json.loads(self.query("SELECT Filter FROM Filters WHERE Name=?", (ID,))[0][0])
        if not con:
            return None
        args = " WHERE"
        # My sh!tty atempt to protect againest sql injection but probably failed but this does not really need it. :)
        for part in filters:
            args += " "
            if isinstance(part, (tuple, list)):
                col = part[0]
                op = part[1]
                value = part[2]
                # Column
                if col == "OfferID":
                    args += "OfferID "
                elif col == "Active":
                    args += "Active"
                elif col == "Displayed":
                    args += "Displayed "
                elif col == "ProductID":
                    args += "ProductID "
                elif col == "Normal_Price":
                    args += "Normal_Price "
                elif col == "Offer_Price":
                    args += "Offer_Price "
                elif col == "Shop_URL":
                    args += "Shop_URL = " + str(value)
                    continue
                elif col == "Shop_Name":
                    args += "Shop_Name = " + str(value)
                    continue
                elif col == "Updated":
                    args += "Updated "
                elif col == "Flames":
                    args += "Flames "
                elif col == "Name":
                    args += "Name = " + str(value)
                    continue
                elif col == "ProductTypeID":
                    args += "ProductTypeID "
                elif col == "PCPP_URL":
                    args += "PCPP_URL = " + str(value)
                    continue
                elif col == "ProductType":
                    args += "ProductTypeID = " + str(self.query("SELECT ProductTypeID FROM ProductTypes WHERE Description = ?", (value,))[0][0])
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
                args += str(value)
            # Main clause ops
            elif part.upper() == "AND":
                args += "AND"
            elif part.upper() == "OR":
                args += "OR"
            else:
                raise FilterBuildError("Can not build filter from filter data: {0} in {1}".format(part, filters))
        # Call
        if args == " WHERE":
            args = ""
        sql = "SELECT OfferID FROM Offers JOIN Products ON Offers.ProductID = Products.ProductID" + args
        return self.query(sql)

    def clean_up(self, displayed=False):
        """Remove all inactive (and displayed) offers

        displayed - Removed displayed offers | boolean

        """
        self.query("DELETE FROM Offers WHERE Active=0")
        if displayed:
            self.query("DELETE FROM Offers WHERE Displayed=1")

    def get_product_id(self, item):
        """Get a products id.

        item - all item data | dict

        """
        result = self.query("SELECT ProductID FROM Products WHERE Name=?", (item["name"],))
        self.debug_msg("FIND PROD ID: {0}".format(result))
        if len(result) < 1:
            self.debug_msg("Adding...")
            self.query("INSERT INTO Products(Name, ProductTypeID, PCPP_URL) VALUES (?,?,?)",
                       (item["name"], self.get_product_type_id(item["catagorty"]), item["pcpp url"]))
            self.debug_msg("Added")
            return self.c.lastrowid
        return result[0][0]

    def get_product_type_id(self, cat):
        """Get a product catagorty id.

        cat - the catagorty | sting

        """
        self.debug_msg("GET PROD TYPE ID: {0}".format(cat))
        result = self.query("SELECT ProductTypeID FROM ProductTypes WHERE Description=?", (cat,))
        self.debug_msg("RESULTS: {0}".format(result))
        if len(result) < 1:
            self.query("INSERT INTO ProductTypes(Description) VALUES (?)", (cat,))
            return self.c.lastrowid
        return result[0][0]

    def first_setup(self):
        """First time setup."""
        self.query("PRAGMA foreign_keys = '1'")
        self.if_not_table("Products", """CREATE TABLE Products(
                                                      ProductID integer,
                                                      Name text,
                                                      ProductTypeID integer,
                                                      PCPP_URL text,
                                                      Primary Key(ProductID),
                                                      Foreign Key(ProductTypeID) references ProductTypes(ProductTypeID))""")
        self.if_not_table("ProductTypes", """CREATE TABLE ProductTypes(
                                                          ProductTypeID integer,
                                                          Description text,
                                                          Primary Key(ProductTypeID))""")
        self.if_not_table("Offers", """CREATE TABLE Offers(
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
                                                    Foreign Key(ProductID) references Products(ProductID))""")
        self.if_not_table("Filters", """CREATE TABLE Filters(
                                                     FilterID integer,
                                                     Name text,
                                                     Filter text,
                                                     Date_Time real,
                                                     Primary Key(FilterID))""")

    def if_not_table(self, name, sql):
        """If table does not exist, execute sql.

        name - Name of the table | string
        sql - SQL command | string

        """
        result = self.query("select name from sqlite_master where name=?", (name,))
        if len(result) != 1:
            self.query(sql)

    def open(self):
        """Open a connection to a database."""
        self.db = sqlite3.connect(self.path)
        self.c = self.db.cursor()

    def close(self, commit=True):
        """Close the connection to the database.

        commit - Do a final commit? | boolean

        """
        if commit:
            self.db.commit()
        self.db.close()

    def query(self, sql, data=()):
        """Send a query to the database.

        sql - SQL code to execute | string
        data - Data to provide to replace ?s | tuple
                / Not required.

        """
        self.debug_msg("SELF.QUERY sql:\n{0}\nwith data: {1}".format(sql, data))
        self.c.execute(sql, data)
        self.db.commit()
        return self.c.fetchall()

if __name__ == '__main__':
    main(__doc__)
