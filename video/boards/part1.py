from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Arrow, Rectangle, VGroup

import facts
from boards.intro import BOARD as INTRO
from kit import board, pics, style, zones
from kit.beat import Board, Erase, Write
from kit.style import BLUE, GREEN, ORANGE, STROKE

BEATS = ("1.1", "1.2", "1.3", "1.4")
LOOP_LINES = {"for": 3, "if": 4, "return": 5}


def c_code():
    return zones.fit(board.code_card(facts.C_SOURCE, size=24), "WORK", align="left")


def _scan_row(value: int):
    return zones.fit(pics.switch_row(value, h=0.85), "RIGHT").shift(UP * 0.4)


def scan_start():
    return _scan_row(facts.EXAMPLE)


def scan_demo():
    row = _scan_row(facts.EXAMPLE_AND)
    ptr = pics.pointer().next_to(row.bit(2), UP, buff=0.12)
    i_label = style.mono("i = 2", 34, ORANGE).next_to(row, DOWN, buff=0.6)
    return VGroup(row, ptr, i_label)


def _immediate(line: str) -> dict:
    parts = line.split(", ")
    return {parts[1]: ORANGE} if line.startswith("mov") and len(parts) == 2 else {}


def asm_wall():
    return zones.fit(board.asm_wall(facts.CLANG_ASM_LINES, columns=5, size=13, t2c_for=_immediate), "WORK")


def asm_group():
    card = board.program_card(list(facts.CLANG_ASM_LINES[1:4]), size=28)
    card.frame.set_stroke(color=ORANGE)
    return zones.fit(card, "RIGHT", align="top").shift(DOWN * 0.5)


def asm_math():
    return zones.fit(style.math(r"32 \times 3 + 2 = 98", 54), "RIGHT").shift(DOWN * 1.2)


def bars():
    rows = ((style.mono("clang -O3", 40), facts.CLANG_CLEAR_LOWEST_BIT, ORANGE),
            (style.math(r"x \mathbin{\&} (x-1)", 54), facts.TRICK_INSTRUCTIONS, GREEN))
    group = VGroup()
    group.bars = VGroup()
    for i, (label, value, colour) in enumerate(rows):
        y = -i * 1.5
        label.move_to([-0.35, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max(0.08, 6.0 * value / facts.CLANG_CLEAR_LOWEST_BIT), height=0.8).set_stroke(width=0)
        bar.set_fill(colour, 0.9).move_to([0, y, 0], aligned_edge=LEFT)
        num = style.mono(str(value), 48, colour).next_to(bar, RIGHT, buff=0.3)
        group.bars.add(bar)
        group.add(VGroup(label, bar, num))
    return zones.fit(group, "WORK", align="top").shift(DOWN * 0.4)


def two_asm():
    card = board.program_card(["lea eax, [rdi - 1]", "and eax, edi"], size=28)
    meanings = VGroup()
    arrows = VGroup()
    for line, tex in zip(card.lines, (r"x - 1", r"\&")):
        meaning = style.math(tex, 44, BLUE).move_to([card.get_right()[0] + 1.3, line.get_y(), 0], aligned_edge=LEFT)
        arrows.add(Arrow([card.get_right()[0] + 0.1, line.get_y(), 0], meaning.get_left(), buff=0.1, color=BLUE,
                         stroke_width=STROKE, max_tip_length_to_length_ratio=0.25))
        meanings.add(meaning)
    return zones.fit(VGroup(card, arrows, meanings), "RIGHT", align="top").shift(DOWN * 0.5)


def all_inputs():
    grid = pics.dot_grid(6, 18, GREEN)
    label = style.math(r"2^{32}", 46, GREEN).next_to(grid, RIGHT, buff=0.4)
    tick = pics.check(0.45).next_to(label, RIGHT, buff=0.3)
    return zones.fit(VGroup(grid, label, tick), "WORK").shift(DOWN * 1.9)


def title():
    name = style.serif("superopt", 120)
    proof = VGroup(pics.tile_strip(["sub", "and"], GREEN), pics.check(0.6)).arrange(RIGHT, buff=0.4)
    return zones.fit(VGroup(name, proof).arrange(DOWN, buff=0.6), "CENTER")


BOARD = Board("part1", BEATS, (
    Write("1.1", "c_code", c_code),
    Write("1.1", "scan_demo", scan_demo),
    Erase("1.2", "scan_demo"),
    Erase("1.2", "c_code"),
    Write("1.2", "asm_wall", asm_wall),
    Write("1.2", "asm_group", asm_group),
    Write("1.2", "asm_math", asm_math),
    Erase("1.3", "asm_wall"),
    Erase("1.3", "asm_group"),
    Erase("1.3", "asm_math"),
    Write("1.3", "bars", bars),
    Write("1.3", "two_asm", two_asm),
    Write("1.3", "all_inputs", all_inputs),
    Erase("1.4", "bars"),
    Erase("1.4", "two_asm"),
    Erase("1.4", "all_inputs"),
    Write("1.4", "title", title),
), previous=INTRO, wipe="shove")
