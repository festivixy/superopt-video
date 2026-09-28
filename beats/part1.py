from __future__ import annotations

from manim import LEFT, UP, Create, FadeIn, GrowFromEdge, Indicate, LaggedStart, Write

from boards.part1 import BOARD
from kit.beat import BeatScene
from kit.style import ORANGE


class Part1Beat(BeatScene):
    board = BOARD


class B_1_1(Part1Beat):
    beat_id = "1.1"

    def animate_beat(self):
        s = self.step(6)
        self.write("headline", anim=Write, run_time=s)
        self.write("c_code", anim=FadeIn, run_time=2 * s, shift=UP * 0.2)
        self.write("c_notes", anim=lambda m: LaggedStart(*[Create(n) for n in m], lag_ratio=0.6), run_time=3 * s)


class B_1_2(Part1Beat):
    beat_id = "1.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("c_notes")
        self.keep("c_code")
        self.write("asm_wall", anim=lambda m: LaggedStart(*[FadeIn(l) for l in m.lines], lag_ratio=0.03),
                   run_time=3 * s)
        self.write("asm_box", run_time=s)
        self.write("asm_group", anim=FadeIn, run_time=s)
        self.write("asm_math", anim=Write, run_time=2 * s)


class B_1_3(Part1Beat):
    beat_id = "1.3"

    def animate_beat(self):
        s = self.step(6)
        self.erase("asm_box", "asm_wall", "asm_group")
        self.write("bars", anim=lambda m: LaggedStart(
            *[GrowFromEdge(b, LEFT) for b in m.bars], *[FadeIn(t) for t in [*m.labels, *m.values]], lag_ratio=0.2),
            run_time=2 * s)
        self.write("two_asm", anim=FadeIn, run_time=s)
        self.play(Indicate(self.items["bars"].bars[1], color=ORANGE), run_time=s)
        self.write("same_note", anim=FadeIn, run_time=s)


class B_1_4(Part1Beat):
    beat_id = "1.4"

    def animate_beat(self):
        s = self.step(4)
        self.erase("headline", "c_code", "asm_math", "bars", "two_asm", "same_note", run_time=s)
        self.write("title", anim=Write, run_time=2 * s)
