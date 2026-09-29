from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Line, Mobject, Rectangle, RoundedRectangle, Square, Text, VGroup

from kit import style, zones
from kit.style import BLUE, DIM, INK, STROKE

ADVANCE = 1.55


def _advance(size: float) -> float:
    return style.mono("0", size).width * ADVANCE


def char_row(text: str, size: float = 34, color: str = INK,
             colors: Mapping[int, str] | None = None) -> VGroup:
    colors = colors or {}
    adv = _advance(size)
    row = VGroup()
    row.columns = {}
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        glyph = style.mono(ch, size, colors.get(i, color))
        glyph.move_to(np.array([i * adv, 0.0, 0.0]))
        row.columns[i] = glyph
        row.add(glyph)
    row.digits = [row.columns[i] for i in sorted(row.columns)]
    row.adv = adv
    return row


def register(value: int, n_bits: int = 8, cell: float = 0.62, place_values: bool = False,
             one_color: str = BLUE) -> VGroup:
    if not 0 <= value < (1 << n_bits):
        raise ValueError(f"{value} does not fit in {n_bits} bits")
    bits = format(value, f"0{n_bits}b")
    cells = VGroup(*[Square(side_length=cell, stroke_color=INK, stroke_width=STROKE * 0.7)
                     for _ in range(n_bits)]).arrange(RIGHT, buff=0)
    digits = VGroup()
    for sq, b in zip(cells, bits):
        digits.add(style.mono(b, cell * 55, one_color if b == "1" else INK).move_to(sq))
    places = VGroup()
    if place_values:
        for sq, p in zip(cells, range(n_bits - 1, -1, -1)):
            places.add(style.mono(str(1 << p), cell * 26, DIM).next_to(sq, UP, buff=0.12))
    reg = VGroup(cells, digits, places)
    reg.cells, reg.digits, reg.places = cells, digits, places

    def bit(i: int) -> VGroup:
        j = n_bits - 1 - i
        return VGroup(cells[j], digits[j])

    reg.bit = bit
    return reg


_TRUTH = {"&": lambda a, b: a & b, "|": lambda a, b: a | b, "^": lambda a, b: a ^ b}


def truth_table(op: str = "&", size: float = 28) -> VGroup:
    lines = VGroup()
    for a in (1, 0):
        for b in (1, 0):
            r = _TRUTH[op](a, b)
            lines.add(char_row(f"{a}{op}{b}={r}", size, colors={4: style.GREEN if r else DIM}))
    return lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18)


def note(text: str, size: float = 26, color: str = DIM) -> Text:
    return style.serif(text, size, color)


def stack(*mobs: Mobject, buff: float = 0.25) -> VGroup:
    return VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def _indented_lines(lines: Sequence[str], size: float, colors: Mapping[int, str],
                    t2c: Mapping[str, str] | None = None) -> VGroup:
    adv = _advance(size)
    line_h = style.mono("0", size).height * 1.9
    out = VGroup()
    for i, line in enumerate(lines):
        text = line.lstrip(" ")
        indent = len(line) - len(text)
        y = -i * line_h
        if text:
            m = style.mono(text, size, colors.get(i, INK), t2c=dict(t2c or {}))
            m.move_to(np.array([indent * adv, y, 0.0]), aligned_edge=LEFT)
        else:
            m = Rectangle(width=0.01, height=0.01, stroke_width=0, fill_opacity=0).move_to(np.array([0.0, y, 0.0]))
        out.add(m)
    return out


def _card(body: VGroup, footer: Mobject | None) -> VGroup:
    content = VGroup(body) if footer is None else VGroup(body, footer.next_to(body, DOWN, buff=0.3, aligned_edge=LEFT))
    frame = RoundedRectangle(corner_radius=0.15, width=content.width + 0.6, height=content.height + 0.5,
                             stroke_color=INK, stroke_width=STROKE * 0.7).move_to(content)
    card = VGroup(frame, content)
    card.frame = frame
    card.lines = body
    return card


def program_card(lines: Sequence[str], size: float = 26, colors: Mapping[int, str] | None = None,
                 footer: Mobject | None = None) -> VGroup:
    return _card(_indented_lines(lines, size, colors or {}), footer)


C_KEYWORDS = {"#include": DIM, "uint32_t": BLUE, "for": BLUE, "if": BLUE, "return": BLUE}


def code_card(source: str, size: float = 22) -> VGroup:
    return _card(_indented_lines(source.split("\n"), size, {}, t2c=C_KEYWORDS), None)


def asm_wall(lines: Sequence[str], columns: int = 5, size: float = 13,
             t2c_for=None) -> VGroup:
    per_col = -(-len(lines) // columns)
    cols = VGroup()
    flat: list[Text] = []
    for c in range(columns):
        chunk = lines[c * per_col:(c + 1) * per_col]
        if not chunk:
            break
        col = VGroup(*[style.mono(l, size, DIM if l.endswith(":") else INK, t2c=(t2c_for(l) if t2c_for else {}))
                       for l in chunk])
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cols.add(col)
        flat.extend(col)
    cols.arrange(RIGHT, aligned_edge=UP, buff=0.45)
    cols.lines = flat
    return cols


def headline(text: str, size: float = 40) -> VGroup:
    words = style.serif(text, size)
    underline = Line(LEFT, RIGHT, color=DIM, stroke_width=STROKE * 0.6)
    underline.scale_to_fit_width(words.width).next_to(words, DOWN, buff=0.08)
    return zones.fit(VGroup(words, underline), "HEADLINE", align="left")
