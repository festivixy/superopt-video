from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Rectangle, VGroup

import facts
from boards.part2 import BOARD as PART2
from kit import board, pics, style, zones
from kit.beat import Board, Erase, Write
from kit.style import BLUE, DIM, GREEN, ORANGE

BEATS = ("3.1", "3.2", "3.3", "3.4")


def _machine(covered: bool):
    return zones.fit(pics.program_machine(3, w=8.0, covered=covered), "CENTER")


def machine_open():
    return _machine(False)


def machine():
    m = _machine(True)
    ask = style.mono("?", 110, ORANGE).move_to(m.cover)
    return VGroup(m, ask)


FACES = (r"x + x", r"x \cdot 2", r"x \ll 1")


def trio():
    ms = VGroup(*[pics.program_machine(1, face=f, w=3.8) for f in FACES]).arrange(DOWN, buff=0.45)
    return zones.fit(ms, "HALF_L").move_to([-3.3, 0, 0])


def _shift_row(value: int):
    return zones.fit(pics.switch_row(value, h=1.3), "HALF_R").shift(UP * 1.3)


def shift_start():
    return _shift_row(7)


def shift14():
    row = _shift_row(14)
    values = VGroup(style.mono("7", 52, DIM), style.mono("→", 52, DIM), style.mono("14", 52, BLUE)).arrange(RIGHT, buff=0.3)
    return VGroup(row, values.next_to(row, DOWN, buff=0.4))


def decimal():
    d = VGroup(style.mono("42", 60, DIM), style.mono("→", 60, DIM), style.mono("420", 60, ORANGE)).arrange(RIGHT, buff=0.35)
    return zones.fit(d, "HALF_R").shift(DOWN * 1.9)


def recipes():
    strips = [["add"], ["mul"], ["shl"], ["mul", "sub", "sub"]]
    rows = VGroup()
    for names in strips:
        strip = pics.tile_strip(names, GREEN if len(names) == 1 else DIM)
        rows.add(VGroup(style.mono(str(len(names)), 34, DIM), strip).arrange(RIGHT, buff=0.4))
    rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    return rows.scale_to_fit_width(5.6).move_to([-3.4, 0, 0])


def mystery():
    rows = VGroup(*[pics.tile_strip([""] * n, DIM) for n in (5, 2, 4, 3, 6)]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    ask = style.mono("?", 110, ORANGE).next_to(rows, RIGHT, buff=0.6)
    return VGroup(rows, ask).scale_to_fit_width(5.8).move_to([3.4, 0, 0])


RULES = (["x * 2  →  x << 1"], ["y + 0  →  y"], ["b = a; c = b  →  c = a"])
STEPS = (["mul", "add", "mov"], ["shl", "add", "mov"], ["shl", "mov"], ["shl"])


def rules():
    cards = VGroup(*[board.program_card(r, size=24) for r in RULES]).arrange(DOWN, buff=0.35)
    return zones.fit(cards, "RIGHT", align="top").shift(DOWN * 0.6)


def _passes():
    boxes = VGroup(*[pics.press_machine(w=1.7) for _ in range(4)]).arrange(RIGHT, buff=0.55)
    return zones.fit(boxes, "WORK", align="top").shift(DOWN * 0.9)


def passes():
    boxes = _passes()
    out = pics.tile_strip(STEPS[-1], GREEN).scale(1.35).next_to(boxes, DOWN, buff=0.55).align_to(boxes[-1], LEFT)
    ask = style.mono("?", 72, ORANGE).next_to(out, RIGHT, buff=0.4)
    return VGroup(boxes, out, ask)


def strip_at(stage: int):
    boxes = _passes()
    anchor = boxes[0] if stage == 0 else boxes[stage - 1]
    strip = pics.tile_strip(STEPS[stage], ORANGE if stage == 0 else GREEN).scale(1.35)
    return strip.next_to(boxes, DOWN, buff=0.55).align_to(anchor, LEFT)


def ninety_eight():
    cells = VGroup(*[Rectangle(width=0.2, height=0.2).set_stroke(width=0).set_fill(ORANGE, 0.85)
                     for _ in range(facts.CLANG_CLEAR_LOWEST_BIT)]).arrange_in_grid(rows=4, cols=25, buff=0.05)
    count = style.mono(str(facts.CLANG_CLEAR_LOWEST_BIT), 54, ORANGE).next_to(cells, RIGHT, buff=0.4)
    return VGroup(cells, count).scale_to_fit_width(7.6).move_to([-2.5, -2.5, 0])


BOARD = Board("part3", BEATS, (
    Write("3.1", "machine", machine),
    Erase("3.2", "machine"),
    Write("3.2", "trio", trio),
    Write("3.2", "shift14", shift14),
    Write("3.2", "decimal", decimal),
    Erase("3.3", "trio"),
    Erase("3.3", "shift14"),
    Erase("3.3", "decimal"),
    Write("3.3", "recipes", recipes),
    Write("3.3", "mystery", mystery),
    Erase("3.4", "recipes"),
    Erase("3.4", "mystery"),
    Write("3.4", "rules", rules),
    Write("3.4", "passes", passes),
    Write("3.4", "ninety_eight", ninety_eight),
), previous=PART2, wipe="swipe")
