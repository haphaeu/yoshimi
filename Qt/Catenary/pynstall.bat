:: need to install pyinstall
::  > pip install pyinstaller

pyinstaller --clean --windowed --add-data="catenary.ui;." --add-data="icon.png;." catenary.py

pause