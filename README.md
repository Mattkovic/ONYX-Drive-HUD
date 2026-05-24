# ONYX Drive HUD v4.8 DynoAxisFullRecord

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
release\ONYX_Drive_HUD.exe
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


## v4.3 International Units

New Units tab:

- Metric preset: KMH / PS / bar
- Imperial preset: MPH / HP / PSI
- Custom mode
- Speed unit: KMH or MPH
- Power unit: PS, HP or kW
- Boost unit: bar or PSI
- Gear label: GEAR or GANG

Overlay values are converted live.
CSV/XLSX export uses the selected unit names in the column headers.
English remains the default language.


## v4.4 StabilityFix

Fixed boost unit conversion and improved Dyno/Peak Measurements stability.

### BoostFix

Forza Data Out / Dash boost is now interpreted as PSI.

Correct display behavior:
- PSI mode: raw Forza boost value
- bar mode: raw PSI divided by 14.5038

This fixes incorrect values such as several hundred PSI and bar displaying PSI-like values.

### Dyno / Peak Measurements CrashFix

The Peak Measurements / Dyno graph now catches invalid telemetry/UI errors instead of crashing the whole app.

Added:
- crash log: logs/onyx_crash.log
- safe graph fallback
- safer Peak Recording sample handling
- safer Metric / Imperial / Custom unit conversion
- safer CSV/XLSX export rows
- Stability tab with BoostFix notes and crash log path

### Units

Metric: KMH / PS / bar
Imperial: MPH / HP / PSI
Custom: KMH or MPH, PS or HP or kW, bar or PSI, GEAR or GANG


## v4.5 Hotfix

Fixed remaining boost unit conversion and Dyno graph crash.

- Forza boost is treated as PSI raw input.
- PSI displays raw value directly.
- bar displays PSI / 14.5038.
- Example: -11.02 PSI now displays about -0.76 bar.
- Dyno graph now supports smoothed dyno point objects with power_ps instead of only power_w.
- Export rows are more defensive against invalid telemetry samples.


## v4.6 DynoPerformanceFix

Fixed manager freezes during Peak Measurements / Dyno recording.

### What changed

- Graph repainting is throttled to about 10 FPS.
- Peak labels are throttled instead of updating on every UDP packet.
- UDP queue is bounded so the UI cannot build an infinite backlog.
- Manager processes a limited number of telemetry packets per UI tick.
- Dyno graph now draws the current clean full-throttle pull while recording.
- A new full-throttle pull can reset the live dyno run, instead of the graph staying visually stuck forever.
- Peak values still remain tracked over the whole recording.

### Why the graph can look "full"

The DynoClean graph is not a simple time graph. It plots cleaned samples by RPM for a pull.
Once the RPM range is filled, the curve will mostly update its best/cleanest values instead of scrolling forever.
v4.6 adds live-run reset behavior so a new pull starts a fresh curve.


## v4.7 DynoZoomFix

Added safe Dyno graph zoom controls:

- Dyno Zoom Out
- Dyno Zoom In
- Reset Dyno Zoom

The zoom only changes graph rendering scale. It does not change telemetry collection, unit conversion, exports, or UDP handling.

Recommended use:
- Use Zoom Out if the curve is pressed against the right/top graph edge.
- Use Reset Dyno Zoom to return to the default dyno view.

This keeps the v4.6 performance fixes:
- throttled graph repainting
- bounded UDP queue
- live pull reset
- Peak Measurements freeze protection


## v4.8 DynoAxisFullRecord

Improved the Peak Measurements / Dyno Clean View.

### Added axis labels

- Left axis now shows the current power/torque scale.
- Bottom axis now shows RPM ticks.
- The axis labels follow the selected unit system:
  - PS / HP / kW for power
  - RPM on the bottom axis
  - Boost legend shows bar or PSI depending on the selected boost unit

### Full Record mode

The Dyno graph now uses the whole recording as graph data instead of only the current live pull window.

It still filters internally to useful throttle/performance samples, so steering, braking and coasting garbage should not create the old rectangle mess.

This keeps:
- v4.5 boost conversion fix
- v4.6 UI freeze protection
- v4.7 Dyno zoom controls


## Short EXE name

The built executable is now named:

ONYX_Drive_HUD.exe

The internal app version/title remains ONYX Drive HUD v4.8 DynoAxisFullRecord.
