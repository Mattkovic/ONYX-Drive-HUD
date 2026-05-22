@echo off
setlocal
title ONYX Drive HUD v4 OneEXE - Builder
cd /d "%~dp0"

echo ==========================================
echo  ONYX DRIVE HUD v4.2 SafeExit - Builder
echo ==========================================
echo.

where python >nul 2>nul
if %errorlevel%==0 (
    set "PY=python"
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set "PY=py"
    ) else (
        echo FEHLER: Python nicht gefunden.
        pause
        exit /b 1
    )
)

echo [1/5] Dependencies installieren...
%PY% -m pip install --upgrade pip
%PY% -m pip install PyQt6 pywin32 pyinstaller openpyxl pillow

echo.
echo [2/5] Alte Build-Dateien entfernen...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist release rmdir /s /q release

echo.
echo [3/5] Single EXE bauen...
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name ONYX_Drive_HUD_v4_2_2 --icon onyx_icon.ico --add-data "onyx_icon.ico;." --add-data "onyx_icon.png;." onyx_app.py

echo.
echo [4/5] Release-Ordner erstellen...
mkdir release
copy /Y dist\ONYX_Drive_HUD_v4_2_2.exe release\ONYX_Drive_HUD_v4_2_2.exe
copy /Y onyx_icon.ico release\onyx_icon.ico
copy /Y onyx_icon.png release\onyx_icon.png
copy /Y README.md release\README.md
copy /Y NEXUSMODS_REVIEW.md release\NEXUSMODS_REVIEW.md
copy /Y SECURITY.md release\SECURITY.md
copy /Y LICENSE.txt release\LICENSE.txt

echo.
echo [5/5] Fertig.
echo Single EXE:
echo release\ONYX_Drive_HUD_v4_2_2.exe
echo.
pause
