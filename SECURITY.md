# Security Notes

ONYX Drive HUD v4 does not inject into Forza or any other process.

It does not edit game files.

It does not read or write game memory.

It listens for local UDP telemetry and draws a transparent overlay.

Local written files:

```text
onyx_drive_hud_config.json
CSV/XLSX files chosen by the user
```

PyInstaller EXEs can sometimes trigger false positives because they bundle Python. Source code is included so reviewers can rebuild locally.


## v4.1 DynoClean

The dyno graph is a local visualization of UDP telemetry. It does not access game memory.


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
