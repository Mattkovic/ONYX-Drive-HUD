@echo off
setlocal
cd /d "%~dp0"
title ONYX Drive HUD v5.2.7e Vehicle Database No-AI - Builder

echo ==========================================
echo  ONYX DRIVE HUD v5.2.7e Vehicle Database No-AI - Builder
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
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name ONYX_Drive_HUD --icon onyx_icon.ico --add-data "onyx_icon.ico;." --add-data "onyx_icon.png;." onyx_app.py
if errorlevel 1 (
    echo.
    echo FEHLER: PyInstaller build failed.
    pause
    exit /b 1
)

echo.
echo [4/5] Release-Ordner erstellen...
mkdir release
copy /Y dist\ONYX_Drive_HUD.exe release\ONYX_Drive_HUD.exe
copy /Y onyx_icon.ico release\onyx_icon.ico
copy /Y onyx_icon.png release\onyx_icon.png
copy /Y README.md release\README.md
copy /Y NEXUSMODS_REVIEW.md release\NEXUSMODS_REVIEW.md
copy /Y SECURITY.md release\SECURITY.md
copy /Y LICENSE.txt release\LICENSE.txt
copy /Y car_database.json release\car_database.json
copy /Y car_database_custom.json release\car_database_custom.json
copy /Y car_database_generated_cleaned.json release\car_database_generated_cleaned.json
copy /Y README_VEHICLE_DATABASE.txt release\README_VEHICLE_DATABASE.txt
copy /Y unknown_vehicles.json release\unknown_vehicles.json
copy /Y CHANGELOG_v5_2_7e.txt release\CHANGELOG_v5_2_7e.txt
copy /Y V5_2_7E_VEHICLE_DATABASE_NO_AI_NOTES.txt release\V5_2_7E_VEHICLE_DATABASE_NO_AI_NOTES.txt
copy /Y MANIFEST_SHA256.txt release\MANIFEST_SHA256.txt

echo.
echo [5/5] Fertig.
echo Single EXE:
echo release\ONYX_Drive_HUD.exe
echo.
pause
