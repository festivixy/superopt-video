from __future__ import annotations

from manim import (
    DOWN, UP, Create, FadeIn, FadeOut, Indicate, LaggedStart, ReplacementTransform, Rotate, Write,
    there_and_back,
)

from boards.intro import BOARD
from kit import board, draw, style, zones
from kit.beat import BeatScene
from kit.style import ORANGE


class IntroBeat(BeatScene):
    board = BOARD

    def type_a_bit(self, run_time: float = 1.0) -> None:
        arm = self.items["desk"].person.forearm
        self.play(Rotate(arm, angle=0.12, about_point=arm.get_start(), rate_func=there_and_back), run_time=run_time)


class B_I_1(IntroBeat):
    beat_id = "I.1"

    def animate_beat(self):
        s = self.step(4)
        self.write("desk", run_time=2 * s)
        self.write("namecard", anim=FadeIn, run_time=s, shift=UP * 0.2)
        self.write("timeline_axis", run_time=s)


class B_I_2(IntroBeat):
    beat_id = "I.2"

    def animate_beat(self):
        s = self.step(5)
        self.erase("namecard")
        self.type_a_bit(run_time=s)
        self.write("compile_flow", run_time=3 * s)
        self.type_a_bit(run_time=s)


class B_I_3(IntroBeat):
    beat_id = "I.3"

    def animate_beat(self):
        s = self.step(5)
        self.erase("compile_flow")
        closed = zones.fit(draw.book(), "SIDE", align="top")
        self.play(Create(closed), run_time=2 * s)
        self.write("book", anim=lambda m: ReplacementTransform(closed, m), run_time=1.5 * s)
        self.write("bits_note", anim=FadeIn, run_time=s)


class B_I_4(IntroBeat):
    beat_id = "I.4"

    def animate_beat(self):
        s = self.step(6)
        self.erase("book", "bits_note")
        cards = self.write("loop_vs_trick", run_time=3 * s)
        self.play(Indicate(cards[1], color=ORANGE), run_time=s)
        self.write("why_note", anim=FadeIn, run_time=s)


class B_I_5(IntroBeat):
    beat_id = "I.5"

    def animate_beat(self):
        s = self.step(5)
        self.erase("loop_vs_trick", "why_note")
        q = self.write("question", run_time=3 * s)
        self.play(Indicate(q[0][2], color=ORANGE), run_time=s)
        self.write("later_note", anim=FadeIn, run_time=0.5 * s)


class B_I_6(IntroBeat):
    beat_id = "I.6"

    def animate_beat(self):
        s = self.step(8)
        self.erase("question", "later_note")
        item = self.write("chess", run_time=2 * s)
        grid = item[0]
        ones = [style.mono("1", 20, style.BLUE).move_to(grid.squares[i]) for i in grid.occupied]
        self.play(FadeIn(*ones), run_time=s)
        for k in range(3):
            self.play(Indicate(grid.pieces[k], color=ORANGE), ones[k].animate.set_color(ORANGE), run_time=0.6 * s)
            self.play(FadeOut(ones[k]), run_time=0.4 * s)
        self.play(FadeOut(*ones[3:]), run_time=0.5 * s)


class B_I_7(IntroBeat):
    beat_id = "I.7"

    def animate_beat(self):
        s = self.step(4)
        self.erase("chess")
        g = self.write("scale", run_time=2 * s)
        self.play(LaggedStart(*[Indicate(d) for d in g[0][1]], lag_ratio=0.3), run_time=s)


class B_I_8(IntroBeat):
    beat_id = "I.8"

    def animate_beat(self):
        s = self.step(4)
        self.erase("scale")
        self.write("problem", anim=Write, run_time=3 * s)


class B_I_9(IntroBeat):
    beat_id = "I.9"

    def animate_beat(self):
        s = self.step(4)
        self.write("headline", anim=Write, run_time=s)
        self.write("timeline_ticks", anim=lambda m: LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in m], lag_ratio=0.4),
                   run_time=2.5 * s)
