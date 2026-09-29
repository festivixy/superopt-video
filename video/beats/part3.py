from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, AnimationGroup, FadeIn, FadeOut, GrowFromCenter, Indicate, LaggedStart,
    ReplacementTransform, Wiggle, Write, config,
)

import boards.part3 as B
from boards.part3 import BOARD
from kit import board, motion, pics, style
from kit.beat import BeatScene
from kit.style import BLUE, GREEN, ORANGE
import facts


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


class Part3Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)

    def run_through(self, m, value_in: str, value_out: str, run_time: float) -> None:
        token = (style.mono(value_in, 56, BLUE) if value_in else pics.marble(BLUE, 0.2)).next_to(m.inlet, LEFT, buff=0.5)
        self.play(FadeIn(token, shift=RIGHT * 0.4), run_time=run_time * 0.2)
        self.play(token.animate(rate_func=motion.ANTICIPATE).move_to(m.inlet).scale(0.5).set_opacity(0),
                  run_time=run_time * 0.2)
        if len(m.stations) and m.cover.get_fill_opacity() == 0:
            self.play(LaggedStart(*[Indicate(st, color=BLUE, scale_factor=1.35) for st in m.stations], lag_ratio=0.5),
                      run_time=run_time * 0.35)
        out = (style.mono(value_out, 56, GREEN) if value_out else pics.marble(GREEN, 0.2)).next_to(m.outlet, RIGHT, buff=0.5)
        self.play(FadeIn(out, shift=RIGHT * 0.5, rate_func=motion.SPRING), run_time=run_time * 0.25)


class B_3_1(Part3Beat):
    beat_id = "3.1"

    def animate_beat(self):
        m = B.machine_open()
        self.play(pop_in(m), run_time=1.5)
        self.run_through(m, "", "", run_time=6.0)
        self.clear_transients()
        self.add(m)
        self.run_through(m, "6", "12", run_time=3.5)
        self.clear_transients()
        self.add(m)
        self.run_through(m, "21", "42", run_time=3.5)
        self.clear_transients()
        self.add(m)
        self.play(FadeIn(B.machine()[0].cover, shift=DOWN * 0.8, rate_func=motion.SPRING), run_time=1.5)
        self.clear_transients()
        self.write("machine", anim=lambda g: AnimationGroup(FadeIn(g[0], run_time=0.01),
                                                           GrowFromCenter(g[1], rate_func=motion.ELASTIC)), run_time=1.2)
        self.wait(2.0)
        self.play(Wiggle(self.items["machine"][1], scale_value=1.4), run_time=1.5)


class B_3_2(Part3Beat):
    beat_id = "3.2"

    def animate_beat(self):
        s = self.step(9)
        self.erase("machine", style="pop", run_time=0.5)
        trio = self.write("trio", anim=lambda t: LaggedStart(*[pop_in(m) for m in t], lag_ratio=0.3), run_time=1.5 * s)
        row = B.shift_start()
        target = B.shift14()[0]
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.08), run_time=s)
        moves = [row.switches[j].animate(rate_func=motion.SPRING).move_to(target.switches[j - 1]) for j in range(1, 8)]
        newcomer = target.switches[7].copy()
        self.play(*moves, FadeOut(row.switches[0], shift=LEFT * 0.6), GrowFromCenter(newcomer), run_time=1.2 * s)
        self.clear_transients()
        self.write("shift14", anim=lambda g: AnimationGroup(FadeIn(g[0], run_time=0.01), Write(g[1])), run_time=0.8 * s)
        self.write("decimal", anim=lambda d: LaggedStart(*[FadeIn(x, shift=LEFT * 0.3) for x in d], lag_ratio=0.4),
                   run_time=1.2 * s)
        for x, y in (("7", "14"), ("3", "6"), ("10", "20")):
            tokens = [style.mono(x, 38, BLUE).next_to(m.inlet, LEFT, buff=0.35) for m in trio]
            outs = [style.mono(y, 38, GREEN).next_to(m.outlet, RIGHT, buff=0.35) for m in trio]
            self.play(*[FadeIn(t, shift=RIGHT * 0.3) for t in tokens], run_time=0.3 * s)
            self.play(*[t.animate.move_to(m.inlet).scale(0.4).set_opacity(0) for t, m in zip(tokens, trio)], run_time=0.3 * s)
            self.play(*[FadeIn(o, shift=RIGHT * 0.3, rate_func=motion.SPRING) for o in outs], run_time=0.3 * s)
            self.play(*[FadeOut(o) for o in outs], run_time=0.15 * s)
            self.clear_transients()


class B_3_3(Part3Beat):
    beat_id = "3.3"

    def animate_beat(self):
        s = self.step(5)
        self.erase("trio", "shift14", "decimal", style="pop", run_time=0.5)
        self.write("recipes", anim=lambda r: LaggedStart(*[pop_in(row) for row in r], lag_ratio=0.35), run_time=1.5 * s)
        self.play(Indicate(self.items["recipes"][0], color=GREEN, scale_factor=1.15), run_time=0.7 * s)
        self.write("mystery", anim=lambda m: LaggedStart(*[pop_in(row) for row in m[0]], GrowFromCenter(m[1], rate_func=motion.ELASTIC),
                                                          lag_ratio=0.2), run_time=1.5 * s)
        self.play(Wiggle(self.items["mystery"][1], scale_value=1.3), run_time=s)


class B_3_4(Part3Beat):
    beat_id = "3.4"

    def animate_beat(self):
        s = self.step(9)
        self.erase("recipes", "mystery", style="fall", run_time=1.0)
        cards = self.write("rules", anim=lambda r: LaggedStart(*[pop_in(c) for c in r], lag_ratio=0.3), run_time=s)
        boxes = B._passes()
        self.play(LaggedStart(*[pop_in(b) for b in boxes], lag_ratio=0.2), run_time=0.7 * s)
        strip = B.strip_at(0)
        self.play(FadeIn(strip, shift=RIGHT * 0.4), run_time=0.4 * s)
        for stage in (1, 2, 3):
            nxt = B.strip_at(stage)
            self.play(boxes[stage - 1].plate.animate(rate_func=motion.looped(lambda t: 1 - abs(2 * t - 1), 1)).shift(DOWN * 0.2),
                      Indicate(cards[stage - 1], color=ORANGE, scale_factor=1.06),
                      ReplacementTransform(strip, nxt, rate_func=motion.SPRING), run_time=0.9 * s)
            strip = nxt
        self.play(strip.animate(rate_func=motion.SPRING).align_to(boxes[-1], LEFT), run_time=0.5 * s)
        self.clear_transients()
        self.write("passes", anim=lambda p: AnimationGroup(FadeIn(p[0], run_time=0.01), FadeIn(p[1], run_time=0.01),
                                                          GrowFromCenter(p[2], rate_func=motion.ELASTIC)), run_time=0.8 * s)
        loop = board.code_card(facts.C_SOURCE, size=11).scale_to_fit_width(3.2).move_to([-5.0, -2.4, 0])
        self.play(FadeIn(loop, shift=RIGHT * 0.5), run_time=0.5 * s)
        self.play(loop.animate(rate_func=motion.ANTICIPATE).move_to(self.items["passes"][0][0]).scale(0.1).set_opacity(0),
                  run_time=0.5 * s)
        self.clear_transients()
        self.write("ninety_eight", anim=lambda n: AnimationGroup(
            LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in n[0]], lag_ratio=0.02), FadeIn(n[1], scale=1.6)), run_time=1.6 * s)
