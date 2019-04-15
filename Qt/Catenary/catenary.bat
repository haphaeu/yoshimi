@echo off
echo Launching application in a conda environment...
call  C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
call conda activate qt5
if errorlevel 1 (
    echo !!!
    echo !!! Error activating environemt.
    echo !!! Have you run the installer?
    echo !!!
    goto :EOF
)
cd /d %~dp0
python catenary_qt5.py
