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
