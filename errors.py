"""Errors for PPCPScrapper.



Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""

AUTHOR = "mtech0 | https://github.com/mtech0"
LICENSE = "GNU-GPLv3 | https://www.gnu.org/licenses/gpl.txt"
VERSION = "0.2.0"
STATUS = "Development"
URL = ""
__doc__ = __doc__.format(AUTHOR, VERSION, STATUS, LICENSE, URL)


class Error(Exception):
    """General Error class."""

    def __init__(self, msg=None):
        """Error Raising."""
        if not msg:
            msg = self.__doc__
        super(Error, self).__init__(msg)
        self.msg = msg

class UnknownSiteError(Error):
    """General unknown site error."""

class UnknownCountryError(Error):
    """Unknown country."""

if __name__ == '__main__':
    main(__doc__)
