#!/bin/bash
# Run one command inside the nested demo session: its private D-Bus, its Wayland socket, and the
# demo HOME. Nothing from the real session's environment is passed through.
# Needs DEMO_ROOT (the folder holding home/, bus-address and wayland-display).
: "${DEMO_ROOT:?set DEMO_ROOT to the demo folder}"
exec env --ignore-environment HOME="$DEMO_ROOT/home" USER="$USER" LOGNAME="$USER" PATH=/usr/local/bin:/usr/bin:/bin \
  XDG_RUNTIME_DIR="/run/user/$(id --user)/dej" XDG_CONFIG_DIRS="$DEMO_ROOT/home/.config/kdedefaults:/etc/xdg" \
  XDG_DATA_DIRS=/usr/local/share:/usr/share XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=KDE \
  KDE_SESSION_VERSION=6 KDE_FULL_SESSION=true LANG=en_US.UTF-8 DEMO_ROOT="$DEMO_ROOT" \
  WAYLAND_DISPLAY="$(cat "$DEMO_ROOT/wayland-display")" DBUS_SESSION_BUS_ADDRESS="$(cat "$DEMO_ROOT/bus-address")" \
  "$@"
