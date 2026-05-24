# Nexus Mods Review Notes

## Project

ONYX Drive HUD v4.8 DynoAxisFullRecord

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


## v4.3 International Units

The app includes a local unit conversion tab. Unit conversion happens locally in the UI/export layer only.


## v4.4 StabilityFix

This update fixes boost unit conversion and improves crash safety in the local Peak Measurements / Dyno UI.

No game files, memory, saves, executable files or anti-cheat systems are touched.


## v4.5 Hotfix

Fixed remaining boost unit conversion and Dyno graph crash.

- Forza boost is treated as PSI raw input.
- PSI displays raw value directly.
- bar displays PSI / 14.5038.
- Example: -11.02 PSI now displays about -0.76 bar.
- Dyno graph now supports smoothed dyno point objects with power_ps instead of only power_w.
- Export rows are more defensive against invalid telemetry samples.


## v4.6 DynoPerformanceFix

This update only changes local UI performance and Dyno graph update handling.
No game files, memory, saves, executables or anti-cheat systems are touched.


## v4.7 DynoZoomFix

This update only adds local Dyno graph zoom controls.
It does not modify game files, memory, saves, executables or anti-cheat systems.


## v4.8 DynoAxisFullRecord

This update only changes the local Dyno graph display:
- axis labels
- RPM scale labels
- full-record graph data mode

No game files, memory, saves, executables or anti-cheat systems are touched.
