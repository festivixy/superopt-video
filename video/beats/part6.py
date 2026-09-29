from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, AnimationGroup, Create, FadeIn, FadeOut, GrowFromCenter, GrowFromEdge, Indicate,
    LaggedStart, Transform, TransformFromCopy, Wiggle, Write, config,
)

import boards.part6 as B
from boards.part6 import BOARD
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import DIM, GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def slam(m):
    return FadeIn(m, scale=2.5, rate_func=motion.SPRING)


class Part6Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)

    def flip(self, switch, run_time: float) -> None:
        self.play(Transform(switch, pics.flipped(switch), rate_func=motion.SPRING), run_time=run_time)
        switch.on = not switch.on


class B_6_1(Part6Beat):
    beat_id = "6.1"

    def animate_beat(self):
        s = self.step(10)
        self.write("halves", anim=lambda g: LaggedStart(pop_in(g[0]), FadeIn(g[1], scale=1.5), slam(g[2]), lag_ratio=0.45),
                   run_time=1.6 * s)
        row = B.eight_row(0)
        final = B.eight()
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.08), run_time=0.9 * s)
        self.play(Write(final[1]), run_time=0.9 * s)
        grid = B._grid256()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in grid], lag_ratio=0.003), run_time=0.9 * s)
        candidate = self.items["halves"][0][0][2].copy()
        self.play(candidate.animate(rate_func=motion.SPRING).scale(1.6).next_to(grid, UP, buff=0.25), run_time=0.7 * s)
        lit = B.all256()
        for r in range(16):
            value = min(16 * (r + 1), B.EIGHT_BIT_INPUTS) - 1
            self.play(Transform(row, B.eight_row(value)),
                      *[Transform(grid[16 * r + c], lit[16 * r + c]) for c in range(16)], run_time=3.2 * s / 16)
        self.play(Indicate(self.items["halves"][2], color=GREEN, scale_factor=1.12), FadeOut(candidate), run_time=0.8 * s)
        self.settle("eight")
        self.settle("all256")
        self.clear_transients()


class B_6_2(Part6Beat):
    beat_id = "6.2"

    def animate_beat(self):
        s = self.step(8)
        self.erase("halves", "eight", "all256", style="pop", run_time=0.6)
        self.write("book_date", anim=lambda g: LaggedStart(FadeIn(g[0], shift=DOWN * 0.3), pop_in(g[1]), lag_ratio=0.4),
                   run_time=1.3 * s)
        final = B.job()
        x = final.x.copy()
        self.play(LaggedStart(*[pop_in(sw) for sw in x.switches], lag_ratio=0.08), run_time=1.0 * s)
        self.play(Create(final[1][0]), TransformFromCopy(x, final.trick), run_time=1.3 * s)
        self.play(Write(final[4]), run_time=0.8 * s)
        self.play(Create(final[1][1]), TransformFromCopy(x, final.keep), run_time=1.3 * s)
        self.play(Create(final[6]), GrowFromCenter(final[5], rate_func=motion.ELASTIC), run_time=1.0 * s)
        self.settle("job")
        self.clear_transients()


class B_6_3(Part6Beat):
    beat_id = "6.3"

    def animate_beat(self):
        s = self.step(7)
        self.erase("book_date", "job", style="fall", run_time=1.0)
        final = B.ones()
        self.play(FadeIn(final[0], scale=1.5), LaggedStart(*[pop_in(t) for t in final[1]], lag_ratio=0.08), run_time=1.3 * s)
        self.play(LaggedStart(*[GrowFromCenter(m) for m in final[2]], lag_ratio=0.12), run_time=1.4 * s)
        self.play(FadeIn(final[3], scale=1.6, rate_func=motion.SPRING), run_time=0.4 * s)
        self.settle("ones")
        self.clear_transients()
        self.write("found", anim=lambda g: LaggedStart(FadeIn(g[0], scale=1.5), LaggedStart(*[pop_in(t) for t in g[1]], lag_ratio=0.4),
                                                        Write(g[2]), lag_ratio=0.35), run_time=2.2 * s)
        self.play(Indicate(self.items["found"][2], color=GREEN, scale_factor=1.12), run_time=0.8 * s)


class B_6_4(Part6Beat):
    beat_id = "6.4"

    def animate_beat(self):
        s = self.step(11)
        self.erase("ones", style="pop", run_time=0.6)
        self.write("x_row", anim=lambda g: LaggedStart(FadeIn(g[0]), LaggedStart(*[pop_in(w) for w in g.row.switches], lag_ratio=0.08),
                                                        FadeIn(g[2]), lag_ratio=0.3), run_time=1.5 * s)
        work = B.carry_row()
        self.play(TransformFromCopy(self.items["x_row"][0], work[0]),
                  TransformFromCopy(self.items["x_row"].row, work.row, path_arc=-0.4), run_time=1.2 * s)
        self.play(LaggedStart(*[Transform(w, pics.flipped(w), rate_func=motion.SPRING) for w in work.row.switches], lag_ratio=0.12),
                  Transform(work[0], B.flip_row()[0]), run_time=2.4 * s)
        for w in work.row.switches:
            w.on = not w.on
        plus = style.math("+1", 56, ORANGE).next_to(work.row, RIGHT, buff=0.6)
        self.play(FadeIn(plus, shift=LEFT * 0.3), run_time=0.6 * s)
        carry = pics.marble(ORANGE, 0.16).next_to(work.row.bit(0), UP, buff=0.15)
        self.play(FadeIn(carry, scale=0.3), run_time=0.4 * s)
        for i in range(B.LOWEST_BIT + 1):
            self.play(carry.animate(rate_func=motion.SPRING).next_to(work.row.bit(i), UP, buff=0.15), run_time=0.5 * s)
            self.flip(work.row.bit(i), run_time=0.7 * s)
        self.play(FadeOut(carry, scale=0.3), FadeOut(plus), run_time=0.5 * s)
        final = B.neg_row()
        self.play(Transform(work[0], final[0]), FadeIn(final[2], shift=LEFT * 0.3), run_time=0.9 * s)
        self.settle("neg_row")
        self.clear_transients()
        self.play(Indicate(self.items["neg_row"].row, color=ORANGE, scale_factor=1.05), run_time=0.8 * s)


class B_6_5(Part6Beat):
    beat_id = "6.5"

    def animate_beat(self):
        s = self.step(10)
        final = B.and_row()
        result, rule, frame = final
        self.play(Create(rule), FadeIn(result[0], scale=1.5), run_time=0.8 * s)
        high = range(7, B.LOWEST_BIT, -1)
        low = range(B.LOWEST_BIT - 1, -1, -1)
        for i in high:
            box = B.column_box(i, ORANGE)
            self.play(Create(box), pop_in(result.row.bit(i)), run_time=0.55 * s)
            self.play(FadeOut(box), run_time=0.15 * s)
        box = B.column_box(B.LOWEST_BIT, GREEN)
        self.play(Create(box), run_time=0.6 * s)
        self.play(pop_in(result.row.bit(B.LOWEST_BIT)), run_time=0.8 * s)
        self.play(FadeOut(box), run_time=0.2 * s)
        for i in low:
            box = B.column_box(i, DIM)
            self.play(Create(box), pop_in(result.row.bit(i)), run_time=0.5 * s)
            self.play(FadeOut(box), run_time=0.15 * s)
        self.play(FadeIn(result[2], shift=LEFT * 0.3), Create(frame), run_time=1.0 * s)
        self.settle("and_row")
        self.clear_transients()
        self.play(Indicate(self.items["found"][0], color=GREEN, scale_factor=1.4), run_time=0.6 * s)
        self.write("minimum", anim=lambda g: AnimationGroup(pop_in(g[0]), GrowFromCenter(g[1], rate_func=motion.ELASTIC)),
                   run_time=0.8 * s)


class B_6_6(Part6Beat):
    beat_id = "6.6"

    def animate_beat(self):
        s = self.step(10)
        self.erase("found", "x_row", "neg_row", "and_row", "minimum", style="fall", run_time=1.0)
        self.write("counts", anim=lambda g: LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN, rate_func=motion.SPRING),
                                                                         FadeIn(b[2]), FadeIn(b[1], shift=DOWN * 0.2))
                                                          for b in g], lag_ratio=0.6), run_time=3.6 * s)
        self.write("constant", anim=lambda g: LaggedStart(pop_in(g[1]), GrowFromEdge(g[0], DOWN), Write(g[2]), lag_ratio=0.45),
                   run_time=2.4 * s)
        final = B.wall()
        bricks, glass = final
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.8, rate_func=motion.DROP) for b in bricks], lag_ratio=0.03),
                  run_time=1.6 * s)
        walker = glass.copy().move_to([-6.4, -3.4, 0])
        self.play(FadeIn(walker, scale=0.5), run_time=0.3 * s)
        self.play(walker.animate(rate_func=motion.ANTICIPATE).move_to(glass), run_time=1.2 * s)
        self.play(Wiggle(walker, scale_value=1.2), run_time=0.8 * s)
        self.settle("wall")
        self.clear_transients()
