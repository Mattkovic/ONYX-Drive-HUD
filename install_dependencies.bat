@echo off
setlocal
title ONYX Drive HUD v4 OneEXE - Dependencies
cd /d "%~dp0"
echo ==========================================
echo  ONYX DRIVE HUD v4 OneEXE - Dependencies
echo ==========================================
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
%PY% --version
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt
echo.
echo Fertig.
pause
