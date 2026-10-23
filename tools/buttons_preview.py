"""Mock up Dracula title bars with different close/minimize/maximize colors, stacked in one PNG.

Usage: python3 buttons_preview.py OUT_PNG
"""
import subprocess
import sys

# (label, close, minimize, maximize)
OPTIONS = [
    ("1  Now: Dracula red / yellow / green", "#ff5555", "#f1fa8c", "#50fa7b"),
    ("2  Pink / purple / cyan", "#ff79c6", "#bd93f9", "#8be9fd"),
    ("3  Red / orange / green", "#ff5555", "#ffb86c", "#50fa7b"),
    ("4  Pink / orange / green", "#ff79c6", "#ffb86c", "#50fa7b"),
    ("5  All purple", "#bd93f9", "#bd93f9", "#bd93f9"),
    ("6  Purple shades (dark to light)", "#7e57c2", "#9d7cd8", "#bd93f9"),
]
BAR_W, BAR_H, ROW_H = 520, 34, 74
BG, BAR, FG, MUTED = "#1e1f29", "#282a36", "#f8f8f2", "#a6a2c4"


def main() -> None:
    out = sys.argv[1]
    rows = []
    for i, (label, close, minimize, maximize) in enumerate(OPTIONS):
        y = i * ROW_H
        rows.append(f'<text x="20" y="{y + 18}" fill="{MUTED}" font-family="DejaVu Sans" font-size="13">{label}</text>')
        rows.append(f'<rect x="20" y="{y + 26}" width="{BAR_W}" height="{BAR_H}" rx="6" fill="{BAR}"/>')
        for j, color in enumerate((close, minimize, maximize)):
            rows.append(f'<circle cx="{40 + j * 22}" cy="{y + 26 + BAR_H / 2}" r="7" fill="{color}"/>')
        rows.append(f'<text x="{20 + BAR_W / 2}" y="{y + 26 + 22}" fill="{FG}" font-family="DejaVu Sans" '
                    f'font-size="13" text-anchor="middle">Home - Dolphin</text>')
    height = len(OPTIONS) * ROW_H + 10
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{BAR_W + 40}" height="{height}">'
           f'<rect width="100%" height="100%" fill="{BG}"/>' + "".join(rows) + "</svg>")
    svg_path = out.rsplit(".", 1)[0] + ".svg"
    open(svg_path, "w", encoding="utf-8").write(svg)
    subprocess.run(["rsvg-convert", "-z", "2", svg_path, "-o", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
