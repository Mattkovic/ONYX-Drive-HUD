# ONYX Drive HUD v5.2.6 – Security Notes

ONYX Drive HUD is an external telemetry overlay.

It does not:
- inject DLL files
- edit game memory
- modify save files
- modify Forza game files
- patch the game executable
- bypass anti-cheat

It only listens to local UDP telemetry from Forza Data Out and renders a local overlay.

The EXE version is built with PyInstaller. Some antivirus engines may flag PyInstaller-built EXE files because they bundle the Python runtime. This does not automatically mean the file is malicious.

Users and reviewers can inspect or rebuild the source code manually.
