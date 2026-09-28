from __future__ import annotations

import pytest
from manim import Text

from kit import draw, style

BUILDERS = [
    draw.desk_scene, draw.book, draw.open_book, draw.chess_board, draw.compiler_machine,
    draw.phone, draw.browser_window, draw.laptop_icon, draw.code_icon, draw.game_controller,
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


def test_desk_scene_exposes_parts():
    s = draw.desk_scene()
    for name in ("person", "laptop", "desk", "chair", "book"):
        assert getattr(s, name) in s.submobjects
    assert s.person.forearm in s.person.submobjects


def test_chess_board_geometry():
    b = draw.chess_board()
    assert len(b.squares) == 64
    assert b.squares[0].get_y() < b.squares[63].get_y()
    assert b.squares[0].get_x() < b.squares[7].get_x()
    assert len(b.pieces) == len(b.occupied)
    assert list(b.occupied) == sorted(b.occupied)


def test_book_title_is_ours():
    titles = [t.text for t in draw.book().get_family() if isinstance(t, Text)]
    joined = " ".join(titles)
    assert "Hacker's" in joined and "Delight" in joined
