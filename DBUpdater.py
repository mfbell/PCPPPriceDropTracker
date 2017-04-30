"""Datebase handler for PCPPScrapper.



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
from errors import UnknownCountryError
from tools import main, Tools
from dataScrapper import scrapper

class Handler(Tools):
    """The database handler."""

    def __init__(self, path="X:\coding\projects\pcppScraper\pcpp_offers.db", country="uk", debug=False):
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
        data = scrapper(self.country)
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
        self.query("PRAGMA foreign_keys = ON")
        result = self.query("select name from sqlite_master where name=?", ("Products",))
        if len(result) != 1:
            self.query("""CREATE TABLE Products(
                                       ProductID integer,
                                       Name text,
                                       ProductTypeID integer,
                                       PCPP_URL text,
                                       Primary Key(ProductID),
                                       Foreign Key(ProductTypeID) references ProductTypes(ProductTypeID))""")
        result = self.query("select name from sqlite_master where name=?", ("ProductTypes",))
        if len(result) != 1:
            self.query("""CREATE TABLE ProductTypes(
                                       ProductTypeID integer,
                                       Description text,
                                       Primary Key(ProductTypeID))""")
        result = self.query("select name from sqlite_master where name=?", ("Offers",))
        if len(result) != 1:
            self.query("""CREATE TABLE Offers(
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


def handler_handler(*args):
    try:
        a = Handler(*args)
    except Exception as e:
        a.db.rollback()
        raise e
    finally:
        a.db.close()


if __name__ == '__main__':
    main(__doc__)
