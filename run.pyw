"""Run file for PCPPPriceDropTracker

Runs without console.

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

import PCPPPriceDropTracker

def main():
    """Run."""
    PCPPPriceDropTracker.run()
    exit(0)

if __name__ == '__main__':
    main()
