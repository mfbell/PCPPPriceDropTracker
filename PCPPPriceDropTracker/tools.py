"""Tools for PCPPPriceDropTracker.



Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""

AUTHOR = "mtech0 | https://github.com/mtech0"
LICENSE = "GNU-GPLv3 | https://www.gnu.org/licenses/gpl.txt"
VERSION = "0.5.0"
STATUS = "Ongoing development"
URL = ""
__doc__ = __doc__.format(AUTHOR, VERSION, STATUS, LICENSE, URL)

from time import time
import os
from threading import Thread
import logging

def main(doc=None, itu=None, pause=True, xit=True):
    """Module run as main function.

    doc - Either docstring or info to print | string
            / Defaults to 'README.md' file contents.
    itu - If to print "Import to use." at the end | boolean
            / Defaults to None
            / Behaviour:
                If doc=None and itu=None: itu=None
                If doc=None and itu=False: itu=False
                If doc=None and itu=True: itu=True
            --> If doc=True and itu=None: itu=True
                If doc=True and itu=False: itu=False
                If doc=True and itu=True: itu=True
    pause - Wait for user to press enter | boolean
    xit - Auto exit? | boolean

    """
    if doc and itu == None:
        itu = True
    if not doc:
        doc = open("README.md").read()
    print("\n" + doc)
    if itu:
        print("Import to use.")
    print()
    if xit:
        if pause:
            print("Press Enter to exit...")
        print("Terminated")
        exit(0)
    elif pause:
        input("Press Enter to continue...")

def sys_args(*check):
    """System Arg Handler Function.

    Check if arg(s) were given or return all.

    *check - Args to compare to those give to sys | Strings
            / If none are give, argv given to system are returned.
            / If args are give, it will check if they were given to sys.
                Returning a list of Trues/False or signle if single arg is given.

    """
    if not check:
        return sys.argv[1:]
    else:
        re = [i in sys.argv[1:] for i in check]
        if len(re) == 1: re = re[0]
        return re

class Tools():
    """General Class Tools."""

    def __init__(self, *args, **kwargs):
        """Initialization."""
        if "debug" in kwargs:
            del(kwargs["debug"]) # Cleaning, to be removed when codes in updated
        self.args = args
        self.kwargs = kwargs

    def debug(self, *args, **kwargs): # Removed when other code cleaned
        pass

    def debug_msg(self, *args, **kwargs): # Removed when other code cleaned
        pass

class Thread_tools(Tools, Thread):
    """Threading Class Tools."""

    def __init__(self, *args, **kwargs):
        """Initialization."""
        Thread.__init__(self)
        Tools.__init__(self, *args, **kwargs)
        self.autorun()

    def autorun(self):
        """Autorun thread if kwargs["run"] is True."""
        if "run" in self.kwargs and self.kwargs["run"]:
            self.start()


if __name__ == '__main__':
    main(__doc__)
