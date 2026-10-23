"""Build the DraculaEJ Klassy window-decoration preset from Klassy's bundled "Eaten Fruits" preset.

Klassy draws buttons natively at the screen's real resolution, so they stay crisp at 125% where
Aurorae's scaled SVG buttons look soft. The colours match tools/make_buttons.py.

Per-button colour overrides are JSON: {"BackgroundNormal": [R, G, B]} or [opacity%, R, G, B].
State keys (Klassy libbreezecommon/decorationbuttoncolors.h): Icon/Background/Outline x Normal/Hover/Press.

Usage: python3 make_klassy_preset.py EATEN_FRUITS.klpw OUT.klpw
"""
import json
import sys

PRESET_NAME = "DraculaEJ"

# button: (fill, pressed fill, edge, glyph) as RGB
BUTTONS = {
    "Close": ((255, 121, 198), (226, 92, 169), (214, 83, 158), (94, 26, 64)),
    "Minimize": ((255, 184, 108), (232, 160, 82), (212, 144, 74), (107, 61, 16)),
    "Maximize": ((80, 250, 123), (62, 224, 106), (47, 196, 88), (17, 85, 42)),
}

SETTINGS = {
    "ButtonShape": "ShapeSmallCircle",
    "ButtonBackgroundColorsActive": "AccentTrafficLights",
    "ShowIconOnHoverActive": "true",
    "ShowIconOnHoverInactive": "true",
    "ShowCloseIconOnHoverActive": "true",
    "ShowCloseIconOnHoverInactive": "true",
    "KwinButtonsOnLeft": "XIA",
    "KwinButtonsOnRight": "",
    # Circle size follows the icon size. IconMedium measured 25 px at 125% scale; Eric wanted
    # about the 17-18 px of Aurorae ButtonSize=2.
    "IconSize": "IconSmall",
    # Solid title bar (Eaten Fruits uses 50 / 30).
    "TitleBarOpacityActive": "100",
    "TitleBarOpacityInactive": "100",
}


def active_override(fill, pressed, edge, glyph) -> str:
    return json.dumps({
        "BackgroundNormal": list(fill),
        "BackgroundHover": list(fill),
        "BackgroundPress": list(pressed),
        "IconHover": list(glyph),
        "IconPress": list(glyph),
        "OutlineNormal": [100, *edge],
        "OutlineHover": [100, *edge],
        "OutlinePress": [100, *edge],
    }, separators=(",", ":"))


INACTIVE_FILL, INACTIVE_EDGE = (90, 92, 110), (74, 76, 92)


def inactive_override(fill, pressed, edge, glyph) -> str:
    # Unfocused window: plain gray, no symbol until hovered (Klassy otherwise shows the symbols).
    return json.dumps({
        "BackgroundNormal": list(INACTIVE_FILL),
        "BackgroundHover": list(fill),
        "BackgroundPress": list(pressed),
        "IconNormal": [0, 0, 0, 0],
        "IconHover": list(glyph),
        "IconPress": list(glyph),
        "OutlineNormal": [100, *INACTIVE_EDGE],
        "OutlineHover": [100, *edge],
        "OutlinePress": [100, *edge],
    }, separators=(",", ":"))


def main() -> None:
    src, out = sys.argv[1], sys.argv[2]
    lines = open(src, encoding="utf-8").read().splitlines()
    wanted = dict(SETTINGS)
    for button, colours in BUTTONS.items():
        wanted[f"ButtonOverrideColorsActive{button}"] = active_override(*colours)
        wanted[f"ButtonOverrideColorsInactive{button}"] = inactive_override(*colours)
    seen = set()
    result = []
    for line in lines:
        if line.startswith("[Windeco Preset "):
            result.append(f"[Windeco Preset {PRESET_NAME}]")
            continue
        key, sep, _ = line.partition("=")
        if sep and key in wanted:
            result.append(f"{key}={wanted[key]}")
            seen.add(key)
        else:
            result.append(line)
    missing = [k for k in wanted if k not in seen]
    result.extend(f"{k}={wanted[k]}" for k in missing)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(result) + "\n")
    print(f"wrote {out}; added {len(missing)} keys not in the base preset: {missing}")


if __name__ == "__main__":
    main()
