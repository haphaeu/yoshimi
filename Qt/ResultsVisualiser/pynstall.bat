:: need to install pyinstall
::  > pip install pyinstaller

pyinstaller --clean --windowed --add-data="help.txt;." --add-data="icon.png;." results_visualiser.py

pause