"""Errors file for PCPPPriceDropTracker.

"""

from logging import getLogger


class Error(Exception):
    """General Error class."""

    def __init__(self, msg = None, *args, **kwargs):
        """Error Raising."""
        if not msg:
            msg = self.__doc__
        getLogger(pdname + "." + __name__).exception("Exception raised: {0}".format(msg))
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
