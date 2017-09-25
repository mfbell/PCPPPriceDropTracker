"""General PCPPPriceDropTracker tools module."""

import subprocess
from threading import Thread
from logging import getLogger


__all__ = ["main", "get_number_in_range", "get_git_commit_hash", "ThreadTools",
           "CallbackWithArgs"]

def main(doc = None, itu = None, pause = True, xit = True):
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

def get_number_in_range(number, min_ = None, max_ = None):
    """If number is outside the range of min/max, the min/max it exceeds is
    returned, if not the number is returned.

    number - The middle number | integer
    min_ - Minimum possible number | integer
        / If not given, no minimum is set.
    max_ - Maximum possible number | integer
        / If not given, no maximum is set.

    """
    logger = getLogger(__name__ + ".get_number_in_range")
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

def get_git_commit_hash(version = "long"):
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


class ThreadTools(Thread):
    """Threading Class Tools."""

    def __init__(self, run = False, *a, **kw):
        """Initialization."""
        logger = getLogger(__name__ + ".ThreadTools.__init__")
        logger.debug("ThreadTools Class called.")
        super().__init__(*a, **kw)
        if run:
            logger.debug("Autorunning")
            self.start()
        return


class CallbackWithArgs():
    """CallbackWithArgs give you the ability to use args on a callback
    which would also be given args by the caller.

    For example Tkinter's bind, where you can not use lambda as the callback
    passes the arg event.
    To use, subclass CallbackWithArgs and write a method named call with the
    self, non-positional arguments and possitional argument perimitors.
    To then impliment, call the class. Passesing any args or kwargs you want to
    be able to access in call. These are available from call under list
    self.args and dictionary self.kwargs with the keyword been the key.
    Then pass the object as a function to the binding.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwarg

    def __call__(self, *a, **kw):
        self.call(*a, **kw)

    def call(self, *a, **kw):
        # Example method.
        print(*a)
        print(**kw)


if __name__ == '__main__':
    main(__doc__)
