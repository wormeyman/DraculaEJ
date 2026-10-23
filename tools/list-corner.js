// KWin script: print every window that covers the top-left corner, where the launcher button sits.
const windows = workspace.stackingOrder;
for (let i = 0; i < windows.length; i++) {
    const w = windows[i];
    const g = w.frameGeometry;
    if (g.x <= 12 && g.y <= 12 && g.x + g.width >= 12 && g.y + g.height >= 12) {
        print("CORNER stack=" + i + " class=" + w.resourceClass + " caption=" + w.caption +
              " geo=" + g.x + "," + g.y + " " + g.width + "x" + g.height +
              " dock=" + w.dock + " desktop=" + w.desktopWindow + " normal=" + w.normalWindow +
              " keepAbove=" + w.keepAbove + " opacity=" + w.opacity + " minimized=" + w.minimized +
              " onAllDesktops=" + w.onAllDesktops + " popup=" + w.popupWindow + " special=" + w.specialWindow + " managed=" + w.managed + " x11=" + (w.windowId !== undefined) + " skipTaskbar=" + w.skipTaskbar + " pid=" + w.pid);
    }
}
print("CORNER-END total=" + windows.length);
