from __future__ import annotations

from manim import DOWN, LEFT, UP, FadeIn, GrowFromCenter, Indicate, LaggedStart, Transform, Write, config

import boards.part4 as B
from boards.part4 import BOARD
from kit import motion, pics
from kit.beat import BeatScene
from kit.style import GREEN


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


class Part4Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_4_1(Part4Beat):
    beat_id = "4.1"

    def animate_beat(self):
        s = self.step(8)
        self.write("massalin", anim=lambda g: LaggedStart(FadeIn(g[0], shift=DOWN * 0.3), pop_in(g[1]), Write(g[2]),
                                                           lag_ratio=0.35), run_time=1.5 * s)
        final = B.search()
        rows = B.search_start()
        self.play(LaggedStart(*[pop_in(strip) for row in rows for strip in row], lag_ratio=0.08), run_time=s)
        glass = pics.magnifier(1.3).next_to(rows[0][0], UP + LEFT, buff=0.05)
        self.play(FadeIn(glass, scale=0.5), run_time=0.3 * s)
        strips = B._flat(rows)
        hop = 2.6 * s / (B.WINNER + 1)
        for k in range(B.WINNER):
            self.play(glass.animate(rate_func=motion.SPRING).move_to(strips[k].get_center() + UP * 0.1 + LEFT * 0.1),
                      run_time=hop * 0.55)
            self.play(GrowFromCenter(final[1][k].copy()), run_time=hop * 0.45)
        self.play(glass.animate(rate_func=motion.SPRING).move_to(strips[B.WINNER].get_center()), run_time=hop)
        winner = B.winner_of(final).copy()
        self.play(Transform(strips[B.WINNER], winner, rate_func=motion.SPRING), glass.animate.set_opacity(0), run_time=0.5 * s)
        tests = final[2].copy()
        self.play(LaggedStart(*[pop_in(d) for d in tests[0]], lag_ratio=0.3), run_time=0.5 * s)
        self.play(LaggedStart(*[GrowFromCenter(c, rate_func=motion.ELASTIC) for c in tests[1]], lag_ratio=0.3), run_time=0.8 * s)
        self.clear_transients()
        self.settle("search")


class B_4_2(Part4Beat):
    beat_id = "4.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("massalin", "search", style="fall", run_time=1.0)
        final1 = B.len1()
        self.play(FadeIn(final1[0], scale=1.5), LaggedStart(*[pop_in(t) for t in final1[1]], lag_ratio=0.08), run_time=1.2 * s)
        self.play(LaggedStart(*[GrowFromCenter(x) for x in final1[2]], lag_ratio=0.12), run_time=1.2 * s)
        self.play(FadeIn(final1[3], scale=1.6, rate_func=motion.SPRING), run_time=0.4 * s)
        self.clear_transients()
        self.settle("len1")
        start = B.len2_start()
        final2 = B.len2()
        self.play(FadeIn(start[0], scale=1.5), LaggedStart(*[FadeIn(c) for c in start[1]], lag_ratio=0.004), run_time=1.3 * s)
        self.play(FadeIn(start[2], scale=1.6, rate_func=motion.SPRING), run_time=0.4 * s)
        visited = [Transform(c, f) for c, f in zip(start[1][:B.LEN2_WINNER], final2[1][:B.LEN2_WINNER])]
        self.play(LaggedStart(*visited, lag_ratio=0.01), run_time=1.6 * s)
        self.play(Transform(start[1][B.LEN2_WINNER], final2[1][B.LEN2_WINNER], rate_func=motion.SPRING), run_time=0.4 * s)
        self.play(GrowFromCenter(final2[3], rate_func=motion.ELASTIC), run_time=0.6 * s)
        self.clear_transients()
        self.settle("len2")
        self.play(Indicate(self.items["len2"][1][B.LEN2_WINNER], color=GREEN, scale_factor=2.5), run_time=0.6 * s)


class B_4_3(Part4Beat):
    beat_id = "4.3"

    def animate_beat(self):
        s = self.step(4)
        self.erase("len1", style="pop", run_time=0.5)
        final = B.catch()
        passed, field, ask = final
        self.play(pop_in(passed[0]), LaggedStart(*[pop_in(d) for d in passed[1][0]], lag_ratio=0.3), run_time=0.6 * s)
        self.play(LaggedStart(*[GrowFromCenter(c, rate_func=motion.ELASTIC) for c in passed[1][1]], lag_ratio=0.3), run_time=0.6 * s)
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in field], lag_ratio=0.01), run_time=1.2 * s)
        self.play(GrowFromCenter(ask, rate_func=motion.ELASTIC), run_time=0.8 * s)
        self.clear_transients()
        self.settle("catch")
