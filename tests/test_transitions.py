from __future__ import annotations

import pytest
from manim import Circle, Dot, Square

from kit import transitions
from kit.beat import Board, BeatScene, Erase, Write, leaf_ids
from tests.conftest import render_dry

STYLES = ["fade", "pop", "fall", "swipe", "shove", "dive"]


def _board(style: str) -> Board:
    return Board(f"t-{style}", ("t1", "t2"), (
        Write("t1", "a", lambda: Dot().shift([-2, 1, 0])),
        Write("t1", "b", lambda: Square().shift([2, -1, 0])),
        Write("t1", "c", lambda: Circle(radius=0.4)),
        Erase("t2", "a"),
        Erase("t2", "b"),
    ))


@pytest.mark.parametrize("style", STYLES)
def test_each_style_removes_exactly_the_erased_items(style):
    board = _board(style)

    class Leave(BeatScene):
        beat_id, timing = "t2", {"t1": 4.0, "t2": 4.0}

        def animate_beat(self):
            self.erase("a", "b", style=style, run_time=1.5)

    Leave.board = board
    scene = render_dry(Leave)
    assert set(scene.items) == {"c"}
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


@pytest.mark.parametrize("style", ["fall", "shove", "swipe"])
def test_part_change_uses_the_boards_wipe_style(style):
    first = _board("x")
    second = Board("next", ("n1",), (Write("n1", "d", Dot),), previous=first, wipe=style)

    class Next(BeatScene):
        beat_id, board, timing = "n1", second, {"n1": 4.0}

        def animate_beat(self):
            self.write("d", run_time=0.5)

    scene = render_dry(Next)
    assert set(scene.items) == {"d"}
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


def test_unknown_style_is_rejected():
    with pytest.raises(ValueError, match="unknown transition"):
        transitions.get("teleport")


def test_board_rejects_unknown_wipe_style():
    from kit.beat import BoardMismatch

    with pytest.raises((ValueError, BoardMismatch), match="teleport"):
        Board("x", ("x1",), (), wipe="teleport")


def test_idle_motion_fills_the_hold_and_keeps_frames_exact():
    from kit import motion

    board = Board("idle", ("i1",), (Write("i1", "sq", lambda: Square(fill_color="#58A6FF", fill_opacity=0.4)),))

    class Idle(BeatScene):
        beat_id, timing = "i1", {"i1": 3.0}

        def animate_beat(self):
            self.write("sq", run_time=0.5)

        def idle_animations(self):
            return [motion.ColorCycle(self.items["sq"], ["#58A6FF", "#FF7EE3"], cycles=2)]

    Idle.board = board
    scene = render_dry(Idle)
    assert scene.frames == round(3.0 * 15)


@pytest.mark.parametrize("style", ["fade", "pop", "fall", "swipe", "shove"])
def test_transitions_clear_a_screenshot_too(style):
    import numpy as np
    from manim import Group, ImageMobject, Square

    shot = Group(Square(), ImageMobject(np.full((4, 4, 3), 200, dtype=np.uint8)))
    transitions.get(style)([shot, Square()])
