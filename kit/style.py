from __future__ import annotations

from pathlib import Path

import manimpango
from manim import MathTex, Text, config

BG = "#0E1116"
INK = "#ECECEC"
DIM = "#6E7681"
BLUE = "#58A6FF"
ORANGE = "#FFB86B"
GREEN = "#7EE787"
MAGENTA = "#FF7EE3"

SERIF = "STIX Two Text"
MONO = "JetBrains Mono"
REQUIRED_FAMILIES = (SERIF, MONO)
STROKE = 3

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"


class FontError(RuntimeError):
    pass


def register_fonts() -> None:
    files = sorted(FONT_DIR.glob("*.ttf"))
    if not files:
        raise FontError(f"no .ttf files in {FONT_DIR}")
    for path in files:
        manimpango.register_font(str(path))
    available = set(manimpango.list_fonts())
    missing = [family for family in REQUIRED_FAMILIES if family not in available]
    if missing:
        raise FontError(f"font families not available after registration: {missing}")


register_fonts()
config.background_color = BG


def serif(text: str, size: float = 32, color: str = INK, **kwargs) -> Text:
    return Text(text, font=SERIF, font_size=size, color=color, **kwargs)


def mono(text: str, size: float = 28, color: str = INK, **kwargs) -> Text:
    return Text(text, font=MONO, font_size=size, color=color, **kwargs)


def math(tex: str, size: float = 40, color: str = INK) -> MathTex:
    return MathTex(tex, font_size=size, color=color)
