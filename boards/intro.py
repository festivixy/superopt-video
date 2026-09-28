from __future__ import annotations

from manim import DOWN, RIGHT, Arrow, VGroup

import facts
from kit import board, draw, style, zones
from kit.beat import Board, Erase, Write
from kit.style import DIM, GREEN, INK, ORANGE, STROKE

BEATS = ("I.1", "I.2", "I.3", "I.4", "I.5", "I.6", "I.7", "I.8", "I.9")


def _arrow(a, b):
    return Arrow(a, b, buff=0.12, color=DIM, stroke_width=STROKE, max_tip_length_to_length_ratio=0.2)


def desk():
    return zones.fit(draw.desk_scene(), "ART")


def namecard():
    name = style.serif("Curtis", 60)
    role = style.serif("high school", 30, DIM)
    likes = VGroup(
        board.stack(draw.code_icon(), board.note("coding")),
        board.stack(draw.game_controller(), board.note("games")),
    ).arrange(RIGHT, buff=1.0)
    return zones.fit(VGroup(name, role, likes).arrange(DOWN, buff=0.4), "SIDE")


def _timeline():
    return zones.fit(board.timeline(facts.TIMELINE), "STRIP")


def timeline_axis():
    return _timeline().axis


def timeline_ticks():
    return _timeline().ticks


def compile_flow():
    src = board.program_card(["return x & (x - 1);"], size=24)
    machine = draw.compiler_machine()
    out = board.program_card(["lea eax, [rdi - 1]", "and eax, edi"], size=24)
    column = VGroup(src, machine, out).arrange(DOWN, buff=0.7)
    a1, a2 = _arrow(src.get_bottom(), machine.get_top()), _arrow(machine.get_bottom(), out.get_top())
    t1 = board.note("translate", color=INK).next_to(a1, RIGHT, buff=0.2)
    t2 = board.note("+ make it fast", color=ORANGE).next_to(a2, RIGHT, buff=0.2)
    rule = board.rule_box(board.stack(style.serif("compiler =", 28), style.serif("translator", 28),
                                      style.serif("+ optimizer", 28, ORANGE)))
    return zones.fit(VGroup(VGroup(column, a1, a2, t1, t2), rule).arrange(RIGHT, buff=0.9), "SIDE")


def book():
    return zones.fit(draw.open_book(board.register(facts.EXAMPLE, 8, cell=0.3)), "SIDE", align="top")


def bits_note():
    return zones.fit(board.note("bit tricks: shortcuts that work\ndirectly on the 1s and 0s"), "SIDE", align="bottom")


def loop_vs_trick():
    loop = board.program_card(["for i in 0..31:", "  if bit i of x is 1:", "    turn it off, return", "return 0"],
                              size=22, footer=board.note("≤ 32 checks"))
    trick = board.program_card(["x & (x - 1)"], size=30, footer=board.note("2 instructions", color=GREEN))
    return zones.fit(VGroup(loop, trick).arrange(RIGHT, buff=0.6, aligned_edge=DOWN), "SIDE", align="top")


def why_note():
    return zones.fit(board.note("why it works: Part 2"), "SIDE", align="bottom")


def question():
    loop = board.program_card(["for i in 0..31:", "  ..."], size=20)
    machine = draw.compiler_machine()
    ask = style.serif("2 instructions?", 34, ORANGE)
    row = VGroup(loop, machine, ask).arrange(RIGHT, buff=0.9)
    arrows = VGroup(_arrow(loop.get_right(), machine.get_left()), _arrow(machine.get_right(), ask.get_left()))
    return zones.fit(VGroup(row, arrows), "SIDE")


def later_note():
    return zones.fit(board.note("measured later in the summer"), "SIDE", align="bottom")


def chess():
    b = draw.chess_board()
    code = board.program_card(["b &= b - 1"], size=26)
    side = board.stack(code, board.note("millions of times\na second"), buff=0.5)
    return zones.fit(VGroup(b, side).arrange(RIGHT, buff=0.7), "SIDE")


def scale():
    clang = draw.compiler_machine(label="clang")
    devices = VGroup(draw.phone(), draw.browser_window(), draw.laptop_icon()).arrange(DOWN, buff=0.5)
    row = VGroup(clang, devices).arrange(RIGHT, buff=1.6)
    arrows = VGroup(*[_arrow(clang.get_right(), d.get_left()) for d in devices])
    mult = style.serif("× calls per second  × devices", 30, ORANGE).next_to(row, DOWN, buff=0.6)
    return zones.fit(VGroup(row, arrows, mult), "SIDE")


def problem():
    eq = style.math(r"\min\ |P| \quad \text{such that} \quad \forall x:\ P(x) = f(x)", 40)
    goals = board.stack(style.serif("1.  find the shortest P", 30), style.serif("2.  prove nothing shorter exists", 30))
    return zones.fit(board.stack(eq, goals, buff=0.7), "SIDE")


def headline():
    return board.headline("superoptimization  (1987 →)")


BOARD = Board("intro", BEATS, (
    Write("I.1", "desk", desk),
    Write("I.1", "namecard", namecard),
    Write("I.1", "timeline_axis", timeline_axis),
    Erase("I.2", "namecard"),
    Write("I.2", "compile_flow", compile_flow),
    Erase("I.3", "compile_flow"),
    Write("I.3", "book", book),
    Write("I.3", "bits_note", bits_note),
    Erase("I.4", "book"),
    Erase("I.4", "bits_note"),
    Write("I.4", "loop_vs_trick", loop_vs_trick),
    Write("I.4", "why_note", why_note),
    Erase("I.5", "loop_vs_trick"),
    Erase("I.5", "why_note"),
    Write("I.5", "question", question),
    Write("I.5", "later_note", later_note),
    Erase("I.6", "question"),
    Erase("I.6", "later_note"),
    Write("I.6", "chess", chess),
    Erase("I.7", "chess"),
    Write("I.7", "scale", scale),
    Erase("I.8", "scale"),
    Write("I.8", "problem", problem),
    Write("I.9", "headline", headline),
    Write("I.9", "timeline_ticks", timeline_ticks),
))
