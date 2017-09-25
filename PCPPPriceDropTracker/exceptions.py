"""General Custom Errors file for PCPPPriceDropTracker."""

from logging import getLogger


__all__ = ["CustomException"]

class CustomException(Exception):
    """Custom Exception Tools class.

    Not to be raised directly, subclass to give more informative information.
    Subclass and do not overwrite __init__ method. This means the error will
    automaticly take a message argument, saved to self.msg. If one is not given
    the subclass' docstring will be used. It will also takes args which are
    stored in self.args, plus kwargs which are set at attributes.
    An exception is also logged with only the message.
    Then self.script is called. Overwrite this method to add custom handling.

    """
    def __init__(self, msg = None, *args, **kwargs):
        """CustomException standard __init__ method."""
        if not msg:
            msg = self.__doc__
        getLogger(__name__ + "." + type(self).__name__ + ".__init__").exception("Exception raised: {}".format(msg))
        super().__init__(msg)
        self.msg = msg
        self.args = args
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.script()

    def script():
        """Custom script."""
        pass


if __name__ == '__main__':
    main(__doc__)
