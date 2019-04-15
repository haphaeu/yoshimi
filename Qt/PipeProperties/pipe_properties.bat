@echo off
echo Launching application in a conda environment...
call  C:\Anaconda3\Scripts\activate.bat C:\Anaconda3
call conda activate qt5
if errorlevel 1 (
    echo !!!
    echo !!! Error activating environemt.
    echo !!! Have you run the installer?
    echo !!!
    ::goto :EOF
    echo Trying to lauch the application anyway...
)
cd %~dp0
call python pipe_properties_qt5.py
echo Fail to launch using qt5. Trying with qt4...
if errorlevel 1 (
    call python pipe_properties.pyw
)
pause
