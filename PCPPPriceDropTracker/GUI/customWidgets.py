"""Custom Widgets.

Custom widgets writen for PCPPPriceDropTracker.

All widgets use the grid manager.

"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from logging import getLogger
from os.path import basename

from tools import Thread_tools, get_number_in_range, pdname, main

__all__ = ["Panel", "MessageBox", "ScrollablePanel", "AutoHidingScollbar", "FileList",
           "FileEntry", "FilePathEntry"]

class _Limitation():
    """Some methods to inherit to limit functions/explain error."""

    def pack(self, *a, **kw):
        raise tk.TclError("Cannot use pack with this widget.")

    def place(self, *a, **kw):
        raise tk.TclError("Cannot use place with this widget.")


class Panel(ttk.Frame):
    """"Parent panel class."""

    def __init__(self, master, *args, **kwargs):
        """Initialization. Same args as ttk.Frame and Tools."""
        getLogger(pdname + "." + __name__ + ".Panel.__init__").debug("Panel object called.")
        self.master = master
        ttk.Frame.__init__(self, self.master, *args, **kwargs)
        return


class MessageBox(tk.Toplevel, _Limitation):
    """Custom message box."""

    def __init__(self, msg = [], title = "MessageBox", icon = None, buttons = {}, focus = True, grab = None, on_close = None):
        """Initialization.

        msg - One or more messages to show | string, tk Var or list of them
            / If a list if given, they are stacked below each other.
        title - The title for the windows | string
            / Default to "Message"
        icon - Path of an icon | string
        buttons - A list of "button data" | dictionary
            / {"id": ["Button text" or tk Vars, Function to call when pressed], ...}
            / Other button setting can be set though <self>.buttons[id]
        focus - Run focus_set() | boolean
            / Defaults to True
        grab - Run grab_set() | boolean
            / Defaults to False
        on_close - Callback for if the window is closed | function
            / Defaults to nothing

        """
        logger = getLogger(pdname + "." + __name__ + ".MessageBox.__init__")
        logger.debug("MessageBox initialization.")
        tk.Toplevel.__init__(self)
        self.main = ttk.Frame(self, padding = 6)
        self.main.grid()
        # Messages
        if not isinstance(msg, list):
            msg = [msg]
        self.msgs = []
        for m in msg:
            if isinstance(m, type(tk.StringVar())):
                self.msgs.append(ttk.Label(self.main, textvariable = m))
            else:
                self.msgs.append(ttk.Label(self.main, text = m))
        c = 4
        for m in self.msgs:
            m.grid(column = 4, row = c, padx = 3)
            c +=  1
        # Title
        self.title(title)
        # Icon
        if icon:
            try:
                self.icon_image = ImageTk.PhotoImage(Image.open(icon).resize((48, 48), Image.ANTIALIAS))
                self.icon = ttk.Label(self.main, image = self.icon_image)
            except FileNotFoundError as e:
                self.icon = ttk.Label(self.main, text = "----------\nIcon couldn't be found\n----------")
                logger.exception(("FileNotFoundError while adding icon.", e))
            self.icon.grid(column = 2, row = 4, rowspan = c - 4, pady = 6, padx = 6)
        # Splitter
        self.bar = ttk.Separator(self.main, orient = "horizontal")
        self.bar.grid(column = 0, columnspan = 99, row = c + 1, sticky = "ew", pady = 6)
        # Buttons
        self.buttons = {}
        self.button_frame = ttk.Frame(self.main)
        self.button_frame.grid(column = 4, row = c + 2, sticky = "e")
        c = 0
        for b in buttons:
            if buttons[b][1]  ==  "KILL":
                buttons[b][1] = self.destroy
            elif buttons[b][1]  ==  "ICONIFY":
                buttons[b][1] = self.iconify
            elif buttons[b][1]  ==  "WITHDRAW":
                buttons[b][1] = self.withdraw
            if isinstance(buttons[b][0], type(tk.StringVar())):
                self.buttons[b] = ttk.Button(self.button_frame, textvariable = buttons[b][0], command = buttons[b][1])
            else:
                self.buttons[b] = ttk.Button(self.button_frame, text = buttons[b][0], command = buttons[b][1])
            self.buttons[b].grid(column = c, row = 0)
            c += 1
        # Other
        if focus:
            self.focus_set()
        if grab:
            self.grab_set()
        if on_close:
            self.protocol('WM_DELETE_WINDOW', on_close)
        logger.debug("MessageBox setup.")
        return


class ScrollablePanel(Panel, _Limitation):
    """Custom scrolling frame widget.

    With auto resizing, max sizes, min sizes, auto-scollbars, scroll wheel auto
    (un)binding for x and y and more.

    """

    def __init__(self, master, max_width = None, max_height = None, min_width = None, min_height = None, *args, **kwargs):
        """Initialization.

        max_width - Max widget width
        max_height - Max widget height
        min_width - Min widget width
        min_height - Min widget height
            / All include scrollbars in that range if they are pressent.
            / Function or integer.

        The minumun size at 32 by 32 or I could not get it working, and it
        looped unsure if to hide or show the scrollbars. :\
        May work lower than that, I did get it working vertical at 20 but
        leaving it at that.

        """
        logger = getLogger(pdname + "." + __name__ + ".ScrollablePanel.__init__")
        logger.debug("ScrollablePanel called.")
        self._sizes = {"max_width": max_width,
                       "max_height": max_height,
                       "min_width": min_width,
                       "min_height": min_height}
        super().__init__(master, *args, **kwargs)
        self.xscrlbr = AutoHidingScollbar(self, show_callback = self._bind_x,
                                          hide_callback = self._unbind_x,
                                          orient = "horizontal", name = "ybar")
        self.yscrlbr = AutoHidingScollbar(self, show_callback = self._bind_y,
                                          hide_callback = self._unbind_y,
                                          orient = "vertical", name = "xbar")
        self.canvas = tk.Canvas(self)
        self.canvas.config(relief = "flat", width = 20, heigh = 20, bd = 2)
        self.xscrlbr.config(command = self.canvas.xview)
        self.yscrlbr.config(command = self.canvas.yview)
        self.scrollwindow = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window = self.scrollwindow, anchor = "nw")
        self.canvas.config(xscrollcommand = self.xscrlbr.set,
                           yscrollcommand = self.yscrlbr.set,
                           scrollregion = (0, 0, 10, 10))
        self.xscrlbr.grid(column = 0, row = 1, sticky = "ew") #, columnspan = 2)
        self.yscrlbr.grid(column = 1, row = 0, sticky = "ns")
        self.canvas.grid(column = 0, row = 0, sticky = "nswe")
        self.yscrlbr.lift(self.scrollwindow)
        self.xscrlbr.lift(self.scrollwindow)

        # I would bind self to y scroll but it makes tranfer between y and x
        # complex to a level which I will not use in my project.
        # Only useful when you make self bigger than contence in
        # scrollwindow, to cover unused frame space.
        self.scrollwindow.bind("<Configure>", self._configure_window)
        logger.debug("ScrollablePanel setup complete.")
        return

    def update(self):
        return self._configure_window(None)

    def _bind_y(self):
        """Bind all y binds."""
        self.scrollwindow.bind("<Enter>", self._bound_to_mousewheel_y)
        self.scrollwindow.bind("<Leave>", self._unbound_to_mousewheel)
        self.yscrlbr.bind("<Enter>", self._bound_to_mousewheel_y)
        self.yscrlbr.bind("<Leave>", self._unbound_to_mousewheel)
        return

    def _unbind_y(self):
        """Unbind all y binds."""
        self.scrollwindow.unbind("<Enter>")
        self.scrollwindow.unbind("<Leave>")
        self.yscrlbr.unbind("<Enter>")
        self.yscrlbr.unbind("<Leave>")
        return

    def _bind_x(self):
        """Bind all x binds."""
        self.xscrlbr.bind("<Enter>", self._bound_to_mousewheel_x)
        self.xscrlbr.bind("<Leave>", self._unbound_to_mousewheel)
        return

    def _unbind_x(self):
        self.xscrlbr.unbind("<Enter>")
        self.xscrlbr.unbind("<Leave>")
        return

    def _bound_to_mousewheel_x(self, event):
        """Mouse bind x."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_x)
        return

    def _bound_to_mousewheel_y(self, event):
        """Mouse bind y."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_y)
        return

    def _unbound_to_mousewheel(self, event):
        """Mouse unbind."""
        self.canvas.unbind_all("<MouseWheel>")
        return

    def _on_mousewheel_y(self, event):
        """Mouse scroll y."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return

    def _on_mousewheel_x(self, event):
        """Mouse scroll x."""
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        return

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        logger = getLogger(pdname + "." + __name__ + ".ScrollablePanel._configure_window")
        logger.debug("Update widgets.")
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        logger.debug("Current size %s", size)
        self.canvas.config(scrollregion = self.canvas.bbox("all"))
        if self.scrollwindow.winfo_reqwidth() !=  self.canvas.winfo_width():
            # update the canvas"s width to fit the inner frame
            self.canvas.config(width = self._size_cal("width"))
        if self.scrollwindow.winfo_reqheight() !=  self.canvas.winfo_height():
            # update the canvas"s width to fit the inner
            self.canvas.config(height = self._size_cal("height"))
        return

    def _size_cal(self, dimension, *args, **kwargs):
        """Return size for canvas config.

        dimension - width or height | string

        """
        logger = getLogger(pdname + "." + __name__ + ".ScrollablePanel._size_cal")
        logger.debug("Size calculator called.")
        #logger.debug("Values given: max_width {max_width}, max_heighth {max_height}, min_width {min_width}, min_height {min_height}".format(**self.sizes()))
        needed, scrollbar = self._get_dimensions(dimension)
        if self.sizes("min_" + dimension) is None and self.sizes("max_" + dimension) is None:
            return needed # No need to remove scrollbar space as there is no set size.
        elif self.sizes("min_" + dimension) is None and self.sizes("max_" + dimension):
            return get_number_in_range(needed, max_ = self.sizes("max_" + dimension) - scrollbar)
        elif self.sizes("max_" + dimension) is None and self.sizes("min_" + dimension):
            return get_number_in_range(needed, min_ = self.sizes("min_" + dimension) - scrollbar)
        else:
            return get_number_in_range(needed, min_ = self.sizes("min_" + dimension) - scrollbar, max_ = self.sizes("max_" + dimension) - scrollbar)

    def _get_dimensions(self, dimension):
        """Get needed size of scrollwindow and size of scrollbar.

        dimension - width or height | string

        """
        getLogger(pdname + "." + __name__ + ".ScrollablePanel._get_dimensions").debug("_get_dimensions called.")
        if dimension  ==  "width":
            return self.scrollwindow.winfo_reqwidth(), self.yscrlbr.winfo_width() if not "disabled" in self.yscrlbr.state() else 0
        elif dimension  ==  "height":
            return self.scrollwindow.winfo_reqheight(), self.xscrlbr.winfo_height() if not "disabled" in self.xscrlbr.state() else 0
        else:
            raise ValueError("Invalid value for dimension: {0}".format(dimension))
        return

    def sizes(self, size = None):
        """Return filtered dimension given when object was called.

        Filtered been, if dimension given was below 32, 32 is return.

        size - dimension name | string or None
            / Or None to return all as dictionary.
            / Defaults to all.
        """
        if size is None:
            d = {}
            for key in self._sizes:
                if callable(self._sizes[key]):
                    d[key] = self._sizes[key]() if self._sizes[key]() >= 32 else 32
                else:
                    d[key] = self._sizes[key] if self._sizes[key] is None or self._sizes[key] >= 32 else 32
            return d
        else:
            try:
                if callable(self._sizes[size]):
                    return self._sizes[size]() if self._sizes[size]() is None or self._sizes[size]() >=  32 else 32
                else:
                    return self._sizes[size] if self._sizes[size] is None or self._sizes[size] >=  32 else 32
            except KeyError:
                raise ValueError("Invalid dimension given.")


class AutoHidingScollbar(ttk.Scrollbar, _Limitation):
    """A scrollbar which hides itself if it is not needed, reappearing when needed.

    With callbacks when hide and show.

    """

    def __init__(self, master, show_callback = None, hide_callback = None, *args, **kwargs):
        """Initialization.

        show_callback - Function to call when shown | Function
        hide_callback - Function to call when hiden | Function
            / Both are not required.
        Standard Scrollbar args too.

        """
        self.show_callback = show_callback
        self.hide_callback = hide_callback
        super().__init__(*args, **kwargs)
        return

    def set(self, lo, hi):
        """Modified set."""
        logger = getLogger(pdname + "." + __name__ + ".AutoHidingScollbar.set")
        logger.debug("AutoHidingScollbar Set called with: {0} {1}".format(lo, hi))
        logger.debug("Passed to super")
        if float(lo) <=  0.0 and float(hi) >=  1.0:
            self.grid_remove()
            if self.hide_callback:
                self.hide_callback()
            logger.debug("Hiden")
        else:
            self.grid()
            if self.show_callback:
                self.show_callback()
            logger.debug("Shown")
        ttk.Scrollbar.set(self, lo, hi)
        return


class FileList(ScrollablePanel):
    """Multi-FileEntry widget in a ScrollablePanel.

    Each path is given a FileEntry which is call contrained in this object.
    The path of the pressed widget is passed to the argument 'path' when called.

    FileList.build can be called at anytime to add more FileEntrys.
    FileList.entries is the list containing the FileEntry objects.

    """

    def __init__(self, master, callback, paths = [], *args, **kwargs):
        """Initialization

        master - Master widget | object
        callback - Function to call when a FileEntry is pressed | Function
        path - A list of paths | list[str, ...]
            / Not required
        Args and kwargs passed to ScrollablePanel.

        """
        logger = getLogger(pdname + "." + __name__ + ".FileList")
        logger.debug("FileList initalization.")
        super().__init__(master, *args, **kwargs)
        self.callback = callback
        self.build(paths)
        logger.debug("Filelist setup complete.")
        return

    def build(self, paths):
        """Creation function of FileEntrys

        path - A list of paths | list[str, ...]

        """
        self.scrollwindow.entries = []
        for path in paths:
            e = FileEntry(self.scrollwindow, path, callback = self.callback, takefocus = True, padding = 3, relief = "groove")
            e.grid(column = 0, row = len(self.scrollwindow.entries), sticky = "new", pady = 2, padx = 6)
            self.scrollwindow.entries.append(e)
        self.entries = self.scrollwindow.entries
        return


class FileEntry(Panel):
    """File path button widget."""

    def __init__(self, master, path, callback, name_style = "TLabel", path_style = "TLabel", *args, **kwargs):
        """Initialization

        master - Master widget | object
        callback - Function to call when pressed | Function
        path - Path string | String
        Args and kwargs passed to Panel.

        When pressed the path is passed to the callback argument 'path'.

        """
        super().__init__(master, *args, **kwargs)
        self.path = path
        self.name_style = name_style
        self.path_style = path_style
        self.callback_ = callback
        self.lname = ttk.Label(self, text = basename(path), style = self.name_style, padding = 2)
        self.lpath = ttk.Label(self, text = path, style = self.path_style, padding = 2)

        self.lname.grid(column = 0, row = 0, sticky = "nw")
        self.lpath.grid(column = 0, row = 1, sticky = "nw")

        self.bind("<Button-1>", self.callback)
        self.lname.bind("<Button-1>", self.callback)
        self.lpath.bind("<Button-1>", self.callback)

    def callback(self, event):
        self.callback_(path = self.path, event = event)


class FilePathEntry(Panel):
    """File entry widget, old style.

    With entry box, system UI dialog button and action button.
    If the action button is pressed without there been anything in the entry box
    the system UI dialog is called.
    Returning from the system UI dialog with a string triggers a callback.

    The path is given to the callback under the argument 'path'.

    """

    def __init__(self, master, callback, action_text, finder, *args, **kwargs):
        """Initialization.

        master - Master widget | Object
        callback - Function to call when path is choosen | Function
        action_text - Text to display on main button | String
        finder - System UI dialog to launch | Function or String
            / Either pass a callable which returns the choosen path on completion
              Or 'getopenfile', 'getsavefile' or 'choosedirectory' for
              Tkinter.filedialog options.
        Args and kwargs passed to Panel.

        """
        super().__init__(master, *args, **kwargs)
        self.callback_ = callback
        self.action_text = action_text
        if isinstance(finder, str):
            if finder.lower()  ==  "getopenfile":
                self.finder = filedialog.askopenfilename
            elif finder.lower()  ==  "getsavefile":
                self.finder = filedialog.asksaveasfilename
            elif finder.lower()  ==  "choosedirectory":
                self.finder = filedialog.askdirectory
            else:
                raise ValueError("Invalid finder arg.")
        elif callable(finder):
            self.finder = finder
        else:
            raise ValueError("Invalid finder arg.")
        self.path = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable = self.path)
        self.find_button = ttk.Button(self, text = "...", command = self.ask, width = 2)
        self.open_button = ttk.Button(self, text = action_text, command = self.callback)
        self.entry.grid(column = 0, row = 0, sticky = "we")
        self.find_button.grid(column = 1, row = 0)
        self.open_button.grid(column = 2, row = 0)
        self.grid_columnconfigure(0, weight = 1)
        return

    def ask(self):
        path = self.finder()
        if not path:
            return
        else:
            self.path.set(path)
            self.callback()

    def callback(self):
        path = self.path.get()
        if not path:
            self.ask()
        else:
            self.callback_(path = path, event = self.finder)


if __name__  ==  "__main__":
    main(__doc__)
