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
from logging import getLogger
import subprocess

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
    return

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

def get_number_in_range(number, min_=None, max_=None):
    """If number is outside the range of min/max, the min/max it exceeds is
    returned, if not the number is returned.

    number - The middle number | integer
    min_ - Minimum possible number | integer
        / If not given, no minimum is set.
    max_ - Maximum possible number | integer
        / If not given, no maximum is set.

    """
    logger = getLogger(__name__+".get_number_in_range")
    logger.debug("Call to get_number_in_range.")
    logger.debug("Args given: {0}, {1}, {2}".format(number, min_, max_))
    if min_ is None and max_ is None:
        raise TypeError("get_number_in_range expected 2 arguments, got 1")
    elif min_ is not None and max_ is None:
        return max([min_, number])
    elif max_ is not None and min_ is None:
        return min([max_, number])
    else:
        return max([min_, min([max_, number])])

def get_git_commit_hash(version="long"):
    """Get git commit hash

    version - either long or short | string
        / Defaults to long

    """
    if version == "long":
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().replace("\n", "")
    elif version == "short":
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().replace("\n", "")
    else:
        raise ValueError("Invalid arg for version.")

class Tools():
    """General Class Tools."""

    def __init__(self, *args, **kwargs):
        """Initialization."""
        getLogger(__name__+".Tools.__init__").debug("Tools Class called")
        if "debug" in kwargs:
            del(kwargs["debug"]) # Cleaning, to be removed when codes in updated
        self.args = args
        self.kwargs = kwargs
        return


class Thread_tools(Tools, Thread):
    """Threading Class Tools."""

    def __init__(self, *args, **kwargs):
        """Initialization."""
        getLogger(__name__+".Thread_tools.__init__").debug("Thread_tools Class called.")
        Thread.__init__(self)
        Tools.__init__(self, *args, **kwargs)
        self.autorun()
        return

    def autorun(self):
        """Autorun thread if kwargs["run"] is True."""
        logger = getLogger(__name__+".Tools.autorun")
        logger.debug("Autorun called.")
        if "run" in self.kwargs and self.kwargs["run"]:
            logger.debug("Autorunning.")
            self.start()
        return


if __name__ == '__main__':
    main(__doc__)
