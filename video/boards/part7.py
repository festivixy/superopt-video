from __future__ import annotations

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, ArcBetweenPoints, Arrow, Circle, CurvedArrow, DashedVMobject, Dot, Line, Polygon,
    Rectangle, RoundedRectangle, Square, VGroup,
)

from boards.part5 import z3_chip
from boards.part6 import BOARD as PART6
from kit import pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8")

TARGET = 0xAAAAAAAA
GUESSES = (0x88280288, 0x8AAAAAAA, 0xAAAAAAAA)
COUNTEREXAMPLES = (0x0282A822, 0x20000000)


def bits_of(v: int) -> list[int]:
    return [int(b) for b in format(v, "032b")]


def wrong_cells(guess: int) -> list[int]:
    diff = TARGET & ~guess & 0xFFFFFFFF
    return [j for j, b in enumerate(bits_of(diff)) if b]


def hexs(v: int) -> str:
    return f"0x{v:08X}"


def solver(tex: str, w: float = 2.0, color: str = BLUE):
    body = RoundedRectangle(corner_radius=0.12, width=w, height=w * 0.7).set_stroke(INK, STROKE).set_fill(opacity=0)
    pins = VGroup()
    for k in range(4):
        y = body.get_top()[1] - body.height * (k + 0.8) / 4.6
        for side, d in ((body.get_left()[0], -1), (body.get_right()[0], 1)):
            pins.add(Line([side, y, 0], [side + d * 0.2, y, 0]).set_stroke(DIM, THIN))
    label = style.math(tex, w * 20, color).move_to(body)
    chip = VGroup(pins, body, label)
    chip.body, chip.label = body, label
    return chip


def question():
    return style.math(r"\exists P\ \forall x:\ P(x) = f(x)", 56).move_to([0, 3.0, 0])


def layers():
    rows = VGroup()
    for n in (1, 2, 2, 3):
        strip = VGroup(*[pics.tile("", DIM, w=0.45, h=0.36) for _ in range(n)]).arrange(RIGHT, buff=0.06)
        grid = pics.dot_grid(3, 10, DIM, gap=0.2)
        rows.add(VGroup(strip, grid))
    for r in rows:
        r[1].move_to([1.5, 0, 0])
        r[0].move_to([-1.2, 0, 0])
    rows.arrange(DOWN, buff=0.4)
    for r in rows:
        r[0].align_to(rows[0][0], LEFT)
        r[1].align_to(rows[0][1], LEFT)
    exists = style.math(r"\exists P", 40, BLUE).next_to(VGroup(*[r[0] for r in rows]), UP, buff=0.35)
    forall = style.math(r"\forall x", 40, BLUE).next_to(VGroup(*[r[1] for r in rows]), UP, buff=0.35)
    g = VGroup(rows, exists, forall).scale(1.25).move_to([-3.2, -0.6, 0])
    g.rows = rows
    return g


def clock(size: float = 1.0):
    face = Circle(radius=size * 0.5).set_stroke(INK, STROKE)
    ticks = VGroup(*[Line(UP * size * 0.4, UP * size * 0.47).set_stroke(DIM, THIN).rotate(k * np.pi / 6, about_point=[0, 0, 0])
                     for k in range(12)])
    hand = Line([0, 0, 0], UP * size * 0.36).set_stroke(ORANGE, STROKE)
    g = VGroup(face, ticks, hand)
    g.hand, g.face = hand, face
    return g


def timeout():
    chip = z3_chip(2.4)
    clk = clock(1.3).next_to(chip, RIGHT, buff=0.7)
    limit = style.mono("1:00", 32, DIM).next_to(clk, DOWN, buff=0.2)
    verdict = pics.stamp("UNKNOWN", ORANGE).scale(0.75)
    top = VGroup(chip, VGroup(clk, limit))
    verdict.next_to(top, DOWN, buff=0.6)
    g = VGroup(chip, clk, limit, verdict).move_to([3.6, -0.6, 0])
    g.chip, g.clock, g.verdict = chip, clk, verdict
    return g


def cegis_name():
    return style.mono("CEGIS", 52, INK).move_to([0, 3.1, 0])


def _tray(n_blue: int, n_orange: int):
    dots = VGroup(*[Dot(radius=0.13, color=BLUE) for _ in range(n_blue)],
                  *[Dot(radius=0.13, color=ORANGE) for _ in range(n_orange)])
    dots.arrange_in_grid(rows=2, cols=3, buff=0.2) if len(dots) > 3 else dots.arrange(RIGHT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.15, width=1.9, height=1.3).set_stroke(INK, STROKE).move_to(dots)
    g = VGroup(box, dots)
    g.box, g.dots = box, dots
    return g


def _loop_layout(n_orange: int):
    tray = _tray(3, n_orange).move_to([-5.3, 0.6, 0])
    guess = solver(r"\exists P", 2.1).move_to([-2.2, 0.6, 0])
    program = pics.tile_strip(["", ""], GREEN).scale(0.7).move_to([0.45, 0.6, 0])
    check = solver(r"\forall x", 2.1).move_to([3.1, 0.6, 0])
    done = pics.check(0.7).move_to([5.8, 1.9, 0])
    a1 = Arrow(tray.get_right(), guess.body.get_left(), buff=0.15, stroke_width=STROKE, color=DIM)
    a2 = Arrow(guess.body.get_right(), program.get_left(), buff=0.25, stroke_width=STROKE, color=DIM)
    a3 = Arrow(program.get_right(), check.body.get_left(), buff=0.25, stroke_width=STROKE, color=DIM)
    a_done = Arrow(check.body.get_right(), done.get_left() + DOWN * 0.1, buff=0.25, stroke_width=STROKE, color=GREEN)
    back = CurvedArrow(check.body.get_bottom() + DOWN * 0.15, tray.get_bottom() + DOWN * 0.15, angle=-1.2)
    back.set_stroke(ORANGE, STROKE).set_fill(ORANGE)
    back.get_tip().set_fill(ORANGE, 1).set_stroke(ORANGE)
    g = VGroup(tray, guess, program, check, done, a1, a2, a3, a_done, back)
    g.tray, g.guess, g.program, g.check, g.done, g.back = tray, guess, program, check, done, back
    g.arrows = VGroup(a1, a2, a3)
    return g


def loop_start():
    return _loop_layout(0)


def loop():
    return _loop_layout(1)


CELL = 0.19
STRIP_X, CONST_X, EX_X, BADGE_X = 2.7, -2.4, -4.95, -6.5
ROW_Y = {"hole": 3.2, "target": 2.15, 1: 0.85, 2: -0.4, 3: -1.65, "summary": -3.0}


def strip32(v: int, y: float, color: str = BLUE):
    s = pics.bit_strip(bits_of(v), cell=CELL).move_to([STRIP_X, y, 0])
    for c in s.cells:
        if c.on:
            c.set_fill(color, 0.9)
    return s


def hole():
    x_and = style.math(r"x \mathbin{\&}", 48)
    blank = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=2.5, height=0.62), num_dashes=24)
    blank.set_stroke(ORANGE, STROKE)
    g = VGroup(x_and, blank).arrange(RIGHT, buff=0.25)
    g.shift([CONST_X - blank.get_center()[0], ROW_Y["hole"] - g.get_center()[1], 0])
    tile = pics.tile("and", INK).scale(0.9).next_to(g, LEFT, buff=0.6)
    out = VGroup(tile, g)
    out.blank = blank
    return out


def target():
    s = strip32(TARGET, ROW_Y["target"], GREEN)
    f = style.math("f", 48, GREEN).move_to([CONST_X, ROW_Y["target"], 0])
    return VGroup(f, s)


def _badge(k: int):
    ring = Circle(radius=0.28).set_stroke(DIM, THIN)
    return VGroup(ring, style.mono(str(k), 28, DIM).move_to(ring)).move_to([BADGE_X, ROW_Y[k], 0])


def _example(k: int):
    y = ROW_Y[k]
    if k == 1:
        return VGroup(Dot(radius=0.14, color=BLUE)).move_to([EX_X, y, 0])
    dot = Dot(radius=0.14, color=ORANGE)
    value = style.mono(hexs(COUNTEREXAMPLES[k - 2]), 22, ORANGE)
    return VGroup(dot, value).arrange(RIGHT, buff=0.18).move_to([EX_X, y, 0])


def const_text(k: int):
    return style.mono(hexs(GUESSES[k - 1]), 30, INK if k < 3 else GREEN).move_to([CONST_X, ROW_Y[k], 0])


def _rings(strip, cells):
    return VGroup(*[Square(side_length=CELL * 1.5).set_stroke(ORANGE, STROKE).move_to(strip.cells[j]) for j in cells])


def round_row(k: int):
    strip = strip32(GUESSES[k - 1], ROW_Y[k])
    rings = _rings(strip, wrong_cells(GUESSES[k - 1]))
    parts = [_badge(k), _example(k), const_text(k), strip, rings]
    if k == 3:
        parts.append(pics.check(0.5).next_to(strip, RIGHT, buff=0.25))
    g = VGroup(*parts)
    g.strip, g.rings, g.const = strip, rings, parts[2]
    return g


def round1():
    return round_row(1)


def round2():
    return round_row(2)


def round3():
    return round_row(3)


def summary():
    dots = VGroup(Dot(radius=0.13, color=BLUE), Dot(radius=0.13, color=ORANGE), Dot(radius=0.13, color=ORANGE)).arrange(RIGHT, buff=0.18)
    few = style.math(r"3 \ll 2^{32}", 50).next_to(dots, RIGHT, buff=0.45)
    verdict = pics.stamp("UNSAT", GREEN).scale(0.7)
    g = VGroup(VGroup(dots, few), verdict).arrange(RIGHT, buff=1.6).move_to([0.2, ROW_Y["summary"], 0])
    return g


FIELD_ROWS, FIELD_COLS = 12, 40
_ORDER = np.random.RandomState(0).permutation(FIELD_ROWS * FIELD_COLS)
SURVIVORS = (list(_ORDER[:48]), list(_ORDER[:5]), list(_ORDER[:1]))


def _field_grid():
    grid = pics.dot_grid(FIELD_ROWS, FIELD_COLS, BLUE, gap=0.25).move_to([0.9, -0.3, 0])
    for d in grid:
        d.scale(1.5)
    return grid


def field_at(stage: int):
    grid = _field_grid()
    if stage:
        keep = set(SURVIVORS[stage - 1])
        for i, d in enumerate(grid):
            if i not in keep:
                d.set_color(DIM).set_opacity(0.35)
    return grid


def field_examples():
    ex = VGroup(Dot(radius=0.15, color=BLUE), Dot(radius=0.15, color=ORANGE), Dot(radius=0.15, color=ORANGE))
    return ex.arrange(DOWN, buff=0.6).move_to([-5.7, -0.3, 0])


def field():
    grid = field_at(3)
    last = grid[SURVIVORS[2][0]]
    last.set_color(GREEN).scale(2.2)
    ring = Circle(radius=0.26).set_stroke(GREEN, STROKE).move_to(last)
    count = style.math(r"2^{32}", 52, DIM).next_to(grid, UP, buff=0.4)
    g = VGroup(grid, ring, field_examples(), count)
    g.grid, g.ring, g.examples, g.count = grid, ring, g[2], count
    return g


BAR_W = 6.0


def brute():
    bar = Rectangle(width=BAR_W, height=0.34).set_stroke(INK, THIN).move_to([-3.4, 0.2, 0])
    lo = style.mono(hexs(0), 22, DIM).next_to(bar, DOWN, buff=0.2).align_to(bar, LEFT)
    hi = style.mono(hexs(0xFFFFFFFF), 22, DIM).next_to(bar, DOWN, buff=0.2).align_to(bar, RIGHT)
    frac = TARGET / 2 ** 32
    at = bar.get_left() + RIGHT * BAR_W * frac
    marker = Line(at + UP * 0.35, at + DOWN * 0.35).set_stroke(ORANGE, STROKE)
    answer = style.mono(hexs(TARGET), 26, ORANGE).next_to(marker, UP, buff=0.2)
    fill = Rectangle(width=BAR_W * 0.004, height=0.34).set_stroke(width=0).set_fill(BLUE, 0.9).align_to(bar, LEFT).align_to(bar, UP)
    tries = style.math(r"2^{32}", 46, DIM).next_to(bar, UP, buff=1.0)
    g = VGroup(bar, fill, lo, hi, marker, answer, tries)
    g.bar, g.fill, g.marker, g.answer = bar, fill, marker, answer
    return g


def solve():
    eq = style.math(r"x \mathbin{\&} c", 64)
    eq[0][-1].set_color(ORANGE)
    chip = z3_chip(2.2)
    value = VGroup(style.math("c =", 48, ORANGE), style.mono(hexs(TARGET), 34, GREEN)).arrange(RIGHT, buff=0.3)
    g = VGroup(eq, chip, value).arrange(DOWN, buff=0.55).move_to([3.7, -0.1, 0])
    g.eq, g.chip, g.value = eq, chip, value
    return g


SLOT_X, SLOT_Y = -0.9, (1.7, 0.0, -1.7)


def paper2010():
    doc = pics.paper(1.3)
    year = style.mono("2010", 34, ORANGE).next_to(doc, UP, buff=0.2)
    names = VGroup(*[style.serif(n, 24, DIM) for n in ("Jha", "Gulwani", "Seshia", "Tiwari")]).arrange(DOWN, buff=0.08)
    names.next_to(doc, RIGHT, buff=0.3)
    return VGroup(year, doc, names).move_to([-5.2, 2.2, 0])


def _sack():
    pts = [[-1.0, 0.7, 0], [-1.25, -0.6, 0], [-0.9, -1.0, 0], [0.9, -1.0, 0], [1.25, -0.6, 0], [1.0, 0.7, 0]]
    sack = Polygon(*pts).set_stroke(INK, STROKE).set_fill(opacity=0)
    tie = Line([-0.55, 0.85, 0], [0.55, 0.85, 0]).set_stroke(ORANGE, STROKE)
    return VGroup(sack, tie)


def bag():
    sack = _sack()
    tiles = VGroup(pics.tile("neg", INK, w=0.9, h=0.45), pics.tile("and", INK, w=0.9, h=0.45)).arrange(DOWN, buff=0.18)
    tiles.move_to(sack[0]).shift(DOWN * 0.1)
    g = VGroup(sack, tiles).move_to([-5.2, -1.4, 0])
    g.tiles = tiles
    return g


def lines():
    g = VGroup()
    for k, y in enumerate(SLOT_Y):
        slot = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.0).set_stroke(DIM, THIN).move_to([SLOT_X, y, 0])
        num = style.mono(str(k), 34, DIM).next_to(slot, LEFT, buff=0.3)
        g.add(VGroup(num, slot))
    x = style.math("x", 48, BLUE).move_to(g[0][1])
    out = VGroup(g, x)
    out.slots = [row[1] for row in g]
    out.x = x
    return out


def _port(label: str, color: str = ORANGE):
    box = RoundedRectangle(corner_radius=0.06, width=0.42, height=0.42).set_stroke(color, THIN)
    return VGroup(box, style.mono(label, 22, color).move_to(box))


def _instr(name: str, outs: str, ins: tuple[str, ...], color: str = ORANGE):
    tile = pics.tile(name, INK, w=1.0, h=0.5)
    out_port = _port(outs, color).next_to(tile, LEFT, buff=0.12)
    in_ports = VGroup(*[_port(i, color) for i in ins]).arrange(RIGHT, buff=0.08).next_to(tile, RIGHT, buff=0.12)
    g = VGroup(out_port, tile, in_ports)
    if color == ORANGE:
        g.add(style.math("o", 32, DIM).next_to(out_port, DOWN, buff=0.1))
        g.add(*[style.math("a", 32, DIM).next_to(p, DOWN, buff=0.1) for p in in_ports])
    g.tile, g.out_port, g.in_ports = tile, out_port, in_ports
    return g


def unknowns():
    neg = _instr("neg", "?", ("?",))
    band = _instr("and", "?", ("?", "?"))
    return VGroup(neg, band).arrange(DOWN, buff=0.8, aligned_edge=LEFT).scale(1.25).move_to([3.7, -1.6, 0])


def rules():
    lines_ = [r"a < o", r"o_{\text{neg}} \neq o_{\text{and}}", r"y = v_2", r"a = j \;\Rightarrow\; v_a = v_j"]
    g = VGroup(*[style.math(t, 48, BLUE) for t in lines_]).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
    return g.move_to([4.7, 1.65, 0])


def wired():
    ls = lines()
    neg = _instr("neg", "1", ("0",), GREEN)
    band = _instr("and", "2", ("0", "1"), GREEN)
    for ins, slot in ((neg, ls.slots[1]), (band, ls.slots[2])):
        ins.move_to(slot)
    reads = VGroup()
    for src, dst in ((0, 1), (0, 2), (1, 2)):
        a = ls.slots[src].get_right() + RIGHT * 0.1
        b = ls.slots[dst].get_right() + RIGHT * 0.1
        arc = ArcBetweenPoints(a, b, angle=-1.4 if dst - src == 1 else -1.9).set_stroke(BLUE, THIN)
        reads.add(arc)
    answer = Arrow(ls.slots[2].get_bottom(), ls.slots[2].get_bottom() + DOWN * 0.75, buff=0.05,
                   stroke_width=STROKE, color=GREEN)
    g = VGroup(neg, band, reads, answer)
    g.neg, g.band, g.reads, g.answer = neg, band, reads, answer
    return g


def found():
    eq = style.math(r"x \mathbin{\&} -x", 56, GREEN)
    stats = VGroup(style.mono("32 bit", 28, DIM), style.mono("0.03 s", 28, DIM)).arrange(RIGHT, buff=0.6)
    return VGroup(eq, stats).arrange(DOWN, buff=0.3).move_to([4.7, -2.4, 0])


BOARD = Board("part7", BEATS, (
    Write("7.1", "question", question),
    Write("7.1", "layers", layers),
    Write("7.1", "timeout", timeout),
    Erase("7.2", "question"),
    Erase("7.2", "layers"),
    Erase("7.2", "timeout"),
    Write("7.2", "cegis_name", cegis_name),
    Write("7.2", "loop", loop),
    Erase("7.3", "cegis_name"),
    Erase("7.3", "loop"),
    Write("7.3", "hole", hole),
    Write("7.3", "target", target),
    Write("7.3", "round1", round1),
    Write("7.4", "round2", round2),
    Write("7.4", "round3", round3),
    Write("7.4", "summary", summary),
    Erase("7.5", "hole"),
    Erase("7.5", "target"),
    Erase("7.5", "round1"),
    Erase("7.5", "round2"),
    Erase("7.5", "round3"),
    Erase("7.5", "summary"),
    Write("7.5", "field", field),
    Erase("7.6", "field"),
    Write("7.6", "brute", brute),
    Write("7.6", "solve", solve),
    Erase("7.7", "brute"),
    Erase("7.7", "solve"),
    Write("7.7", "paper2010", paper2010),
    Write("7.7", "bag", bag),
    Write("7.7", "lines", lines),
    Write("7.7", "unknowns", unknowns),
    Erase("7.8", "paper2010"),
    Erase("7.8", "bag"),
    Erase("7.8", "unknowns"),
    Write("7.8", "rules", rules),
    Write("7.8", "wired", wired),
    Write("7.8", "found", found),
), previous=PART6, wipe="shove")
