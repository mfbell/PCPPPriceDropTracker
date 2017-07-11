"""PCPPPriceDropTracker main __init__ module."""

from tools import main
from app import main as app_main
from log_setup import setup


def run():
    setup()
    app_main()

if __name__ == '__main__':
    main(__doc__, ixt=False)
    run()
