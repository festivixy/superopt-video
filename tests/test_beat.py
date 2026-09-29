from __future__ import annotations

import pytest
from manim import Circle, Dot, FadeIn, FadeOut, Square

from kit.beat import (
    Board, BoardMismatch, BeatScene, Erase, Keep, TimingOverrun, Write, fingerprint, leaf_ids, replay,
)
from tests.conftest import render_dry

A = Board("A", ("a1", "a2"), (
    Write("a1", "dot", lambda: Dot()),
    Write("a1", "sq", lambda: Square().shift([2, 0, 0])),
    Keep("a2", "sq", 0),
    Erase("a2", "dot"),
    Write("a2", "circle", lambda: Circle().shift([-2, 0, 0])),
))
B = Board("B", ("b1",), (Write("b1", "dot", lambda: Dot().shift([0, 1, 0])),), previous=A)
TIMES = {"a1": 3.0, "a2": 4.0, "b1": 2.0}


class A1(BeatScene):
    beat_id, board, timing = "a1", A, TIMES

    def animate_beat(self):
        self.write("dot", anim=FadeIn, run_time=0.5)
        self.write("sq", run_time=0.5)


class A2(BeatScene):
    beat_id, board, timing = "a2", A, TIMES

    def animate_beat(self):
        self.keep("sq")
        self.erase("dot")
        self.write("circle", run_time=0.5)


class B1(BeatScene):
    beat_id, board, timing = "b1", B, TIMES

    def animate_beat(self):
        self.write("dot", run_time=0.5)


def test_records_must_name_known_beats_in_order():
    with pytest.raises(BoardMismatch, match="unknown beat"):
        Board("X", ("x1",), (Write("zz", "k", Dot),))
    with pytest.raises(BoardMismatch, match="order"):
        Board("X", ("x1", "x2"), (Write("x2", "k", Dot), Write("x1", "j", Dot)))


def test_replay_applies_write_keep_erase():
    items = replay(A.records_through("a2"))
    assert sorted(items) == ["circle", "sq"]
    assert items["sq"].height <= 0.8 + 1e-6


def test_replay_rejects_double_write_and_missing_erase():
    with pytest.raises(BoardMismatch, match="written twice"):
        replay((Write("a1", "k", Dot), Write("a1", "k", Dot)))
    with pytest.raises(BoardMismatch, match="not on the board"):
        replay((Erase("a1", "k"),))


@pytest.mark.parametrize("cls", [A1, A2, B1])
def test_scene_ends_on_the_replayed_board_and_on_time(cls):
    scene = render_dry(cls)
    expected = replay(cls.board.records_through(cls.beat_id))
    assert {k: fingerprint(m) for k, m in scene.items.items()} == {
        k: fingerprint(m) for k, m in expected.items()
    }
    assert scene.elapsed == pytest.approx(TIMES[cls.beat_id], abs=0.05)


def test_first_beat_of_a_part_wipes_the_previous_board():
    scene = render_dry(B1)
    assert set(scene.items) == {"dot"}
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


def test_indicating_part_of_an_item_does_not_count_as_stray():
    class Pointy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            from manim import Indicate, LaggedStart
            self.write("dot", run_time=0.5)
            sq = self.write("sq", run_time=0.5)
            self.play(LaggedStart(Indicate(sq), Indicate(self.items["dot"])), run_time=0.5)

    render_dry(Pointy)


def test_unperformed_record_raises():
    class Lazy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)

    with pytest.raises(BoardMismatch, match="sq"):
        render_dry(Lazy)


def test_record_not_on_the_board_raises():
    class Rogue(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("nope")

    with pytest.raises(BoardMismatch, match="nope"):
        render_dry(Rogue)


def test_stray_mobject_raises():
    class Messy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)
            self.write("sq", run_time=0.5)
            self.play(FadeIn(Circle()), run_time=0.2)

    with pytest.raises(BoardMismatch, match="stray"):
        render_dry(Messy)


def test_transient_mobject_removed_in_time_is_fine():
    class Tidy(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.5)
            self.write("sq", run_time=0.5)
            tmp = Circle()
            self.play(FadeIn(tmp), run_time=0.2)
            self.play(FadeOut(tmp), run_time=0.2)

    render_dry(Tidy)


def test_overrun_raises_with_beat_and_amount():
    class Slow(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=2.5)
            self.write("sq", run_time=2.5)

    with pytest.raises(TimingOverrun, match=r"a1.*2\.1"):
        render_dry(Slow)


def test_missing_timing_raises():
    class NoTime(BeatScene):
        beat_id, board, timing = "a1", A, {"a2": 1.0}

        def animate_beat(self):
            pass

    with pytest.raises(BoardMismatch, match="no timing"):
        render_dry(NoTime)


def test_restyling_a_board_item_in_place_is_caught():
    class Recolor(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            dot = self.write("dot", run_time=0.5)
            self.write("sq", run_time=0.5)
            self.play(dot.animate.set_color("#FC6255").set_opacity(0.1), run_time=0.3)

    with pytest.raises(BoardMismatch, match="dot.*changed"):
        render_dry(Recolor)


ODD = Board("odd", ("o1",), (Write("o1", "dot", lambda: Dot()),))


class Odd(BeatScene):
    beat_id, board, timing = "o1", ODD, {"o1": 3.0}

    def animate_beat(self):
        dot = self.write("dot", run_time=0.35)
        for _ in range(4):
            self.play(dot.animate.shift([0.01, 0, 0]).shift([-0.01, 0, 0]), run_time=0.35)


def test_frame_count_lands_exactly_on_target_in_dry_run():
    scene = render_dry(Odd)
    assert scene.frames == round(3.0 * 15)


def test_rendered_clip_has_exactly_the_target_frames(tmp_path):
    import av
    from manim import tempconfig

    with tempconfig({"quality": "low_quality", "disable_caching": True, "media_dir": str(tmp_path)}):
        scene = Odd()
        scene.render()
        path = scene.renderer.file_writer.movie_file_path
    with av.open(str(path)) as clip:
        frames = sum(1 for _ in clip.decode(video=0))
    assert frames == round(3.0 * 15)


SWAP = Board("swap", ("s1", "s2"), (
    Write("s1", "old", lambda: Square()),
    Erase("s2", "old"),
    Write("s2", "new", lambda: Circle()),
))


def test_swap_replaces_one_item_with_another_in_zero_frames():
    class Swap(BeatScene):
        beat_id, board, timing = "s2", SWAP, {"s1": 2.0, "s2": 2.0}

        def animate_beat(self):
            before = self.frames
            self.swap("old", "new")
            assert self.frames == before

    scene = render_dry(Swap)
    assert set(scene.items) == {"new"}
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


def test_clear_transients_removes_working_left_after_lagged_pops():
    from manim import GrowFromCenter, LaggedStart, VGroup

    class Working(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.3)
            self.write("sq", run_time=0.3)
            scratch = VGroup(*[Circle(radius=0.2).shift([x, -2, 0]) for x in range(4)])
            self.play(LaggedStart(*[GrowFromCenter(c) for c in scratch], lag_ratio=0.2), run_time=0.5)
            self.clear_transients()

    scene = render_dry(Working)
    assert leaf_ids(scene.mobjects) == leaf_ids(scene.items.values())


def test_float_noise_below_a_pixel_is_not_a_board_change():
    class Nudge(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.3)
            sq = self.write("sq", run_time=0.3)
            self.play(sq.animate.scale(1.0006), run_time=0.2)

    render_dry(Nudge)


def test_a_visible_move_is_still_a_board_change():
    class Shove(BeatScene):
        beat_id, board, timing = "a1", A, TIMES

        def animate_beat(self):
            self.write("dot", run_time=0.3)
            sq = self.write("sq", run_time=0.3)
            self.play(sq.animate.shift([0.05, 0, 0]), run_time=0.2)

    with pytest.raises(BoardMismatch, match="sq.*changed"):
        render_dry(Shove)


def test_signature_covers_screenshots():
    import numpy as np
    from manim import Group, ImageMobject

    from kit.beat import signature, same_look

    shot = Group(Square(), ImageMobject(np.full((4, 4, 3), 200, dtype=np.uint8)))
    moved = shot.copy().shift([1, 0, 0])
    assert same_look(signature(shot), signature(shot.copy()))
    assert not same_look(signature(shot), signature(moved))
