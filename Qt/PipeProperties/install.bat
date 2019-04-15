@echo off
echo Installing a conda environment for the application...
conda create --name pipe_properties --file spec-file.txt
if errorlevel 1 (
    echo Oops, something went wrong during installation...
)
pause
