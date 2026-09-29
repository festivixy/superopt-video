from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, TAU, UP, AnimationGroup, Create, FadeIn, FadeOut, GrowArrow, GrowFromCenter, Indicate,
    LaggedStart, Rotate, Succession, Transform, TransformFromCopy, Wiggle, Write, config,
)

import boards.part8 as B
from boards.part8 import BOARD
from kit import motion, pics
from kit.beat import BeatScene
from kit.style import BLUE, DIM, GREEN, INK, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def slam(m):
    return FadeIn(m, scale=2.5, rate_func=motion.SPRING)


class Part8Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)

    def replace(self, old: str, new: str, build, run_time: float) -> None:
        self.play(Transform(self.items[old], build(), rate_func=motion.SPRING), run_time=run_time)
        self.swap(old, new)


class B_8_1(Part8Beat):
    beat_id = "8.1"

    def animate_beat(self):
        s = self.step(12)
        p = B.lane_proof()
        self.play(LaggedStart(*[pop_in(t) for t in p.strip], lag_ratio=0.3), run_time=0.6 * s)
        self.play(GrowArrow(p.arrows[0]), TransformFromCopy(p.strip, p.formula), run_time=1.0 * s)
        self.play(GrowArrow(p.arrows[1]), pop_in(p.chip), run_time=0.8 * s)
        self.play(GrowArrow(p.arrows[2]), GrowFromCenter(p.ok, rate_func=motion.ELASTIC), run_time=0.6 * s)
        self.clear_transients()
        self.settle("lane_proof")
        lane = self.items["lane_proof"]
        critter = pics.bug(0.7).next_to(lane.arrows[0], UP, buff=0.15)
        self.play(FadeIn(critter, shift=RIGHT * 0.6, rate_func=motion.SPRING), run_time=0.5 * s)
        self.play(Indicate(lane.formula, color=ORANGE, scale_factor=1.1), run_time=0.6 * s)
        self.play(Indicate(lane.ok, color=GREEN, scale_factor=1.5), run_time=0.6 * s)
        self.play(FadeOut(critter, shift=RIGHT * 0.6), run_time=0.3 * s)
        f = B.lane_fuzz()
        self.play(TransformFromCopy(lane.strip, f.strip, path_arc=0.6), run_time=0.8 * s)
        self.play(GrowArrow(f.arrows[0]), pop_in(f.machine), run_time=0.8 * s)
        rain = [pics.marble(BLUE, 0.07).move_to(f.machine.inlet.get_center() + DOWN * (1.2 + 0.12 * k) + LEFT * 0.3 * (k % 3))
                for k in range(12)]
        self.play(Write(f.count), LaggedStart(*[r.animate(rate_func=motion.SPRING).move_to(f.machine.inlet).set_opacity(0)
                                                for r in rain], lag_ratio=0.12), run_time=1.6 * s)
        self.play(GrowArrow(f.arrows[1]), pop_in(f.original), run_time=0.8 * s)
        self.play(GrowArrow(f.arrows[2]), GrowFromCenter(f.ok, rate_func=motion.ELASTIC), run_time=0.6 * s)
        self.clear_transients()
        self.settle("lane_fuzz")
        self.write("both", anim=lambda g: Succession(GrowFromCenter(g[0]), GrowFromCenter(g[1], rate_func=motion.ELASTIC)),
                   run_time=1.2 * s)


class B_8_2(Part8Beat):
    beat_id = "8.2"

    def shift_row(self, row, key: str, sign_copy: bool, run_time: float) -> None:
        start = B.shift_strip(B.BEFORE, key)
        self.play(pop_in(row.name), LaggedStart(*[pop_in(c) for c in start.cells], lag_ratio=0.06), run_time=0.35 * run_time)
        pitch = B.CELL + 0.03
        self.play(*[c.animate(rate_func=motion.SPRING).shift(RIGHT * pitch) for c in start.cells[:-1]],
                  FadeOut(start.cells[-1], shift=DOWN * 0.8 + RIGHT * pitch), run_time=0.35 * run_time)
        incoming = row.strip.cells[0].copy()
        if sign_copy:
            self.play(TransformFromCopy(start.cells[0], incoming, path_arc=-2.2), run_time=0.3 * run_time)
        else:
            self.play(GrowFromCenter(incoming, rate_func=motion.ELASTIC), run_time=0.3 * run_time)

    def animate_beat(self):
        s = self.step(12)
        self.erase("lane_proof", "lane_fuzz", "both", style="fall", run_time=1.0)
        rows = B.shifts()
        self.shift_row(rows[0], "lshr", sign_copy=False, run_time=2.7 * s)
        self.shift_row(rows[1], "ashr", sign_copy=True, run_time=2.7 * s)
        self.play(LaggedStart(*[FadeIn(r.spelling, shift=LEFT * 0.4) for r in rows], lag_ratio=0.5), run_time=0.8 * s)
        self.play(Indicate(rows[1].spelling, color=ORANGE, scale_factor=1.25), run_time=0.6 * s)
        self.clear_transients()
        self.settle("shifts")
        self.write("trap", anim=lambda g: LaggedStart(*[pop_in(m) for m in g], lag_ratio=0.35), run_time=1.5 * s)
        self.play(Indicate(self.items["trap"][3], color=GREEN, scale_factor=1.5), run_time=0.6 * s)
        self.write("fuzz_catch", anim=lambda g: Succession(FadeIn(g[0], shift=RIGHT * 0.3), pop_in(g[1]),
                                                             GrowFromCenter(g[2], rate_func=motion.ELASTIC)), run_time=1.8 * s)


class B_8_3(Part8Beat):
    beat_id = "8.3"

    def animate_beat(self):
        s = self.step(7)
        self.erase("shifts", "trap", "fuzz_catch", style="swipe", run_time=1.2)
        r = B.min_run()
        self.play(pop_in(r.machine), run_time=0.8 * s)
        self.play(FadeIn(r.ins, shift=RIGHT * 0.3), run_time=0.6 * s)
        riders = r.ins.copy()
        self.play(riders.animate(rate_func=motion.ANTICIPATE).move_to(r.machine.inlet).scale(0.3).set_opacity(0), run_time=0.6 * s)
        self.play(FadeIn(r.got, shift=RIGHT * 0.5, rate_func=motion.SPRING), run_time=0.6 * s)
        self.play(FadeIn(r.want, shift=LEFT * 0.3), run_time=0.6 * s)
        self.clear_transients()
        self.settle("min_run")
        self.play(Indicate(self.items["min_run"].got, color=ORANGE, scale_factor=1.5), run_time=0.6 * s)
        self.write("no_compare", anim=lambda g: Succession(LaggedStart(*[pop_in(t) for t in g[0]], lag_ratio=0.08),
                                                             FadeIn(g[1], scale=1.3), GrowFromCenter(g[2], rate_func=motion.ELASTIC)),
                   run_time=2.1 * s)
        self.write("rejected", anim=slam, run_time=0.8 * s)


class B_8_4(Part8Beat):
    beat_id = "8.4"

    def animate_beat(self):
        s = self.step(10)
        self.erase("min_run", "no_compare", "rejected", style="fall", run_time=1.0)
        rows = B.suite()
        for row in rows:
            row[0].set_color(DIM)
            row[2].set_opacity(0)
        self.play(LaggedStart(*[pop_in(r) for r in rows], lag_ratio=0.1), run_time=1.0 * s)
        self.write("floor", anim=lambda g: Succession(Write(g[0]), LaggedStart(*[pop_in(t) for t in g[1]], lag_ratio=0.4)),
                   run_time=1.5 * s)
        self.write("bags1", anim=lambda g: Succession(LaggedStart(*[pop_in(b) for b in g.row], lag_ratio=0.12),
                                                        FadeIn(g.count, scale=1.5),
                                                        LaggedStart(*[GrowFromCenter(t) for t in g.ticks], lag_ratio=0.12)),
                   run_time=2.5 * s)
        final = B.bags2()
        start = B.bags2()
        for b in start.grid:
            b[0].set_stroke(INK)
        self.play(LaggedStart(*[pop_in(b) for b in start.grid], lag_ratio=0.02), FadeIn(start.count, scale=1.5), run_time=1.5 * s)
        self.play(LaggedStart(*[Transform(b[0], f[0]) for b, f in zip(start.grid, final.grid)], lag_ratio=0.02), run_time=1.3 * s)
        self.clear_transients()
        self.add(rows)
        self.settle("bags2")
        done = B.suite()
        self.play(LaggedStart(*[Transform(r, d) for r, d in zip(rows, done)], lag_ratio=0.15), run_time=1.2 * s)
        self.clear_transients()
        self.settle("suite")


class B_8_5(Part8Beat):
    beat_id = "8.5"

    def animate_beat(self):
        s = self.step(6)
        self.erase("floor", "bags1", "bags2", "suite", style="pop", run_time=0.6)
        self.write("space8", anim=lambda g: LaggedStart(*[FadeIn(d, scale=0.3) for d in g], lag_ratio=0.003), run_time=1.2 * s)
        self.play(LaggedStart(*[Indicate(d, color=BLUE, scale_factor=1.8) for d in self.items["space8"]], lag_ratio=0.003),
                  run_time=1.2 * s)
        final = B.watch()
        w = B.stopwatch(0.0, r=1.3).move_to(final.watch)
        self.play(pop_in(w), run_time=0.8 * s)
        self.play(Rotate(w.hand, angle=-TAU * 0.015, about_point=w.face.get_center()), run_time=0.6 * s)
        self.play(slam(final.readout), run_time=0.6 * s)
        self.clear_transients()
        self.settle("watch")
        self.play(Wiggle(self.items["watch"].readout, scale_value=1.3), run_time=0.8 * s)


class B_8_6(Part8Beat):
    beat_id = "8.6"

    def animate_beat(self):
        s = self.step(9)
        self.erase("space8", "watch", style="fall", run_time=1.0)
        self.write("lines", anim=lambda g: Succession(LaggedStart(*[pop_in(t) for t in g.row], lag_ratio=0.2),
                                                        LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in g.codes], lag_ratio=0.2)),
                   run_time=2.2 * s)
        self.write("rule4", anim=Write, run_time=1.0 * s)
        self.play(Indicate(self.items["rule4"], color=BLUE, scale_factor=1.15), run_time=0.6 * s)
        four_m, link, strip = B.four_start()
        self.play(FadeIn(four_m, scale=1.5), run_time=0.5 * s)
        self.play(GrowArrow(link), LaggedStart(*[pop_in(c) for c in strip.cells], lag_ratio=0.25), run_time=1.0 * s)
        self.play(Indicate(strip, color=BLUE, scale_factor=1.08), run_time=0.5 * s)
        final = B.four()
        self.play(Create(final.frame), run_time=0.8 * s)
        self.play(Transform(strip.cells[0], final.fallen, rate_func=motion.DROP), run_time=1.0 * s)
        self.play(slam(final.zero), run_time=0.6 * s)
        self.clear_transients()
        self.settle("four")


class B_8_7(Part8Beat):
    beat_id = "8.7"

    def animate_beat(self):
        s = self.step(8)
        self.replace("rule4", "wrong_rule", B.wrong_rule, run_time=0.8 * s)
        line = B.empty_line()
        self.play(Create(line[0]), LaggedStart(*[FadeIn(n) for n in line[1]], lag_ratio=0.15), run_time=0.8 * s)
        seeker = pics.pointer(ORANGE).next_to(line[0].n2p(4), UP, buff=0.1)
        self.play(FadeIn(seeker), run_time=0.2 * s)
        self.play(seeker.animate(rate_func=motion.SPRING).next_to(line[2], UP, buff=0.1), FadeIn(line[2]), run_time=0.8 * s)
        self.play(GrowFromCenter(line[3], rate_func=motion.ELASTIC), FadeOut(seeker), run_time=0.5 * s)
        self.clear_transients()
        self.settle("empty_line")
        self.write("unsat8", anim=slam, run_time=0.6 * s)
        self.play(Indicate(self.items["wrong_rule"], color=ORANGE, scale_factor=1.25), run_time=0.6 * s)
        self.erase("unsat8", style="pop", run_time=0.4 * s)
        self.replace("four", "fix", B.fix, run_time=1.2 * s)
        self.replace("wrong_rule", "rule_fixed", B.rule_fixed, run_time=0.8 * s)


class B_8_8(Part8Beat):
    beat_id = "8.8"

    def animate_beat(self):
        s = self.step(10)
        self.erase("lines", "rule_fixed", "empty_line", "fix", style="fall", run_time=1.0)
        self.write("expect", anim=lambda g: Succession(FadeIn(g[0]), FadeIn(g[1]), slam(g[2]),
                                                         GrowFromCenter(g[3], rate_func=motion.ELASTIC)), run_time=2.0 * s)
        self.write("setup4", anim=lambda g: Succession(LaggedStart(*[pop_in(t) for t in g[0]], lag_ratio=0.2), FadeIn(g[1], scale=1.6)),
                   run_time=1.2 * s)
        self.play(Indicate(self.items["setup4"][1], color=ORANGE, scale_factor=1.6), run_time=0.5 * s)
        self.write("floors3", anim=lambda g: Succession(LaggedStart(*[AnimationGroup(pop_in(c[0]), pop_in(c[1])) for c in g], lag_ratio=0.3),
                                                          LaggedStart(*[FadeIn(c[2], shift=RIGHT * 0.5) for c in g], lag_ratio=0.3)),
                   run_time=1.8 * s)
        miss = pics.x_mark(0.5).next_to(self.items["setup4"][1], RIGHT, buff=0.25)
        self.play(GrowFromCenter(miss, rate_func=motion.ELASTIC), run_time=0.4 * s)
        final = B.bumped()
        down = B.arrow(self.items["setup4"][0].get_bottom(), final[0].get_top())
        self.play(GrowArrow(down), run_time=0.4 * s)
        self.write("bumped", anim=lambda g: Succession(LaggedStart(*[pop_in(t) for t in g[0]], lag_ratio=0.15),
                                                         FadeIn(g[1], scale=1.5), FadeIn(g[2])), run_time=1.4 * s)
        self.play(FadeOut(miss), FadeOut(down), run_time=0.4 * s)


class B_8_9(Part8Beat):
    beat_id = "8.9"

    def animate_beat(self):
        s = self.step(7)
        self.erase("expect", "setup4", "floors3", "bumped", style="swipe", run_time=1.2)
        self.write("all_no", anim=lambda g: LaggedStart(*[slam(st) for st in g], lag_ratio=0.08), run_time=2.0 * s)
        self.write("regression", anim=lambda g: Succession(LaggedStart(*[pop_in(t) for t in g.row], lag_ratio=0.2), GrowArrow(g.link),
                                                             Write(g.program), GrowFromCenter(g.ok, rate_func=motion.ELASTIC)),
                   run_time=3.0 * s)
        self.play(Indicate(self.items["regression"].program, color=GREEN, scale_factor=1.15), run_time=0.6 * s)


class B_8_10(Part8Beat):
    beat_id = "8.10"

    def animate_beat(self):
        s = self.step(9)
        self.erase("all_no", "regression", style="pop", run_time=0.6)
        final = B.watches()
        self.play(pop_in(final.old[0]), run_time=0.6 * s)
        self.play(GrowFromCenter(final.old[1], rate_func=motion.ELASTIC), run_time=0.4 * s)
        new, checked = final.new.copy(), final.checked.copy()
        for d in checked:
            d.set_color(BLUE)
        self.play(pop_in(new), LaggedStart(*[FadeIn(d, scale=0.3) for d in checked], lag_ratio=0.005), run_time=0.8 * s)
        self.play(Rotate(new.hand, angle=-TAU * 3, about_point=new.face.get_center()),
                  LaggedStart(*[d.animate.set_color(DIM) for d in checked], lag_ratio=0.01), run_time=2.5 * s)
        self.clear_transients()
        self.settle("watches")
        self.write("held", anim=lambda g: LaggedStart(*[Succession(AnimationGroup(pop_in(c[0]), pop_in(c[1])),
                                                                   GrowFromCenter(c[2], rate_func=motion.ELASTIC)) for c in g],
                                                      lag_ratio=0.35), run_time=1.6 * s)
        self.write("habit", anim=lambda g: Succession(AnimationGroup(pop_in(g[0]), slam(g[1])),
                                                        FadeIn(g[2], shift=LEFT * 1.2, rate_func=motion.SPRING)), run_time=1.6 * s)
