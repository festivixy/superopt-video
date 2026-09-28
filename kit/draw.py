"""Monoline illustrations. Coordinates for the desk scene follow the approved
mockup (160x90 viewBox, y down) and are mapped to Manim units by _p."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Circle, Line, Mobject, Polygon, Rectangle,
    RoundedRectangle, Square, Triangle, VGroup, VMobject,
)

from kit import style
from kit.board import register
from kit.style import BLUE, DIM, INK, ORANGE, STROKE

MAX_FILL = 0.15
S = 0.1
THIN = STROKE * 0.7
OCCUPIED = (3, 12, 21, 30, 42, 45, 52, 61)


def _round(m: VMobject) -> VMobject:
    try:
        from manim.constants import CapStyleType, LineJointType

        m.set_cap_style(CapStyleType.ROUND)
        m.joint_type = LineJointType.ROUND
    except (ImportError, AttributeError):
        pass
    return m


def _p(x: float, y: float) -> np.ndarray:
    return np.array([x * S, -y * S, 0.0])


def _line(*pts: tuple[float, float], color: str = INK, width: float = STROKE) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=width, fill_opacity=0)
    m.set_points_as_corners([_p(*p) for p in pts])
    return _round(m)


def _curve(*pts: tuple[float, float], color: str = INK) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=STROKE, fill_opacity=0)
    m.set_points_smoothly([_p(*p) for p in pts])
    return _round(m)


def _outline(m: VMobject, color: str = INK, width: float = STROKE) -> VMobject:
    m.set_stroke(color=color, width=width)
    m.set_fill(opacity=0)
    return _round(m)


def desk_scene() -> VGroup:
    desk = VGroup(_line((8, 62), (82, 62)), _line((13, 62), (13, 86)), _line((77, 62), (77, 86)))
    chair = VGroup(_line((17, 38), (19, 65), (33, 65), color=DIM, width=THIN),
                   _line((26, 65), (26, 86), color=DIM, width=THIN),
                   _line((19, 65), (17, 86), color=DIM, width=THIN))
    head = _outline(Circle(radius=5.2 * S)).move_to(_p(30, 33))
    hair = _curve((25.5, 31), (27, 27.6), (31, 27.2), (34.2, 28.4), (35.3, 31.5))
    torso = _curve((29, 38.5), (28.3, 50), (29, 63))
    upper_arm = _line((29.5, 43), (37, 53))
    forearm = _line((37, 53), (49, 58.5))
    leg = _line((29, 63), (42, 64), (43, 82), (47, 82))
    person = VGroup(head, hair, torso, upper_arm, forearm, leg)
    person.forearm = forearm
    glow = Polygon(_p(61, 43), _p(64, 61.5), _p(57, 50), stroke_width=0, fill_color=BLUE, fill_opacity=0.12)
    laptop = VGroup(_line((46, 61.5), (64, 61.5)), _line((64, 61.5), (61, 43)), glow)
    book_small = VGroup(_line((67, 61.5), (79, 61.5), (79, 58), (67, 58), (67, 61.5), color=ORANGE, width=THIN),
                        _line((67, 59.7), (79, 59.7), color=ORANGE, width=THIN))
    scene = VGroup(chair, desk, person, laptop, book_small).move_to(ORIGIN)
    scene.person, scene.laptop, scene.desk, scene.chair, scene.book = person, laptop, desk, chair, book_small
    return scene


def book(title: str = "Hacker's Delight") -> VGroup:
    cover = _outline(RoundedRectangle(corner_radius=0.08, width=2.4, height=3.2))
    spine = Line(cover.get_corner(UP + LEFT) + RIGHT * 0.25, cover.get_corner(DOWN + LEFT) + RIGHT * 0.25,
                 stroke_color=DIM, stroke_width=THIN)
    first, _, rest = title.partition(" ")
    words = VGroup(style.serif(first, 30), style.serif(rest, 30)).arrange(DOWN, buff=0.08)
    words.move_to(cover.get_center() + UP * 0.6)
    squares = VGroup()
    for bit in "01101100":
        sq = Square(side_length=0.18, stroke_color=DIM, stroke_width=THIN,
                    fill_color=ORANGE, fill_opacity=MAX_FILL if bit == "1" else 0)
        squares.add(sq)
    squares.arrange(RIGHT, buff=0.04).move_to(cover.get_center() + DOWN * 0.7)
    return VGroup(cover, spine, words, squares)


def open_book(page: Mobject | None = None) -> VGroup:
    left = _outline(RoundedRectangle(corner_radius=0.06, width=2.6, height=3.2), width=THIN)
    right = left.copy().next_to(left, RIGHT, buff=0)
    lines = VGroup(*[Line(LEFT * 0.95, RIGHT * 0.95, stroke_color=DIM, stroke_width=THIN) for _ in range(7)])
    lines.arrange(DOWN, buff=0.28).move_to(left)
    spread = VGroup(left, right, lines)
    if page is not None:
        if page.width > 2.2:
            page.scale(2.2 / page.width)
        spread.add(page.move_to(right))
    return spread


def chess_board(size: float = 3.2, occupied: Sequence[int] = OCCUPIED) -> VGroup:
    cell = size / 8
    squares = VGroup()
    for i in range(64):
        rank, file = divmod(i, 8)
        dark = (rank + file) % 2 == 0
        sq = Square(side_length=cell, stroke_color=DIM, stroke_width=THIN,
                    fill_color=DIM, fill_opacity=0.12 if dark else 0)
        sq.move_to(np.array([(file - 3.5) * cell, (rank - 3.5) * cell, 0.0]))
        squares.add(sq)
    occ = tuple(sorted(occupied))
    pieces = VGroup(*[_outline(Circle(radius=cell * 0.28)).move_to(squares[i]) for i in occ])
    frame = _outline(Square(side_length=size))
    g = VGroup(squares, frame, pieces)
    g.squares, g.pieces, g.occupied = squares, pieces, occ
    return g


def compiler_machine(label: str = "compiler", width: float = 2.6) -> VGroup:
    h = width * 0.55
    body = _outline(RoundedRectangle(corner_radius=0.18, width=width, height=h))
    inlet = _outline(Triangle().scale_to_fit_height(h * 0.3).rotate(-np.pi / 2), width=THIN).move_to(body.get_left())
    outlet = inlet.copy().move_to(body.get_right())
    gears = VGroup(_outline(Circle(radius=h * 0.16), DIM, THIN), _outline(Circle(radius=h * 0.11), DIM, THIN))
    gears.arrange(RIGHT, buff=0.1).move_to(body.get_center() + UP * h * 0.15)
    name = style.serif(label, 24).move_to(body.get_center() + DOWN * h * 0.25)
    return VGroup(body, inlet, outlet, gears, name)


def phone() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.12, width=0.8, height=1.5))
    speaker = Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=DIM, stroke_width=THIN).move_to(body.get_top() + DOWN * 0.15)
    return VGroup(body, speaker)


def browser_window() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.08, width=1.8, height=1.2))
    bar = Line(body.get_corner(UP + LEFT) + DOWN * 0.25, body.get_corner(UP + RIGHT) + DOWN * 0.25,
               stroke_color=DIM, stroke_width=THIN)
    dots = VGroup(*[_outline(Circle(radius=0.04), DIM, THIN) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    dots.move_to(body.get_corner(UP + LEFT) + np.array([0.25, -0.13, 0.0]))
    return VGroup(body, bar, dots)


def laptop_icon() -> VGroup:
    screen = _outline(RoundedRectangle(corner_radius=0.06, width=1.5, height=0.95))
    base = _outline(Polygon(np.array([-0.95, 0, 0]), np.array([0.95, 0, 0]),
                            np.array([0.8, 0.12, 0]), np.array([-0.8, 0.12, 0])), width=THIN)
    base.next_to(screen, DOWN, buff=0.03)
    return VGroup(screen, base)


def code_icon() -> VGroup:
    ring = _outline(Circle(radius=0.45), DIM, THIN)
    glyph = style.mono("</>", 26, BLUE).move_to(ring)
    return VGroup(ring, glyph)


def game_controller() -> VGroup:
    body = _outline(RoundedRectangle(corner_radius=0.3, width=1.3, height=0.72))
    dpad = VGroup(Line(LEFT * 0.12, RIGHT * 0.12, stroke_color=INK, stroke_width=THIN),
                  Line(DOWN * 0.12, UP * 0.12, stroke_color=INK, stroke_width=THIN))
    dpad.move_to(body.get_center() + LEFT * 0.33)
    buttons = VGroup(_outline(Circle(radius=0.06), ORANGE, THIN), _outline(Circle(radius=0.06), BLUE, THIN))
    buttons.arrange(RIGHT, buff=0.1).move_to(body.get_center() + RIGHT * 0.33)
    return VGroup(body, dpad, buttons)
