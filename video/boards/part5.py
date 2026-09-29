from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Circle, Line, RoundedRectangle, Square, VGroup

from boards.part4 import BOARD as PART4
from kit import pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7")


def _twin(face: str, w: float = 4.2):
    return pics.program_machine(1, face=face, w=w)


def z3_chip(w: float = 2.2):
    body = RoundedRectangle(corner_radius=0.12, width=w, height=w * 0.7).set_stroke(INK, STROKE).set_fill(opacity=0)
    pins = VGroup()
    for k in range(4):
        y = body.get_top()[1] - body.height * (k + 0.8) / 4.6
        for side, d in ((body.get_left()[0], LEFT), (body.get_right()[0], RIGHT)):
            start = [side, y, 0]
            pins.add(Line(start, [side + d[0] * 0.22, y, 0]).set_stroke(DIM, THIN))
    name = style.mono("Z3", w * 22, BLUE).move_to(body)
    chip = VGroup(pins, body, name)
    chip.body = body
    return chip


TRIED = (7, 12, 40, 77, 101, 150)


def twins():
    return VGroup(_twin(r"x + x"), _twin(r"x \ll 1")).arrange(DOWN, buff=1.0).move_to([-3.2, 0.3, 0])


def _input_grid():
    return pics.dot_grid(12, 18, DIM, gap=0.3).move_to([3.6, 0.3, 0])


def tried():
    grid = _input_grid()
    for i in TRIED:
        grid[i].set_color(GREEN).scale(1.6)
    return grid


SPACE = 64
HIT = 27 * SPACE + 40
MOST_NEGATIVE = (SPACE - 1) * SPACE


def space():
    cells = VGroup(*[Square(side_length=0.058).set_stroke(width=0).set_fill(DIM, 0.55) for _ in range(SPACE * SPACE)])
    cells.arrange_in_grid(rows=SPACE, cols=SPACE, buff=0.026).move_to([-3.4, 0, 0])
    cells[HIT].set_fill(GREEN, 1)
    cells[MOST_NEGATIVE].set_fill(ORANGE, 1)
    hit_ring = Circle(radius=0.2).set_stroke(GREEN, THIN).move_to(cells[HIT])
    corner_ring = Circle(radius=0.2).set_stroke(ORANGE, THIN).move_to(cells[MOST_NEGATIVE])
    g = VGroup(cells, hit_ring, corner_ring)
    g.cells, g.hit_ring, g.corner_ring = cells, hit_ring, corner_ring
    return g


def c32():
    return style.math(r"2^{32} = 4{,}294{,}967{,}296", 44).move_to([3.6, 2.8, 0])


def share():
    return style.math(r"10^{6} \approx 0.02\%", 44, GREEN).move_to([3.6, 1.7, 0])


def c64():
    return style.math(r"2^{64} \approx 1.8 \times 10^{19}", 44).move_to([3.6, 0.5, 0])


def most_negative_bits():
    return [1] + [0] * 31


def negate_strip(bits):
    return pics.bit_strip(bits, cell=0.16).move_to([3.6, -1.5, 0])


def negate():
    strip = negate_strip(most_negative_bits())
    eq = style.math(r"-(-2^{31}) = -2^{31}", 44, ORANGE).next_to(strip, DOWN, buff=0.45)
    return VGroup(strip, eq)


def evens():
    a, b, total = pics.domino(3), pics.domino(2), pics.domino(5)
    plus, eq = style.math("+", 60), style.math("=", 60)
    return VGroup(a, plus, b, eq, total).arrange(RIGHT, buff=0.45).scale(1.4).move_to([0, 1.3, 0])


def algebra():
    return style.math(r"2a + 2b = 2(a + b)", 64).move_to([0, -1.5, 0])


SAT_BITS = (1, 0, 1)


def _sat_parts(bits):
    formula = style.math(r"a \land \lnot b \land c", 48)
    switches = VGroup(*[pics.switch(bool(v), 0.75) for v in bits]).arrange(RIGHT, buff=0.35)
    names = VGroup(*[style.mono(n, 28, DIM).next_to(s, DOWN, buff=0.15) for n, s in zip("abc", switches)])
    lamp = pics.lamp(on=bits == SAT_BITS, size=1.1).next_to(switches, RIGHT, buff=1.2)
    wires = VGroup(Line(switches.get_right(), lamp.bulb.get_left()).set_stroke(DIM, THIN))
    body = VGroup(wires, switches, names, lamp)
    formula.next_to(body, UP, buff=0.4)
    g = VGroup(formula, body).scale(1.5).move_to([-2.9, 1.6, 0])
    g.switches, g.lamp = switches, lamp
    return g


def sat_at(bits):
    return _sat_parts(tuple(bits))


def sat():
    return _sat_parts(SAT_BITS)


def chip():
    return z3_chip(2.6).move_to([3.6, 1.8, 0])


def bits():
    x = style.math("x", 60, BLUE)
    strip = pics.bit_strip([0, 1, 1, 0, 1, 1, 0, 0] * 4, cell=0.15)
    return VGroup(x, strip).arrange(RIGHT, buff=0.5).move_to([-3.4, -2.1, 0])


def gates():
    add = pics.tile("add", INK)
    net = VGroup(*[pics.and_gate(0.55) for _ in range(4)]).arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.25))
    arrow = style.mono("→", 40, DIM)
    return VGroup(add, arrow, net).arrange(RIGHT, buff=0.4).scale(1.4).move_to([3.6, -2.1, 0])


def query():
    pair = VGroup(_twin(r"x + x", 3.4), _twin(r"x \ll 1", 3.4)).arrange(DOWN, buff=0.8).move_to([-4.2, 0.2, 0])
    ne = style.math(r"\neq", 72, ORANGE).move_to([-0.9, 0.2, 0])
    wires = VGroup(*[Line(m.outlet.get_right(), ne.get_left() + LEFT * 0.1).set_stroke(DIM, THIN) for m in pair])
    box = z3_chip(2.2).move_to([1.6, 0.2, 0])
    into = Line(ne.get_right() + RIGHT * 0.1, box.body.get_left()).set_stroke(DIM, THIN)
    g = VGroup(pair, wires, ne, into, box)
    g.pair, g.ne, g.box = pair, ne, box
    return g


def unsat():
    return pics.stamp("UNSAT", GREEN).scale(0.9).move_to([4.6, 2.5, 0])


def forall():
    return style.math(r"\forall x:\ x + x = x \ll 1", 52, GREEN).move_to([2.9, -2.6, 0])


REGIONS = (3, 4, 2)
CONFLICTS = (16, 21, 26)
CLAUSES = (r"\lnot a \lor \lnot b", r"\lnot a \lor b", r"a")


def _tree():
    return pics.tree(depth=4, width=8.2, level_gap=1.25).move_to([-2.4, -0.1, 0])


def _grey(t, roots):
    for r in roots:
        for i in t.subtree(r):
            t.nodes[i].set_fill(DIM, 0.12).set_stroke(DIM, THIN)
            if i:
                t.edges[i - 1].set_stroke(DIM, THIN, opacity=0.35)
    return t


def tree_at(ruled_out: int):
    return _grey(_tree(), REGIONS[:ruled_out])


def conflict_marks(t):
    return VGroup(*[pics.x_mark(0.34).move_to(t.nodes[i]) for i in CONFLICTS])


def tree():
    t = _grey(_tree(), REGIONS)
    root_fill = t.nodes[0]
    root_fill.set_fill(DIM, 0.12).set_stroke(DIM, THIN)
    g = VGroup(t, conflict_marks(t))
    g.t = t
    return g


def learned():
    rules = VGroup(*[style.math(c, 52, BLUE) for c in CLAUSES]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    return rules.move_to([4.6, 0.0, 0])


def counter():
    pair = VGroup(_twin(r"x + x", 3.4), _twin(r"x \ll 2", 3.4)).arrange(DOWN, buff=0.8).move_to([-3.6, 0.6, 0])
    ins = VGroup(*[style.mono("1", 48, BLUE).next_to(m.inlet, LEFT, buff=0.4) for m in pair])
    outs = VGroup(style.mono("2", 48, GREEN).next_to(pair[0].outlet, RIGHT, buff=0.4),
                  style.mono("4", 48, ORANGE).next_to(pair[1].outlet, RIGHT, buff=0.4))
    g = VGroup(pair, ins, outs)
    g.pair, g.ins, g.outs = pair, ins, outs
    return g


def sat_stamp():
    st = pics.stamp("SAT", ORANGE)
    witness = style.mono("x = 1", 44, ORANGE).next_to(st, DOWN, buff=0.35)
    return VGroup(st, witness).move_to([3.4, 1.2, 0])


def summary():
    proof = VGroup(pics.stamp("UNSAT", GREEN).scale(0.6), style.mono("→", 40, DIM), pics.check(0.6)).arrange(RIGHT, buff=0.35)
    evidence = VGroup(pics.stamp("SAT", ORANGE).scale(0.6), style.mono("→", 40, DIM), pics.bug(0.8)).arrange(RIGHT, buff=0.35)
    return VGroup(proof, evidence).arrange(RIGHT, buff=1.4).scale(1.3).move_to([0, -2.9, 0])


BOARD = Board("part5", BEATS, (
    Write("5.1", "twins", twins),
    Write("5.1", "tried", tried),
    Erase("5.2", "twins"),
    Erase("5.2", "tried"),
    Write("5.2", "space", space),
    Write("5.2", "c32", c32),
    Write("5.2", "share", share),
    Write("5.2", "c64", c64),
    Write("5.2", "negate", negate),
    Erase("5.3", "space"),
    Erase("5.3", "c32"),
    Erase("5.3", "share"),
    Erase("5.3", "c64"),
    Erase("5.3", "negate"),
    Write("5.3", "evens", evens),
    Write("5.3", "algebra", algebra),
    Erase("5.4", "evens"),
    Erase("5.4", "algebra"),
    Write("5.4", "sat", sat),
    Write("5.4", "chip", chip),
    Write("5.4", "bits", bits),
    Write("5.4", "gates", gates),
    Erase("5.5", "sat"),
    Erase("5.5", "chip"),
    Erase("5.5", "bits"),
    Erase("5.5", "gates"),
    Write("5.5", "query", query),
    Write("5.5", "unsat", unsat),
    Write("5.5", "forall", forall),
    Erase("5.6", "query"),
    Erase("5.6", "forall"),
    Write("5.6", "tree", tree),
    Write("5.6", "learned", learned),
    Erase("5.7", "tree"),
    Erase("5.7", "learned"),
    Erase("5.7", "unsat"),
    Write("5.7", "counter", counter),
    Write("5.7", "sat_stamp", sat_stamp),
    Write("5.7", "summary", summary),
), previous=PART4, wipe="fall")
