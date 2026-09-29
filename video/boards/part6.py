from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, DashedVMobject, Line, Rectangle, RoundedRectangle, VGroup

import facts
from boards.part5 import BOARD as PART5
from kit import pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("6.1", "6.2", "6.3", "6.4", "6.5", "6.6")

X = facts.EXAMPLE
FLIPPED = X ^ 0xFF
NEG = (-X) & 0xFF
LOWEST = X & NEG
LOWEST_BIT = LOWEST.bit_length() - 1
EIGHT_BIT_INPUTS = 1 << 8
COUNTS = (("1", "11"), ("2", "385"), ("3", "27,720"), ("4", "3,381,840"))
COUNT_VALUES = (11, 385, 27_720, 3_381_840)


def halves():
    strips = VGroup(*[pics.tile_strip([""] * n, DIM) for n in (1, 2, 3)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    for s in strips:
        for t in s:
            t.scale(0.55)
        s.arrange(RIGHT, buff=0.06)
    strips.arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    search = VGroup(strips, pics.magnifier(0.9).next_to(strips, RIGHT, buff=0.25))
    plus = style.math("+", 70)
    proof = pics.stamp("UNSAT", GREEN).scale(0.7)
    return VGroup(search, plus, proof).arrange(RIGHT, buff=0.7).move_to([0, 2.55, 0])


def eight_row(value: int):
    return pics.switch_row(value, h=1.0).move_to([-3.4, -0.6, 0])


def eight():
    row = eight_row(EIGHT_BIT_INPUTS - 1)
    count = style.math(r"2^{8} = 256", 56).next_to(row, DOWN, buff=0.5)
    return VGroup(row, count)


def _grid256():
    return pics.dot_grid(16, 16, DIM, gap=0.24).move_to([3.4, -1.1, 0])


def all256():
    grid = _grid256()
    for d in grid:
        d.set_color(GREEN)
    return grid


def book_date():
    book = pics.book_open().scale(0.55)
    date = style.mono(facts.TIMELINE[1][0], 40, ORANGE).next_to(book, UP, buff=0.3)
    return VGroup(date, book).move_to([-4.6, 1.0, 0])


def _row(value: int, h: float = 0.72):
    return pics.switch_row(value, h=h)


def job():
    x = _row(X).move_to([2.0, 2.0, 0])
    trick = _row(facts.EXAMPLE_AND, 0.55)
    keep = _row(LOWEST, 0.55)
    VGroup(trick, keep).arrange(RIGHT, buff=1.0).move_to([2.0, -0.9, 0])
    trick.fade(0.55)
    arrows = VGroup(*[Line(x.get_bottom() + DOWN * 0.15, r.get_top() + UP * 0.35).add_tip(tip_length=0.18)
                      .set_stroke(DIM, THIN).set_fill(DIM, 1) for r in (trick, keep)])
    trick_label = style.math(r"x \,\&\, (x-1)", 38, DIM).next_to(trick, DOWN, buff=0.35)
    keep_label = style.mono("?", 64, ORANGE).next_to(keep, DOWN, buff=0.3)
    ring = RoundedRectangle(corner_radius=0.1, width=keep.bit(LOWEST_BIT).width + 0.2,
                            height=keep.bit(LOWEST_BIT).height + 0.2).set_stroke(GREEN, STROKE).move_to(keep.bit(LOWEST_BIT))
    g = VGroup(x, arrows, trick, keep, trick_label, keep_label, ring)
    g.x, g.trick, g.keep = x, trick, keep
    return g


def job_start():
    return job().x


def ones():
    strip = VGroup(*[pics.tile(op, INK, w=1.0, h=0.5) for op in facts.OPS]).arrange(RIGHT, buff=0.1)
    crosses = VGroup(*[pics.x_mark(0.3).next_to(t, UP, buff=0.12) for t in strip])
    size = style.mono("1", 40, DIM).next_to(strip, LEFT, buff=0.45)
    count = style.mono(str(len(facts.OPS)), 40, ORANGE).next_to(strip, RIGHT, buff=0.45)
    return VGroup(size, strip, crosses, count).scale_to_fit_width(12.4).move_to([0, -0.6, 0])


def found():
    tiles = pics.tile_strip(["neg", "and"], GREEN).scale(1.3)
    size = style.mono("2", 48, GREEN).next_to(tiles, LEFT, buff=0.5)
    eq = style.math(r"x \,\&\, (-x)", 60, GREEN).next_to(tiles, RIGHT, buff=0.8)
    return VGroup(size, tiles, eq).move_to([0, 2.9, 0])


ROW_H = 0.95


def _labelled(value: int, label: str, number: str, y: float):
    row = pics.switch_row(value, h=ROW_H)
    name = style.math(label, 56).next_to(row, LEFT, buff=0.6)
    num = style.mono(number, 44, DIM).next_to(row, RIGHT, buff=0.6) if number else VGroup()
    g = VGroup(name, row, num)
    g.shift([0, y - row.get_center()[1], 0] - row.get_center() * [1, 0, 0])
    g.row = row
    return g


def x_row():
    return _labelled(X, "x", str(X), 1.2)


def flip_row():
    return _labelled(FLIPPED, r"\sim x", "", -0.45)


def neg_row():
    return _labelled(NEG, "-x", f"-{X}", -0.45)


def carry_row():
    return _labelled(X, "x", "", -0.45)


def and_row():
    g = _labelled(LOWEST, r"\&", str(LOWEST), -2.35)
    rule = Line(LEFT * 4.2, RIGHT * 4.2).set_stroke(DIM, THIN).move_to([0, -1.45, 0])
    top = x_row().row.bit(LOWEST_BIT)
    frame = Rectangle(width=top.width + 0.25, height=1.2 + 2.35 + ROW_H + 0.3).set_stroke(GREEN, STROKE)
    frame.move_to([top.get_center()[0], (1.2 - 2.35) / 2, 0])
    return VGroup(g, rule, frame)


def column_box(i: int, color: str):
    top = x_row().row.bit(i)
    box = Rectangle(width=top.width + 0.2, height=1.2 + 0.45 + ROW_H + 0.2).set_stroke(color, STROKE)
    return DashedVMobject(box.move_to([top.get_center()[0], (1.2 - 0.45) / 2, 0]), num_dashes=30)


def minimum():
    two = style.mono("2", 60, GREEN)
    return VGroup(two, pics.check(0.6).next_to(two, RIGHT, buff=0.2)).move_to([5.7, 2.9, 0])


UNIT = 0.55
BASE_Y = -2.7


def _bar(count: float, x: float, color: str, w: float = 0.8):
    from math import log10
    h = log10(count) * UNIT
    return Rectangle(width=w, height=h).set_stroke(color, THIN).set_fill(color, 0.35).move_to([x, BASE_Y + h / 2, 0])


def counts():
    bars = VGroup()
    for k, ((length, label), value) in enumerate(zip(COUNTS, COUNT_VALUES)):
        x = -5.6 + k * 1.45
        bar = _bar(value, x, BLUE)
        top = style.mono(label, 26, INK).next_to(bar, UP, buff=0.15)
        under = style.mono(length, 32, DIM).next_to(bar, DOWN, buff=0.2)
        bars.add(VGroup(bar, top, under))
    return bars


def constant():
    value = COUNT_VALUES[-1] * 2 ** 32
    bar = _bar(value, 0.6, ORANGE)
    tile = pics.tile("c", ORANGE, w=0.8, h=0.55).next_to(bar, DOWN, buff=0.2)
    times = style.math(r"\times 2^{32}", 52, ORANGE).next_to(bar, RIGHT, buff=0.3).shift(DOWN * 0.8)
    return VGroup(bar, tile, times)


def wall():
    bricks = VGroup()
    w, h = 0.9, 0.42
    for r in range(13):
        offset = 0 if r % 2 == 0 else w / 2
        for c in range(3):
            bricks.add(Rectangle(width=w, height=h).set_stroke(INK, THIN).set_fill(DIM, 0.2)
                       .move_to([4.1 + offset + c * w, BASE_Y + h / 2 + r * h, 0]))
    glass = pics.magnifier(1.2).next_to(bricks, LEFT, buff=0.15).align_to([0, BASE_Y, 0], DOWN)
    return VGroup(bricks, glass)


BOARD = Board("part6", BEATS, (
    Write("6.1", "halves", halves),
    Write("6.1", "eight", eight),
    Write("6.1", "all256", all256),
    Erase("6.2", "halves"),
    Erase("6.2", "eight"),
    Erase("6.2", "all256"),
    Write("6.2", "book_date", book_date),
    Write("6.2", "job", job),
    Erase("6.3", "book_date"),
    Erase("6.3", "job"),
    Write("6.3", "ones", ones),
    Write("6.3", "found", found),
    Erase("6.4", "ones"),
    Write("6.4", "x_row", x_row),
    Write("6.4", "neg_row", neg_row),
    Write("6.5", "and_row", and_row),
    Write("6.5", "minimum", minimum),
    Erase("6.6", "found"),
    Erase("6.6", "x_row"),
    Erase("6.6", "neg_row"),
    Erase("6.6", "and_row"),
    Erase("6.6", "minimum"),
    Write("6.6", "counts", counts),
    Write("6.6", "constant", constant),
    Write("6.6", "wall", wall),
), previous=PART5, wipe="swipe")
