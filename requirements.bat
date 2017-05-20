
::===============================================
:: Just a simple requirements install script.
:: Probably could be done much better.
:: Also tests them.
::
:: Written by mtech0 | https://github.com/mtech0
::===============================================

@echo OFF
pip install beautifulsoup4
pip install requests
pip install Pillow
python -c "import bs4; import requests; import PIL, print('[Test]: Successful :)');"
PAUSE
