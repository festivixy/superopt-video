from __future__ import annotations

from manim import (
    DOWN, RIGHT, UP, AnimationGroup, Create, FadeIn, FadeOut, GrowFromCenter, Indicate, LaggedStart,
    ReplacementTransform, Rotate, Succession, Transform, VGroup, Wiggle, Write, config, rate_functions,
)

import boards.intro as B
from boards.intro import BOARD
from kit import cartoon, motion, pics, stage, style
from kit.beat import BeatScene
from kit.style import BLUE, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def one_frame() -> float:
    return 1 / config.frame_rate


class IntroBeat(stage.StageMoves, BeatScene):
    board = BOARD

    def idle_animations(self) -> list:
        anims = cartoon.desk_idle(self.items["desk"]) if "desk" in self.items else []
        if "game" in self.items:
            runner = self.items["game"].runner
            anims.append(runner.animate(rate_func=motion.looped(rate_functions.there_and_back, 4)).shift(UP * 0.35))
        return anims

    def taps(self, cycles: int) -> list:
        hands = self.items["desk"].hands
        return [Rotate(h, angle=0.07 if i == 0 else -0.07, about_point=h.shoulder,
                       rate_func=motion.looped(rate_functions.there_and_back, cycles + i))
                for i, h in enumerate(hands)]

    def type_bars(self, bars, run_time: float) -> None:
        total = sum(bar.get_length() for bar in bars)
        typing = [Create(bar, rate_func=rate_functions.linear, run_time=run_time * bar.get_length() / total) for bar in bars]
        self.play(Succession(*typing), *self.taps(max(2, int(run_time * 3))), run_time=run_time)

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=one_frame())


class B_I_0(IntroBeat):
    beat_id = "I.0"
    ZOOM_TIME = 1.4
    FADE_TIME = 0.35

    def animate_beat(self):
        room = self.write("room", anim=lambda r: LaggedStart(*[Create(part) for part in r], lag_ratio=0.2), run_time=1.8)
        guy = stage.stick("run1", -8.0)
        self.add(guy)
        self.run_to(guy, -8.0, stage.GUY_X, strides=13)
        self.pull_chain(guy, room, lit_after=True)
        self.play(room.screen.animate(rate_func=rate_functions.there_and_back).set_fill(BLUE, 0.6), run_time=0.25)
        self.play(Transform(room.monitor, stage.room(lit=True).monitor), run_time=0.3)
        self.wait(max(0.2, self.target - self.elapsed - self.ZOOM_TIME - self.FADE_TIME - 0.1))
        self.play(VGroup(room, guy).animate(rate_func=rate_functions.ease_in_cubic)
                  .scale(stage.ZOOM * 1.03, about_point=stage.SCREEN_CENTER).shift(-stage.SCREEN_CENTER),
                  run_time=self.ZOOM_TIME)
        self.clear_transients()
        self.erase("room", style="fade", run_time=self.FADE_TIME)


class B_I_1(IntroBeat):
    beat_id = "I.1"

    def animate_beat(self):
        s = self.step(6)
        self.write("desk", anim=lambda m: LaggedStart(
            *[pop_in(part) for part in (m.led, m.left_monitor, m.right_monitor)],
            *[FadeIn(part, shift=UP * 0.3) for part in m.submobjects[3:11]],
            FadeIn(m.hands, shift=UP * 1.2, rate_func=motion.SPRING), lag_ratio=0.12), run_time=1.2 * s)
        bars = list(B.code(1)())
        first = len(bars) // 3
        self.type_bars(bars[:first], run_time=1.5 * s)
        self.write("game", anim=pop_in, run_time=0.4 * s)
        self.type_bars(bars[first:], run_time=2.6 * s)
        self.clear_transients()
        self.settle("code_1")
        self.play(Wiggle(self.items["desk"].robot), run_time=0.8 * s)


class B_I_2(IntroBeat):
    beat_id = "I.2"

    def animate_beat(self):
        s = self.step(6)
        self.erase("desk", "code_1", "game", style="fall", run_time=1.6)
        m = self.write("machine", anim=pop_in, run_time=s)
        card = B.input_card()
        self.play(FadeIn(card, shift=DOWN * 0.4, rate_func=motion.SPRING), run_time=0.6 * s)
        self.play(card.animate(rate_func=motion.ANTICIPATE).move_to(m.hopper).scale(0.1).set_opacity(0), run_time=0.8 * s)
        self.clear_transients()
        raw = B.raw_strip()
        self.play(FadeIn(raw, shift=RIGHT * 0.6), run_time=0.8 * s)
        self.play(m.plate.animate(rate_func=rate_functions.there_and_back).shift(DOWN * 0.45), run_time=0.5 * s)
        self.write("fast_strip", anim=lambda f: ReplacementTransform(raw, f, rate_func=motion.SPRING), run_time=0.8 * s)
        self.play(Indicate(self.items["fast_strip"], color=ORANGE, scale_factor=1.3), run_time=0.8 * s)


class B_I_3(IntroBeat):
    beat_id = "I.3"

    def animate_beat(self):
        s = self.step(5)
        self.erase("machine", "fast_strip", style="pop", run_time=0.5)
        page = B.bithacks_page()
        self.play(FadeIn(page, shift=UP * 0.6, rate_func=rate_functions.ease_out_cubic), run_time=0.35 * s)
        self.wait(0.9 * s)
        self.play(FadeOut(page, scale=0.1, shift=DOWN * 3.2, rate_func=rate_functions.ease_in_cubic), run_time=0.25 * s)
        self.clear_transients()
        row = self.write("switches_108", anim=lambda r: LaggedStart(*[pop_in(sw) for sw in r.switches], lag_ratio=0.15),
                         run_time=1.5 * s)
        ons = [row.bit(i) for i in (6, 5, 3, 2)]
        self.play(LaggedStart(*[Indicate(sw, scale_factor=1.25) for sw in ons], lag_ratio=0.25), run_time=0.8 * s)
        self.write("book", anim=pop_in, run_time=1.2 * s)


class B_I_4(IntroBeat):
    beat_id = "I.4"

    def animate_beat(self):
        s = self.step(9)
        self.erase("book", "switches_108", style="pop", run_time=0.5)
        row = B.scan_start()
        self.play(LaggedStart(*[pop_in(sw) for sw in row.switches], lag_ratio=0.1), run_time=s)
        ptr = pics.pointer().next_to(row.bit(0), UP, buff=0.12)
        count = style.mono("1 / 32", 34, ORANGE).next_to(row, DOWN, buff=0.6)
        self.play(GrowFromCenter(ptr, rate_func=motion.SPRING), FadeIn(count), run_time=0.5 * s)
        for k in (1, 2):
            self.play(ptr.animate(rate_func=motion.SPRING).next_to(row.bit(k), UP, buff=0.12),
                      Transform(count, style.mono(f"{k + 1} / 32", 34, ORANGE).move_to(count)), run_time=0.6 * s)
        self.play(Transform(row.bit(2), pics.flipped(row.bit(2)), rate_func=motion.SPRING), run_time=0.6 * s)
        self.clear_transients()
        self.settle("scan_side")
        row2 = B.trick_start()
        self.play(LaggedStart(*[pop_in(sw) for sw in row2.switches], lag_ratio=0.1), run_time=s)
        side = B.trick_side()
        self.play(Write(side[1]), run_time=s)
        self.play(LaggedStart(*[pop_in(t) for t in side[2]], lag_ratio=0.5), run_time=s)
        self.play(Transform(row2.bit(2), pics.flipped(row2.bit(2)), rate_func=motion.SPRING),
                  Indicate(side[1], color=ORANGE, scale_factor=1.15), run_time=0.8 * s)
        self.play(FadeIn(side[3], scale=1.6), run_time=0.5 * s)
        self.clear_transients()
        self.settle("trick_side")


class B_I_5(IntroBeat):
    beat_id = "I.5"

    def animate_beat(self):
        s = self.step(5)
        self.erase("trick_side", style="pop", run_time=0.5)
        q = self.write("compiler_q", anim=pop_in, run_time=1.5 * s)
        machine, ask = q[0], q[1]
        ghost = self.items["scan_side"][0].copy()
        self.play(ghost.animate(rate_func=motion.ANTICIPATE).move_to(machine.hopper).scale(0.08).set_opacity(0),
                  run_time=1.2 * s)
        self.clear_transients()
        self.play(machine.plate.animate(rate_func=rate_functions.there_and_back).shift(DOWN * 0.4), run_time=0.5 * s)
        self.play(Wiggle(ask, scale_value=1.4, n_wiggles=5), run_time=1.3 * s)


class B_I_6(IntroBeat):
    beat_id = "I.6"

    def animate_beat(self):
        s = self.step(9)
        self.erase("scan_side", "compiler_q", style="fall", run_time=1.0)
        item = self.write("chess", anim=lambda c: AnimationGroup(pop_in(c[0]), FadeIn(c[1], shift=UP * 0.2)), run_time=1.5 * s)
        grid, strip = item[0][0], item[1]
        drops = []
        for i in grid.occupied:
            ghost = grid.squares[i].copy().set_fill(ORANGE, 0.6)
            drops.append(ghost)
        self.play(LaggedStart(*[g.animate(rate_func=motion.DROP).move_to(strip.cells[i]).scale_to_fit_width(strip.cells[i].width)
                                for g, i in zip(drops, grid.occupied)], lag_ratio=0.12), run_time=2 * s)
        self.play(FadeOut(*drops), run_time=0.3 * s)
        for k, i in enumerate(grid.occupied[:3]):
            flash = strip.cells[i].copy().set_fill(ORANGE, 1)
            self.play(FadeIn(flash, scale=1.8), Indicate(grid.pieces[k], color=ORANGE, scale_factor=1.6), run_time=0.6 * s)
            self.play(FadeOut(flash, shift=DOWN * 0.3), run_time=0.3 * s)
        self.play(Indicate(item[0][1][1], color=ORANGE, scale_factor=1.3), run_time=0.8 * s)


class B_I_7(IntroBeat):
    beat_id = "I.7"

    def animate_beat(self):
        s = self.step(5)
        self.erase("chess", style="fall", run_time=1.0)
        wasted = pics.tile("", ORANGE, w=0.9)
        self.play(GrowFromCenter(wasted, rate_func=motion.ELASTIC), run_time=s)
        copies = [wasted.copy() for _ in range(12)]
        targets = B.devices()
        self.play(*[c.animate(rate_func=motion.SPRING).move_to(t.get_center()).scale(0.25) for c, t in zip(copies, targets)],
                  FadeOut(wasted), run_time=s)
        self.write("devices", anim=lambda d: LaggedStart(*[pop_in(x) for x in d], lag_ratio=0.08), run_time=1.5 * s)
        self.play(FadeOut(*copies), run_time=0.3 * s)
        self.play(LaggedStart(*[Indicate(d[-1], scale_factor=2.2) for d in self.items["devices"]], lag_ratio=0.05),
                  run_time=1.2 * s)


class B_I_8(IntroBeat):
    beat_id = "I.8"

    def animate_beat(self):
        s = self.step(5)
        self.erase("devices", style="pop", run_time=0.6)
        self.write("problem", anim=Write, run_time=1.5 * s)
        self.write("ladder", anim=lambda l: AnimationGroup(
            LaggedStart(*[pop_in(r) for r in reversed(l[0])], lag_ratio=0.3), Create(l[1])), run_time=1.5 * s)
        self.write("inputs", anim=lambda g: AnimationGroup(
            LaggedStart(*[FadeIn(d, scale=2) for d in g[0]], lag_ratio=0.01), FadeIn(g[1])), run_time=1.5 * s)
        self.play(Indicate(self.items["problem"], scale_factor=1.05), run_time=0.5 * s)


class B_I_9(IntroBeat):
    beat_id = "I.9"

    def animate_beat(self):
        s = self.step(6)
        self.erase("ladder", "inputs", style="pop", run_time=0.5)
        self.write("headline", anim=Write, run_time=s)
        far = B.long_view()
        self.play(Create(far[0]), LaggedStart(pop_in(far[1]), pop_in(far[2]), lag_ratio=0.6), run_time=1.5 * s)
        self.play(far.animate(rate_func=rate_functions.ease_in_cubic).scale(6, about_point=far[2].get_center()).set_opacity(0),
                  run_time=s)
        self.clear_transients()
        self.write("summer", anim=lambda t: AnimationGroup(
            FadeIn(t[1]), LaggedStart(*[pop_in(tick) for tick in t[0]], lag_ratio=0.3)), run_time=2.5 * s)
