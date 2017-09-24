"""Custom dictionaries for PCPPPriceDropTracker."""

import os
import json

from . import main


__all__ = ["CallbackOnEditDict", "SelfSavingDict", "ActiveJSONDictionary"]

class CallbackOnEditDict(dict):
    """Dictionary subclass with callback when edited.

    If dictionary content given when initialized, all dictionaries are
    converted.
    Callback is not called for self.convert edits.

    convert - A dictionary (/nested) to convert | dictionary
        / Not required
    callback - A function to call when changes are made | function

    """

    def __init__(self, convert = None, callback = None, *a, **kw):
        #getLogger(pdname + "." + __name__ + ".CallbackOnEditDict.__init__").debug("CallbackOnEditDict initialized.")
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

    def callback(self, condition = None):
        #getLogger(pdname + "." + __name__ + ".CallbackOnEditDict.callback").debug("Callback called, {0}?, con: {0}".format(not self.setup_mode, condition))
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

    def convert(self, d = None):
        """Convert nested dictionaries into CallbackOnEditDict dictionaries.

        d - The dictionaries to convert and add to self | Dictionary
            / If not given, dictionaries already in self are converted.

        """
        if d is None or d is True:
            d = self
        self.setup_mode = True
        for k in d:
            if isinstance(d[k], dict):
                self[k] = CallbackOnEditDict(convert = d[k], callback = self._passed_callback)
            else:
                self[k] = d[k]
        self.setup_mode = False
        return


class SelfSavingFileDictionary(CallbackOnEditDict):
    """Self Saving File Dictionary.

    Loads json format data from file into self as a dictionary.
    On edit, saves dictionary the file.

    """
    def __init__(self, path, indent = 2):
        """Setup

        path - File path | String
        indent - Level of indentation | Integer

        """
        self.path = path
        self.indent = indent
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                if not f.read():
                    super().__init__(callback = self.save)
                else:
                    f.seek(0)
                    super().__init__(convert = json.load(f), callback = self.save)
        else:
            with open(self.path, "w") as f:
                super().__init__(callback = self.save)

    def save(self):
        """Auto-saving callback method."""
        with open(self.path, "w") as f:
            json.dump(self, f, indent = self.indent)
        return


class ActiveJSONDictionary(CallbackOnEditDict):
    """I/O JSON Dictionary.

    Loads json format data from function into self as a dictionary.
    On edit, saves dictionary the output.

    """
    def __init__(self, current, output, indent = 0):
        """Setup

        current - JSON data to load info dictionary | String
        output - Function to pass JSON string too | Function
        indent - Level of indentation | Integer

        """
        self.output = output
        self.indent = indent
        if current:
            super().__init__(convert = json.loads(current), callback = self.save)
        else:
            super().__init__(callback = self.save)

    def save(self):
        """Auto-saving callback method."""
        self.output(json.dumps(self, indent = self.indent))
        return


if __name__ == '__main__':
    main(__doc__)
