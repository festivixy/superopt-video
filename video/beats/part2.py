from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, ArcBetweenPoints, Create, FadeIn, FadeOut, GrowFromCenter, Indicate, LaggedStart,
    TransformFromCopy, Transform, Write, config,
)

import boards.part2 as B
from boards.part2 import BOARD
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import BLUE, GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


class Part2Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_2_1(Part2Beat):
    beat_id = "2.1"

    def animate_beat(self):
        s = self.step(8)
        row = B.row_off()
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.08), run_time=s)
        places = list(reversed(row.places))
        self.play(FadeIn(places[0], scale=1.5), run_time=0.3 * s)
        for a, b in zip(places, places[1:]):
            hop = ArcBetweenPoints(a.get_top() + UP * 0.05, b.get_top() + UP * 0.05, angle=-2.2).set_stroke(ORANGE, 2)
            times2 = style.math(r"\times 2", 24, ORANGE).next_to(hop, UP, buff=0.02)
            self.play(Create(hop), FadeIn(times2), FadeIn(b, scale=1.5), run_time=0.25 * s)
            self.play(FadeOut(hop), FadeOut(times2), run_time=0.08 * s)
        ons = (6, 5, 3, 2)
        self.play(LaggedStart(*[Transform(row.bit(i), pics.flipped(row.bit(i)), rate_func=motion.SPRING) for i in ons],
                              lag_ratio=0.3), run_time=1.2 * s)
        total = B.sum108()
        drops = [row.places[7 - i].copy().set_color(BLUE) for i in ons]
        self.play(LaggedStart(*[d.animate(rate_func=motion.DROP).move_to(total[0][k * 3:k * 3 + 2].get_center() if k < 3 else total[0][9].get_center())
                                for k, d in enumerate(drops)], lag_ratio=0.2), run_time=s)
        self.clear_transients()
        self.settle("sw108")
        self.write("sum108", anim=Write, run_time=s)
        wide = pics.switch_row(0, n=32, h=0.32).next_to(self.items["sum108"], DOWN, buff=0.7)
        self.play(LaggedStart(*[pop_in(sw) for sw in wide.switches], lag_ratio=0.02), run_time=0.8 * s)
        self.play(wide.animate(rate_func=motion.ANTICIPATE).scale(0.05).move_to(self.items["sw108"]).set_opacity(0), run_time=0.6 * s)
        self.clear_transients()


class B_2_2(Part2Beat):
    beat_id = "2.2"

    def animate_beat(self):
        s = self.step(7)
        self.erase("sum108", style="pop", run_time=0.5)
        self.write("odometer", anim=lambda o: LaggedStart(FadeIn(o[0]), Create(o[1]), TransformFromCopy(o[0], o[2]),
                                                          lag_ratio=0.6), run_time=2 * s)
        row = self.items["sw108"]
        ball = pics.marble().next_to(row.bit(0), RIGHT, buff=0.9).shift(DOWN * 0.1)
        self.play(FadeIn(ball, shift=LEFT * 0.4), run_time=0.4 * s)
        for i in (0, 1, 2):
            self.play(ball.animate(rate_func=motion.SPRING).move_to(row.bit(i)[0].get_bottom() + DOWN * 0.25),
                      Transform(row.bit(i), pics.flipped(row.bit(i)), rate_func=motion.SPRING), run_time=0.6 * s)
        self.play(Indicate(row.bit(2), color=ORANGE, scale_factor=1.3), FadeOut(ball, scale=0.3), run_time=0.6 * s)
        self.swap("sw108", "sw107")
        self.play(Indicate(self.items["sw107"][1], color=BLUE, scale_factor=1.3), run_time=0.8 * s)


class B_2_3(Part2Beat):
    beat_id = "2.3"

    def animate_beat(self):
        s = self.step(8)
        self.erase("sw107", "odometer", style="pop", run_time=0.5)
        self.write("truth", anim=lambda t: LaggedStart(*[FadeIn(line, shift=LEFT * 0.2) for line in t], lag_ratio=0.3),
                   run_time=s)
        self.write("and_rows", anim=lambda g: LaggedStart(
            LaggedStart(*[pop_in(sw) for sw in g.rows[0].switches], lag_ratio=0.05),
            LaggedStart(*[pop_in(sw) for sw in g.rows[1].switches], lag_ratio=0.05),
            FadeIn(g.labels[0]), FadeIn(g.labels[1]), FadeIn(g.labels[2]),
            LaggedStart(*[pop_in(sw) for sw in reversed(g.rows[2].switches)], lag_ratio=0.12),
            FadeIn(g.tint_keep), FadeIn(g.tint_clear), Create(g.boundary), FadeIn(g.value, scale=1.4),
            lag_ratio=0.25), run_time=4 * s)
        g = self.items["and_rows"]
        self.play(Indicate(g.tint_keep, color=BLUE, scale_factor=1.03), run_time=s)
        self.play(Indicate(g.tint_clear, color=ORANGE, scale_factor=1.05), run_time=s)


class B_2_4(Part2Beat):
    beat_id = "2.4"

    def animate_beat(self):
        s = self.step(6)
        self.erase("truth", "and_rows", style="fall", run_time=1.0)
        pal = self.write("palette", anim=lambda p: LaggedStart(*[pop_in(t) for t in p], lag_ratio=0.08), run_time=2 * s)
        self.write("program", anim=lambda p: LaggedStart(
            TransformFromCopy(pal.names["sub"], p[0][0], path_arc=-1.2),
            TransformFromCopy(pal.names["and"], p[0][1], path_arc=-1.2),
            FadeIn(p[1], scale=2.2), lag_ratio=0.45), run_time=2 * s)
        self.play(Indicate(self.items["program"][1], color=GREEN, scale_factor=1.4), run_time=s)
