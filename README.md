# ONYX Drive HUD v5.2.6

ONYX Drive HUD is an external telemetry overlay for Forza Horizon 6 using the official Forza Data Out UDP telemetry feature.

It listens to local UDP telemetry and renders a transparent customizable HUD.

## Security / Transparency

ONYX Drive HUD does not:
- inject DLL files
- edit game memory
- modify save files
- modify Forza game files
- patch the game executable
- bypass anti-cheat

It only listens to local UDP telemetry and renders an overlay.

## Main Features

- Transparent external HUD overlay
- Live speed display
- Live RPM display
- Current gear display
- Engine power display
- Boost pressure display
- Moveable HUD tiles
- Custom tile colors
- Custom tile size and position
- Click-through mode
- Blackout / Neon style manager
- Design presets
- Language selector
- International Units tab
- Metric / Imperial / Custom unit system
- KMH / MPH speed unit selection
- PS / HP / kW power unit selection
- bar / PSI boost unit selection
- GEAR / GANG label option
- Peak Measurements / DynoClean
- Dyno Clean View with axis labels
- Full Record mode for Peak Measurements
- Dyno Zoom controls
- Performance Lab
- Live Telemetry Graph with separate scales
- Drag Timer
- Drag Timer Overlay Tile
- Grip Monitor
- Smart Hints
- Session Report
- Vehicle Analysis / Performance Summary
- HUD Presets
- Profiles
- Support Info
- Open Crash Folder button
- GRIP Warning overlay tile
- Optional RPM Gauge / Tachometer overlay
- Overlay Monitor selector
- Tile label visibility / custom labels
- CSV export
- XLSX / Excel export
- Single EXE version
- Short EXE filename: ONYX_Drive_HUD.exe
- No Python required for normal users

## International Units

ONYX Drive HUD includes a dedicated Units tab.

Available presets:
- Metric
- Imperial
- Custom

Available unit options:
- Speed: KMH or MPH
- Power: PS, HP or kW
- Boost: bar or PSI
- Gear label: GEAR or GANG

Metric preset:
KMH / PS / bar

Imperial preset:
MPH / HP / PSI

The overlay converts values live based on the selected unit settings.

Boost conversion is fixed:
- Forza Data Out boost is handled as PSI.
- PSI mode displays the raw boost value.
- bar mode converts PSI to bar.
- Example: 40 PSI = about 2.76 bar.
- Example: -11 PSI = about -0.76 bar.

CSV and XLSX exports also use the selected unit names in the column headers.

## Peak Measurements / DynoClean

DynoClean includes:
- Full Record mode
- Dyno Clean View axis labels
- Left-side power / torque scale
- Bottom RPM scale
- Boost legend with bar / PSI support
- Dyno Zoom Out
- Dyno Zoom In
- Reset Dyno Zoom

The Dyno graph uses the full recording as graph data while still filtering useful throttle/performance samples.

The Dyno view is not a simple live time graph. It is designed like a performance/dyno graph:
- Bottom axis: RPM
- Left axis: power / torque scale
- Curves: power, torque and boost

## Performance Lab

Performance Lab includes:
- Live Telemetry Graph
- Drag Timer
- Grip Monitor
- Smart Hints
- Session Report
- Vehicle Analysis / Performance Summary
- HUD Presets
- Profiles
- Support Info

## Performance Summary

The Vehicle Analysis / Performance Summary is shown directly inside ONYX.

Buttons:
- Analyze Current Session
- Copy Summary
- Reset Summary

The summary can analyze:
- Speed
- RPM
- Power
- Boost
- Drag Timer results
- Grip / slip behavior
- Smart Hints
- Session samples
- Car ID if available

The summary includes:
- Telemetry Score
- Detected Car ID if available
- Peak Speed
- Peak RPM
- Peak Power
- Peak Boost
- Drag Times
- What looks good
- What needs attention
- Grip summary
- Suggestions
- Smart Hints

Important:
ONYX only sees telemetry data. It does not know installed tuning parts or exact build configuration. Suggestions are telemetry-based tuning hints, not forced upgrade advice.

## Drag Timer Overlay Tile

The Drag Timer Overlay Tile is optional and disabled by default.

It can show directly on the overlay:
- 0-100
- 0-200
- 100-200
- 200-300

It mirrors the existing Performance Lab Drag Timer values. It does not create a second independent drag timer core.

## RPM Gauge / Tachometer

The RPM Gauge / Tachometer is optional and disabled by default.

It can show:
- circular RPM gauge
- RPM needle
- RPM number
- current gear
- custom label / label visibility

## GRIP Warning Tile

The GRIP Warning overlay tile is optional.

Possible states:
- GRIP OK
- GRIP WARN
- FRONT WARN
- REAR WARN
- UNDERSTEER
- OVERSTEER
- FRONT SLIP
- REAR SLIP
- LOW GRIP
- HIGH LOAD

Color behavior:
- green/cyan = OK
- yellow = warning
- orange = risk
- red = critical
- blinking red/white = critical grip loss

This is heuristic telemetry logic, not a physical tire simulation.

## Overlay Monitor Selector

The General tab includes an Overlay Monitor selector:
- Primary Monitor
- Monitor 1
- Monitor 2
- Monitor 3

If the selected monitor no longer exists, ONYX falls back to the primary monitor.

## Layout Saving

Tile positions are saved to the config when dragging and saving.

If the overlay is hidden after saving, press Show Overlay again.

## Requirements

- Windows 10 or Windows 11
- Forza Horizon 6
- Data Out enabled in Forza
- No Python required for the EXE version

## Recommended Forza Data Out Settings

Data Out: On  
Data Out IP Address: 127.0.0.1  
Data Out Port: 5607

Recommended display mode:
Borderless / Windowed

## Troubleshooting

If no telemetry data appears:
- Make sure Data Out is enabled in Forza.
- Make sure the IP address is 127.0.0.1.
- Make sure the port is 5607.
- Close other telemetry tools that may use the same UDP port.
- Allow ONYX through Windows Firewall if prompted.
- Restart ONYX.
- Restart Forza.

If the app crashes:
- Open Performance Lab.
- Use Support Info → Open Crash Folder.
- Send the `onyx_crash.log` file with your bug report.


## Full Added / Fixed History Since v5.0

### Added

- Added Performance Lab.
- Added Live Telemetry Graph.
- Added separate Live Graph scaling for Speed, RPM, Power and Boost.
- Added time axis to Live Telemetry Graph.
- Added latest-value display inside Live Telemetry Graph.
- Added Pause / Resume Live Graph control.
- Added Clear Live Graph control.
- Added Drag Timer.
- Added Drag Timer live measurements.
- Added Drag Timer manual record workflow.
- Added Drag Timer Overlay Tile.
- Added optional Drag Timer Overlay display for 0-100, 0-200, 100-200 and 200-300.
- Added Grip Monitor.
- Added Grip live monitoring.
- Added Grip record and analysis workflow.
- Added GRIP Warning overlay tile.
- Added GRIP tile states such as GRIP OK, GRIP WARN, FRONT WARN, REAR WARN, UNDERSTEER, OVERSTEER, FRONT SLIP, REAR SLIP, LOW GRIP and HIGH LOAD.
- Added dynamic GRIP tile warning colors.
- Added critical grip-loss blinking warning state.
- Added front/rear slip based warning logic.
- Added fallback grip warning logic when direct slip telemetry is unavailable.
- Added Smart Hints.
- Added Smart Hints live feedback.
- Added Smart Hints record and analysis workflow.
- Added Session Report system.
- Added Session live stats.
- Added Session record workflow.
- Added Session report export.
- Added Vehicle Analysis / Performance Summary.
- Added Analyze Current Session button.
- Added Copy Summary button.
- Added Reset Summary button.
- Added telemetry score.
- Added Detected Car ID display if available.
- Added local telemetry-based tuning suggestions.
- Added HUD Presets.
- Added Profiles.
- Added Support Info section.
- Added Copy Support Info button.
- Added Open Crash Folder button.
- Added optional RPM Gauge / Tachometer overlay.
- Added Tachometer Gauge as an optional overlay element.
- Added current gear display inside Tachometer Gauge.
- Added Overlay Monitor selector.
- Added Primary Monitor / Monitor 1 / Monitor 2 / Monitor 3 selection.
- Added label visibility option in Tiles tab.
- Added Auto Unit Label option in Tiles tab.
- Added custom label support for tiles.
- Added Show Overlay hint after saving.
- Added short EXE naming workflow: ONYX_Drive_HUD.exe.
- Added improved README, SECURITY and Nexus review documentation.

### Fixed

- Fixed bar / PSI boost conversion.
- Fixed boost handling by treating Forza Data Out boost as PSI.
- Fixed PSI mode displaying raw boost value.
- Fixed bar mode converting PSI to bar.
- Fixed examples such as 40 PSI = about 2.76 bar.
- Fixed Peak Measurements / Dyno crash during recording.
- Fixed DynoGraph power conversion crash.
- Fixed manager/UI freeze during longer Dyno recordings.
- Fixed Live Telemetry Graph values being flattened by RPM scale.
- Fixed Speed, RPM, Power and Boost graph scaling.
- Fixed Boost appearing as a flat line in Live Telemetry Graph.
- Fixed Speed not being readable in Live Telemetry Graph.
- Fixed overlay fullscreen positioning behavior.
- Fixed overlay start behavior.
- Fixed overlay position clipping issue.
- Fixed overlay hotkey behavior.
- Fixed Queue Scroll / UDP queue overload behavior.
- Fixed layout save persistence.
- Fixed dragged Speed tile position not saving.
- Fixed dragged RPM tile position not saving.
- Fixed dragged Gear tile position not saving.
- Fixed dragged Power tile position not saving.
- Fixed dragged Boost tile position not saving.
- Fixed dragged Grip tile position not saving.
- Fixed dragged Tachometer Gauge position not saving.
- Fixed dragged Drag Timer Overlay position not saving.
- Fixed tiles jumping back to default positions after restart.
- Fixed Save Layout not pulling current overlay coordinates into config.
- Fixed normal Save button not preserving live overlay positions.
- Fixed small HUD scale layout problems around 0.70.
- Fixed text overlapping values at small HUD scale.
- Fixed tile spacing not scaling down correctly.
- Fixed labels running into numbers.
- Fixed edit handle being too visually intrusive.
- Fixed old prototype/fix labels appearing in the final UI header.
- Fixed README / SECURITY / Nexus review notes being too rough for final release.
- Fixed EXE naming being too long in earlier builds.

### Improved

- Improved Performance Lab layout.
- Improved Live Telemetry Graph readability.
- Improved DynoClean view.
- Improved Dyno axis labels.
- Improved left-side power / torque scale.
- Improved bottom RPM scale.
- Improved Boost legend with bar / PSI support.
- Improved Dyno Zoom controls.
- Improved Full Record mode for Peak Measurements.
- Improved crash logging.
- Improved precise crash context and traceback logging.
- Improved Support Info workflow for bug reports.
- Improved user workflow with Open Crash Folder.
- Improved Minimal HUD preset readability.
- Improved tile scaling behavior.
- Improved tile label handling.
- Improved profile/preset handling so custom labels and colors are not unnecessarily overwritten.
- Improved final UI header cleanup.
- Improved security/transparency documentation.
- Improved Nexus review documentation.
- Improved Performance Summary wording so it does not pretend to know installed tuning parts.
- Improved Performance Summary logic so suggestions are telemetry-based tuning hints instead of forced upgrade advice.
- Improved community-request workflow by adding optional features disabled by default.

### Security / Transparency

ONYX Drive HUD is still an external telemetry overlay only.

It does not:
- inject DLL files
- edit game memory
- modify save files
- modify Forza game files
- patch the game executable
- bypass anti-cheat

It only listens to local Forza Data Out UDP telemetry and renders a local overlay.

The EXE version is built with PyInstaller. Some antivirus engines may flag PyInstaller-built EXE files because they bundle the Python runtime. This does not automatically mean the file is malicious. The source code is included for inspection and local rebuilding.
