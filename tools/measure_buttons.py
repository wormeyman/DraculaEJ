"""Measure each colored button blob in a title bar crop: width vs height, and how many pixels are
off the main color (the fringe). Uses ImageMagick's txt: dump, so no Python imaging library is needed.

Usage: python3 measure_buttons.py SCREENSHOT X Y W H
"""
import subprocess
import sys

BG = (30, 31, 41)


def main() -> None:
    path, x, y, w, h = sys.argv[1], *map(int, sys.argv[2:6])
    out = subprocess.run(["magick", path, "-crop", f"{w}x{h}+{x}+{y}", "+repage", "txt:-"],
                         capture_output=True, text=True, check=True).stdout
    pixels = {}
    for line in out.splitlines()[1:]:
        pos, _, rest = line.partition(":")
        px, py = map(int, pos.split(","))
        rgb = tuple(int(v) for v in rest.split("(")[1].split(")")[0].split(",")[:3])
        pixels[(px, py)] = rgb
    # A pixel belongs to a button if it is clearly not background.
    def is_button(c):
        return sum(abs(a - b) for a, b in zip(c, BG)) > 60
    cols = sorted({p[0] for p, c in pixels.items() if is_button(c)})
    groups, cur = [], [cols[0]]
    for c in cols[1:]:
        if c == cur[-1] + 1:
            cur.append(c)
        else:
            groups.append(cur)
            cur = [c]
    groups.append(cur)
    for g in groups:
        pts = [p for p, c in pixels.items() if is_button(c) and g[0] <= p[0] <= g[-1]]
        ys = [p[1] for p in pts]
        width, height = g[-1] - g[0] + 1, max(ys) - min(ys) + 1
        centre = pixels[((g[0] + g[-1]) // 2, (min(ys) + max(ys)) // 2)]
        print(f"button x={g[0]}-{g[-1]} y={min(ys)}-{max(ys)}  size {width}x{height}  centre colour #{centre[0]:02x}{centre[1]:02x}{centre[2]:02x}")


if __name__ == "__main__":
    main()
