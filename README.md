# ONYX Drive HUD v4.2 SafeExit

ONYX Drive HUD v4 is a single executable external telemetry HUD for Forza Data Out UDP.

## Main change in v4

Manager, Overlay and Peak Measurements now run inside **one EXE** and share **one UDP receiver**.

This fixes the old problem where the overlay and Peak Measurements tried to listen on the same UDP port at the same time.

## Features

- Single EXE
- Transparent overlay
- Blackout/Neon manager
- KMH / RPM / Gear / PS / Boost tiles
- Drag-and-drop tile positioning
- Peak Measurements / Dyno Lab
- CSV export
- XLSX/Excel export
- Design themes
- Language tab
- English default
- German included
- additional major languages with partial UI labels
- Custom ONYX icon included
- PyInstaller build BAT included

## Run from source

```bat
install_dependencies.bat
start_onyx_drive_hud.bat
```

## Build single EXE

```bat
build_one_exe.bat
```

Output:

```text
release\ONYX_Drive_HUD_v4_2.exe
```

## Forza settings

```text
Data Out: On
Data Out IP: 127.0.0.1
Data Out Port: 5607
```

Use borderless/windowed display mode for best overlay behavior.

## Important

Do not run another telemetry logger on the same UDP port while ONYX is running.


## v4.1 DynoClean

The Peak Measurements graph has been rewritten.

Old behavior:
- connected raw samples in time order
- steering, shifting or throttle changes could create rectangle/zigzag shapes

New behavior:
- filters clean full-throttle pull samples
- bins by RPM
- sorts by RPM
- draws only real dyno-style curves:
  - PS over RPM
  - NM over RPM
  - Boost over RPM
- KMH is still used for peak-speed measurements and export
- steering is not graphed


## v4.2 SafeExit

This version adds a hard SafeExit/killswitch.

Closing the manager with the red X now:
- saves the config
- stops the UDP socket
- hides the overlay
- quits Qt
- force-exits the process with `os._exit(0)`

There is also an **Exit ONYX** button and `Ctrl+Q` shortcut.
