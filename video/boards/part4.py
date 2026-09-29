from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Dot, Rectangle, VGroup

import facts
from boards.part3 import BOARD as PART3
from kit import pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, ORANGE

BEATS = ("4.1", "4.2", "4.3")


CANDIDATE_ROWS = (1, 1, 1, 1, 1), (2, 2, 2, 2), (3, 3, 3)
WINNER = 11


def massalin():
    doc = pics.paper(2.0)
    year = style.mono("1987", 40, ORANGE).next_to(doc, UP, buff=0.3)
    name = style.serif("Massalin", 36).next_to(doc, DOWN, buff=0.3)
    return VGroup(year, doc, name).move_to([-4.9, 0, 0])


def _candidates(winner_green: bool):
    rows = VGroup()
    k = 0
    for row in CANDIDATE_ROWS:
        strips = VGroup()
        for n in row:
            color = GREEN if (winner_green and k == WINNER) else DIM
            strips.add(VGroup(*[pics.tile("", color, w=0.5, h=0.42) for _ in range(n)]).arrange(RIGHT, buff=0.07))
            k += 1
        rows.add(strips.arrange(RIGHT, buff=0.45))
    rows.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
    return rows


def _flat(rows):
    return [strip for row in rows for strip in row]


def _tests():
    dots = VGroup(*[Dot(radius=0.12, color=BLUE) for _ in range(3)]).arrange(RIGHT, buff=0.45)
    checks = VGroup(*[pics.check(0.3).next_to(d, UP, buff=0.12) for d in dots])
    return VGroup(dots, checks)


def _search_layout(winner_green: bool):
    rows = _candidates(winner_green)
    strips = _flat(rows)
    marks = VGroup(*[pics.x_mark(0.3).move_to(s) for s in strips[:WINNER]])
    tests = _tests().next_to(strips[WINNER], RIGHT, buff=0.6)
    g = VGroup(rows, marks, tests)
    g.scale_to_fit_width(7.6).move_to([2.2, 0, 0])
    return g


def search_start():
    return _search_layout(False)[0]


def search():
    return _search_layout(True)


def winner_of(g):
    return _flat(g[0])[WINNER]


LEN2_ROWS, LEN2_COLS = 11, 35
LEN2_WINNER = 4 * LEN2_COLS + 22


def len1():
    strip = VGroup(*[pics.tile(op, INK, w=1.0, h=0.5) for op in facts.OPS]).arrange(RIGHT, buff=0.1)
    crosses = VGroup(*[pics.x_mark(0.3).next_to(t, UP, buff=0.12) for t in strip])
    size = style.mono("1", 40, DIM).next_to(strip, LEFT, buff=0.45)
    count = style.mono(str(len(facts.OPS)), 40, ORANGE).next_to(strip, RIGHT, buff=0.45)
    g = VGroup(size, strip, crosses, count)
    return g.scale_to_fit_width(12.4).move_to([0, 2.6, 0])


def _cells(visited: bool):
    cells = VGroup(*[Rectangle(width=0.22, height=0.22).set_stroke(DIM, THIN).set_fill(DIM, 0)
                     for _ in range(LEN2_ROWS * LEN2_COLS)]).arrange_in_grid(rows=LEN2_ROWS, cols=LEN2_COLS, buff=0.06)
    if visited:
        for c in cells[:LEN2_WINNER]:
            c.set_fill(DIM, 0.55)
        cells[LEN2_WINNER].set_fill(GREEN, 1).set_stroke(GREEN, THIN)
    return cells


def _len2_layout(visited: bool):
    cells = _cells(visited)
    size = style.mono("2", 40, DIM).next_to(cells, LEFT, buff=0.45)
    count = style.mono("385", 40, ORANGE).next_to(cells, RIGHT, buff=0.45)
    flag = pics.flag(0.55).set_color(GREEN).next_to(cells[LEN2_WINNER], UP, buff=0.02)
    g = VGroup(size, cells, count, flag)
    g.scale_to_fit_width(12.0).move_to([0, -1.2, 0])
    return g


def len2_start():
    return _len2_layout(False)


def len2():
    return _len2_layout(True)


def catch():
    winner = pics.tile("", GREEN, w=0.9, h=0.5)
    tests = _tests().next_to(winner, RIGHT, buff=0.5)
    passed = VGroup(winner, tests)
    field = pics.dot_grid(5, 26, DIM, gap=0.24).next_to(passed, RIGHT, buff=1.0)
    ask = style.mono("?", 90, ORANGE).move_to(field)
    g = VGroup(passed, field, ask)
    return g.scale_to_fit_width(12.0).move_to([0, 2.55, 0])


BOARD = Board("part4", BEATS, (
    Write("4.1", "massalin", massalin),
    Write("4.1", "search", search),
    Erase("4.2", "massalin"),
    Erase("4.2", "search"),
    Write("4.2", "len1", len1),
    Write("4.2", "len2", len2),
    Erase("4.3", "len1"),
    Write("4.3", "catch", catch),
), previous=PART3, wipe="shove")
