from __future__ import annotations

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arrow, Circle, DashedVMobject, Dot, Line, Rectangle, RoundedRectangle, VGroup,
)

import facts
from boards.part9 import BOARD as PART9
from kit import cartoon, draw, pics, stage, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, MAGENTA, ORANGE, STROKE

BEATS = ("10.1", "10.2", "10.3", "10.4", "10.5")


POPCOUNT_EXAMPLE = 0b10110110
MASKS = (0x55, 0x33, 0x0F)
ROUND_SECONDS = (0.06, 0.1, 4, 11, 27)
CHART_BASE = -2.0
CHART_LEFT = 0.4
BAR_W, BAR_GAP = 0.62, 0.36
TALLEST = 3.7


def _ones(value: int, n: int = 8) -> list[int]:
    return [i for i in range(n) if value >> i & 1]


def popcount():
    row = pics.switch_row(POPCOUNT_EXAMPLE, h=0.95).move_to([-3.5, 2.1, 0])
    tally = VGroup(*[pics.marble(ORANGE, 0.17) for _ in _ones(POPCOUNT_EXAMPLE)]).arrange(RIGHT, buff=0.22)
    tally.next_to(row, DOWN, buff=0.75).shift(LEFT * 0.6)
    count = style.mono(str(bin(POPCOUNT_EXAMPLE).count("1")), 60, ORANGE).next_to(tally, RIGHT, buff=0.55)
    g = VGroup(row, tally, count)
    g.row, g.tally, g.count = row, tally, count
    return g


def masks():
    rows = VGroup()
    for m in MASKS:
        strip = pics.bit_strip([m >> (7 - k) & 1 for k in range(8)], cell=0.34)
        rows.add(VGroup(style.mono(f"0x{m:02X}", 30, MAGENTA), strip).arrange(RIGHT, buff=0.4))
    return rows.arrange(DOWN, buff=0.28, aligned_edge=RIGHT).move_to([-3.5, -1.85, 0])


def _bar_x(k: int) -> float:
    return CHART_LEFT + BAR_W / 2 + k * (BAR_W + BAR_GAP)


def _examples(k: int):
    dots = VGroup(*[Dot(radius=0.07, color=BLUE) for _ in range(k + 1)]).arrange(UP, buff=0.07)
    return dots.move_to([_bar_x(k), CHART_BASE - 0.2, 0], aligned_edge=UP)


def bar(k: int):
    height = max(0.05, TALLEST * ROUND_SECONDS[k] / max(ROUND_SECONDS))
    body = Rectangle(width=BAR_W, height=height).set_stroke(width=0).set_fill(ORANGE if k == 4 else BLUE, 0.85)
    body.move_to([_bar_x(k), CHART_BASE, 0], aligned_edge=DOWN)
    label = style.mono(f"{ROUND_SECONDS[k]:g}", 26, INK).next_to(body, UP, buff=0.12)
    return VGroup(body, label, _examples(k))


def axis():
    right = _bar_x(5) + BAR_W / 2 + 0.25
    base = Line([CHART_LEFT - 0.25, CHART_BASE, 0], [right, CHART_BASE, 0]).set_stroke(DIM, THIN)
    unit = style.mono("s", 26, DIM).next_to(base, RIGHT, buff=0.15)
    return VGroup(base, unit)


def unfinished():
    top = CHART_BASE + TALLEST + 0.8
    outline = DashedVMobject(Rectangle(width=BAR_W, height=top - CHART_BASE), num_dashes=34)
    outline.set_stroke(ORANGE, STROKE).move_to([_bar_x(5), (top + CHART_BASE) / 2, 0])
    spinner = pics.loop_icon(0.8).set_color(ORANGE).next_to(outline, UP, buff=0.1)
    g = VGroup(outline, spinner, _examples(5))
    g.outline, g.spinner = outline, spinner
    return g


def rounds():
    return VGroup(axis(), *[bar(k) for k in range(len(ROUND_SECONDS))])


def on_record():
    flag = pics.flag(0.9).set_color(ORANGE)
    return flag.next_to(unfinished().outline, RIGHT, buff=0.08).align_to(unfinished().outline, UP)


def _names(*names: str):
    return VGroup(*[style.serif(n, 38) for n in names])


def credit_search():
    doc = pics.paper(1.3)
    glass = pics.magnifier(0.9).move_to(doc.get_corner(DOWN + RIGHT))
    year = style.mono("1987", 30, ORANGE).next_to(doc, UP, buff=0.25)
    icon = VGroup(year, doc, glass)
    return VGroup(icon, _names("Massalin")).arrange(DOWN, buff=0.45).scale(1.3).move_to([-4.7, 0.2, 0])


def credit_cegis():
    loop = pics.loop_icon(1.9).set_color(BLUE)
    term = style.mono("CEGIS", 30, BLUE).next_to(loop, UP, buff=0.3)
    icon = VGroup(term, loop)
    return VGroup(icon, _names("Solar-Lezama")).arrange(DOWN, buff=0.55).scale(1.3).move_to([0, 0.2, 0])


def wiring_icon():
    a, b = pics.and_gate(0.8), pics.and_gate(0.8)
    VGroup(a, b).arrange(RIGHT, buff=0.9)
    b.shift(DOWN * 0.45)
    wire = Line(a.output.get_end(), b.inputs[0].get_start()).set_stroke(GREEN, THIN)
    return VGroup(a, b, wire)


def credit_wiring():
    names = _names("Jha", "Gulwani", "Seshia", "Tiwari").arrange_in_grid(rows=2, cols=2, buff=(0.45, 0.25))
    return VGroup(wiring_icon(), names).arrange(DOWN, buff=0.7).scale(1.1).move_to([4.6, 0.2, 0])


def stopwatch(size: float = 1.1):
    face = Circle(radius=size * 0.42).set_stroke(INK, STROKE)
    button = Line(face.get_top(), face.get_top() + UP * size * 0.14).set_stroke(INK, STROKE * 1.4)
    hand = Line(face.get_center(), face.get_center() + np.array([size * 0.2, size * 0.22, 0])).set_stroke(ORANGE, STROKE)
    ticks = VGroup(*[Line(face.point_at_angle(a) * 0.82 + face.get_center() * 0.18, face.point_at_angle(a))
                     .set_stroke(DIM, THIN) for a in np.linspace(0, 2 * np.pi, 8, endpoint=False)])
    return VGroup(face, ticks, button, hand)


def built():
    ops = VGroup(*[pics.tile(op, INK, w=0.95, h=0.42) for op in facts.OPS]).arrange_in_grid(rows=3, cols=4, buff=0.08)
    formulas = VGroup(pics.tile("add", INK), style.mono("→", 36, DIM), pics.and_gate(0.7)).arrange(RIGHT, buff=0.25)
    checks = VGroup(pics.check(0.7), pics.check(0.7)).arrange(RIGHT, buff=0.25)
    pieces = VGroup(ops, formulas, checks, pics.bars_icon(1.3), stopwatch(1.3))
    pieces.arrange(RIGHT, buff=0.75, aligned_edge=DOWN)
    return pieces.scale_to_fit_width(12.4).move_to([0, 2.2, 0])


def tests():
    dots = VGroup(*[Dot(radius=0.075, color=GREEN) for _ in range(110)]).arrange_in_grid(rows=10, cols=11, buff=0.1)
    count = style.mono("100+", 48, GREEN).next_to(dots, DOWN, buff=0.3)
    return VGroup(dots, count).move_to([-4.9, -1.5, 0])


def rerun():
    laptop = draw.laptop_icon().scale(1.9)
    stamp = pics.stamp("UNSAT", GREEN).scale_to_fit_width(laptop[0].width * 0.62).move_to(laptop[0])
    again = pics.loop_icon(0.9).set_color(BLUE).next_to(laptop, RIGHT, buff=0.3)
    g = VGroup(laptop, stamp, again).move_to([-0.55, -1.5, 0])
    g.laptop, g.stamp, g.again = laptop, stamp, again
    return g


def _net():
    layers = [VGroup(*[Circle(radius=0.11).set_stroke(DIM, THIN) for _ in range(n)]).arrange(DOWN, buff=0.22)
              for n in (3, 4, 2)]
    VGroup(*layers).arrange(RIGHT, buff=0.6)
    links = VGroup(*[Line(a.get_center(), b.get_center(), buff=0.11).set_stroke(DIM, THIN * 0.6)
                     for left, right in zip(layers, layers[1:]) for a in left for b in right])
    return VGroup(links, *layers)


def stretch():
    net = _net()
    guide = style.mono("→", 36, DIM)
    search_tree = pics.tree(depth=2, width=1.6, level_gap=0.55).set_color(DIM)
    inside = VGroup(net, guide, search_tree).arrange(RIGHT, buff=0.35)
    box = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=inside.width + 0.7, height=inside.height + 0.7),
                         num_dashes=40).set_stroke(DIM, THIN).move_to(inside)
    g = VGroup(box, inside).scale_to_fit_width(4.3).move_to([4.45, -1.5, 0])
    g.box, g.net, g.guide, g.tree = box, net, guide, search_tree
    return g


def desk():
    return cartoon.pov_desk()


def program_on_screen():
    tiles = pics.tile_strip(["sub", "and"], GREEN)
    result = style.mono(f"{facts.EXAMPLE} → {facts.EXAMPLE_AND}", 34, BLUE).next_to(tiles, DOWN, buff=0.35)
    return cartoon.on_screen(VGroup(tiles, result).scale(1.3), "left").shift(LEFT * 0.5 + DOWN * 0.2)


def link_on_screen():
    icon = draw.code_icon().scale(1.5)
    down = Arrow(UP * 0.5, DOWN * 0.5, buff=0, color=BLUE, stroke_width=6).next_to(icon, DOWN, buff=0.2)
    g = cartoon.on_screen(VGroup(icon, down), "right")
    g.down = down
    return g


ON_SCREEN_AT_END = ("desk", "program_on_screen", "link_on_screen")


def dark_room():
    return stage.room(lit=False)


def bow():
    return stage.stick("bow", stage.GUY_X)


def thanks():
    return stage.speech("thanks!").move_to([3.55, -0.35, 0])


BOARD = Board("part10", BEATS, (
    Write("10.1", "popcount", popcount),
    Write("10.1", "masks", masks),
    Write("10.1", "rounds", rounds),
    Write("10.1", "unfinished", unfinished),
    Write("10.1", "on_record", on_record),
    Erase("10.2", "popcount"),
    Erase("10.2", "masks"),
    Erase("10.2", "rounds"),
    Erase("10.2", "unfinished"),
    Erase("10.2", "on_record"),
    Write("10.2", "credit_search", credit_search),
    Write("10.2", "credit_cegis", credit_cegis),
    Write("10.2", "credit_wiring", credit_wiring),
    Erase("10.3", "credit_search"),
    Erase("10.3", "credit_cegis"),
    Erase("10.3", "credit_wiring"),
    Write("10.3", "built", built),
    Write("10.3", "tests", tests),
    Write("10.3", "rerun", rerun),
    Write("10.3", "stretch", stretch),
    Erase("10.4", "built"),
    Erase("10.4", "tests"),
    Erase("10.4", "rerun"),
    Erase("10.4", "stretch"),
    Write("10.4", "desk", desk),
    Write("10.4", "program_on_screen", program_on_screen),
    Write("10.4", "link_on_screen", link_on_screen),
    *[Erase("10.5", key) for key in ON_SCREEN_AT_END],
    Write("10.5", "room", dark_room),
    Write("10.5", "bow", bow),
    Write("10.5", "thanks", thanks),
), previous=PART9, wipe="shove")
