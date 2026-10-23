// Move the dock (the panel holding the task manager) to the right screen edge, centered.
var ps = panels();
for (var i = 0; i < ps.length; i++) {
    var ws = ps[i].widgets();
    for (var j = 0; j < ws.length; j++) {
        if (ws[j].type === "org.kde.plasma.icontasks") {
            ps[i].location = "right";
            ps[i].alignment = "center";
        }
    }
}
