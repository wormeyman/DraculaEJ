#!/bin/bash
# Install the DraculaEJ global theme. Pass -a / --apply to also switch to it.
# Tela-dracula icons and Klassy are installed separately: see README.md.

set -e

SRC_DIR=$(cd "$(dirname "$0")" && pwd)

NAME=DraculaEJ
LNF_ID=com.eric.DraculaEJ

AURORAE_DIR="$HOME/.local/share/aurorae/themes"
SCHEMES_DIR="$HOME/.local/share/color-schemes"
PLASMA_DIR="$HOME/.local/share/plasma/desktoptheme"
LOOKFEEL_DIR="$HOME/.local/share/plasma/look-and-feel"
KVANTUM_DIR="$HOME/.config/Kvantum"
ICONS_DIR="$HOME/.local/share/icons"
KONSOLE_DIR="$HOME/.local/share/konsole"

mkdir --parents "$AURORAE_DIR" "$SCHEMES_DIR" "$PLASMA_DIR" "$LOOKFEEL_DIR" "$KVANTUM_DIR" "$ICONS_DIR/hicolor/22x22/actions" "$KONSOLE_DIR"

echo "Installing '${NAME}'..."

rm --recursive --force "$AURORAE_DIR/$NAME" "$PLASMA_DIR/$NAME" "$KVANTUM_DIR/$NAME" "$LOOKFEEL_DIR/$LNF_ID" "$ICONS_DIR/$NAME-cursors"
rm --force "$SCHEMES_DIR/$NAME.colors"

cp --recursive "$SRC_DIR/aurorae/themes/$NAME"                  "$AURORAE_DIR"
cp "$SRC_DIR/color-schemes/$NAME.colors"            "$SCHEMES_DIR"
cp --recursive "$SRC_DIR/Kvantum/$NAME"                         "$KVANTUM_DIR"
cp --recursive "$SRC_DIR/plasma/desktoptheme/$NAME"             "$PLASMA_DIR"
cp --recursive "$SRC_DIR/plasma/look-and-feel/$LNF_ID"          "$LOOKFEEL_DIR"
cp --recursive "$SRC_DIR/cursors/$NAME-cursors"                 "$ICONS_DIR"
cp "$SRC_DIR/icons/hicolor/22x22/actions/"*.svg     "$ICONS_DIR/hicolor/22x22/actions/"
cp "$SRC_DIR/konsole/Dracula.colorscheme"           "$KONSOLE_DIR"
cp "$SRC_DIR/konsole/$NAME.profile"                 "$KONSOLE_DIR"

echo "Install finished."

if [[ "$1" == "-a" || "$1" == "--apply" ]]; then
  echo "Applying '${NAME}'..."

  # A global theme cannot set the Kvantum theme, so do it here.
  kwriteconfig6 --file "$KVANTUM_DIR/kvantum.kvconfig" --group General --key theme "$NAME"

  plasma-apply-lookandfeel -a "$LNF_ID"

  # The user's own kwinrc overrides any theme for button order, so write it there.
  # --notify makes Plasma copy the order to GTK apps too.
  kwriteconfig6 --notify --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft XIA
  kwriteconfig6 --notify --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight ""

  # Konsole ignores the KDE color scheme; make the Dracula profile its default.
  kwriteconfig6 --file konsolerc --group "Desktop Entry" --key DefaultProfile "$NAME.profile"

  # Aurorae fallback button size (3 and 4 were too big).
  kwriteconfig6 --notify --file auroraerc --group "$NAME" --key ButtonSize 2

  # Klassy draws crisp buttons at fractional scales; use it when it's installed.
  if command -v klassy-settings >/dev/null; then
    klassy-settings --import-preset "$SRC_DIR/klassy/$NAME.klpw"
    klassy-settings --load-windeco-preset "$NAME"
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.klassy
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme Klassy
  else
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.kwin.aurorae.v2
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme "__aurorae__svg__$NAME"
  fi

  qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
  systemctl --user restart plasma-plasmashell.service

  echo "Applied. Restart already-running Qt apps to pick up the Kvantum style."
fi
