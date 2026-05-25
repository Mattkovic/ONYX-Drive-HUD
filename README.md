# ONYX Drive HUD v5.2.0

ONYX Drive HUD is an external telemetry overlay for Forza Horizon 6 using the official Data Out UDP telemetry feature.

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
- Live Telemetry Graph
- Drag Timer
- Grip Monitor
- Smart Hints
- Session Report
- HUD Presets
- Profiles
- Support Info
- Open Crash Folder button
- GRIP Warning overlay tile
- CSV export
- XLSX / Excel export
- Single EXE version
- No Python required for normal users

## Performance Lab

The Performance Lab includes:
- Live Telemetry Graph with separated scales
- Drag Timer
- Grip Monitor
- Smart Hints
- Session Report
- HUD Presets
- Profiles
- Support Info

## Grip Warning Tile

The GRIP Warning overlay tile is an optional HUD tile.

It can show:
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
