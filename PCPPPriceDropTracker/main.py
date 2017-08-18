"""Main control functions."""

import platform
import queue
from threading import Event
from logging import getLogger
from time import sleep

import pystray
from PIL import Image

from GUI import GUI
from log_setup import setup as logging_setup
from tools import pdname, PD, ThreadTools


def main():
    """Main thread oporations."""
    logging_setup()
    logger = getLogger(pdname + "." + __name__ + ".main")
    logger.info("PCPPPriceDropTracker launching...")
    # Because Tkinter...
    # does not like not running in the main thread.
    # This make it so much more complicated :( and pystray not working on
    # OSX. pystray was doing to be the mainloop but no...
    # Resulting in AppHandler, SystrayIcon and not just GUIHandler.
    gui = GUI()
    AppHandler(gui)
    logging.debug("Main thread loop running.")
    gui.mainloop()
    logger.info("PCPPPriceDropTracker finished.")
    exit(0)


class AppHandler(ThreadTools):
    """Main control thread."""

    def __init__(self, mainthread_queue, end, run = True):
        logger = getLogger(pdname + "." + __name__ + ".AppHandler.__init__")
        logger.debug("PCPPPriceDropTracker AppHandler launching...")
        self.background_thread_handler = BackgroundThread(self.end)
        self.gui_handler = GUIHandler()
        self.icon_handler = SystrayIcon(launch_gui = self.mainthread_queue.put(self.gui_handler.launch),
                                        scan = self.background_thread_handler.scan,
                                        quit = self.quit,
                                        mainthread_queue = self.mainthread_queue)
        super().__init__(run = run)

    def run(self):
        pass

    def quit(self, *a):
        self.end.set()
        self.icon_handler.quit()
        self.gui_handler.quit()


class GUIHandler():

    gui = None

    def launch(self, *a):
        if self.gui is not None:
            return
        self.gui = GUIMain()
        self.gui.mainloop()
        self.gui = None



    def quit(self):
        if self.gui:
            self.gui.quit()


class BackgroundThread(ThreadTools):

    def __init__(self, end, run = True):
        self.end = end
        super().__init__(run = run)

    def run(self):
        c = 0
        while self.end.is_set() is not True:
            sleep(5)
            print("Backgound thread: {0}".format(c))
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

    def __init__(self, launch_gui, scan, quit, mainthread_queue, run = True):
        if platform.platform() == "Darwin":
            # Platform unsupported.
            from widgets.customWidgets import MessageBox
            root = tk.Tk()
            MessageBox(msg = ["OSX is not currently supported due to two mainloops must run the the main thread on OSX.",
                              "We will be working on a solution."],
                       title = "OSX Unsupported",
                       buttons = {"close": ["Close", root.quit]},
                       grab = True)
            root.mainloop()
            exit(0)
        self.launch_gui = launch_gui
        self.scan = scan
        self.quit = quit
        self.mtq = mainthread_queue
        super().__init__(run = run)
        return

    def run(self):
        self.icon = pystray.Icon(PD["project"]["name"],
                                 icon = Image.open(".\PCPPPriceDropTracker\imgs\icon.png"),
                                 title = PD["project"]["name"])
        self.icon.menu = pystray.Menu(pystray.MenuItem("Open", lambda: self.mtq.put(self.launch_gui), default = True),
                                      pystray.MenuItem("Scan", lambda: self.mtq.put(self.launch_gui)),
                                      pystray.MenuItem("Exit", lambda: self.mtq.put(self.launch_gui)))
        self.icon.run()

    def quit(self):
        self.icon.stop()
