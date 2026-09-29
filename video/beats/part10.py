from __future__ import annotations

import numpy as np
from manim import (
    DOWN, RIGHT, UP, AnimationGroup, Create, FadeIn, GrowFromCenter, GrowFromEdge, Indicate, LaggedStart,
    Rotate, ORIGIN, Transform, VGroup, Wiggle, Write, config, rate_functions,
)

import boards.part10 as B
from boards.part10 import BOARD
from kit import cartoon, motion, pics, stage
from kit.beat import BeatScene
from kit.style import ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def spin(icon, turns: int = 1):
    return Rotate(icon, angle=-2 * np.pi * turns, rate_func=rate_functions.linear)


class Part10Beat(stage.StageMoves, BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_10_1(Part10Beat):
    beat_id = "10.1"

    def idle_animations(self) -> list:
        return [spin(self.items["unfinished"].spinner, 3)]

    def animate_beat(self):
        s = self.step(16)
        final = B.popcount()
        row = final.row.copy()
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.08), run_time=1.2 * s)
        drops = [pics.marble(ORANGE, 0.17).move_to(row.bit(i)) for i in B._ones(B.POPCOUNT_EXAMPLE)][::-1]
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in drops], lag_ratio=0.2), run_time=0.8 * s)
        self.play(LaggedStart(*[d.animate(rate_func=motion.DROP).move_to(t) for d, t in zip(drops, final.tally)],
                              lag_ratio=0.25), run_time=1.6 * s)
        self.play(FadeIn(final.count, scale=1.8, rate_func=motion.SPRING), run_time=0.6 * s)
        self.clear_transients()
        self.settle("popcount")
        self.write("masks", anim=lambda m: LaggedStart(*[FadeIn(r, shift=RIGHT * 0.6, rate_func=motion.SPRING) for r in m],
                                                       lag_ratio=0.35), run_time=1.6 * s)
        self.play(Indicate(self.items["masks"], color=ORANGE, scale_factor=1.06), run_time=0.8 * s)
        chart = B.rounds()
        self.play(Create(chart[0][0]), FadeIn(chart[0][1]), run_time=0.5 * s)
        for k, bar in enumerate(chart[1:]):
            body, label, examples = bar
            self.play(LaggedStart(*[pop_in(d) for d in examples], lag_ratio=0.2), run_time=0.45 * s)
            self.play(GrowFromEdge(body, DOWN, rate_func=motion.SPRING), FadeIn(label, shift=UP * 0.2), run_time=(0.6 + 0.12 * k) * s)
        self.clear_transients()
        self.settle("rounds")
        six = B.unfinished()
        self.play(LaggedStart(*[pop_in(d) for d in six[2]], lag_ratio=0.15), run_time=0.6 * s)
        self.play(Create(six.outline, rate_func=rate_functions.linear), run_time=1.8 * s)
        self.play(pop_in(six.spinner), run_time=0.4 * s)
        self.play(spin(six.spinner, 1), run_time=1.0 * s)
        self.clear_transients()
        self.settle("unfinished")
        self.write("on_record", anim=lambda f: GrowFromEdge(f, DOWN, rate_func=motion.ELASTIC), run_time=0.8 * s)


class B_10_2(Part10Beat):
    beat_id = "10.2"

    def animate_beat(self):
        s = self.step(5)
        self.erase("popcount", "masks", "rounds", "unfinished", "on_record", style="fall", run_time=1.0)
        for key in ("credit_search", "credit_cegis", "credit_wiring"):
            self.write(key, anim=lambda g: LaggedStart(pop_in(g[0]), LaggedStart(*[Write(n) for n in g[1]], lag_ratio=0.3),
                                                       lag_ratio=0.45), run_time=1.3 * s)
        self.play(spin(self.items["credit_cegis"][0][1], 1), run_time=0.9 * s)


class B_10_3(Part10Beat):
    beat_id = "10.3"

    def idle_animations(self) -> list:
        return [spin(self.items["rerun"].again, 2)]

    def animate_beat(self):
        s = self.step(11)
        self.erase("credit_search", "credit_cegis", "credit_wiring", style="swipe", run_time=1.0)
        self.write("built", anim=lambda b: LaggedStart(*[pop_in(piece) for piece in b], lag_ratio=0.6), run_time=4.0 * s)
        self.write("tests", anim=lambda t: AnimationGroup(LaggedStart(*[FadeIn(d, scale=0.2) for d in t[0]], lag_ratio=0.01),
                                                          FadeIn(t[1], scale=1.5)), run_time=1.5 * s)
        final = B.rerun()
        self.play(pop_in(final.laptop), run_time=0.7 * s)
        self.play(FadeIn(final.stamp, scale=2.5, rate_func=motion.SPRING), pop_in(final.again), run_time=0.8 * s)
        self.play(spin(final.again, 1), run_time=0.8 * s)
        self.clear_transients()
        self.settle("rerun")
        st = B.stretch()
        self.play(Create(st.box), run_time=0.8 * s)
        self.play(LaggedStart(Create(st.net), FadeIn(st.guide, shift=RIGHT * 0.2), Create(st.tree), lag_ratio=0.4),
                  run_time=1.4 * s)
        self.clear_transients()
        self.settle("stretch")


class B_10_4(Part10Beat):
    beat_id = "10.4"

    def idle_animations(self) -> list:
        anims = cartoon.desk_idle(self.items["desk"])
        arrow = self.items["link_on_screen"].down
        anims.append(arrow.animate(rate_func=motion.looped(rate_functions.there_and_back, 4)).shift(DOWN * 0.18))
        return anims

    def animate_beat(self):
        s = self.step(6)
        self.erase("built", "tests", "rerun", "stretch", style="fall", run_time=1.2)
        self.write("desk", anim=lambda m: LaggedStart(
            *[pop_in(part) for part in (m.led, m.left_monitor, m.right_monitor)],
            *[FadeIn(part, shift=DOWN * 0.4, rate_func=motion.SPRING) for part in m.submobjects[3:11]],
            FadeIn(m.hands, shift=UP * 1.2, rate_func=motion.SPRING), lag_ratio=0.1), run_time=1.8 * s)
        self.write("program_on_screen", anim=lambda p: LaggedStart(*[pop_in(t) for t in p[0]], FadeIn(p[1], shift=UP * 0.2),
                                                                   lag_ratio=0.35), run_time=1.0 * s)
        self.write("link_on_screen", anim=lambda g: LaggedStart(pop_in(g[0]), GrowFromEdge(g[1], UP), lag_ratio=0.4),
                   run_time=0.8 * s)
        self.play(Wiggle(self.items["desk"].robot), run_time=0.8 * s)


class B_10_5(Part10Beat):
    beat_id = "10.5"
    MARGIN = 1.03

    def animate_beat(self):
        on_screen = [self.items[key] for key in B.ON_SCREEN_AT_END]
        room = stage.zoomed(stage.room(lit=True)).scale(self.MARGIN, about_point=ORIGIN)
        room.cursor.set_fill(opacity=0)
        self.add(room)
        self.bring_to_back(room)
        self.play(VGroup(room, *on_screen).animate(rate_func=rate_functions.ease_out_cubic)
                  .scale(1 / (stage.ZOOM * self.MARGIN), about_point=ORIGIN).shift(stage.SCREEN_CENTER), run_time=1.8)
        self.wait(0.3)
        guy = stage.stick("run1", -8.0)
        self.add(guy)
        self.run_to(guy, -8.0, stage.GUY_X, strides=13)
        self.pull_chain(guy, room, lit_after=False)
        self.erase(*B.ON_SCREEN_AT_END, style="fade", run_time=0.3)
        self.wait(0.8)
        self.play(Transform(guy, stage.stick("bow", stage.GUY_X), rate_func=motion.SPRING), run_time=0.9)
        self.settle("room")
        self.settle("bow")
        self.clear_transients()
        self.write("thanks", anim=lambda m: GrowFromCenter(m, rate_func=motion.ELASTIC), run_time=0.7)
