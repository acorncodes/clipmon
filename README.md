# Acorn's ClipMon

Provides info about your current selection/clipboard on X11 through notifications.

More specifically, uses `python3-xlib` to wait for changes to the PRIMARY X-selection, analyzes the selection, then sends a D-Bus message via `gdbus` to update a notification providing useful info about the selection.

Useful metadata:
* Number of characters
* Number of lines
* Conversions to metric and binary suffixes (e.g. Gib, MiB)
* Conversions of timestamps
* Conversions from hexidecimal, binary
* And more!