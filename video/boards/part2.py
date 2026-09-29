from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Arrow, DashedLine, Rectangle, VGroup

import facts
from boards.part1 import BOARD as PART1
from kit import board, pics, style, zones
from kit.beat import Board, Erase, Write
from kit.style import BLUE, DIM, GREEN, ORANGE, STROKE

BEATS = ("2.1", "2.2", "2.3", "2.4")


def _row(value: int):
    return zones.fit(pics.switch_row(value, h=1.0, place_values=True), "WORK", align="top").shift(DOWN * 0.4)


def row_off():
    return _row(0)


def sw108():
    return _row(facts.EXAMPLE)


def sum108():
    return style.math(r"64 + 32 + 8 + 4 = 108", 52, BLUE).next_to(sw108(), DOWN, buff=0.9)


def sw107():
    row = _row(facts.EXAMPLE_MINUS_ONE)
    return VGroup(row, style.mono(str(facts.EXAMPLE_MINUS_ONE), 44, BLUE).next_to(row, DOWN, buff=0.7))


def odometer():
    top = style.mono("1000", 54)
    bottom = style.mono("0999", 54, ORANGE)
    arrow = Arrow(UP * 0.4, DOWN * 0.4, buff=0, color=DIM, stroke_width=STROKE)
    return zones.fit(VGroup(top, arrow, bottom).arrange(DOWN, buff=0.2), "RIGHT").shift(DOWN * 0.3)


def and_rows():
    values = (facts.EXAMPLE, facts.EXAMPLE_MINUS_ONE, facts.EXAMPLE_AND)
    rows = VGroup(*[pics.switch_row(v, h=0.8) for v in values]).arrange(DOWN, buff=0.45)
    labels = VGroup(style.math("x", 40), style.math("x-1", 40), style.math(r"\&", 40))
    for lab, row in zip(labels, rows):
        lab.next_to(row, LEFT, buff=0.45)
    keep = VGroup(*[rows[r].bit(i) for r in (0, 1) for i in range(3, 8)])
    clear = VGroup(*[rows[r].bit(i) for r in (0, 1, 2) for i in range(0, 3)])
    tint_keep = Rectangle(width=keep.width + 0.2, height=keep.height + 0.2).move_to(keep).set_stroke(width=0).set_fill(BLUE, 0.12)
    tint_clear = Rectangle(width=clear.width + 0.2, height=clear.height + 0.2).move_to(clear).set_stroke(width=0).set_fill(ORANGE, 0.12)
    x = (rows[0].bit(3).get_right()[0] + rows[0].bit(2).get_left()[0]) / 2
    boundary = DashedLine([x, rows.get_top()[1] + 0.2, 0], [x, rows.get_bottom()[1] - 0.2, 0]).set_stroke(ORANGE, STROKE)
    value = style.math(r"= 104", 44, GREEN).next_to(rows[2], RIGHT, buff=0.45)
    group = VGroup(tint_keep, tint_clear, rows, labels, boundary, value)
    group.rows, group.labels, group.tint_keep, group.tint_clear = rows, labels, tint_keep, tint_clear
    group.boundary, group.value = boundary, value
    return zones.fit(group, "WORK")


def truth():
    return zones.fit(board.truth_table("&", size=34), "RIGHT")


def palette():
    tiles = VGroup(*[pics.tile(name) for name in facts.OPS]).arrange_in_grid(rows=4, cols=3, buff=(0.25, 0.25))
    tiles.names = dict(zip(facts.OPS, tiles))
    return zones.fit(tiles, "RIGHT")


def program():
    strip = pics.tile_strip(["sub", "and"], GREEN).scale(1.6)
    badge = style.mono("2", 60, GREEN)
    return zones.fit(VGroup(strip, badge).arrange(RIGHT, buff=0.6), "WORK")


BOARD = Board("part2", BEATS, (
    Write("2.1", "sw108", sw108),
    Write("2.1", "sum108", sum108),
    Erase("2.2", "sum108"),
    Erase("2.2", "sw108"),
    Write("2.2", "sw107", sw107),
    Write("2.2", "odometer", odometer),
    Erase("2.3", "sw107"),
    Erase("2.3", "odometer"),
    Write("2.3", "truth", truth),
    Write("2.3", "and_rows", and_rows),
    Erase("2.4", "truth"),
    Erase("2.4", "and_rows"),
    Write("2.4", "palette", palette),
    Write("2.4", "program", program),
), previous=PART1, wipe="fall")
