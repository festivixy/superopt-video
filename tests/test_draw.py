from __future__ import annotations

import pytest
from manim import Text

from kit import draw, style

BUILDERS = [
    draw.chess_board, draw.phone, draw.browser_window, draw.laptop_icon, draw.code_icon,
]


def non_text_parts(m):
    if isinstance(m, Text):
        return []
    out = [m]
    for sub in m.submobjects:
        out.extend(non_text_parts(sub))
    return out


@pytest.mark.parametrize("build", BUILDERS, ids=lambda b: b.__name__)
def test_builds_something_visible(build):
    m = build()
    assert m.width > 0 and m.height > 0


@pytest.mark.parametrize("build", BUILDERS, ids=lambda b: b.__name__)
def test_monoline_rules(build):
    for part in non_text_parts(build()):
        if not part.has_points():
            continue
        assert part.get_fill_opacity() <= draw.MAX_FILL + 1e-9
        if part.get_stroke_opacity() > 0 and part.get_stroke_width() > 0:
            assert part.get_stroke_width() in (style.STROKE, style.STROKE * 0.7)


def test_chess_board_geometry():
    b = draw.chess_board()
    assert len(b.squares) == 64
    assert b.squares[0].get_y() < b.squares[63].get_y()
    assert b.squares[0].get_x() < b.squares[7].get_x()
    assert len(b.pieces) == len(b.occupied)
    assert list(b.occupied) == sorted(b.occupied)


