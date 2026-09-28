from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, Arrow, Line, SurroundingRectangle, VGroup

import facts
from boards.intro import BOARD as INTRO
from kit import board, style, zones
from kit.beat import Board, Erase, Keep, Write
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("1.1", "1.2", "1.3", "1.4")
C_NOTES = ((4, "check bit i"), (5, "switch it off"), (8, "x = 0  →  0"))


def headline():
    return board.headline("98 vs 2")


def c_code():
    return zones.fit(board.code_card(facts.C_SOURCE, size=24), "WORK", align="left")


def c_notes():
    card = c_code()
    notes = VGroup()
    for line_no, text in C_NOTES:
        line = card.lines[line_no]
        label = board.note(text, color=ORANGE).move_to([3.0, line.get_y(), 0], aligned_edge=LEFT)
        arrow = Arrow(label.get_left(), line.get_right() + RIGHT * 0.1, buff=0.1, color=ORANGE,
                      stroke_width=STROKE * 0.8, max_tip_length_to_length_ratio=0.12)
        notes.add(VGroup(arrow, label))
    return notes


def asm_wall():
    return zones.fit(board.asm_wall(facts.CLANG_ASM_LINES, columns=5, size=13), "WORK")


def asm_box():
    wall = asm_wall()
    return SurroundingRectangle(VGroup(*wall.lines[1:4]), color=ORANGE, buff=0.05, stroke_width=STROKE)


def asm_group():
    card = board.program_card(list(facts.CLANG_ASM_LINES[1:4]), size=26)
    card.frame.set_stroke(color=ORANGE)
    label = board.note("one group, for bit 0", color=ORANGE)
    return zones.fit(board.stack(label, card), "NOTES", align="top")


def asm_math():
    content = board.stack(board.note("boxed group of 3, once per bit", color=ORANGE),
                          style.math(r"32 \times 3 + 2 = 98", 44))
    return zones.fit(board.rule_box(content), "RULE")


def bars():
    rows = [("clang -O3", facts.CLANG_CLEAR_LOWEST_BIT, ORANGE), ("the trick", facts.TRICK_INSTRUCTIONS, GREEN)]
    return zones.fit(board.count_bars(rows, width=6.0), "WORK")


def two_asm():
    return zones.fit(board.program_card(["lea eax, [rdi - 1]", "and eax, edi"], size=26), "NOTES", align="top")


def same_note():
    g = board.stack(board.note("same result for every input"), style.math(r"x \in [0,\ 2^{32})", 34, BLUE))
    return zones.fit(g, "NOTES", align="bottom")


def title():
    name = style.serif("superopt", 110)
    underline = Line(LEFT, RIGHT, color=BLUE, stroke_width=STROKE)
    underline.scale_to_fit_width(name.width).next_to(name, DOWN, buff=0.1)
    sub = style.serif("the shortest program, proven", 34, DIM)
    return zones.fit(VGroup(name, underline, sub).arrange(DOWN, buff=0.3), "CENTER")


BOARD = Board("part1", BEATS, (
    Write("1.1", "headline", headline),
    Write("1.1", "c_code", c_code),
    Write("1.1", "c_notes", c_notes),
    Erase("1.2", "c_notes"),
    Keep("1.2", "c_code", 0),
    Write("1.2", "asm_wall", asm_wall),
    Write("1.2", "asm_box", asm_box),
    Write("1.2", "asm_group", asm_group),
    Write("1.2", "asm_math", asm_math),
    Erase("1.3", "asm_box"),
    Erase("1.3", "asm_wall"),
    Erase("1.3", "asm_group"),
    Write("1.3", "bars", bars),
    Write("1.3", "two_asm", two_asm),
    Write("1.3", "same_note", same_note),
    Erase("1.4", "headline"),
    Erase("1.4", "c_code"),
    Erase("1.4", "asm_math"),
    Erase("1.4", "bars"),
    Erase("1.4", "two_asm"),
    Erase("1.4", "same_note"),
    Write("1.4", "title", title),
), previous=INTRO)
