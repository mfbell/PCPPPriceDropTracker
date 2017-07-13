"""PCPPPriceDropTracker main __main__ module.

Work In Progress.

"""

#import sys
from logging import getLogger

from widgets import App
from log_setup import setup
from tools import pdname

def main(args=None):
    """The main routine."""
    setup()
    logger = getLogger(pdname+"."+__name__+".main")
    logger.debug("Logging setup. Main called, calling and running App")
    app = App()
    app.mainloop()
    logger.debug("App closed.")
    return

    """if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")
    print("It should do something interesting.")

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do."""

if __name__ == "__main__":
    main()
