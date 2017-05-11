"""Tools for PPCPScraper.



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

def debug_msg(debug, msg):
    """Debug message printer. if True.

    debug - Test | boolean or object to retrieve self.debug from
    msg - Msg to print | string
    """
    if isinstance(debug, (bool, int)):
        pass
    else:
        try:
            debug = debug.debug
        except NameError:
            raise NameError("Could not find self.debug in {0}".format(debug))
        except AttributeError:
            raise TypeError("Invalid Argument Type for 'debug': {0} ({1})".format(debug, type(debug)))
    if debug:
        if "\n" in msg:
            print("[DEBUGGING]:\n", msg, "\n[/-------]")
        else:
            print("[DEBUGGING]:", msg)

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
    def __init__(self):
        """Initialization."""
        self.debug_msg(self.__doc__.splitlines()[0][:-1] + " initialized.")

    def debug_msg(self, msg):
        """Class rapper for debug_msg."""
        return debug_msg(self, msg)


if __name__ == '__main__':
    main(__doc__)
