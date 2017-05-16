"""Tools for PPCPScraper.



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
#from uuid import uuid4

#def uuid(dict):
#    id_ = uuid4().hex
#    while id_ in dict:
#        id_ = uuid4().hex
#    return id_

def main(doc=None, itu=None, pause=True):
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

    """
    if doc and itu == None:
        itu = True
    if not doc:
        doc = open("README.md", "r").read()
    print("\n" + doc)
    if itu:
        print("Import to use.")
    print()
    input("Press Enter to exit...")
    print("Terminated")
    exit(0)

def sys_args(*check):
    """System Arg Handler Function.

    Check if arg(s) were given or return all.

    *check - Args to compare to those give to sys | Strings
            / If none are give, all argv given to system are returned.
            / If args are give, it will check if they were given to sys.
                Returning a list of Trues/False or signal if isngle arg is given.

    """
    if not check:
        return sys.argv[1:]
    else:
        re = []
        for i in check:
            re.append(i in sys.argv[1:])
        if len(re) == 1: re = re[0]
        return re

class Tools():
    """General Tool class."""
    def __init__(self, *args, **kwargs):
        """Initialization."""
        if "debug" in kwargs:
            self.debug = kwargs["debug"]
            del(kwargs["debug"])
        else:
            self.debug_ = False
        if "log" in kwargs:
            self.log_ = True
            self.log_p = kwargs["log"]
            del(kwargs["log"])
        else:
            self.log_ = False
            self.log_p = False
        self.args = args
        self.kwargs = kwargs
        self.debug_msg(self.__doc__.splitlines()[0][:-1] + " initialized.")

    def debug_msg(self, msg):
        """Debug message printer. if True.

        Looks for the method self.debug to know if to print as it returns T/F
        msg - Msg to print | string
        """
        if self.debug():
            if "\n" in msg:
                print("[DEBUGGING]:\n", msg, "\n[/-------]")
            else:
                print("[DEBUGGING]:", msg)
            if self.debug(log="get"):
                if isinstance(self.log_p, str):
                    log_file = open(self.log_p, "a")
                else:
                    path = ".\logs"
                    if not os.path.exists(path):
                        os.makedirs(path)
                    n_time = round(time())
                    self.log_p = path + "\log-{0}.txt".format(n_time)
                    log_file = open(self.log_p, "a")
                    log_file.write("#====================\n# Log file started at {0}.\n#====================\n\n".format(n_time))
                log_file.write(str(time()) + " --- " + msg + "\n")
                log_file.close()

    def debug(self, set_=None, log=None):
        if log == True:
            self.debug_ = True
            self.log_ = True
        elif log == False:
            self.log_ = False
        elif set_ == False:
            self.debug_ = False
            self.log_ = False
        elif set_ == True:
            self.debug_ = True
        elif log == "get":
            return self.log_
        else:
            return self.debug_


class Thread_tools(Tools, Thread):
    """A set of thread class tools."""
    def __init__(self, *args, **kwargs):
        """Initialization."""
        Thread.__init__(self)
        Tools.__init__(self, *args, **kwargs)
        self.autorun()

    def autorun(self):
        """Autorun thread if kwargs["run"] is True."""
        if self.kwargs["run"]:
            self.start()

if __name__ == '__main__':
    main(__doc__)
