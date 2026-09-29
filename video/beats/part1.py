from __future__ import annotations

from manim import (
    DOWN, LEFT, UP, Create, FadeIn, GrowFromCenter, GrowFromEdge, Indicate, LaggedStart, SurroundingRectangle,
    Transform, VGroup, Write, config,
)

import boards.part1 as B
from boards.part1 import BOARD, LOOP_LINES
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


class Part1Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_1_1(Part1Beat):
    beat_id = "1.1"

    def animate_beat(self):
        s = self.step(8)
        card = self.write("c_code", anim=FadeIn, run_time=1.5 * s, shift=UP * 0.2)
        row = B.scan_start()
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.1), run_time=s)
        lit = SurroundingRectangle(card.lines[LOOP_LINES["for"]], color=ORANGE, buff=0.06)
        ptr = pics.pointer().next_to(row.bit(0), UP, buff=0.12)
        i_label = style.mono("i = 0", 34, ORANGE).next_to(row, DOWN, buff=0.6)
        self.play(Create(lit), GrowFromCenter(ptr), FadeIn(i_label), run_time=0.5 * s)
        for k in range(3):
            if k:
                self.play(Transform(lit, SurroundingRectangle(card.lines[LOOP_LINES["for"]], color=ORANGE, buff=0.06)),
                          ptr.animate(rate_func=motion.SPRING).next_to(row.bit(k), UP, buff=0.12),
                          Transform(i_label, style.mono(f"i = {k}", 34, ORANGE).move_to(i_label)), run_time=0.45 * s)
            self.play(Transform(lit, SurroundingRectangle(card.lines[LOOP_LINES["if"]], color=ORANGE, buff=0.06)),
                      Indicate(row.bit(k), scale_factor=1.25), run_time=0.45 * s)
        self.play(Transform(lit, SurroundingRectangle(card.lines[LOOP_LINES["return"]], color=GREEN, buff=0.06)),
                  Transform(row.bit(2), pics.flipped(row.bit(2)), rate_func=motion.SPRING), run_time=0.8 * s)
        self.clear_transients()
        self.settle("scan_demo")


class B_1_2(Part1Beat):
    beat_id = "1.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("scan_demo", "c_code", style="pop", run_time=0.5)
        wall = self.write("asm_wall", anim=lambda w: LaggedStart(*[FadeIn(l, shift=DOWN * 0.1) for l in w.lines],
                                                                  lag_ratio=0.02), run_time=2 * s)
        self.write("asm_group", anim=pop_in, run_time=0.7 * s)
        box = SurroundingRectangle(VGroup(*wall.lines[1:4]), color=ORANGE, buff=0.03)
        count = style.mono("3", 40, ORANGE).move_to(B.asm_math())
        self.play(Create(box), FadeIn(count), run_time=0.4 * s)
        for g in range(1, 32):
            group = VGroup(*wall.lines[1 + 3 * g:4 + 3 * g])
            slow = g < 3
            self.play(Transform(box, SurroundingRectangle(group, color=ORANGE, buff=0.03)),
                      Transform(count, style.mono(str(3 * (g + 1)), 40, ORANGE).move_to(count)),
                      run_time=(0.35 if slow else 0.045) * s)
        xors = [l for l in wall.lines if l.text.startswith("xor")]
        self.play(*[Indicate(x, color=GREEN, scale_factor=1.4) for x in xors], run_time=0.5 * s)
        self.clear_transients()
        self.write("asm_math", anim=Write, run_time=s)


class B_1_3(Part1Beat):
    beat_id = "1.3"

    def animate_beat(self):
        s = self.step(6)
        self.erase("asm_wall", "asm_group", "asm_math", style="swipe", run_time=1.4)
        bars = self.write("bars", anim=lambda b: LaggedStart(
            *[FadeIn(row[0]) for row in b], *[GrowFromEdge(bar, LEFT, rate_func=motion.SPRING) for bar in b.bars],
            *[FadeIn(row[2], scale=1.5) for row in b], lag_ratio=0.15), run_time=1.5 * s)
        self.write("two_asm", anim=lambda t: LaggedStart(pop_in(t[0]), Create(t[1]), FadeIn(t[2]), lag_ratio=0.4),
                   run_time=1.5 * s)
        self.write("all_inputs", anim=lambda g: AnimationGroupOf(g), run_time=1.5 * s)
        self.play(Indicate(bars.bars[1], color=GREEN, scale_factor=1.4), run_time=0.8 * s)


def AnimationGroupOf(g):
    return LaggedStart(LaggedStart(*[FadeIn(d, scale=2) for d in g[0]], lag_ratio=0.01), FadeIn(g[1]), Create(g[2]),
                       lag_ratio=0.5)


class B_1_4(Part1Beat):
    beat_id = "1.4"

    def animate_beat(self):
        s = self.step(4)
        bars = self.items["bars"].bars
        self.play(bars[0].animate(rate_func=motion.ANTICIPATE).stretch_to_fit_width(bars[1].width).align_to(bars[0], LEFT),
                  run_time=s)
        self.erase("bars", "two_asm", "all_inputs", style="fall", run_time=1.0)
        self.write("title", anim=lambda t: LaggedStart(Write(t[0]), pop_in(t[1][0]), Create(t[1][1]), lag_ratio=0.5),
                   run_time=2 * s)
