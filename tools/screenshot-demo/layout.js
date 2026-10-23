/*
 * macOS-style panel layout used for the README screenshots (from the author's
 * LyanEJ setup).
 *
 *   top bar (full width, fixed)   [launcher] [global menu] ...... [tray] [clock]
 *   dock    (floating, centered)                  [ app icons ]
 *
 * Feed it to plasmashell inside the demo session (see README.md). It removes
 * every existing panel first.
 */

var TOP_HEIGHT = 30;
var DOCK_HEIGHT = 56;

// Pinned dock entries. preferred:// resolves to whatever you've set as default.
var DOCK_LAUNCHERS = [
    "preferred://filemanager",
    "preferred://browser",
    "applications:org.kde.konsole.desktop",
    "applications:systemsettings.desktop",
];

// --- start clean -----------------------------------------------------------
// Panels only. Desktop containments (wallpaper, folder view) are left alone.
var existing = panels();
for (var i = 0; i < existing.length; i++) {
    existing[i].remove();
}

// --- top bar ---------------------------------------------------------------
var top = new Panel();
top.location = "top";
top.alignment = "left";
top.height = TOP_HEIGHT;
try { top.lengthMode = "fill"; } catch (e) {}
try { top.floating = false; } catch (e) {}

// ☰ launcher, icon only, no text label
var launcher = top.addWidget("org.kde.plasma.kickoff");
launcher.currentConfigGroup = ["General"];
launcher.writeConfig("icon", "application-menu");
launcher.writeConfig("menuLabel", "");
launcher.writeConfig("compactMode", "alwaysCompact");
launcher.reloadConfig();

// File / Edit / View ... of the focused window
top.addWidget("org.kde.plasma.appmenu");

// pushes everything after it to the right edge
top.addWidget("org.kde.plasma.panelspacer");

top.addWidget("org.kde.plasma.systemtray");

var clock = top.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", true);
clock.writeConfig("dateFormat", "shortDate");
clock.reloadConfig();

// --- bottom dock -----------------------------------------------------------
var dock = new Panel();
dock.location = "bottom";
dock.alignment = "center";
dock.height = DOCK_HEIGHT;
// "fit" shrinks the panel to its contents, which is what makes it read as a dock
// rather than a full-width bar.
try { dock.lengthMode = "fit"; } catch (e) {}
try { dock.floating = true; } catch (e) {}

var tasks = dock.addWidget("org.kde.plasma.icontasks");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("launchers", DOCK_LAUNCHERS);
tasks.writeConfig("showOnlyCurrentDesktop", false);
tasks.writeConfig("showOnlyCurrentScreen", false);
tasks.writeConfig("groupingStrategy", 1);
tasks.reloadConfig();
