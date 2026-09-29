from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Arrow, VGroup

import facts
from kit import board, cartoon, draw, pics, stage, style, zones
from kit.beat import Board, Erase, Write
from kit.style import BLUE, DIM, GREEN, ORANGE, STROKE

BEATS = ("I.0", "I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "I.8", "I.9")
MACHINE_AT = LEFT * 1.8 + DOWN * 0.4


def dark_room():
    return stage.room(lit=False)


def desk():
    return cartoon.pov_desk()


def code(seed: int, rows: int = 7):
    return lambda: cartoon.code_lines("left", rows=rows, seed=seed)


def game():
    return cartoon.on_screen(pics.mini_game(), "right")


def machine():
    return pics.press_machine(w=5.0).move_to(MACHINE_AT)


def fast_strip():
    m = machine()
    return pics.tile_strip(["add"], GREEN).scale(1.6).next_to(m.chute, RIGHT, buff=0.6)


def raw_strip():
    m = machine()
    return pics.tile_strip(["mov", "imul"]).scale(1.6).next_to(m.chute, RIGHT, buff=0.6)


def input_card():
    m = machine()
    return board.program_card(["y = x * 2"], size=34).next_to(m.hopper, UP, buff=0.4)


def bithacks_page():
    return pics.screenshot("bithacks.png", "graphics.stanford.edu/~seander/bithacks.html", width=11.5)


def book():
    return zones.fit(pics.book_open(), "HALF_L")


def switches_108():
    return zones.fit(pics.switch_row(facts.EXAMPLE, h=0.9), "HALF_R")


def _row_at(value: int, zone: str):
    row = pics.switch_row(value, h=1.0)
    return zones.fit(row, zone).shift(UP * 0.4)


def scan_start():
    return _row_at(facts.EXAMPLE, "HALF_L")


def scan_side():
    row = _row_at(facts.EXAMPLE_AND, "HALF_L")
    ptr = pics.pointer().next_to(row.bit(2), UP, buff=0.12)
    count = style.mono("3 / 32", 34, ORANGE).next_to(row, DOWN, buff=0.6)
    return VGroup(row, ptr, count)


def trick_start():
    return _row_at(facts.EXAMPLE, "HALF_R")


def trick_side():
    row = _row_at(facts.EXAMPLE_AND, "HALF_R")
    expr = style.math(r"x \mathbin{\&} (x - 1)", 54, ORANGE).next_to(row, UP, buff=0.55)
    tiles = pics.tile_strip(["sub", "and"], GREEN).next_to(row, DOWN, buff=0.5)
    count = style.mono("2", 34, GREEN).next_to(tiles, RIGHT, buff=0.35)
    return VGroup(row, expr, tiles, count)


def compiler_q():
    m = pics.press_machine(w=3.0)
    q = pics.tile("?", ORANGE, w=0.75).next_to(m.chute, RIGHT, buff=0.4)
    return zones.fit(VGroup(m, q), "HALF_R")


def _chess_parts():
    b = draw.chess_board(size=4.2)
    bits = [1 if i in b.occupied else 0 for i in range(64)]
    strip = pics.bit_strip(bits, cell=0.16)
    code_line = board.program_card(["b &= b - 1"], size=26)
    rate = style.math(r"\times 10^6 \,/\, \text{s}", 40, ORANGE)
    top = VGroup(b, VGroup(code_line, rate).arrange(DOWN, buff=0.5)).arrange(RIGHT, buff=1.2)
    return zones.fit(VGroup(top, strip).arrange(DOWN, buff=0.55), "CENTER")


def chess():
    return _chess_parts()


def devices():
    kinds = (draw.phone, draw.laptop_icon, draw.browser_window)
    icons = VGroup()
    for i in range(12):
        d = kinds[i % 3]()
        d.add(pics.marble(ORANGE, r=0.07).move_to(d.get_corner(UP + RIGHT)))
        icons.add(d)
    return zones.fit(icons.arrange_in_grid(rows=3, cols=4, buff=(0.9, 0.55)), "CENTER")


def problem():
    eq = style.math(r"\min\ |P| \quad \text{such that} \quad \forall x:\ P(x) = f(x)", 52)
    return zones.fit(eq, "CENTER").shift(UP * 2.0)


def ladder():
    rungs = VGroup(*[pics.tile_strip([""] * n, GREEN if n == 1 else DIM) for n in (1, 2, 3, 4)])
    rungs.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    tick = pics.check(0.45).next_to(rungs[0], RIGHT, buff=0.3)
    return zones.fit(VGroup(rungs, tick), "HALF_L").shift(DOWN * 0.9)


def inputs():
    grid = pics.dot_grid(8, 16, GREEN)
    label = style.math(r"2^{32}", 48, GREEN).next_to(grid, DOWN, buff=0.35)
    return zones.fit(VGroup(grid, label), "HALF_R").shift(DOWN * 0.9)


def headline():
    return board.headline("superoptimization")


MILESTONES = (("May 29", pics.flag), ("Jun 9", pics.magnifier), ("Jun 17", pics.loop_icon),
              ("Jul 28", pics.bug), ("Jul 29", pics.bars_icon), ("Aug 12", pics.check))


def summer():
    assert [d for d, _ in MILESTONES] == [d for d, _ in facts.TIMELINE]
    ticks = VGroup()
    for date, icon in MILESTONES:
        ticks.add(VGroup(icon(0.55), style.mono(date, 22, BLUE)).arrange(DOWN, buff=0.18))
    ticks.arrange(RIGHT, buff=1.0)
    axis = Arrow(ticks.get_corner(DOWN + LEFT) + DOWN * 0.25 + LEFT * 0.3, ticks.get_corner(DOWN + RIGHT) + DOWN * 0.25 + RIGHT * 0.3,
                 buff=0, color=DIM, stroke_width=STROKE, max_tip_length_to_length_ratio=0.02)
    return zones.fit(VGroup(ticks, axis), "CENTER").shift(DOWN * 1.9)


def long_view():
    axis = Arrow(LEFT * 5, RIGHT * 5, buff=0, color=DIM, stroke_width=STROKE, max_tip_length_to_length_ratio=0.02)
    start = VGroup(pics.marble(BLUE, r=0.12), style.mono("1987", 26, BLUE)).arrange(DOWN, buff=0.15)
    end = VGroup(pics.marble(ORANGE, r=0.12), style.mono("2026", 26, ORANGE)).arrange(DOWN, buff=0.15)
    start.move_to(axis.point_from_proportion(0.03)).shift(DOWN * 0.25)
    end.move_to(axis.point_from_proportion(0.97)).shift(DOWN * 0.25)
    return VGroup(axis, start, end).shift(DOWN * 1.9)


BOARD = Board("intro", BEATS, (
    Write("I.0", "room", dark_room),
    Erase("I.0", "room"),
    Write("I.1", "desk", desk),
    Write("I.1", "code_1", code(1)),
    Write("I.1", "game", game),
    Erase("I.2", "desk"),
    Erase("I.2", "code_1"),
    Erase("I.2", "game"),
    Write("I.2", "machine", machine),
    Write("I.2", "fast_strip", fast_strip),
    Erase("I.3", "machine"),
    Erase("I.3", "fast_strip"),
    Write("I.3", "switches_108", switches_108),
    Write("I.3", "book", book),
    Erase("I.4", "book"),
    Erase("I.4", "switches_108"),
    Write("I.4", "scan_side", scan_side),
    Write("I.4", "trick_side", trick_side),
    Erase("I.5", "trick_side"),
    Write("I.5", "compiler_q", compiler_q),
    Erase("I.6", "scan_side"),
    Erase("I.6", "compiler_q"),
    Write("I.6", "chess", chess),
    Erase("I.7", "chess"),
    Write("I.7", "devices", devices),
    Erase("I.8", "devices"),
    Write("I.8", "problem", problem),
    Write("I.8", "ladder", ladder),
    Write("I.8", "inputs", inputs),
    Erase("I.9", "ladder"),
    Erase("I.9", "inputs"),
    Write("I.9", "headline", headline),
    Write("I.9", "summer", summer),
))
