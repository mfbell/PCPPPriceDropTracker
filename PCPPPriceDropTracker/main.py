"""Main control functions."""

import platform
import queue
import argparse
from sys import exit
from threading import Event
from logging import getLogger
from time import sleep

import pystray
from PIL import Image

from GUI import GUI
from log_setup import setup as logging_setup
from tools import pdname, PD, ThreadTools


def app():
    """Main thread oporations."""
    logging_setup()
    logger = getLogger(pdname + "." + __name__ + ".main")
    logger.info("PCPPPriceDropTracker launching...")
    # Arg parser
    parser = argparse.ArgumentParser(prog = PD["project"]["name"],
                                     description = PD["project"]["description"])
    parser.add_argument("--background", action = "store_true", help = "Launch without GUI")
    args = parser.parse_args()
    # Launching
    gui = GUI()
    if not args.background:
        gui.launch()
    bg_thread = BackgroundThread(lambda: print("BGThread activity"))
    icon = SystrayIcon(launch_gui = gui.launch,
                       scan = lambda: print("Launch scan..."),
                       quit = gui.destroy)
    logger.debug("Main thread loop running.")
    gui.mainloop()
    logger.info("PCPPPriceDropTracker closing.")
    icon.quit()
    logger.info("PCPPPriceDropTracker closed.")
    exit(0)

class BackgroundThread(ThreadTools):

    def __init__(self, hits, run = True):
        self.hits = hits
        super().__init__(run = run, daemon = True)

    def run(self):
        c = 0
        while True:
            sleep(10)
            self.scan()
            self.hits()
            c += 1
        print("Backgound thread: End")

    def scan(self, *a):
        print("Backgound thread: Scan")


class SystrayIcon(ThreadTools):
    """System tray icon handler.

    Dev notes:
    https://media.readthedocs.org/pdf/pystray/latest/pystray.pdf
    http://pystray.readthedocs.io/en/latest/usage.html

    """

    def __init__(self, launch_gui, scan, quit, run = True):
        if platform.system() == "Darwin":
            # Platform unsupported.
            from GUI.customWidgets import MessageBox
            from tkinter import Tk
            root = Tk()
            root.withdraw()
            MessageBox(msg = ["OSX is not currently supported due to two modules needing to run in the main thread.",
                              "We will be working on a solution."],
                       title = "PCPPPriceDropTracker: OSX Unsupported",
                       buttons = {"close": ["Close", root.quit]},
                       grab = True,
                       on_close = root.quit)
            root.mainloop()
            exit(0)
        self.launch_gui_cmd = launch_gui
        self.scan_cmd = scan
        self.quit_cmd = quit
        super().__init__(run = run, daemon = True)

    def run(self):
        self.icon = pystray.Icon(PD["project"]["name"],
                                 icon = Image.open(".\PCPPPriceDropTracker\imgs\icon.png"),
                                 title = PD["project"]["name"])
        self.icon.menu = pystray.Menu(pystray.MenuItem("Open", self.launch_gui_cmd, default = True),
                                      pystray.MenuItem("Scan", self.scan_cmd),
                                      pystray.MenuItem("Exit", self.quit_cmd))
        getLogger(pdname + "." + __name__ + ".SystrayIcon.quit").debug("SystrayIcon build and running.")
        self.icon.run()

    def quit(self):
        getLogger(pdname + "." + __name__ + ".SystrayIcon.quit").debug("SystrayIcon quit.")
        self.icon.visible = False
        self.icon.stop()
