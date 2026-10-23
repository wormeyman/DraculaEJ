#!/bin/bash
# Runs inside the nested KWin (started by it). Records the private bus address so the
# outside can drive this session, then starts Plasma's shell.
echo "$DBUS_SESSION_BUS_ADDRESS" > "$DEMO_ROOT/bus-address"
echo "$WAYLAND_DISPLAY" > "$DEMO_ROOT/wayland-display"
/usr/lib/kactivitymanagerd >/dev/null 2>&1 &
kded6 >/dev/null 2>&1 &
exec plasmashell --no-respawn
