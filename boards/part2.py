from __future__ import annotations

from manim import DOWN, RIGHT, Brace, VGroup

import facts
from boards.part1 import BOARD as PART1
from kit import board, style, zones
from kit.beat import Board, Erase, Keep, Write
from kit.style import BLUE, DIM, GREEN, INK, ORANGE

BEATS = ("2.1", "2.2", "2.3", "2.4")


def headline():
    return board.headline("numbers are rows of switches")


def reg108():
    return zones.fit(board.register(facts.EXAMPLE, 8, cell=0.8, place_values=True), "WORK", align="top")


def sum108():
    return style.math(r"108 = 64 + 32 + 8 + 4", 44).next_to(reg108(), DOWN, buff=0.8)


def note_regs():
    return zones.fit(board.note("real registers hold\n32 or 64 bits"), "NOTES")


def sub_bin():
    op = board.column_op([("x", "0110 1100"), ("− 1", "1"), ("", "0110 1011")])
    return op.next_to(reg108(), DOWN, buff=0.9)


def borrow_bin():
    return board.borrow_marks(sub_bin(), 0, (1, 0))


def sub_dec():
    op = board.column_op([("", "1000"), ("− 1", "1"), ("", "0999")], size=28)
    marks = board.borrow_marks(op, 0, (2, 1, 0))
    label = board.note("decimal: borrow from the left")
    return zones.fit(board.stack(label, VGroup(op, marks), buff=0.4), "NOTES", align="top")


def minus_rule():
    content = board.stack(style.serif("x − 1:", 28), style.serif("trailing 0s → 1", 26),
                          style.serif("lowest 1 → 0", 26, ORANGE), style.serif("everything above: same", 26))
    return zones.fit(board.rule_box(content), "RULE")


def and_op():
    op = board.column_op([("x", "0110 1100"), ("x − 1", "0110 1011"), ("&", "0110 1000")])
    return op.next_to(reg108(), DOWN, buff=0.9)


def and_marks():
    op = and_op()
    above = VGroup(*[op.digit(2, k) for k in range(3, 8)])
    below = VGroup(*[op.digit(2, k) for k in range(0, 3)])
    b1, b2 = Brace(above, DOWN, color=BLUE), Brace(below, DOWN, color=ORANGE)
    t1 = board.note("kept", color=BLUE)
    t2 = board.note("cleared", color=ORANGE)
    b1.put_at_tip(t1)
    b2.put_at_tip(t2)
    if t2.get_left()[0] < t1.get_right()[0] + 0.15:  # labels would touch: drop the second one a line
        t2.shift(DOWN * (t2.height + 0.12))
    value = style.math(r"= 104", 40).next_to(op.rows[2], RIGHT, buff=0.5)
    return VGroup(b1, t1, b2, t2, value)


def and_table():
    return zones.fit(board.rule_box(board.stack(style.serif("AND: 1 only if both are 1", 26),
                                                board.truth_table("&"))), "RULE")


def isa():
    names = VGroup(*[style.mono(n, 24) for n in facts.OPS]).arrange_in_grid(rows=4, cols=3, buff=(0.5, 0.2))
    names.by_name = dict(zip(facts.OPS, names))
    box = board.rule_box(board.stack(style.serif("the 11 instructions I allow", 26), names))
    box.names = names.by_name
    return zones.fit(box, "RULE")


def length_def():
    return zones.fit(style.math(r"\text{length}(P) = \#\ \text{instructions in } P", 34), "NOTES", align="top")


def tally():
    card = board.program_card(["x - 1  →  sub", "x & …  →  and", "total  =  2"], size=24, colors={2: GREEN})
    return zones.fit(card, "NOTES", align="bottom")


BOARD = Board("part2", BEATS, (
    Write("2.1", "headline", headline),
    Write("2.1", "reg108", reg108),
    Write("2.1", "sum108", sum108),
    Write("2.1", "note_regs", note_regs),
    Erase("2.2", "note_regs"),
    Keep("2.2", "sum108", 0),
    Write("2.2", "sub_bin", sub_bin),
    Write("2.2", "borrow_bin", borrow_bin),
    Write("2.2", "sub_dec", sub_dec),
    Write("2.2", "minus_rule", minus_rule),
    Erase("2.3", "sub_dec"),
    Erase("2.3", "minus_rule"),
    Erase("2.3", "borrow_bin"),
    Erase("2.3", "sub_bin"),
    Write("2.3", "and_table", and_table),
    Write("2.3", "and_op", and_op),
    Write("2.3", "and_marks", and_marks),
    Erase("2.4", "and_marks"),
    Erase("2.4", "and_table"),
    Write("2.4", "isa", isa),
    Write("2.4", "length_def", length_def),
    Write("2.4", "tally", tally),
), previous=PART1)
