"""Errors file for PCPPPriceDropTracker.



Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""

AUTHOR = "mtech0 | https://github.com/mtech0"
LICENSE = "GNU-GPLv3 | https://www.gnu.org/licenses/gpl.txt"
VERSION = "0.3.0"
STATUS = "Ongoing development"
URL = ""
__doc__ = __doc__.format(AUTHOR, VERSION, STATUS, LICENSE, URL)


class Error(Exception):
    """General Error class."""

    def __init__(self, msg=None, *args, **kwargs):
        """Error Raising."""
        if not msg:
            msg = self.__doc__
        getLogger(__name__).exception("Exception raised: {0}".format(msg))
        super().__init__(msg)
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

class UnknownSiteError(Error):
    """General unknown site error."""

class UnknownCountryError(Error):
    """Unknown country."""

class FilterError(Error):
    """General filter error."""

class FilterBuildError(FilterError):
    """General filter build error."""

class UnknownPropertyError(Error):
    """General unknown property error."""

if __name__ == '__main__':
    main(__doc__)
