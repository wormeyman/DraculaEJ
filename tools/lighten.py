"""Find the least-lightened version of a color (same hue and saturation) that reaches a contrast target.

Usage: python3 lighten.py FG_HEX BG_HEX TARGET
"""
import colorsys
import sys


def lum(hex_color: str) -> float:
    def ch(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def main() -> None:
    fg, bg, target = sys.argv[1], sys.argv[2], float(sys.argv[3])
    print(f"start {fg} on {bg}: {contrast(fg, bg):.2f}:1")
    r, g, b = (int(fg[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    while l < 1:
        rr, gg, bb = colorsys.hls_to_rgb(h, l, s)
        cand = "#{:02x}{:02x}{:02x}".format(round(rr * 255), round(gg * 255), round(bb * 255))
        if contrast(cand, bg) >= target:
            print(f"result {cand}: {contrast(cand, bg):.2f}:1 (lightness {l:.3f})")
            return
        l += 0.005
    print("not reachable")


if __name__ == "__main__":
    main()
