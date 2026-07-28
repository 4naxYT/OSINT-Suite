cls
@echo off
setlocal enabledelayedexpansion

set "dir=.\Exif tool\DATA"

:: Directory check
if not exist "%dir%" (
    echo Error: Directory "%dir%" not found.
    pause
    exit /b 1
)

:: exiftool check
where exiftool >nul 2>nul
if errorlevel 1 (
    echo Error: exiftool not found in PATH.
    echo Please install ExifTool or add it to your system PATH.
    pause
    exit /b 1
)

:: Get console width 
for /f "tokens=2" %%a in ('mode con ^| find "Columns"') do set "cols=%%a"
if not defined cols set "cols=80"   :: fallback

echo Processing files in "%dir%" ...
echo ---------------------------------------------

set start=%time%
if "%start:~0,1%"==" " set start=0%start:~1%

:: Loop through every file in the directory
for %%F in ("%dir%\*.*") do (
    set "gps="

    for /f "delims=" %%L in ('exiftool -GPSPosition "%%F" 2^>nul') do (
        set "gps=%%L"
    )

    :: justify or smth
    set "leftpart=- %%~nxF"
    if defined gps (
        set "rightpart= : !gps!"
    ) else (
        set "rightpart= : [ No Location Detected ]"
    )

    :: calculate len
    call :strlen leftpart leftlen
    call :strlen rightpart rightlen

    :: calculate padding
    set /a "padding=cols - leftlen - rightlen"
    if !padding! lss 0 set "padding=1"   :: fallback: one space if overflow

    :: print out the spaces
    set "spaces="
    for /l %%i in (1,1,!padding!) do set "spaces=!spaces! "

    :: output / return
    echo !leftpart!!spaces!!rightpart!
)

set end=%time%
if "%end:~0,1%"==" " set end=0%end:~1%

:: calculate and print elapsed time 
(
    REM Parse start time
    for /f "tokens=1-4 delims=:,. " %%a in ("!start!") do (
        set start_hh=%%a
        set start_mm=%%b
        set start_ss=%%c
        set start_cs=%%d
    )

    REM Parse end time
    for /f "tokens=1-4 delims=:,. " %%a in ("!end!") do (
        set end_hh=%%a
        set end_mm=%%b
        set end_ss=%%c
        set end_cs=%%d
    )

    REM Convert to centiseconds (use ! for runtime values)
    set /a "start_total = ((1!start_hh! - 100) * 3600 + (1!start_mm! - 100) * 60 + (1!start_ss! - 100)) * 100 + (1!start_cs! - 100)"
    set /a "end_total   = ((1!end_hh!   - 100) * 3600 + (1!end_mm!   - 100) * 60 + (1!end_ss!   - 100)) * 100 + (1!end_cs!   - 100)"

    REM Compute difference (handle midnight crossing)
    set /a diff = !end_total! - !start_total!
    if !diff! LSS 0 set /a diff += 8640000

    REM Convert back to hours, minutes, seconds, centiseconds
    set /a hours = !diff! / 360000
    set /a rem   = !diff! %% 360000
    set /a minutes = !rem! / 6000
    set /a rem     = !rem! %% 6000
    set /a seconds = !rem! / 100
    set /a cs      = !rem! %% 100

    REM Pad with leading zeros
    if !hours! LSS 10 set hours=0!hours!
    if !minutes! LSS 10 set minutes=0!minutes!
    if !seconds! LSS 10 set seconds=0!seconds!
    if !cs! LSS 10 set cs=0!cs!

    REM Fake three-digit milliseconds (add a trailing zero)
    set milliseconds=!cs!0
    
    echo.
    echo Operation Took: !hours!:!minutes!:!seconds!.!milliseconds!
    echo.
)

echo ---------------------------------------------
pause
exit /b

:strlen
setlocal enabledelayedexpansion
set "str=!%1!"
set "len=0"
if not defined str (
    endlocal & set "%2=0" & goto :eof
)
:strlen_loop
if not "!str:~%len%,1!"=="" (
    set /a len+=1
    goto strlen_loop
)
endlocal & set "%2=%len%"
goto :eof
