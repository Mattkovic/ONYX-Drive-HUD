# Nexus Mods Review Notes

## Project

ONYX Drive HUD v4 OneEXE

## What this is

A standalone external telemetry HUD overlay for Forza UDP Data Out.

## What this is not

- Not a cheat
- Not a trainer
- Not an injector
- Not a save editor
- Not a memory editor
- Not a DLL mod
- Not a game-file patcher
- Not an anti-cheat bypass

## v4 architecture

The app is now a single EXE/process:

```text
Manager UI + Overlay + Peak Measurements + UDP receiver
```

Only one UDP socket is opened by the program.

## Network behavior

The program opens a local UDP listener:

```text
Host: 0.0.0.0
Port: 5607 by default
```

This receives Forza telemetry packets.

No intentional outbound networking code is included.

## Local files

The program writes:

```text
onyx_drive_hud_config.json
```

The user can export local CSV/XLSX files from Peak Measurements.

## Dependencies

```text
PyQt6
pywin32
pyinstaller
openpyxl
pillow
```

PyInstaller is only needed for building EXE files.


## v4.1 DynoClean

Dyno graph uses local telemetry samples only. It filters full-throttle pull samples and renders PS/NM/Boost over RPM. No game memory, no injection, no file patching.


## v4.2 SafeExit

The app includes a local exit/killswitch path. It only terminates its own process and does not interact with other processes.
