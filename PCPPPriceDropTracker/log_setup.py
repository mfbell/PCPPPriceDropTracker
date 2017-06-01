"""The logging module of PCPPPriceDropTracker.



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

import logging
import logging.config
from time import strftime
import os
from .tools import main

LOG_DIR = ".\logs"
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "PCPPPriceDropTracker": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "fileHandler"],
            "propagate": False
        }
    },
    "handlers": {
        "consoleHandler": {
            "level": "ERROR",
            "formatter": "console",
            "class": "logging.StreamHandler",
            #"args": (sys.stdout, )
        },
        "fileHandler": {
            "level": "DEBUG",
            "formatter": "file",
            "class": "logging.FileHandler",
            "filename": LOG_DIR + strftime("\%Y-%m-%d %H-%M-%S.log"),
        }
    },
    "formatters": {
        "file": {
            "format": "{asctime} | {levelname:8s} | line {lineno:<4} in {name:60s} - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
            "style": "{"
        },
        "console": {
            "format": "{asctime} | {levelname:8s} | line {lineno:<4} in {name:60s} - {message}",
            "datefmt": "%H:%M:%S",
            "style": "{"
        }
    },
}

def setup():
    """Load logging config."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.config.dictConfig(logging_config)
    return None

if __name__ == "__main__":
    main(__doc__)
