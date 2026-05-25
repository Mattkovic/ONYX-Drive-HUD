@echo off
title ONYX Reset Config and Layout
echo This resets local ONYX config/layout files in this folder.
echo Close ONYX before running this.
echo.
if exist onyx_drive_hud_config.json del /f /q onyx_drive_hud_config.json
if exist config.json del /f /q config.json
if exist profiles rmdir /S /Q profiles
echo Done. Start ONYX again.
pause
