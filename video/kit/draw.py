from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Circle, Line, Polygon, RoundedRectangle, Square, VGroup, VMobject

from kit import style
from kit.style import BLUE, DIM, INK, STROKE

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


