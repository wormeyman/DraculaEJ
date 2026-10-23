#!/bin/bash
# Remove the DraculaEJ pieces. Switch to another global theme first (for example
# Breeze Dark in System Settings); this script does not change the active theme.

NAME=DraculaEJ
LNF_ID=com.eric.DraculaEJ

rm --recursive --force "$HOME/.local/share/aurorae/themes/$NAME"
rm --force "$HOME/.local/share/color-schemes/$NAME.colors"
rm --recursive --force "$HOME/.local/share/plasma/desktoptheme/$NAME"
rm --recursive --force "$HOME/.local/share/plasma/look-and-feel/$LNF_ID"
rm --recursive --force "$HOME/.config/Kvantum/$NAME"
rm --recursive --force "$HOME/.local/share/icons/$NAME-cursors"
rm --force "$HOME/.local/share/icons/hicolor/22x22/actions/draculaej-menu-launcher.svg"
rm --force "$HOME/.local/share/konsole/Dracula.colorscheme" "$HOME/.local/share/konsole/$NAME.profile"

echo "DraculaEJ removed."
