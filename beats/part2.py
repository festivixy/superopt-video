from __future__ import annotations

from manim import UP, Create, FadeIn, Indicate, LaggedStart, Write

from boards.part2 import BOARD
from kit.beat import BeatScene
from kit.style import BLUE, ORANGE


class Part2Beat(BeatScene):
    board = BOARD


class B_2_1(Part2Beat):
    beat_id = "2.1"

    def animate_beat(self):
        s = self.step(7)
        self.write("headline", anim=Write, run_time=s)
        reg = self.write("reg108", anim=lambda m: LaggedStart(Create(m.cells), FadeIn(m.places), FadeIn(m.digits),
                                                               lag_ratio=0.5), run_time=2 * s)
        ones = [reg.bit(i)[1] for i in (6, 5, 3, 2)]
        self.play(LaggedStart(*[Indicate(d, color=BLUE) for d in ones], lag_ratio=0.3), run_time=s)
        self.write("sum108", anim=Write, run_time=2 * s)
        self.write("note_regs", anim=FadeIn, run_time=s)


class B_2_2(Part2Beat):
    beat_id = "2.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("note_regs")
        self.keep("sum108")
        self.write("sub_dec", anim=FadeIn, run_time=2 * s)
        self.write("sub_bin", anim=Write, run_time=2 * s)
        self.write("borrow_bin", run_time=s)
        self.write("minus_rule", anim=FadeIn, run_time=s, shift=UP * 0.2)


class B_2_3(Part2Beat):
    beat_id = "2.3"

    def animate_beat(self):
        s = self.step(7)
        self.erase("sub_dec", "minus_rule", "borrow_bin", "sub_bin")
        self.write("and_table", anim=FadeIn, run_time=s)
        op = self.write("and_op", anim=Write, run_time=2 * s)
        self.play(LaggedStart(*[Indicate(op.digit(2, k), color=ORANGE) for k in range(8)], lag_ratio=0.15),
                  run_time=s)
        self.write("and_marks", run_time=2 * s)


class B_2_4(Part2Beat):
    beat_id = "2.4"

    def animate_beat(self):
        s = self.step(6)
        self.erase("and_marks", "and_table")
        box = self.write("isa", anim=FadeIn, run_time=2 * s)
        self.write("length_def", anim=Write, run_time=s)
        self.write("tally", anim=FadeIn, run_time=s)
        self.play(Indicate(box.names["sub"], color=ORANGE), Indicate(box.names["and"], color=ORANGE), run_time=s)
