# README screenshots

The screenshots in `screenshots/` come from a throwaway Plasma session that runs on
an invisible screen (`kwin_wayland --virtual`). It has its own private D-Bus, its own
home folder and generic sample files, so nothing personal can show up and the real
desktop is never touched.

Needs: Plasma 6, Klassy, Tela-dracula installed for your user, fastfetch, spectacle,
and ImageMagick. `layout.js` builds the top bar and dock. The wallpaper is
"Mountains" from [dracula/wallpaper](https://github.com/dracula/wallpaper) (MIT):
`second-collection/illustrations/trees-and-mountains/dracula-mnt-bd93f9.png`.

## 1. Build the demo home

```sh
export DEMO_ROOT=$HOME/.cache/draculaej-demo     # any empty folder
T=~/Projects/DraculaEJ/tools/screenshot-demo
H=$DEMO_ROOT/home
mkdir --parents $H/{Desktop,Documents,Downloads,Music,Pictures,Projects,Public,Templates,Videos} $H/.config/fastfetch $H/.local/share/icons $H/.local/share/konsole
mkdir --parents /run/user/$(id --user)/dej && chmod 700 /run/user/$(id --user)/dej
cp $T/user-dirs.dirs $H/.config/
cp $T/fastfetch.jsonc $H/.config/fastfetch/config.jsonc
sed "s#DEMO_HOME#$H#g" $T/demo-bashrc > $H/.demo-bashrc
sed "s#DEMO_HOME#$H#g" $T/demo.profile > $H/.local/share/konsole/DraculaEJ.profile
printf '[Desktop Entry]\nDefaultProfile=DraculaEJ.profile\n\n[MainWindow]\nMenuBar=Disabled\n' > $H/.config/konsolerc
printf '# Notes\n\nIdeas for the weekend.\n' > $H/Documents/notes.md
printf 'Milk\nBread\nCoffee\n' > $H/Documents/shopping-list.txt
cp <the wallpaper png> $H/Pictures/mountains.png
for t in Tela-dracula Tela-dracula-dark Tela-dracula-light; do ln --symbolic ~/.local/share/icons/$t $H/.local/share/icons/$t; done
```

## 2. Start the invisible session

The runtime folder must have a short path: KDE's file workers use a socket inside
it, and a long path goes over the 108-character limit for socket names.

```sh
env --ignore-environment HOME=$H USER=$USER LOGNAME=$USER PATH=/usr/local/bin:/usr/bin:/bin \
  XDG_RUNTIME_DIR=/run/user/$(id --user)/dej XDG_CONFIG_DIRS=$H/.config/kdedefaults:/etc/xdg \
  XDG_DATA_DIRS=/usr/local/share:/usr/share XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=KDE \
  KDE_SESSION_VERSION=6 KDE_FULL_SESSION=true DEMO_ROOT=$DEMO_ROOT LANG=en_US.UTF-8 \
  dbus-run-session -- kwin_wayland --virtual --width 2048 --height 1152 --scale 1.25 \
  --xwayland --socket wayland-demo $T/session.sh &
```

2048x1152 at 125% gives 2560x1440 screenshots.

## 3. Apply DraculaEJ inside it

Do **not** run `install.sh --apply` here: it ends with `systemctl --user restart`,
which would restart the real Plasma shell. These are the same steps without it.

```sh
X=$T/in-demo.sh
$X ~/Projects/DraculaEJ/install.sh
$X kwriteconfig6 --file $H/.config/Kvantum/kvantum.kvconfig --group General --key theme DraculaEJ
$X plasma-apply-lookandfeel -a com.eric.DraculaEJ
$X kwriteconfig6 --notify --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft XIA
$X kwriteconfig6 --notify --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight ""
$X klassy-settings --import-preset ~/Projects/DraculaEJ/klassy/DraculaEJ.klpw
$X klassy-settings --load-windeco-preset DraculaEJ
$X kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.klassy
$X kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme Klassy
$X qdbus6 org.kde.KWin /KWin reconfigure
$X qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$(cat $T/layout.js)"
$X qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "$(cat $T/dock-right.js)"
$X plasma-apply-wallpaperimage $H/Pictures/mountains.png
$X qdbus6 org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript 'panels().forEach(function (p) { p.widgets("org.kde.plasma.kickoff").forEach(function (w) { w.currentConfigGroup = ["General"]; w.writeConfig("icon", "draculaej-menu-launcher"); w.reloadConfig(); }); });'
```

The layout call may time out with `NoReply`; the panels still appear. The dock
takes a few seconds to fill in.

## 4. Take the shots

```sh
setsid $X dolphin --select $H/Documents </dev/null >/dev/null 2>&1 &
sleep 5
$X qdbus6 org.kde.kglobalaccel /component/kwin org.kde.kglobalaccel.Component.invokeShortcut "Window Quick Tile Left"
$X spectacle -f -b -n -o $DEMO_ROOT/hero.png

$X qdbus6 org.kde.kglobalaccel /component/kwin org.kde.kglobalaccel.Component.invokeShortcut "Window Minimize"
setsid $X konsole </dev/null >/dev/null 2>&1 &
sleep 4
id=$($X qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript $T/size-konsole.js size-konsole)
$X qdbus6 org.kde.KWin /Scripting/Script$id org.kde.kwin.Script.run
$X spectacle -f -b -n -o $DEMO_ROOT/konsole.png
```

**Check every shot for personal data before keeping it.** fastfetch must show
`demo@draculaej`: if it shows your user name, it skipped the demo config, and it
will also print your IP address, hardware and uptime. Delete such a shot. That is
why `demo-bashrc` passes `--config` explicitly (fastfetch did not read
`$HOME/.config/fastfetch` from the demo home). Keep the launcher closed: it shows
the account's real name.

## 5. Save and clean up

```sh
for s in hero konsole; do magick $DEMO_ROOT/$s.png -strip -define png:compression-level=9 ~/Projects/DraculaEJ/screenshots/$s.png; done
pkill --full "^kwin_wayland --virtual --width 2048"    # only the demo session
rm --recursive --force $DEMO_ROOT /run/user/$(id --user)/dej
```
