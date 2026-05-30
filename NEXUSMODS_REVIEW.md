# Nexus Mods Review Notes – ONYX Drive HUD v5.2.6

ONYX Drive HUD is an external telemetry HUD overlay for Forza Horizon 6.

It uses the official Forza Data Out UDP telemetry feature.

The tool does not:
- inject DLL files
- edit game memory
- modify save files
- modify Forza game files
- patch the game executable
- bypass anti-cheat

It only listens to local UDP telemetry, usually on port 5607, and renders a transparent overlay.

The ZIP includes:
- ONYX source/build files
- README
- SECURITY notes
- license/review notes
- crash-log support

The EXE is built with PyInstaller. If scanners flag it, this is likely a false positive caused by the bundled Python runtime.
