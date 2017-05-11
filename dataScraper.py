"""DataScraper for PCPPScraper.

Collects price drop data from PCPP.

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

from bs4 import BeautifulSoup
import requests
from time import time
from errors import UnknownCountryError
from tools import main


def Scraper(country="uk"):
    """The data Scraper.

    country - A country code supported by PCPP | string

    """
    if country not in ["au", "be", "ca", "de", "es", "fr",
                       "in", "it", "nz", "uk", "us"]:
        raise UnknownCountryError("PCPP does not support {0}. :\\".format(country))
    dl_time = time()
    page = requests.get("https://{0}.pcpartpicker.com/products/pricedrop/".format(country))
    soup = BeautifulSoup(page.content, 'html.parser')
    items = []
    secton_header = soup.find("tr")
    try:
        catagorties = soup.find(class_="left-column").find("ul").get_text().strip().split() # Needs fixing.
    except AttributeError:
        return None
    catagorty = -1
    for item in soup.find_all("tr"):
        if item == secton_header:
            catagorty += 1
            continue
        data = list(item.children)
        items.append({"name": data[1].get_text(),
                      "catagorty": catagorties[catagorty],
                      "flames": len(data[1].find_all('img')),
                      "normal price": float(data[3].get_text()[1:]),
                      "offer price": float(data[5].get_text()[1:]),
                      "pcpp url": "https://{0}.pcpartpicker.com".format(country) + data[1].find('a').get("href"),
                      "shop url": "https://{0}.pcpartpicker.com".format(country) + data[5].find('a').get("href"),
                      "shop name": data[7].get_text(),
                      "saving": float(data[9].get_text()[1:]),
                      "saving %": float(data[11].get_text()[:-1])/100,
                      "currency symbol": data[3].get_text()[0],
                      "time": dl_time
                      })
    return items

if __name__ == '__main__':
    main(__doc__)
