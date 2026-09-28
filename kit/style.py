from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import manimpango
from fontTools.ttLib import TTFont
from manim import MarkupText, MathTex, Text, config

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
FONT_FILES = {SERIF: "STIXTwoText[wght].ttf", MONO: "JetBrainsMono[wght].ttf"}


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


@lru_cache(maxsize=None)
def _cmap(family: str) -> frozenset[int]:
    return frozenset(TTFont(str(FONT_DIR / FONT_FILES[family])).getBestCmap())


def has_glyph(family: str, char: str) -> bool:
    return char.isspace() or ord(char) in _cmap(family)


def _require_glyphs(text: str, family: str) -> None:
    missing = sorted({c for c in text if not has_glyph(family, c)})
    if missing:
        codes = ", ".join(f"U+{ord(c):04X}" for c in missing)
        raise FontError(f"missing glyph in {family}: {codes} (text {text!r})")


def _escape(char: str) -> str:
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(char, char)


def serif(text: str, size: float = 32, color: str = INK, **kwargs) -> Text | MarkupText:
    """Serif text; characters the serif font lacks (arrows, ≤, ∀ …) are set in the mono font."""
    borrowed = {c for c in text if not has_glyph(SERIF, c)}
    if not borrowed:
        return Text(text, font=SERIF, font_size=size, color=color, **kwargs)
    _require_glyphs("".join(borrowed), MONO)
    markup = "".join(
        f'<span font_family="{MONO}">{_escape(c)}</span>' if c in borrowed else _escape(c) for c in text
    )
    return MarkupText(markup, font=SERIF, font_size=size, color=color, **kwargs)


def mono(text: str, size: float = 28, color: str = INK, **kwargs) -> Text:
    _require_glyphs(text, MONO)
    return Text(text, font=MONO, font_size=size, color=color, **kwargs)


def math(tex: str, size: float = 40, color: str = INK) -> MathTex:
    return MathTex(tex, font_size=size, color=color)
