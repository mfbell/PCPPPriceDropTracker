"""Custom Widgets.

This module does not contain PCPPPriceDropTracker specific widgets and can be
used universally.

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

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from logging import getLogger
try:
    from .tools import Tools, Thread_tools, get_number_in_range
    from .tools import main as mainprint
except ImportError as e:
    try:
        from tools import Tools, Thread_tools, get_number_in_range
        from tools import main as mainprint
    except Exception:
        raise e


class Panel(ttk.Frame, Tools):
    """"Parent panel class."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Same args as ttk.Frame and Tools."""
        getLogger(__name__+".Panel.__init__").debug("Panel object called.")
        self.root = root
        Tools.__init__(self, *args, **kwargs)
        ttk.Frame.__init__(self, self.root, *self.args, **self.kwargs)
        return None


class MessageBox(tk.Toplevel, Tools):
    """Custom message box."""

    def __init__(self, *args, **kwargs):
        """Initialization.

        kwargs (none are required):
        msg - One or more messages to show | string, tk Var or list of them
            / If a list if given, they are stacked below each other.
        title - The title for the windows | string
            / Default to "Message"
        icon - Path of an icon | string
            / NOTE: To be added
        buttons - A list of "button data" | dictionary
            / {"id": ["Button text" or tk Vars, Function to call when pressed], ...}
            / Other button setting can be set though <self>.buttons[id]
        focus - Run focus_set() | boolean
            / Defaults to True
        grab - Run grab_set() | boolean
            / Defaults to False

        Support for icon will come and I may add a defult button state too.
        Entry box maybe?

        """
        logger = getLogger(__name__+".MessageBox.__init__")
        logger.debug("MessageBox initialization.")
        tk.Toplevel.__init__(self)
        if "msg" in kwargs:
            msg = kwargs["msg"]
            if not isinstance(msg, list):
                msg = [msg]
        else:
            msg = []
        logger.debug("Messages: {0}".format(msg))
        if "title" in kwargs:
            self.title = kwargs["title"]
        else:
            self.title = "Message"
        logger.debug("Title: {0}".format(self.title))
        if "icon" in kwargs:
            icon_path = kwargs["icon"]
        else:
            icon_path = ".\PCPPPriceDropTracker\imgs\info_icon.png"
        logger.debug("Icon path: {0}".format(icon_path))
        if "buttons" in kwargs:
            buttons = kwargs["buttons"]
        else:
            buttons = {}
        logger.debug("Buttons: {0}".format(buttons))
        if not "padding" in kwargs:
            kwargs["padding"] = 10
        Tools.__init__(self, *args, **kwargs)

        # mainframe of padding
        self.main = ttk.Frame(self, padding=6)
        self.main.pack()

        # messages
        self.msgs = []
        for m in msg:
            if isinstance(m, type(tk.StringVar())):
                self.msgs.append(ttk.Label(self.main, textvariable=m))
                print("adding msg: " + m.get())
            else:
                self.msgs.append(ttk.Label(self.main, text=m))
        c = 4
        for m in self.msgs:
            m.grid(column=4, row=c, padx=3)
            c += 1
        # icon
        try:
            self.icon_image = ImageTk.PhotoImage(Image.open(icon_path).resize((48, 48), Image.ANTIALIAS))
            self.icon = ttk.Label(self.main, image=self.icon_image)
            self.icon.grid(column=2, row=4, rowspan=c-4, pady=6, padx=6)
        except FileNotFoundError:
            logger.exception("FileNotFoundError while adding icon.")

        # Splitter
        self.bar = ttk.Separator(self.main, orient="horizontal")
        self.bar.grid(column=0, columnspan=99, row=c+1, sticky="ew", pady=6)
        # buttons
        self.buttons = {}
        self.button_frame = ttk.Frame(self.main)
        self.button_frame.grid(column=4, row=c+2, sticky="e")
        c = 0
        for b in buttons:
            if buttons[b][1] == "KILL":
                buttons[b][1] = self.destroy
            elif buttons[b][1] == "ICONIFY":
                buttons[b][1] = self.iconify
            elif buttons[b][1] == "WITHDRAW":
                buttons[b][1] = self.withdraw
            if isinstance(buttons[b][0], type(tk.StringVar())):
                self.buttons[b] = ttk.Button(self.button_frame, textvariable=buttons[b][0], command=buttons[b][1])
            else:
                self.buttons[b] = ttk.Button(self.button_frame, text=buttons[b][0], command=buttons[b][1])
            self.buttons[b].grid(column=c, row=0)
            c +=1
        if ("focus" in self.kwargs and self.kwargs["focus"]) or "focus" not in self.kwargs:
            self.focus_set()
        if "grab" in kwargs and kwargs["grab"]:
            self.grab_set()
        logger.debug("MessageBox setup.")
        return None


class ScrollablePanel(Panel):
    """Custom scrolling frame widget.

    With auto resizing, max sizes, min sizes, scroll wheel auto (un)binding for
    x and y and more.
    Based off code writen by Mikhail T.
    https://stackoverflow.com/a/37861801/5990054

    """

    def __init__(self, root, *args, **kwargs):
        """Initialization.

        Args as of Panel. Plus:
        kwargs:
        max_width - Max widget width, excluding Y Scrollbar | function
        max_height - Max widget height, including X Scrollbar | function
        min_width - Min widget width, excluding Y Scrollbar | function
        min_height - Min widget height, excluding Y Scrollbar | function

        """
        logger = getLogger(__name__+".ScrollablePanel.__init__")
        logger.debug("ScrollablePanel called.")
        self.sizes = {}
        if "max_width" in kwargs:
            self.sizes["max_width"] = kwargs["max_width"]
            del(kwargs["max_width"])
        else:
            self.sizes["max_width"] = None
        if "max_height" in kwargs:
            self.sizes["max_height"] = kwargs["max_height"]
            del(kwargs["max_height"])
        else:
            self.sizes["max_height"] = None
        if "min_width" in kwargs:
            self.sizes["min_width"] = kwargs["min_width"]
            del(kwargs["min_width"])
        else:
            self.sizes["min_width"] = None
        if "min_height" in kwargs:
            self.sizes["min_height"] = kwargs["min_height"]
            del(kwargs["min_height"])
        else:
            self.sizes["min_height"] = None
        super().__init__(root, *args, **kwargs)

        self.xscrlbr = ttk.Scrollbar(self, orient="horizontal")
        self.yscrlbr = ttk.Scrollbar(self, orient="vertical")
        self.canvas = tk.Canvas(self)
        self.canvas.config(relief="flat", width=20, heigh=20, bd=2)
        self.xscrlbr.config(command=self.canvas.xview)
        self.yscrlbr.config(command=self.canvas.yview)
        self.scrollwindow = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.scrollwindow, anchor="nw")
        self.canvas.config(xscrollcommand = self.xscrlbr.set,
                         yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, 10, 10))
        self.xscrlbr.grid(column=0, row=1, sticky="ew", columnspan=2)
        self.yscrlbr.grid(column=1, row=0, sticky="ns")
        self.canvas.grid(column=0, row=0)
        self.yscrlbr.lift(self.scrollwindow)
        self.xscrlbr.lift(self.scrollwindow)

        self.scrollwindow.bind("<Configure>", self._configure_window)
        self.scrollwindow.bind("<Enter>", self._bound_to_mousewheel_y)
        self.scrollwindow.bind("<Leave>", self._unbound_to_mousewheel)
        self.xscrlbr.bind("<Enter>", self._bound_to_mousewheel_x)
        self.xscrlbr.bind("<Leave>", self._unbound_to_mousewheel)
        self.yscrlbr.bind("<Enter>", self._bound_to_mousewheel_y)
        self.yscrlbr.bind("<Leave>", self._unbound_to_mousewheel)
        logger.debug("ScrollablePanel setup complete.")
        return None

    def _bound_to_mousewheel_x(self, event):
        """Mouse bind."""
        #getLogger(__name__+".ScrollablePanel._bound_to_mousewheel").debug("Binding mouse wheel scroll to ybar.")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_x)

    def _bound_to_mousewheel_y(self, event):
        """Mouse bind."""
        #getLogger(__name__+".ScrollablePanel._bound_to_mousewheel").debug("Binding mouse wheel scroll to ybar.")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_y)

    def _unbound_to_mousewheel(self, event):
        """Mouse unbind."""
        #getLogger(__name__+".ScrollablePanel._unbound_to_mousewheel").debug("Unbinding mouse wheel scroll to ybar.")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel_y(self, event):
        """Mouse scroll."""
        #getLogger(__name__+".ScrollablePanel._on_mousewheel").debug("MouseWheel scroll")
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_mousewheel_x(self, event):
        """Mouse scroll."""
        #getLogger(__name__+".ScrollablePanel._on_mousewheel").debug("MouseWheel scroll")
        self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        logger = getLogger(__name__+".ScrollablePanel._configure_window")
        logger.debug("Update widgets.")
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        logger.debug("Current size %s", size)
        self.canvas.config(scrollregion="0 0 {0} {1}".format(*size))
        if self.scrollwindow.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas"s width to fit the inner frame
            self.canvas.config(width=self._size_cal("width"))
        if self.scrollwindow.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvas"s width to fit the inner
            self.canvas.config(height=self._size_cal("height"))
        return

    def _size_cal(self, dimension, *args, **kwargs):
        """Return size for canvas config.

        dimension - width or height | string

        """
        logger = getLogger(__name__+".ScrollablePanel._size_cal")
        logger.debug("Size calculator called.")
        logger.debug("Values given: max_width {max_width}, max_heighth {max_height}, min_width {min_width}, min_height {min_height}".format(**self.sizes))
        needed, scrollbar = self._get_dimensions(dimension)
        if self.sizes["min_" + dimension] is None and self.sizes["max_" + dimension] is None:
            return needed # No need to remove scrollbar space as there is no set size.
        elif self.sizes["min_" + dimension] is None and self.sizes["max_" + dimension]:
            return get_number_in_range(needed, max_=self.sizes["max_" + dimension]() - scrollbar)
        elif self.sizes["max_" + dimension] is None and self.sizes["min_" + dimension]:
            return get_number_in_range(needed, min_=self.sizes["min_" + dimension]() - scrollbar)
        else:
            return get_number_in_range(needed, min_=self.sizes["min_" + dimension]() - scrollbar, max_=self.sizes["max_" + dimension]() - scrollbar)

    def _get_dimensions(self, dimension):
        """Get needed size of scrollwindow and size of scrollbar.

        dimension - width or height | string

        """
        getLogger(__name__+".ScrollablePanel._get_dimensions").debug("_get_dimensions called.")
        if dimension == "width":
            return self.scrollwindow.winfo_reqwidth(), self.yscrlbr.winfo_width()
        elif dimension == "height":
            return self.scrollwindow.winfo_reqheight(), self.xscrlbr.winfo_height()
        else:
            raise ValueError("Invalid value for dimension: {0}".format(dimension))
        return



def main():
    mainprint(__doc__, xit=False)
    mb = MessageBox(msg=["Updating...", "This is my really long message for a MessageBox"], buttons={"ok":["OK", lambda: print("OK")]}, title="Updating")
    mb.mainloop()
    return None


if __name__ == "__main__":
    main()
