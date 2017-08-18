"""The logging module of PCPPPriceDropTracker.

"""

import logging
import logging.config
from time import strftime
import os

from tools import main, get_git_commit_hash, pdname


DATETIME = strftime("%Y-%m-%d %H-%M-%S")
LOG_DIR = ".\logs"
LOG_FILE_FIRST_LINE = """PCPPPriceDropTracker Log File
Commit Version: {0} ({1})
//Should add a sha hash of files so logs can be IDed when in development//
//Credits here//

""".format(get_git_commit_hash("short"), get_git_commit_hash())

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        pdname : {
            "level": "INFO",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False
        },
        pdname + ".GUI.main.GUI": {
            "level": "DEBUG",
            "propagate": True
        },
        pdname + ".main": {
            "level": "DEBUG",
            "propagate": True
        }
    },
    "handlers": {
        "consoleHandler": {
            "level": "DEBUG",
            "formatter": "console",
            "class": "logging.StreamHandler",
        },
        "fileHandler": {
            "level": "DEBUG",
            "formatter": "file",
            "class": "logging.FileHandler",
            "filename": "{0}\{1}.log".format(LOG_DIR, DATETIME)
        }
    },
    "formatters": {
        "file": {
            "format": "{asctime} | {levelname:8s} | line {lineno:<4} in {name:60s} - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
            "style": "{"
        },
        "console": {
            "format": "{asctime} | {levelname:8s} | line {lineno:<4} in {name:60s} \n{message}\n",
            "datefmt": "%H:%M:%S",
            "style": "{"
        }
    },
}

def setup():
    """Load logging config."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.config.dictConfig(LOG_CONFIG)
    # Only covers handlers using logging.FileHandler
    for handler in LOG_CONFIG["handlers"]:
        if LOG_CONFIG["handlers"][handler]["class"] == "logging.FileHandler":
            with open(LOG_CONFIG["handlers"][handler]["filename"], "a") as f:
                f.write(LOG_FILE_FIRST_LINE)
    return

if __name__ == "__main__":
    main(__doc__)
