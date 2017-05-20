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
from tools import Tools, Thread_tools
from tools import main as mainprint


class Panel(ttk.Frame, Tools):
    """"Parent panel class."""

    def __init__(self, root, *args, **kwargs):
        """Initialization. Same args as ttk.Frame and Tools."""
        self.root = root
        Tools.__init__(self, *args, **kwargs)
        ttk.Frame.__init__(self, self.root, *self.args, **self.kwargs)
        return None


class MessageBox(tk.Toplevel, Tools):
    """Custom message boxes."""

    def __init__(self, *args, **kwargs):
        """Initialization.

        kwargs (none are required):
        msg - One or more messages to show | string, tk Var or list of them
            / If a list if given, they are stacked below each other.
        title - The title for the windows | string
            / Default to 'Message'
        icon - Path of an icon | string
            / NOTE: To be added
        buttons - A list of 'button data' | dictionary
            / {"id": ["Button text" or tk Vars, Function to call when pressed], ...}
            / Other button setting can be set though <self>.buttons[id]
        focus - Run focus_set() | boolean
            / Defaults to True
        grab - Run grab_set() | boolean
            / Defaults to False

        Support for icon will come and I may add a defult button state too.
        Entry box maybe?

        """
        tk.Toplevel.__init__(self)
        if "msg" in kwargs:
            msg = kwargs["msg"]
            if not isinstance(msg, list):
                msg = [msg]
        else:
            msg = []
        if "title" in kwargs:
            self.title = kwargs["title"]
        else:
            self.title = "Message"
        if "icon" in kwargs:
            icon_path = kwargs["icon"]
        else:
            icon_path = ".\info_icon.png"
        if "buttons" in kwargs:
            buttons = kwargs["buttons"]
        else:
            buttons = {}
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
            pass

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





def main():
    mainprint(__doc__, xit=False)
    mb = MessageBox(msg=["Updating...", "This is my really long message for a MessageBox"], buttons={"ok":["OK", lambda: print("OK")]}, title="Updating")
    mb.mainloop()
    return None


if __name__ == '__main__':
    main()
