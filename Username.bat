cls
@echo off
echo.
echo Downloading Sherlock....
python -m pip install --user sherlock-project
cls
echo.
echo Downloading Sherlock....
echo Completed
echo Adding to PATH...
set PATH=%PATH%;%APPDATA%\Python\Python314\Scripts
sherlock --version
echo.
echo Completed
cls
set /p usr=Exter Username to Reverse Search :  
echo.
echo Running Checks On %usr%...
sherlock %usr% --nsfw --no-txt --print-found 
pause
