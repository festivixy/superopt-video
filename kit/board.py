from __future__ import annotations

from collections.abc import Mapping, Sequence

import numpy as np
from manim import (
    DOWN, LEFT, PI, RIGHT, UP, CurvedArrow, Line, Mobject, Rectangle, RoundedRectangle,
    Square, Text, VGroup,
)

from kit import style, zones
from kit.style import BLUE, DIM, INK, ORANGE, STROKE

ADVANCE = 1.55  # monospace column step, in widths of a "0" glyph


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


def column_op(rows: Sequence[tuple[str, str]], size: float = 34, rule_before_last: bool = True,
              colors: Mapping[tuple[int, int], str] | None = None) -> VGroup:
    colors = colors or {}
    width = max(len(digits) for _, digits in rows)
    adv = _advance(size)
    line_h = style.mono("0", size).height * 2.4
    group = VGroup()
    group.rows = []
    group.labels = VGroup()
    for r, (label, digits) in enumerate(rows):
        padded = digits.rjust(width)
        row_colors = {i: c for (rr, i), c in colors.items() if rr == r}
        row = char_row(padded, size, colors=row_colors)
        row.shift(np.array([0.0, -r * line_h, 0.0]))
        group.rows.append(row)
        group.add(row)
        if label:
            lab = style.mono(label, size * 0.8, DIM)
            lab.move_to(np.array([-adv * 1.2, -r * line_h, 0.0]), aligned_edge=RIGHT)
            group.labels.add(lab)
            group.add(lab)
    if rule_before_last and len(rows) > 1:
        y = -(len(rows) - 1.5) * line_h
        group.rule = Line(np.array([-adv * 0.6, y, 0.0]), np.array([(width - 0.4) * adv, y, 0.0]),
                          color=INK, stroke_width=STROKE)
        group.add(group.rule)
    else:
        group.rule = None

    def digit(row: int, k: int) -> Text:
        return group.rows[row].digits[-1 - k]

    group.digit = digit
    return group


def borrow_marks(op: VGroup, row: int, ks: Sequence[int], color: str = ORANGE) -> VGroup:
    marks = VGroup()
    for k in ks:
        src = op.digit(row, k + 1).get_top() + UP * 0.08
        dst = op.digit(row, k).get_top() + UP * 0.08
        marks.add(CurvedArrow(src, dst, angle=-PI / 2, color=color, stroke_width=STROKE * 0.8, tip_length=0.12))
    return marks


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


def rule_box(content: Mobject, pad: float = 0.3, color: str = DIM) -> VGroup:
    frame = RoundedRectangle(corner_radius=0.12, width=content.width + 2 * pad,
                             height=content.height + 2 * pad, stroke_color=color,
                             stroke_width=STROKE * 0.7).move_to(content)
    g = VGroup(frame, content)
    g.frame, g.content = frame, content
    return g


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


def asm_wall(lines: Sequence[str], columns: int = 5, size: float = 13) -> VGroup:
    per_col = -(-len(lines) // columns)
    cols = VGroup()
    flat: list[Text] = []
    for c in range(columns):
        chunk = lines[c * per_col:(c + 1) * per_col]
        if not chunk:
            break
        col = VGroup(*[style.mono(l, size, DIM if l.endswith(":") else INK) for l in chunk])
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cols.add(col)
        flat.extend(col)
    cols.arrange(RIGHT, aligned_edge=UP, buff=0.45)
    cols.lines = flat
    return cols


def count_bars(rows: Sequence[tuple[str, int, str]], width: float = 6.0, size: float = 28) -> VGroup:
    top = max(v for _, v, _ in rows)
    group = VGroup()
    group.bars, group.labels, group.values = VGroup(), VGroup(), VGroup()
    for i, (label, value, color) in enumerate(rows):
        y = -i * 0.9
        lab = style.mono(label, size, INK).move_to(np.array([-0.3, y, 0.0]), aligned_edge=RIGHT)
        bar = Rectangle(width=max(0.06, width * value / top), height=0.36, stroke_width=0,
                        fill_color=color, fill_opacity=0.9).move_to(np.array([0.0, y, 0.0]), aligned_edge=LEFT)
        num = style.mono(f"{value:,}", size, color).next_to(bar, RIGHT, buff=0.25)
        group.labels.add(lab)
        group.bars.add(bar)
        group.values.add(num)
        group.add(lab, bar, num)
    return group


def timeline(ticks: Sequence[tuple[str, str]], width: float = 12.0, size: float = 20) -> VGroup:
    axis = Line(np.array([-width / 2, 0.0, 0.0]), np.array([width / 2, 0.0, 0.0]),
                color=DIM, stroke_width=STROKE * 0.7)
    marks = VGroup()
    for i, (date, label) in enumerate(ticks):
        x = -width / 2 + width * (i + 0.5) / len(ticks)
        mark = Line(np.array([x, -0.12, 0.0]), np.array([x, 0.12, 0.0]), color=INK, stroke_width=STROKE)
        d = style.mono(date, size, BLUE).next_to(mark, UP, buff=0.1)
        t = style.serif(label, size, DIM).next_to(mark, DOWN, buff=0.1)
        marks.add(VGroup(mark, d, t))
    g = VGroup(axis, marks)
    g.axis, g.ticks = axis, marks
    return g


def headline(text: str, size: float = 40) -> VGroup:
    words = style.serif(text, size)
    underline = Line(LEFT, RIGHT, color=DIM, stroke_width=STROKE * 0.6)
    underline.scale_to_fit_width(words.width).next_to(words, DOWN, buff=0.08)
    return zones.fit(VGroup(words, underline), "HEADLINE", align="left")
