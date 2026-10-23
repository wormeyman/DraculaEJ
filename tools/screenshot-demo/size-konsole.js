// KWin script (demo session only): give the Konsole window a fixed size and position for the screenshot.
const windows = workspace.windowList();
for (let i = 0; i < windows.length; i++) {
    const w = windows[i];
    if (String(w.resourceClass).indexOf("konsole") >= 0) {
        w.frameGeometry = { x: 420, y: 230, width: 1180, height: 640 };
        workspace.activeWindow = w;
        print("SIZED konsole");
    }
}
