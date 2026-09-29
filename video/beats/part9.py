from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP, AnimationGroup, Succession, Create, FadeIn, GrowFromCenter, GrowFromEdge, Indicate,
    LaggedStart, MoveAlongPath, Polygon, Transform, TransformFromCopy, VGroup, Write, config, rate_functions,
)

import boards.part9 as B
from boards.part9 import BOARD
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import BLUE, GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


class Part9Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)


class B_9_1(Part9Beat):
    beat_id = "9.1"

    def animate_beat(self):
        s = self.step(9)
        book = self.write("book", anim=lambda b: FadeIn(b, shift=DOWN * 0.6, rate_func=motion.SPRING), run_time=1.2 * s)
        final = B.jobs()
        flyers = [c.copy().scale(0.3).move_to(book) for c in final.chips]
        self.play(LaggedStart(*[Transform(f, c, rate_func=motion.SPRING, path_arc=-0.6) for f, c in zip(flyers, final.chips)],
                              lag_ratio=0.12), run_time=3.0 * s)
        self.clear_transients()
        self.settle("jobs")
        p = B.pair()
        self.play(Create(p.py[0]), LaggedStart(*[Create(r) for r in p.py.rows], lag_ratio=0.3),
                  FadeIn(p.tags[0], shift=RIGHT * 0.3), run_time=1.3 * s)
        self.play(Create(p.c[0]), LaggedStart(*[Create(r) for r in p.c.rows], lag_ratio=0.3),
                  FadeIn(p.tags[1], shift=LEFT * 0.3), run_time=1.3 * s)
        self.play(LaggedStart(*[Create(l) for l in p.links], lag_ratio=0.35), run_time=1.2 * s)
        self.clear_transients()
        self.settle("pair")


class B_9_2(Part9Beat):
    beat_id = "9.2"

    def animate_beat(self):
        s = self.step(10)
        self.erase("book", "jobs", "pair", style="pop", run_time=0.6)
        self.write("rigs", anim=lambda r: LaggedStart(*[pop_in(x) for x in r], lag_ratio=0.4), run_time=1.2 * s)
        a = B.asm()
        self.play(Create(a[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in a.rows], lag_ratio=0.1), run_time=1.2 * s)
        counter = style.mono("0", 56, ORANGE).move_to(a.count)
        self.add(counter)
        for k, tick in enumerate(a.ticks):
            nxt = style.mono(str(k + 1), 56, ORANGE).move_to(a.count)
            self.play(GrowFromCenter(tick), Transform(counter, nxt), run_time=0.28 * s)
        self.play(Indicate(a.dots, color=ORANGE, scale_factor=1.5), Transform(counter, a.count), run_time=1.0 * s)
        self.play(GrowFromCenter(a.no, rate_func=motion.ELASTIC), run_time=0.5 * s)
        self.clear_transients()
        self.settle("asm")
        self.write("badges", anim=lambda b: LaggedStart(*[FadeIn(r, shift=LEFT * 0.4) for r in b], lag_ratio=0.35), run_time=1.8 * s)
        final = B.seven()
        dots = final.dots.copy()
        for d in dots[:B.PROVEN]:
            d.set_stroke(B.DIM).set_fill(B.DIM, 0.2)
        self.play(LaggedStart(*[pop_in(d) for d in dots], lag_ratio=0.06), run_time=1.0 * s)
        self.play(LaggedStart(*[Transform(d, f, rate_func=motion.SPRING) for d, f in zip(dots[:B.PROVEN], final.dots)],
                              lag_ratio=0.2), run_time=1.2 * s)
        self.play(Write(final[1]), run_time=0.8 * s)
        self.clear_transients()
        self.settle("seven")


class B_9_3(Part9Beat):
    beat_id = "9.3"

    def animate_beat(self):
        s = self.step(7)
        self.erase("rigs", "asm", "badges", "seven", style="fall", run_time=0.8)
        self.write("legend", anim=lambda g: LaggedStart(*[FadeIn(x, shift=DOWN * 0.3) for x in g], lag_ratio=0.3), run_time=0.8 * s)
        for k in range(3):
            self.write(f"row{k}", anim=lambda r: LaggedStart(
                FadeIn(r.label, shift=RIGHT * 0.3),
                LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT, rate_func=motion.SPRING), FadeIn(n)) for b, n in zip(r.bars, r.nums)],
                            lag_ratio=0.45),
                GrowFromCenter(r.proof, rate_func=motion.ELASTIC), lag_ratio=0.25), run_time=1.9 * s)
        self.play(*[Indicate(self.items[f"row{k}"].bars[2], color=GREEN, scale_factor=2.0) for k in range(3)], run_time=0.5 * s)


class B_9_4(Part9Beat):
    beat_id = "9.4"

    def animate_beat(self):
        s = self.step(11)
        self.erase("legend", "row0", "row1", "row2", style="pop", run_time=0.6)
        loop = self.write("gcc_loop", anim=lambda g: LaggedStart(
            FadeIn(g[0]), LaggedStart(*[pop_in(t) for t in g.tiles], lag_ratio=0.2), Create(g.arrows), FadeIn(g.strip),
            FadeIn(g.times, scale=1.5), lag_ratio=0.3), run_time=1.5 * s)
        centers = [t.get_center() for t in loop.tiles]
        path = Polygon(*centers)
        dot = pics.marble(ORANGE, 0.14).move_to(centers[0])
        self.add(dot)
        lit = None
        for k in range(4):
            cell = loop.strip.cells[len(loop.strip.cells) - 1 - k].copy().set_fill(BLUE, 0.9)
            anims = [MoveAlongPath(dot, path)]
            anims.append(FadeIn(cell) if lit is None else Transform(lit, cell))
            self.play(*anims, run_time=0.9 * s, rate_func=lambda t: t)
            lit = lit or cell
        self.clear_transients()
        self.write("clang_unrolled", anim=lambda g: LaggedStart(
            FadeIn(g[0]), LaggedStart(*[pop_in(c) for c in g.copies], lag_ratio=0.05), FadeIn(g[2], scale=1.5), lag_ratio=0.2),
                   run_time=2.2 * s)
        self.write("blsr", anim=lambda g: AnimationGroup(pop_in(g[0]), Write(g[1])), run_time=1.3 * s)
        self.play(Indicate(self.items["blsr"][0], color=GREEN, scale_factor=1.3), run_time=0.6 * s)
        self.write("unused", anim=lambda g: LaggedStart(*[AnimationGroup(Create(x[0]), GrowFromCenter(x[1], rate_func=motion.ELASTIC))
                                                          for x in g], lag_ratio=0.4), run_time=1.5 * s)


class B_9_5(Part9Beat):
    beat_id = "9.5"

    def animate_beat(self):
        s = self.step(8)
        self.erase("gcc_loop", "clang_unrolled", "blsr", "unused", style="fall", run_time=1.0)
        self.write("headers", anim=lambda h: LaggedStart(pop_in(h[0]), FadeIn(h[1], shift=DOWN * 0.3), lag_ratio=0.4), run_time=0.8 * s)
        self.write("rotate_row", anim=self._row_in, run_time=2.4 * s)
        rol = self.items["rotate_row"][1][0]
        self.write("instruction_set", anim=lambda g: LaggedStart(
            Create(g.box), LaggedStart(*[pop_in(t) for t in g.tiles], lag_ratio=0.06),
            FadeIn(g.reject[0], target_position=rol.get_center(), rate_func=motion.SPRING),
            GrowFromCenter(g.reject[1], rate_func=motion.ELASTIC), lag_ratio=0.35), run_time=2.4 * s)
        self.write("bswap_row", anim=self._row_in, run_time=2.4 * s)
        rows = (self.items["rotate_row"], self.items["bswap_row"])
        self.play(*[Indicate(r[1], color=ORANGE, scale_factor=1.15) for r in rows], run_time=0.8 * s)

    @staticmethod
    def _row_in(r):
        label, theirs, mine, count = r
        return LaggedStart(FadeIn(label, shift=RIGHT * 0.3), pop_in(theirs),
                           LaggedStart(*[pop_in(t) for t in mine], lag_ratio=0.12), FadeIn(count, scale=1.5), lag_ratio=0.3)


class B_9_6(Part9Beat):
    beat_id = "9.6"

    def animate_beat(self):
        s = self.step(10)
        self.erase("headers", "rotate_row", "instruction_set", "bswap_row", style="swipe", run_time=1.0)
        card = self.write("trick", anim=pop_in, run_time=1.2 * s)
        self.play(Indicate(card.lines[0], color=B.MAGENTA, scale_factor=1.15), run_time=0.8 * s)
        self._case(B.neg_case(), fill=True, run_time=4.0 * s)
        self.settle("neg_case")
        self._case(B.pos_case(), fill=False, run_time=4.0 * s)
        self.settle("pos_case")
        self.play(LaggedStart(*[Indicate(card.lines[i], color=GREEN, scale_factor=1.12) for i in (1, 2)], lag_ratio=0.5),
                  run_time=1.4 * s)

    def _case(self, final, fill: bool, run_time: float) -> None:
        top, bottom = final[0], final[1]
        self.play(FadeIn(top[0]), LaggedStart(*[pop_in(c) for c in final.x.cells], lag_ratio=0.02), run_time=run_time * 0.3)
        self.play(Indicate(final.x.cells[0], color=final.x.cells[0].get_stroke_color(), scale_factor=2.0), run_time=run_time * 0.15)
        self.play(FadeIn(bottom[0], shift=RIGHT * 0.3), run_time=run_time * 0.1)
        if fill:
            self.play(LaggedStart(*[TransformFromCopy(final.x.cells[0], c) for c in final.res.cells], lag_ratio=0.03),
                      run_time=run_time * 0.3)
        else:
            self.play(LaggedStart(*[FadeIn(c, scale=0.4) for c in final.res.cells], lag_ratio=0.03), run_time=run_time * 0.3)
        if len(final) > 2:
            self.play(Write(final[2]), run_time=run_time * 0.15)
        self.clear_transients()


class B_9_7(Part9Beat):
    beat_id = "9.7"

    def animate_beat(self):
        s = self.step(9)
        self.erase("neg_case", "pos_case", style="pop", run_time=0.6)
        self.write("ring", anim=lambda r: AnimationGroup(Create(r[0]), GrowFromCenter(r[1], rate_func=motion.ELASTIC)), run_time=1.2 * s)
        chip = self.write("x86", anim=pop_in, run_time=0.8 * s)
        traveller = self.items["trick"].copy()
        self.play(traveller.animate(rate_func=motion.ANTICIPATE).scale(0.3).move_to(chip.body.get_left() + LEFT * 0.9),
                  run_time=1.2 * s)
        five = B.five()
        self.play(FadeIn(five[0]), LaggedStart(*[pop_in(c) for c in five.amount.cells], lag_ratio=0.02), run_time=1.0 * s)
        self.play(Create(five.box), *[c.animate.set_opacity(0.25) for c in five.amount.cells[:27]], run_time=0.8 * s)
        self.play(FadeIn(five.zero, shift=DOWN * 0.3), Indicate(chip, color=ORANGE, scale_factor=1.08), run_time=0.8 * s)
        halves = VGroup(traveller.copy(), traveller.copy())
        self.remove(traveller)
        self.play(halves[0].animate.rotate(0.35).shift(UP * 0.3 + LEFT * 0.2).set_color(ORANGE),
                  halves[1].animate.rotate(-0.35).shift(DOWN * 0.3 + RIGHT * 0.2).set_color(ORANGE), run_time=0.8 * s)
        self.clear_transients()
        self.settle("five")
        self.write("wrong", anim=lambda w: AnimationGroup(Write(w[0]), GrowFromCenter(w[1], rate_func=motion.ELASTIC)),
                   run_time=1.1 * s)
        self.write("writeup", anim=lambda w: LaggedStart(pop_in(w[0]), GrowFromCenter(w[1]), lag_ratio=0.5), run_time=1.0 * s)


class B_9_8(Part9Beat):
    beat_id = "9.8"

    def animate_beat(self):
        s = self.step(5)
        self.erase("trick", "ring", "x86", "five", "wrong", "writeup", style="fall", run_time=0.9)
        held = self.write("held", anim=lambda h: LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3) for r in h], lag_ratio=0.3),
                          run_time=1.0 * s)
        issue = self.write("issue", anim=lambda g: Succession(FadeIn(g.shot, shift=DOWN * 0.6, rate_func=rate_functions.ease_out_cubic),
                                                               Create(g.ring)), run_time=1.6 * s)
        self.play(LaggedStart(*[TransformFromCopy(r, r.copy().scale(0.05).move_to(issue.shot.image)) for r in held],
                              lag_ratio=0.2), run_time=1.0 * s)
        self.clear_transients()
        self.play(Indicate(issue.ring, color=ORANGE, scale_factor=1.12), run_time=0.8 * s)
