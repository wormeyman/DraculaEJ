# CLAUDE.md - DraculaEJ

Working notes for picking this up in a fresh session.

## What this is

A dark KDE Plasma 6 theme built from the free Dracula KDE theme (`dracula/gtk`,
`kde/` folder, GPL-3.0) and tuned to feel like macOS. It is an unofficial remix,
not made or endorsed by Dracula Theme.

Use only the free, GPL/MIT-licensed Dracula sources. Do not copy anything from
Dracula PRO; its license forbids adapting it.

## Current state (2026-10-23)

- Every piece is named DraculaEJ: look-and-feel `com.eric.DraculaEJ`, color
  scheme / desktop theme / Kvantum / Aurorae `DraculaEJ`, cursors
  `DraculaEJ-cursors`, auroraerc `[DraculaEJ]`, Konsole profile
  `DraculaEJ.profile`. Only the used upstream variants are kept (purple colors,
  see-through purple Kvantum, regular desktop theme); the gray and Solid
  variants can come back from the upstream pin.
- **Upstream pins:** dracula/gtk `71640b9456110f3bac2130d0b387a3154a9fb4d2`,
  Tela `a1fffc5bfab716bd022dd228ee96fe3965cdb33d`, dracula/konsole `d525667`.
- **README screenshots** (`screenshots/`) come from an invisible demo session;
  `tools/screenshot-demo/README.md` has every step and the no-personal-data
  checks.
- A security review before publishing (2026-10-23) found no vulnerabilities:
  no secrets, no active SVG content, the scripts delete only fixed DraculaEJ
  paths, and all symlinks are relative and stay inside the repo.

## Design decisions

| Topic | Decision |
| --- | --- |
| Scope | KDE only: Plasma, KWin, Qt apps, Konsole |
| Launcher | Plasma 6 Kickoff (not the old tabbed one in Dracula's screenshot) |
| Variant | Purple highlights (upstream `DraculaPurple`), see-through Kvantum (upstream `Dracula-purple`) |
| Konsole | Official `dracula/konsole` colors as profile `DraculaEJ`, set as default by `--apply`; font left to the user |
| Buttons | Left, macOS order `XIA` |
| Button colors | Pink `#ff79c6` / orange `#ffb86c` / green `#50fa7b` |
| Decoration | **Klassy** with preset `klassy/DraculaEJ.klpw`; `IconSize=IconSmall` = 18 px circles at 125% (IconVerySmall 16 px, IconMedium 25 px); solid title bar; unfocused = plain gray, symbols on hover |
| Fallback | Aurorae `DraculaEJ` with buttons redrawn by `tools/make_buttons.py`, `ButtonSize=2` |
| Folders | Tela-dracula recolored `#44475a` -> `#7e57c2` |
| Launcher icon | White 3-line hamburger (theme text color), loaded **by name** |
| Screenshots | Dolphin snapped left + "Mountains" wallpaper (`dracula/wallpaper`, MIT); Konsole with generic fastfetch (`demo@draculaej`); dock on the right |

## Changes from upstream, file by file

- **Names:** every folder, file and internal name renamed from Dracula to
  DraculaEJ. Metadata keeps EliverLara as an author and adds "Eric" with no
  email.
- `aurorae/themes/DraculaEJ/{close,minimize,maximize,restore}.svg`: replaced by
  `tools/make_buttons.py` output. Upstream copies are in
  `tools/stock-buttons-71640b9/`. `DraculaEJrc` is upstream's `Dracularc`,
  unchanged (`LeftButtons=XIA`, `ButtonWidth/Height=13`).
- `plasma/look-and-feel/com.eric.DraculaEJ/contents/defaults`: DraculaEJ names,
  icons `Tela-dracula`, Aurorae as the decoration (works without Klassy), plus
  `ButtonsOnLeft=XIA` / `ButtonsOnRight=` (which a user `kwinrc` overrides
  anyway - see below). Based on upstream's `Plasma6/Dracula`; the older
  non-Plasma6 one has Plasma 5 QML lock and logout screens.
- `plasma/look-and-feel/com.eric.DraculaEJ/metadata.json`: rewritten;
  upstream's `X-KPackage-Dependencies` (9 KDE Store items, two unknown
  plasmoids among them) removed so nothing gets downloaded.
- `konsole/`: `Dracula.colorscheme` from `dracula/konsole` with its license,
  and a minimal `DraculaEJ.profile` (colors only).
- `icons/hicolor/22x22/actions/draculaej-menu-launcher.svg`: new.

## Findings - do not re-derive

- **Button order lives in the user's `kwinrc`.** `~/.config/kwinrc`
  `[org.kde.kdecoration2]` `ButtonsOnLeft`/`ButtonsOnRight` beat kdedefaults,
  so a global theme can't change them once set. Write them with
  `kwriteconfig6 --notify`. Without `--notify`, Plasma does not copy the order to
  GTK (`gtk-decoration-layout` in `gtk-3.0`/`gtk-4.0` `settings.ini`,
  xsettingsd, gsettings), and GTK apps that draw their own title bar (Firefox,
  GTK terminals) keep the old side. They draw their own buttons, so those stay
  gray, not Dracula colors.
- **Aurorae button size** is `~/.config/auroraerc`, group = theme name
  (`[DraculaEJ]`), key `ButtonSize`. Same as the size menu under the theme's
  pencil icon in System Settings > Window Decorations. 2 looked right; 3 and 4
  too big. The number-to-size mapping was not worked out.
- **Aurorae button SVGs** need elements `active-center`, `hover-center`,
  `pressed-center`, `inactive-center`, `deactivated-center`. KWin scales each
  element's bounding box to the button, so `make_buttons.py` puts an invisible
  16x16 square in each group to keep the circle (r 7 + 0.5 edge) round and
  unclipped. `qdbus6 org.kde.KWin /KWin reconfigure` picks up new SVGs.
- **Why stock buttons looked soft:** each circle sat on a darker copy offset by
  a fraction, which showed as a muddy fringe at ~19 px. At 125% scale the
  buttons also start at fractional positions, which softens any design a bit.
- **Aurorae can't be crisp at 125%.** Both `org.kde.kwin.aurorae` and `.v2`
  render buttons at logical size and stretch them: a ~2 px soft edge versus a
  1 px edge when the same SVG is rendered at full resolution. Native
  decorations (Klassy, Breeze) don't have this problem.
- **Klassy notes.** Config `~/.config/klassy/klassyrc`; presets
  `~/.config/klassy/windecopresetsrc`. `klassy-settings --import-preset FILE`
  then `--load-windeco-preset NAME` (re-importing the same name replaces it);
  loading also generates `klassy`/`klassy-dark` icon themes (unused) and writes
  `BorderSize=None` + `BorderSizeAuto=false` to `kwinrc`. Switch KWin with user
  `kwinrc` `library=org.kde.klassy`, `theme=Klassy`. Per-button colors are JSON
  in `ButtonOverrideColors{Active,Inactive}{Close,Minimize,Maximize}`: state
  keys `{Icon,Background,Outline}{Normal,Hover,Press}`, values `[R,G,B]` or
  `[opacity%,R,G,B]` (format read from `libbreezecommon/decorationbuttoncolors.cpp`).
  Circle size follows `IconSize`.
- **GTK apps draw their own gray buttons** (client-side title bars): gray
  circles with symbols always shown. Don't mistake them for Klassy's unfocused
  buttons.
- **Launcher icon must be loaded by name.** By file path, Plasma tinted it with
  the panel text color but cached it by path: changing the file's color did
  nothing until the file was renamed, and deleting `~/.cache/icon-cache.kcache`
  didn't help. A name in `~/.local/share/icons/hicolor/22x22/actions/` showed "?"
  until `kbuildsycoca6` and an icon-changed signal
  (`dbus-send --session --type=signal /KIconLoader org.kde.KIconLoader.iconChanged int32:0`).
- **Folder color:** Tela-dracula paints the folder body with its install
  script's `theme_color` and a back tab with `#bd93f9`. Change `theme_color`
  and re-run `install.sh dracula` (`tela/install-ej.patch`).
- **A transparent window can block the launcher.** If clicks on the top-left
  launcher do nothing, look for an unmanaged `xembedsniproxy` window over the
  corner: an app using the old X11 tray (an XWayland Electron app, for example)
  gets a hidden 26 px container there. `tools/list-corner.js` (a KWin script;
  output in `journalctl --user`) lists what covers the corner. Running that app
  natively on Wayland removes it.
- **`kreadconfig6` needs the session's `XDG_CONFIG_DIRS`** to see the
  kdedefaults layer; from a shell without it, every theme key reads blank:
  `export XDG_CONFIG_DIRS=$(tr '\0' '\n' < /proc/$(pgrep -x plasmashell)/environ | sed -n 's/^XDG_CONFIG_DIRS=//p')`.
- **Raising a window from a shell** doesn't work on Wayland. A KWin script can
  (`workspace.activeWindow = w`); put focus back afterwards.
- **Screenshots:** `spectacle -f -b -n -o <file>`. Measure colors with
  `magick <file> -crop WxH+X+Y -format "%c" histogram:info:-`.

## Tools

| File | What it does |
| --- | --- |
| `tools/make_buttons.py OUT_DIR` | Writes the 4 Aurorae button SVGs (fallback; colors at the top) |
| `tools/make_klassy_preset.py BASE.klpw OUT.klpw` | Builds the Klassy preset from Eaten Fruits (colors and sizes at the top) |
| `tools/buttons_preview.py OUT.png` | Mockup of title-bar button color options |
| `tools/folder_preview.py ICON_DIR OUT.png` | Folder icons in candidate colors |
| `tools/lighten.py FG BG TARGET` | Lightens a color, same hue, to a contrast ratio |
| `tools/measure_buttons.py SHOT X Y W H` | Size and center color of each button in a screenshot |
| `tools/list-corner.js` | KWin script: lists windows covering the top-left corner |
| `tools/screenshot-demo/` | Invisible demo session for README screenshots (steps in its README) |

## Demo-session findings (screenshots)

- `kwin_wayland --virtual --width 2048 --height 1152 --scale 1.25` renders to
  an invisible screen; `spectacle -f -b -n` inside it gives 2560x1440 shots.
  Run it under `dbus-run-session` with `env --ignore-environment` and a demo HOME.
- `XDG_RUNTIME_DIR` must be a short path (`/run/user/<uid>/dej`): a long one put
  KIO's worker socket over the 108-character limit ("Can not create a socket
  for launching a KIO worker").
- Never run `install.sh --apply` inside the demo: its `systemctl --user restart`
  would restart the real Plasma shell. The real plasmashell may also run as
  `/usr/bin/plasmashell --no-respawn`, so stop the demo only via its
  `kwin_wayland --virtual` process.
- fastfetch ignored `$HOME/.config/fastfetch` from the demo HOME and printed the
  real user, LAN IP, hardware and uptime. Always pass `--config` explicitly and
  check every shot.

## Environment it was built on

CachyOS, Plasma 6.8.1 on Wayland, 2560x1440 at 125% scale, Kvantum 1.1.8,
Klassy 6.7.3. The panel background under DraculaEJ measures `#1E1F29`.
