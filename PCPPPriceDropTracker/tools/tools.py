"""Tools for PCPPPriceDropTracker.

"""

__all__ = ["main",
           "sys_args",
           "get_number_in_range",
           "get_git_commit_hash",
           "Tools",
           "Thread_tools",
           "CallbackOnEditDict",
           "SelfSavingDict"]

import os
import sys
import subprocess
import json
from time import time
from threading import Thread
from logging import getLogger


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


class CallbackOnEditDict(dict):
    """Dictionary subclass with callback when edited.

    If dictionary content given when initialized, all dictionaries are
    converted.
    Callback is not called for self.convert edits.

    convert - A dictionary (/nested) to convert | dictionary
        / Not required
    callback - A function to call when changes are made | function

    """

    def __init__(self, convert=None, callback=None, *a, **kw):
        getLogger(__name__+".CallbackOnEditDict.__init__").debug("CallbackOnEditDict initialized.")
        if callback is None:
            raise TypeError("CallbackOnEditDict expected function for callback.")
        if not callable(callback):
            raise ValueError("Invalid argument passed for callback.")
        self._passed_callback = callback
        super().__init__(*a, *kw)
        self.setup_mode = False
        if convert:
            self.convert(convert)
        return

    def callback(self, condition=None):
        getLogger(__name__+".CallbackOnEditDict.callback").debug("Callback called, {0}?, con: {0}".format(not self.setup_mode, condition))
        if self.setup_mode is not True:
            if condition == "set":
                self.convert()
            self._passed_callback()

    def __delitem__(self, *a, **kw):
        super().__delitem__(*a, **kw)
        self.callback()
        return

    def __setitem__(self, *a, **kw):
        super().__setitem__(*a, **kw)
        self.callback("set")
        return

    def clear(self, *a, **kw):
        super().clear(*a, **kw)
        self.callback()
        return

    def pop(self, *a, **kw):
        r = super().pop(*a, **kw)
        self.callback()
        return r

    def popitem(self, *a, **kw):
        super().popitem(*a, **kw)
        self.callback()
        return

    def setdefault(self, *a, **kw):
        super().setdefault(*a, **kw)
        self.callback("set")
        return

    def update(self, *a, **kw):
        super().update(*a, **kw)
        self.callback("set")
        return

    def convert(self, d=None):
        """Convert nested dictionaries into CallbackOnEditDict dictionaries.

        d - The dictionaries to convert and add to self | Dictionary
            / If not given, dictionaries already in self are converted.

        """
        if d is None or d is True:
            d = self
        self.setup_mode = True
        for k in d:
            if isinstance(d[k], dict):
                self[k] = CallbackOnEditDict(convert=d[k], callback=self._passed_callback)
            else:
                self[k] = d[k]
        self.setup_mode = False
        return


class SelfSavingDict(CallbackOnEditDict):
    """Salf-saving dictionary - to a file in json format."""

    def __init__(self, path):
        """Initialization

        path - Path of project data | string

        """
        # Dev
        if path == "INPUT":
            path = input("PATH:")
        self.path = path
        with open(self.path, "r") as f:
            super().__init__(convert=json.load(f), callback=self.save)
        return

    def save(self):
        """Auto-saving callback method."""
        with open(self.path, "w") as f:
            json.dump(self, f, indent=2)
        return


if __name__ == '__main__':
    main(__doc__)