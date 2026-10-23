"""Render Tela-dracula folder icons in candidate body colors, side by side on Dracula's background.

Usage: python3 folder_preview.py ICON_DIR OUT_PNG
"""
import os
import subprocess
import sys
import tempfile

# (label, body color, back tab color)
CANDIDATES = [
    ("A  now  #44475a", "#44475a", "#bd93f9"),
    ("B  #7e57c2", "#7e57c2", "#bd93f9"),
    ("C  #9d7cd8", "#9d7cd8", "#6b4fa8"),
    ("D  #bd93f9", "#bd93f9", "#7e57c2"),
]
ICONS = ["default-folder.svg", "default-folder-documents.svg", "default-folder-download.svg"]
BASE_BODY, BASE_TAB = "#44475a", "#bd93f9"


def recolor(svg: str, body: str, tab: str) -> str:
    # Swap through a placeholder so body and tab never overwrite each other.
    return svg.replace(BASE_TAB, "@@TAB@@").replace(BASE_BODY, body).replace("@@TAB@@", tab)


def main() -> None:
    icon_dir, out = sys.argv[1], sys.argv[2]
    work = tempfile.mkdtemp(dir=os.path.dirname(out))
    columns = []
    for i, (label, body, tab) in enumerate(CANDIDATES):
        pngs = []
        for name in ICONS:
            src = open(os.path.realpath(os.path.join(icon_dir, name)), encoding="utf-8").read()
            svg_path = os.path.join(work, f"{i}-{name}")
            open(svg_path, "w", encoding="utf-8").write(recolor(src, body, tab))
            png = svg_path + ".png"
            subprocess.run(["rsvg-convert", "-w", "128", "-h", "128", svg_path, "-o", png], check=True)
            pngs.append(png)
        col = os.path.join(work, f"col{i}.png")
        subprocess.run(
            ["magick", "-background", "#282a36", *pngs, "-gravity", "center", "-append",
             "-fill", "#f8f8f2", "-font", "DejaVu-Sans", "-pointsize", "22",
             "-splice", "0x50", "-annotate", "+0+12", label, "-bordercolor", "#282a36",
             "-border", "30", col],
            check=True,
        )
        columns.append(col)
    subprocess.run(["magick", "-background", "#282a36", *columns, "+append", out], check=True)
    print(out)


if __name__ == "__main__":
    main()
