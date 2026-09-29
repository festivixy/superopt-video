from __future__ import annotations

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, TAU, UP, Arrow, Brace, Circle, DashedVMobject, Dot, Line, NumberLine, Polygon,
    Rectangle, RoundedRectangle, VGroup,
)

import facts
from boards.part5 import z3_chip
from boards.part7 import BOARD as PART7
from kit import draw, pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("8.1", "8.2", "8.3", "8.4", "8.5", "8.6", "8.7", "8.8", "8.9", "8.10")


def arrow(a, b):
    return Arrow(a, b, buff=0.15, stroke_width=3, max_tip_length_to_length_ratio=0.25).set_color(DIM)


def stopwatch(frac: float, r: float = 0.9, hand_color: str = ORANGE):
    face = Circle(radius=r).set_stroke(INK, STROKE)
    button = Rectangle(width=r * 0.32, height=r * 0.2).set_stroke(INK, STROKE).next_to(face, UP, buff=0.03)
    ticks = VGroup(*[Line(UP * r * 0.8, UP * r * 0.94).rotate(-TAU * k / 12, about_point=ORIGIN).set_stroke(DIM, THIN)
                     for k in range(12)])
    hand = Line(ORIGIN, UP * r * 0.72).set_stroke(hand_color, STROKE).rotate(-TAU * frac, about_point=ORIGIN)
    pin = Dot(radius=0.06, color=hand_color)
    g = VGroup(face, button, ticks, hand, pin)
    g.face, g.hand = face, hand
    return g


def bag(content, w: float = 0.8, h: float = 0.72):
    body = RoundedRectangle(corner_radius=0.18, width=w, height=h).set_stroke(INK, THIN)
    top = body.get_top()
    tie = Polygon(top + LEFT * w * 0.18 + UP * 0.16, top + RIGHT * w * 0.18 + UP * 0.16, top).set_stroke(INK, THIN)
    content.move_to(body).shift(DOWN * h * 0.04)
    return VGroup(body, tie, content)


def slots(names, color: str = INK, w: float = 1.1):
    return VGroup(*[pics.tile(n, color, w=w, h=0.6) for n in names]).arrange(RIGHT, buff=0.14)


def interpreter(w: float = 2.4):
    return pics.program_machine(2, w=w, covered=False)


PROOF_Y, FUZZ_Y = 1.7, -1.3
TRICK = ["sub", "and"]


def _lane_start(y: float):
    return pics.tile_strip(TRICK, INK).scale(0.9).move_to([-5.4, y, 0])


def lane_proof():
    strip = _lane_start(PROOF_Y)
    formula = style.math(r"x \,\&\, (x - 1)", 44).move_to([-1.9, PROOF_Y, 0])
    chip = z3_chip(1.7).move_to([1.4, PROOF_Y, 0])
    ok = pics.check(0.6).move_to([4.0, PROOF_Y, 0])
    arrows = VGroup(arrow(strip.get_right(), formula.get_left()), arrow(formula.get_right(), chip.get_left() + LEFT * 0.22),
                    arrow(chip.get_right() + RIGHT * 0.22, ok.get_left()))
    g = VGroup(strip, arrows, formula, chip, ok)
    g.strip, g.arrows, g.formula, g.chip, g.ok = strip, arrows, formula, chip, ok
    return g


def lane_fuzz():
    strip = _lane_start(FUZZ_Y)
    machine = interpreter(2.4).move_to([-1.9, FUZZ_Y, 0])
    count = style.mono("100,000", 30, BLUE).next_to(machine, UP, buff=0.25)
    original = draw.code_icon().scale_to_fit_height(1.0).move_to([1.4, FUZZ_Y, 0])
    ok = pics.check(0.6).move_to([4.0, FUZZ_Y, 0])
    arrows = VGroup(arrow(strip.get_right(), machine.inlet.get_left()),
                    arrow(machine.outlet.get_right(), original.get_left()),
                    arrow(original.get_right(), ok.get_left()))
    g = VGroup(strip, arrows, machine, count, original, ok)
    g.strip, g.arrows, g.machine, g.count, g.original, g.ok = strip, arrows, machine, count, original, ok
    return g


def both():
    pair = VGroup(lane_proof().ok, lane_fuzz().ok)
    brace = Brace(pair, RIGHT, buff=0.35).set_color(DIM)
    big = pics.check(1.1).next_to(brace, RIGHT, buff=0.35)
    return VGroup(brace, big)


BEFORE = (1, 0, 1, 1, 0, 1, 0, 0)
LSHR = (0,) + BEFORE[:-1]
ASHR = (BEFORE[0],) + BEFORE[:-1]
ROW_Y = {"lshr": 2.3, "ashr": 0.6}
CELL = 0.55


def shift_strip(bits, row: str):
    return pics.bit_strip(bits, cell=CELL).move_to([-0.6, ROW_Y[row], 0])


def _shift_row(row: str, bits, z3_name: str, fill_color: str):
    strip = shift_strip(bits, row)
    strip.cells[0].set_stroke(fill_color, STROKE)
    name = pics.tile(row, INK, w=1.3, h=0.6).next_to(strip, LEFT, buff=0.6)
    spelling = style.mono(z3_name, 30, fill_color).next_to(strip, RIGHT, buff=0.6)
    g = VGroup(name, strip, spelling)
    g.name, g.strip, g.spelling = name, strip, spelling
    return g


def shifts():
    return VGroup(_shift_row("lshr", LSHR, "LShR(x, 1)", BLUE), _shift_row("ashr", ASHR, "x >> 1", ORANGE))


def _side():
    body = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.9).set_stroke(INK, THIN)
    return VGroup(body, style.mono("x >> 1", 28, ORANGE).move_to(body))


def trap():
    g = VGroup(_side(), style.math("=", 48), _side(), pics.check(0.55)).arrange(RIGHT, buff=0.35)
    return g.move_to([-3.2, -2.3, 0])


def fuzz_catch():
    machine = interpreter(2.2)
    dots = pics.dot_grid(3, 3, BLUE, gap=0.22).next_to(machine.inlet, LEFT, buff=0.3)
    miss = pics.x_mark(0.6).next_to(machine.outlet, RIGHT, buff=0.4)
    return VGroup(dots, machine, miss).move_to([3.7, -2.3, 0])


def min_run():
    m = pics.program_machine(3, face=r"\min(x, y)", w=4.2).move_to([-1.6, 1.4, 0])
    ins = VGroup(style.math(r"x = -2^{31}", 40, BLUE), style.math(r"y = 1", 40, BLUE)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    ins.next_to(m.inlet, LEFT, buff=0.35)
    got = style.mono("1", 52, ORANGE).next_to(m.outlet, RIGHT, buff=0.45)
    want = VGroup(style.math(r"\neq", 44, DIM), style.math(r"-2^{31}", 40, GREEN)).arrange(RIGHT, buff=0.25)
    want.next_to(got, RIGHT, buff=0.3)
    g = VGroup(m, ins, got, want)
    g.machine, g.ins, g.got, g.want = m, ins, got, want
    return g


def rejected():
    return pics.x_mark(1.3).set_stroke(ORANGE, STROKE * 2.2).move_to(min_run().machine)


def no_compare():
    ops = VGroup(*[pics.tile(op, DIM, w=0.95, h=0.5) for op in facts.OPS])
    ops.arrange_in_grid(rows=2, cols=6, buff=(0.12, 0.2))
    missing = pics.tile("<", ORANGE, w=0.95, h=0.5)
    missing = VGroup(DashedVMobject(missing.body, num_dashes=18).set_stroke(ORANGE, THIN), missing.label)
    missing.move_to(ops[-1]).shift(RIGHT * 1.07)
    cross = pics.x_mark(0.42).move_to(missing)
    return VGroup(ops, missing, cross).move_to([-1.2, -2.3, 0])


SUITE_ROWS = 8


def suite():
    rows = VGroup()
    for _ in range(SUITE_ROWS):
        dot = Dot(radius=0.08, color=GREEN)
        bar = Line(ORIGIN, RIGHT * 1.1).set_stroke(DIM, THIN)
        rows.add(VGroup(dot, bar, pics.check(0.3)).arrange(RIGHT, buff=0.15))
    return rows.arrange(DOWN, buff=0.28).move_to([-5.7, -0.2, 0])


def floor():
    absx = style.math(r"|x|", 56)
    tries = VGroup()
    for n in (1, 2, 3):
        strip = VGroup(*[pics.tile("", GREEN if n == 3 else DIM, w=0.45, h=0.4) for _ in range(n)]).arrange(RIGHT, buff=0.06)
        if n < 3:
            strip.add(pics.x_mark(0.34).move_to(strip))
        tries.add(strip)
    tries.arrange(RIGHT, buff=0.5)
    return VGroup(absx, tries).arrange(RIGHT, buff=0.6).move_to([1.3, 2.9, 0])


def _bags1_row():
    return VGroup(*[bag(pics.tile(op, INK, w=0.62, h=0.3)) for op in facts.OPS]).arrange(RIGHT, buff=0.14)


def bags1():
    row = _bags1_row()
    ticks = VGroup(*[pics.check(0.22).next_to(b, DOWN, buff=0.08) for b in row])
    count = style.mono("11", 40, ORANGE).next_to(row, RIGHT, buff=0.35)
    g = VGroup(row, ticks, count).move_to([1.3, 1.1, 0])
    g.row, g.ticks, g.count = row, ticks, count
    return g


BAGS2 = 66


def bags2():
    pair = lambda: VGroup(*[Rectangle(width=0.16, height=0.16).set_stroke(INK, THIN) for _ in range(2)]).arrange(RIGHT, buff=0.05)
    grid = VGroup(*[bag(pair(), w=0.62, h=0.5) for _ in range(BAGS2)]).arrange_in_grid(rows=6, cols=11, buff=(0.22, 0.24))
    for b in grid:
        b[0].set_stroke(GREEN, THIN)
    grid.scale_to_fit_height(2.6)
    count = style.mono("66", 40, ORANGE).next_to(grid, RIGHT, buff=0.35)
    g = VGroup(grid, count).move_to([1.3, -2.15, 0])
    g.grid, g.count = grid, count
    return g


FAST = 0.02


def space8():
    return pics.dot_grid(14, 22, DIM, gap=0.26).move_to([-2.6, 0, 0])


def watch():
    w = stopwatch(0.015, r=1.3).move_to([4.2, 0.6, 0])
    readout = style.mono(f"{FAST} s", 48, ORANGE).next_to(w, DOWN, buff=0.4)
    g = VGroup(w, readout)
    g.watch, g.readout = w, readout
    return g


LINE_CELL = 0.42


def lines():
    row = slots([str(k) for k in range(4)], INK, w=1.2).move_to([-2.6, 2.7, 0])
    codes = VGroup(*[pics.bit_strip([(k >> 1) & 1, k & 1], cell=LINE_CELL).next_to(t, DOWN, buff=0.3)
                     for k, t in zip(range(4), row)])
    g = VGroup(row, codes)
    g.row, g.codes = row, codes
    return g


def rule(tex: str, color: str = INK):
    return style.math(tex, 60, color).move_to([4.3, 2.4, 0])


def rule4():
    return rule(r"\ell < 4")


FOUR_CELL = 0.8


def _four_parts():
    four = style.mono("4", 64, BLUE).move_to([-4.6, -1.3, 0])
    strip = pics.bit_strip([1, 0, 0], cell=FOUR_CELL).next_to(four, RIGHT, buff=1.4)
    link = arrow(four.get_right(), strip.get_left())
    return four, link, strip


def four_start():
    return VGroup(*_four_parts())


def _register(cells, color: str):
    return RoundedRectangle(corner_radius=0.1, width=cells.width + 0.3, height=cells.height + 0.3).set_stroke(color, STROKE).move_to(cells)


def four():
    four_m, link, strip = _four_parts()
    low = VGroup(*strip.cells[1:])
    frame = _register(low, ORANGE)
    fallen = strip.cells[0].copy().set_opacity(0.3).rotate(0.5).shift(DOWN * 1.3 + LEFT * 0.2)
    kept = VGroup(*strip.cells[1:])
    zero = style.mono("= 0", 56, ORANGE).next_to(frame, RIGHT, buff=0.5)
    g = VGroup(four_m, link, kept, frame, fallen, zero)
    g.kept, g.frame, g.fallen, g.zero = kept, frame, fallen, zero
    return g


def wrong_rule():
    return rule(r"\ell < 0", ORANGE)


def rule_fixed():
    return rule(r"\ell < 4", GREEN)


def empty_line():
    line = NumberLine(x_range=[0, 4, 1], length=4.4, include_numbers=False, color=INK).move_to([4.2, -0.2, 0])
    nums = VGroup(*[style.mono(str(k), 26, DIM).next_to(line.n2p(k), DOWN, buff=0.2) for k in range(5)])
    left_zone = Rectangle(width=1.6, height=0.7).set_stroke(ORANGE, THIN).set_fill(ORANGE, 0.12)
    left_zone.next_to(line.n2p(0), LEFT, buff=0.1)
    nothing = pics.x_mark(0.4).move_to(left_zone)
    return VGroup(line, nums, left_zone, nothing)


def unsat8():
    return pics.stamp("UNSAT", GREEN).scale(0.65).move_to([4.3, 1.1, 0])


def fix():
    four_m, link, strip = _four_parts()
    for c in strip.cells:
        c.set_stroke(GREEN, THIN)
    frame = _register(strip.cells, GREEN)
    return VGroup(four_m, link, strip, frame)


SETUP4 = ("x", "c", "op", "op")
SETUP5 = ("x", "c", "c", "op", "op")


def expect():
    wanted = pics.stamp("UNSAT", DIM).scale(0.7)
    wanted = VGroup(DashedVMobject(wanted[0], num_dashes=30).set_stroke(DIM, THIN), wanted.label)
    got = pics.stamp("UNSAT", GREEN).scale(0.7)
    g = VGroup(wanted, style.math("=", 52), got, pics.check(0.6)).arrange(RIGHT, buff=0.4)
    return g.move_to([-2.6, 2.6, 0])


def setup4():
    row = slots(SETUP4, INK)
    count = style.mono("4", 48, ORANGE).next_to(row, RIGHT, buff=0.45)
    return VGroup(row, count).move_to([-3.0, 0.4, 0])


def floors3():
    cards = VGroup()
    for _ in range(3):
        strip = VGroup(*[pics.tile("", GREEN, w=0.5, h=0.42) for _ in range(3)]).arrange(RIGHT, buff=0.06)
        frame = RoundedRectangle(corner_radius=0.12, width=strip.width + 0.4, height=strip.height + 0.36).set_stroke(DIM, THIN)
        frame.move_to(strip)
        critter = pics.bug(0.5).next_to(frame, RIGHT, buff=0.12)
        cards.add(VGroup(frame, strip, critter))
    return cards.arrange(DOWN, buff=0.4).move_to([4.4, 0.6, 0])


def bumped():
    row = slots(SETUP5, INK)
    count = style.mono("5", 48, DIM).next_to(row, RIGHT, buff=0.45)
    ghost = pics.bug(0.6).set_opacity(0.25).next_to(row, DOWN, buff=0.2)
    return VGroup(row, count, ghost).move_to([-2.6, -2.3, 0])


def all_no():
    stamps = VGroup(*[pics.stamp("UNSAT", GREEN).scale(0.36) for _ in range(18)]).arrange_in_grid(rows=3, cols=6, buff=(0.35, 0.3))
    return stamps.move_to([0, 2.0, 0])


def regression():
    row = slots(SETUP4, INK)
    program = style.math(r"x \,\&\, (x - 1)", 52, GREEN)
    g = VGroup(row, program).arrange(RIGHT, buff=1.6)
    link = arrow(row.get_right(), program.get_left())
    ok = pics.check(0.7).next_to(program, RIGHT, buff=0.5)
    out = VGroup(row, link, program, ok).move_to([0, -1.6, 0])
    out.row, out.link, out.program, out.ok = row, link, program, ok
    return out


def watches():
    old = stopwatch(0.015, r=0.8)
    old_read = style.mono(f"{FAST} s", 30, DIM).next_to(old, DOWN, buff=0.25)
    old.set_stroke(opacity=0.5)
    old_g = VGroup(old, old_read)
    cross = pics.x_mark(0.7).move_to(old)
    new = stopwatch(0.62, r=1.2, hand_color=GREEN)
    checked = pics.dot_grid(8, 12, DIM, gap=0.24)
    g = VGroup(VGroup(old_g, cross), new, checked).arrange(RIGHT, buff=1.1).move_to([0, 1.7, 0])
    g.old, g.new, g.checked = g[0], new, checked
    return g


def held():
    cards = VGroup()
    for _ in range(3):
        strip = VGroup(*[pics.tile("", GREEN, w=0.5, h=0.42) for _ in range(3)]).arrange(RIGHT, buff=0.06)
        frame = RoundedRectangle(corner_radius=0.12, width=strip.width + 0.4, height=strip.height + 0.36).set_stroke(DIM, THIN)
        frame.move_to(strip)
        cards.add(VGroup(frame, strip, pics.check(0.4).next_to(frame, RIGHT, buff=0.15)))
    return cards.arrange(RIGHT, buff=0.5).scale(0.85).move_to([-2.4, -1.9, 0])


def habit():
    quick = stopwatch(0.015, r=0.55)
    st = pics.stamp("UNSAT", GREEN).scale(0.55)
    glass = pics.magnifier(1.1)
    g = VGroup(quick, st, glass).arrange(RIGHT, buff=0.35)
    return g.move_to([4.2, -1.9, 0])


BOARD = Board("part8", BEATS, (
    Write("8.1", "lane_proof", lane_proof),
    Write("8.1", "lane_fuzz", lane_fuzz),
    Write("8.1", "both", both),
    Erase("8.2", "lane_proof"),
    Erase("8.2", "lane_fuzz"),
    Erase("8.2", "both"),
    Write("8.2", "shifts", shifts),
    Write("8.2", "trap", trap),
    Write("8.2", "fuzz_catch", fuzz_catch),
    Erase("8.3", "shifts"),
    Erase("8.3", "trap"),
    Erase("8.3", "fuzz_catch"),
    Write("8.3", "min_run", min_run),
    Write("8.3", "no_compare", no_compare),
    Write("8.3", "rejected", rejected),
    Erase("8.4", "min_run"),
    Erase("8.4", "no_compare"),
    Erase("8.4", "rejected"),
    Write("8.4", "floor", floor),
    Write("8.4", "bags1", bags1),
    Write("8.4", "bags2", bags2),
    Write("8.4", "suite", suite),
    Erase("8.5", "floor"),
    Erase("8.5", "bags1"),
    Erase("8.5", "bags2"),
    Erase("8.5", "suite"),
    Write("8.5", "space8", space8),
    Write("8.5", "watch", watch),
    Erase("8.6", "space8"),
    Erase("8.6", "watch"),
    Write("8.6", "lines", lines),
    Write("8.6", "rule4", rule4),
    Write("8.6", "four", four),
    Erase("8.7", "rule4"),
    Write("8.7", "wrong_rule", wrong_rule),
    Write("8.7", "empty_line", empty_line),
    Write("8.7", "unsat8", unsat8),
    Erase("8.7", "unsat8"),
    Erase("8.7", "wrong_rule"),
    Write("8.7", "rule_fixed", rule_fixed),
    Erase("8.7", "four"),
    Write("8.7", "fix", fix),
    Erase("8.8", "lines"),
    Erase("8.8", "rule_fixed"),
    Erase("8.8", "empty_line"),
    Erase("8.8", "fix"),
    Write("8.8", "expect", expect),
    Write("8.8", "setup4", setup4),
    Write("8.8", "floors3", floors3),
    Write("8.8", "bumped", bumped),
    Erase("8.9", "expect"),
    Erase("8.9", "setup4"),
    Erase("8.9", "floors3"),
    Erase("8.9", "bumped"),
    Write("8.9", "all_no", all_no),
    Write("8.9", "regression", regression),
    Erase("8.10", "all_no"),
    Erase("8.10", "regression"),
    Write("8.10", "watches", watches),
    Write("8.10", "held", held),
    Write("8.10", "habit", habit),
), previous=PART7, wipe="fall")
