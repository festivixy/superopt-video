from __future__ import annotations

import pytest
from manim import Square, config

from kit import cartoon
from kit.beat import signature


def test_desk_exposes_its_parts():
    d = cartoon.pov_desk()
    for name in ("left_monitor", "right_monitor", "led", "robot", "cube", "controller",
                 "headphones", "keyboard", "hands", "plant", "can"):
        assert getattr(d, name) in d.submobjects
    assert d.robot.arm in d.robot.submobjects
    assert len(d.cube.tiles) == 3 and len(d.hands) == 2


def test_desk_fills_the_frame_without_spilling():
    d = cartoon.pov_desk()
    assert d.width <= config.frame_width + 1e-6
    assert d.get_top()[1] <= config.frame_height / 2 + 1e-6


@pytest.mark.parametrize("side", ["left", "right"])
def test_screen_content_lands_inside_its_monitor(side):
    m = cartoon.on_screen(Square(side_length=40), side)
    s = cartoon.screen_zone(side)
    assert s.left - 1e-6 <= m.get_left()[0] and m.get_right()[0] <= s.right + 1e-6
    assert s.bottom - 1e-6 <= m.get_bottom()[1] and m.get_top()[1] <= s.top + 1e-6


def test_idle_motion_returns_the_desk_to_exactly_where_it_started():
    d = cartoon.pov_desk()
    before = signature(d)
    for anim in cartoon.desk_idle(d):
        anim.begin()
        for alpha in (0.13, 0.5, 0.77, 1.0):
            anim.interpolate(alpha)
        anim.finish()
    assert signature(d) == before


def test_code_lines_are_abstract_and_fit_the_screen():
    block = cartoon.code_lines("left", rows=7, seed=3)
    assert len(block) >= 7
    s = cartoon.screen_zone("left")
    assert s.left - 1e-6 <= block.get_left()[0] and block.get_right()[0] <= s.right + 1e-6
    again = cartoon.code_lines("left", rows=7, seed=3)
    assert signature(block) == signature(again)


def test_code_lines_also_fit_a_board_zone():
    from kit import zones

    block = cartoon.code_lines("HALF_L", rows=9, seed=4)
    z = zones.ZONES["HALF_L"]
    assert z.left - 1e-6 <= block.get_left()[0] and block.get_right()[0] <= z.right + 1e-6
    assert z.bottom - 1e-6 <= block.get_bottom()[1] and block.get_top()[1] <= z.top + 1e-6
