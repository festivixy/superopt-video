from __future__ import annotations

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, AnimationGroup, ArcBetweenPoints, Create, FadeIn, FadeOut, GrowArrow, GrowFromCenter,
    Indicate, LaggedStart, MoveAlongPath, Rotate, Transform, TransformFromCopy, Wiggle, Write, config,
)

import boards.part7 as B
from boards.part7 import BOARD
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import BLUE, GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def slam(m):
    return FadeIn(m, scale=2.5, rate_func=motion.SPRING)


class Part7Beat(BeatScene):
    board = BOARD

    @property
    def budget(self) -> float:
        return 0.8 * self.target

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_7_1(Part7Beat):
    beat_id = "7.1"

    def animate_beat(self):
        s = self.step(11)
        self.write("question", anim=Write, run_time=1.5 * s)
        final = B.layers()
        rows = final.rows
        self.play(FadeIn(final[1], shift=DOWN * 0.2), LaggedStart(*[pop_in(r[0]) for r in rows], lag_ratio=0.25), run_time=1.3 * s)
        self.play(FadeIn(final[2], shift=DOWN * 0.2),
                  LaggedStart(*[LaggedStart(*[FadeIn(d, scale=0.3) for d in r[1]], lag_ratio=0.02) for r in rows], lag_ratio=0.3),
                  run_time=1.7 * s)
        self.play(LaggedStart(*[Indicate(d, color=ORANGE, scale_factor=2.0) for r in rows for d in r[1]], lag_ratio=0.006),
                  run_time=1.5 * s)
        self.clear_transients()
        self.settle("layers")
        t = B.timeout()
        self.play(pop_in(t.chip), run_time=0.8 * s)
        self.play(FadeIn(t.clock, scale=0.6), FadeIn(t[2]), run_time=0.5 * s)
        centre = t.clock.face.get_center()
        self.play(Rotate(t.clock.hand, -2 * np.pi, about_point=centre, rate_func=lambda x: x),
                  Indicate(t.chip.body, color=BLUE, scale_factor=1.05), run_time=2.5 * s)
        self.play(slam(t.verdict), run_time=0.8 * s)
        self.clear_transients()
        self.settle("timeout")


class B_7_2(Part7Beat):
    beat_id = "7.2"

    def animate_beat(self):
        s = self.step(11)
        self.erase("question", "layers", "timeout", style="fall", run_time=1.0)
        self.write("cegis_name", anim=Write, run_time=1.0 * s)
        g = B.loop_start()
        final = B.loop()
        self.play(pop_in(g.tray.box), LaggedStart(*[pop_in(d) for d in g.tray.dots], lag_ratio=0.2), run_time=0.8 * s)
        self.play(GrowArrow(g.arrows[0]), pop_in(g.guess), run_time=0.9 * s)
        self.play(FadeIn(g.program, shift=RIGHT * 0.4, rate_func=motion.SPRING), GrowArrow(g.arrows[1]), run_time=0.7 * s)
        self.play(GrowArrow(g.arrows[2]), pop_in(g.check), run_time=0.9 * s)
        self.play(Indicate(g.check.body, color=BLUE, scale_factor=1.08), run_time=0.8 * s)
        self.play(GrowArrow(g[8]), GrowFromCenter(g.done, rate_func=motion.ELASTIC), run_time=0.9 * s)
        self.play(Create(g.back), run_time=0.8 * s)
        start, end = g.check.body.get_bottom() + DOWN * 0.15, g.tray.get_bottom() + DOWN * 0.15
        path = ArcBetweenPoints(start, end, angle=-1.2)
        bad = pics.marble(ORANGE, 0.14).move_to(start)
        self.play(FadeIn(bad, scale=2), run_time=0.3 * s)
        self.play(MoveAlongPath(bad, path), run_time=1.3 * s)
        self.play(bad.animate(rate_func=motion.SPRING).move_to(final.tray.dots[-1]),
                  Transform(g.tray, final.tray), run_time=0.7 * s)
        self.clear_transients()
        self.settle("loop")
        loop = self.items["loop"]
        self.play(LaggedStart(*[Indicate(m, color=ORANGE, scale_factor=1.1)
                                for m in (loop.tray, loop.guess, loop.program, loop.check)], lag_ratio=0.35), run_time=1.3 * s)


class B_7_3(Part7Beat):
    beat_id = "7.3"

    def animate_beat(self):
        s = self.step(10)
        self.erase("cegis_name", "loop", style="pop", run_time=0.6)
        self.write("target", anim=lambda t: AnimationGroup(FadeIn(t[0], scale=1.5),
                                                          LaggedStart(*[pop_in(c) for c in t[1].cells], lag_ratio=0.03)),
                   run_time=1.5 * s)
        tgt = self.items["target"][1]
        self.play(LaggedStart(*[Indicate(c, color=GREEN, scale_factor=1.5) for c in tgt.cells if c.on], lag_ratio=0.08),
                  run_time=1.0 * s)
        self.write("hole", anim=lambda h: LaggedStart(pop_in(h[0]), Write(h[1][0]), Create(h[1][1]), lag_ratio=0.4),
                   run_time=1.5 * s)
        self.play(Wiggle(self.items["hole"].blank, scale_value=1.15), run_time=0.6 * s)
        row = B.round1()
        self.play(pop_in(row[0]), run_time=0.4 * s)
        self.play(pop_in(row[1]), run_time=0.5 * s)
        guess = row.const.copy().move_to(self.items["hole"].blank)
        self.play(FadeIn(guess, scale=1.4, rate_func=motion.SPRING), run_time=0.8 * s)
        self.play(Transform(guess, row.const), run_time=0.8 * s)
        self.play(LaggedStart(*[TransformFromCopy(row.const, c) for c in row.strip.cells], lag_ratio=0.02), run_time=1.2 * s)
        self.play(LaggedStart(*[GrowFromCenter(r, rate_func=motion.ELASTIC) for r in row.rings], lag_ratio=0.1), run_time=1.0 * s)
        self.clear_transients()
        self.settle("round1")


class B_7_4(Part7Beat):
    beat_id = "7.4"

    def animate_beat(self):
        s = self.step(12)
        r1 = self.items["round1"]
        row2 = B.round2()
        self.play(pop_in(row2[0]), run_time=0.4 * s)
        bad = row2[1][0].copy().move_to(r1.rings[0])
        self.play(FadeIn(bad, scale=2.5), run_time=0.3 * s)
        self.play(bad.animate(rate_func=motion.SPRING).move_to(row2[1][0]), FadeIn(row2[1][1], shift=RIGHT * 0.3), run_time=0.8 * s)
        self.play(FadeIn(row2.const, shift=DOWN * 0.3), run_time=0.7 * s)
        self.play(LaggedStart(*[TransformFromCopy(row2.const, c) for c in row2.strip.cells], lag_ratio=0.02), run_time=1.0 * s)
        self.play(GrowFromCenter(row2.rings, rate_func=motion.ELASTIC), run_time=0.6 * s)
        self.clear_transients()
        self.settle("round2")
        row3 = B.round3()
        one = B.strip32(B.COUNTEREXAMPLES[1], B.ROW_Y[2] + 0.9, ORANGE)
        self.play(LaggedStart(*[pop_in(c) for c in one.cells], lag_ratio=0.01), run_time=0.7 * s)
        self.play(one.animate(rate_func=motion.DROP).move_to(self.items["round2"].strip), run_time=0.7 * s)
        self.play(Indicate(self.items["round2"].rings, color=ORANGE, scale_factor=1.6), run_time=0.5 * s)
        self.play(FadeOut(one), pop_in(row3[0]), pop_in(row3[1]), run_time=0.8 * s)
        self.play(FadeIn(row3.const, shift=DOWN * 0.3), run_time=0.7 * s)
        self.play(LaggedStart(*[TransformFromCopy(row3.const, c) for c in row3.strip.cells], lag_ratio=0.02), run_time=1.0 * s)
        self.play(GrowFromCenter(row3[-1], rate_func=motion.ELASTIC), run_time=0.6 * s)
        self.clear_transients()
        self.settle("round3")
        summ = B.summary()
        sources = [self.items["round1"][1][0], self.items["round2"][1][0], self.items["round3"][1][0]]
        self.play(*[TransformFromCopy(src, d) for src, d in zip(sources, summ[0][0])], run_time=1.0 * s)
        self.play(Write(summ[0][1]), run_time=0.8 * s)
        self.play(slam(summ[1]), run_time=0.8 * s)
        self.clear_transients()
        self.settle("summary")


class B_7_5(Part7Beat):
    beat_id = "7.5"

    def animate_beat(self):
        s = self.step(7)
        self.erase("hole", "target", "round1", "round2", "round3", "summary", style="swipe", run_time=1.0)
        final = B.field()
        grid = B.field_at(0)
        self.play(FadeIn(final.count, shift=DOWN * 0.2),
                  LaggedStart(*[FadeIn(d, scale=0.3) for d in grid], lag_ratio=0.002), run_time=1.2 * s)
        for k in range(3):
            ex = final.examples[k].copy()
            self.play(pop_in(ex), run_time=0.3 * s)
            self.play(Transform(grid, B.field_at(k + 1)), Indicate(ex, scale_factor=1.6), run_time=0.9 * s)
        self.play(Transform(grid, final.grid, rate_func=motion.SPRING), GrowFromCenter(final.ring, rate_func=motion.ELASTIC),
                  run_time=0.8 * s)
        self.clear_transients()
        self.settle("field")


class B_7_6(Part7Beat):
    beat_id = "7.6"

    def animate_beat(self):
        s = self.step(9)
        self.erase("field", style="pop", run_time=0.6)
        b = B.brute()
        self.play(Create(b.bar), FadeIn(b[2]), FadeIn(b[3]), FadeIn(b[6], shift=DOWN * 0.2), run_time=1.0 * s)
        counter = style.mono(B.hexs(0), 34, BLUE).next_to(b.bar, UP, buff=0.3).align_to(b.bar, LEFT)
        self.play(FadeIn(counter), FadeIn(b.fill), run_time=0.3 * s)
        for k in range(1, 9):
            self.play(Transform(counter, style.mono(B.hexs(k), 34, BLUE).move_to(counter)), run_time=0.17 * s)
        self.play(FadeOut(counter), Create(b.marker), FadeIn(b.answer, shift=DOWN * 0.2), run_time=0.8 * s)
        self.play(Indicate(b.answer, color=ORANGE, scale_factor=1.2), run_time=0.6 * s)
        self.clear_transients()
        self.settle("brute")
        sv = B.solve()
        self.play(Write(sv.eq), run_time=1.0 * s)
        self.play(Indicate(sv.eq[0][-1], color=ORANGE, scale_factor=1.8), run_time=0.6 * s)
        self.play(pop_in(sv.chip), run_time=0.6 * s)
        self.play(Indicate(sv.chip, color=BLUE, scale_factor=1.08), run_time=0.6 * s)
        self.play(FadeIn(sv.value[0]), TransformFromCopy(self.items["brute"].answer, sv.value[1]), run_time=1.0 * s)
        self.clear_transients()
        self.settle("solve")


class B_7_7(Part7Beat):
    beat_id = "7.7"

    def animate_beat(self):
        s = self.step(10)
        self.erase("brute", "solve", style="fall", run_time=1.0)
        self.write("paper2010", anim=lambda p: LaggedStart(FadeIn(p[0], shift=DOWN * 0.3), pop_in(p[1]),
                                                            LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in p[2]], lag_ratio=0.3),
                                                            lag_ratio=0.3), run_time=1.5 * s)
        self.write("bag", anim=lambda g: AnimationGroup(Create(g[0]), LaggedStart(*[pop_in(t) for t in g.tiles], lag_ratio=0.4)),
                   run_time=1.2 * s)
        self.play(Wiggle(self.items["bag"], scale_value=1.08), run_time=0.6 * s)
        self.write("lines", anim=lambda g: AnimationGroup(LaggedStart(*[pop_in(r) for r in g[0]], lag_ratio=0.3),
                                                          FadeIn(g.x, shift=DOWN * 0.6, rate_func=motion.SPRING)), run_time=1.8 * s)
        u = B.unknowns()
        tiles = self.items["bag"].tiles
        self.play(*[TransformFromCopy(t, ins.tile, path_arc=-0.8) for t, ins in zip(tiles, u)], run_time=1.2 * s)
        self.play(LaggedStart(*[pop_in(ins.out_port) for ins in u], lag_ratio=0.3), run_time=0.7 * s)
        self.play(LaggedStart(*[pop_in(p) for ins in u for p in ins.in_ports], lag_ratio=0.25), run_time=0.8 * s)
        self.play(*[FadeIn(m) for ins in u for m in ins[3:]], run_time=0.4 * s)
        self.clear_transients()
        self.settle("unknowns")
        un = self.items["unknowns"]
        self.play(*[Indicate(ins.out_port, color=ORANGE, scale_factor=1.5) for ins in un], run_time=0.7 * s)
        self.play(*[Indicate(ins.in_ports, color=ORANGE, scale_factor=1.3) for ins in un], run_time=0.7 * s)


class B_7_8(Part7Beat):
    beat_id = "7.8"

    def animate_beat(self):
        s = self.step(13)
        self.erase("paper2010", "bag", style="pop", run_time=0.6)
        rules = B.rules()
        ls = self.items["lines"]
        self.play(Write(rules[0]), run_time=0.8 * s)
        loop = ArcBetweenPoints(ls.slots[2].get_right() + RIGHT * 0.1, ls.slots[1].get_right() + RIGHT * 0.1, angle=1.6)
        loop.set_stroke(ORANGE, 3)
        cross = pics.x_mark(0.4).move_to(loop)
        self.play(Create(loop), run_time=0.5 * s)
        self.play(GrowFromCenter(cross, rate_func=motion.ELASTIC), run_time=0.5 * s)
        self.play(FadeOut(loop), FadeOut(cross), run_time=0.3 * s)
        self.play(Write(rules[1]), run_time=0.8 * s)
        self.play(*[Indicate(ins.out_port, color=ORANGE, scale_factor=1.5) for ins in self.items["unknowns"]], run_time=0.5 * s)
        self.play(Write(rules[2]), run_time=0.8 * s)
        self.play(Indicate(ls.slots[2], color=GREEN, scale_factor=1.08), run_time=0.5 * s)
        self.play(Write(rules[3]), run_time=0.8 * s)
        self.clear_transients()
        self.settle("rules")
        w = B.wired()
        un = self.items["unknowns"]
        self.play(Transform(un[0], w.neg, path_arc=0.6), Transform(un[1], w.band, path_arc=0.6), run_time=1.5 * s)
        self.play(LaggedStart(*[Create(a) for a in w.reads], lag_ratio=0.3), run_time=1.2 * s)
        self.play(GrowArrow(w.answer), run_time=0.5 * s)
        marbles = [pics.marble(BLUE, 0.1).move_to(a.get_start()) for a in w.reads]
        self.play(LaggedStart(*[MoveAlongPath(m, a) for m, a in zip(marbles, w.reads)], lag_ratio=0.3), run_time=1.0 * s)
        self.clear_transients()
        self.settle("wired")
        self.erase("unknowns", style="fade", run_time=1 / config.frame_rate)
        self.write("found", anim=lambda f: AnimationGroup(Write(f[0]), FadeIn(f[1], shift=UP * 0.2)), run_time=1.4 * s)
        self.play(Indicate(self.items["found"][0], color=GREEN, scale_factor=1.1), run_time=0.7 * s)
