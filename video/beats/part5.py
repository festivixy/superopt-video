from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, AnimationGroup, Create, FadeIn, GrowFromCenter, Indicate, LaggedStart, MoveAlongPath,
    Transform, TransformFromCopy, VGroup, Write, config,
)

import boards.part5 as B
from boards.part5 import BOARD
from kit import motion, pics, style
from kit.beat import BeatScene
from kit.style import BLUE, DIM, GREEN, ORANGE


def pop_in(m):
    return GrowFromCenter(m, rate_func=motion.SPRING)


def slam(m):
    return FadeIn(m, scale=2.5, rate_func=motion.SPRING)


class Part5Beat(BeatScene):
    board = BOARD

    def settle(self, key: str) -> None:
        self.write(key, anim=lambda m: FadeIn(m, rate_func=lambda t: 1.0), run_time=1 / config.frame_rate)

    def feed(self, machines, value: str, outs, run_time: float) -> None:
        tokens = [style.mono(value, 48, BLUE).next_to(m.inlet, LEFT, buff=0.4) for m in machines]
        results = [style.mono(v, 48, c).next_to(m.outlet, RIGHT, buff=0.4) for m, (v, c) in zip(machines, outs)]
        self.play(*[FadeIn(t, shift=RIGHT * 0.3) for t in tokens], run_time=run_time * 0.3)
        self.play(*[t.animate(rate_func=motion.ANTICIPATE).move_to(m.inlet).scale(0.4).set_opacity(0)
                    for t, m in zip(tokens, machines)], run_time=run_time * 0.3)
        self.play(*[FadeIn(r, shift=RIGHT * 0.4, rate_func=motion.SPRING) for r in results], run_time=run_time * 0.4)


class B_5_1(Part5Beat):
    beat_id = "5.1"

    def animate_beat(self):
        s = self.step(10)
        twins = self.write("twins", anim=lambda t: LaggedStart(*[pop_in(m) for m in t], lag_ratio=0.3), run_time=1.2 * s)
        grid = B._input_grid()
        final = B.tried()
        self.play(LaggedStart(*[FadeIn(d, scale=0.3) for d in grid], lag_ratio=0.004), run_time=1.0 * s)
        for k, (x, y) in enumerate((("7", "14"), ("12", "24"))):
            self.feed(twins, x, [(y, GREEN), (y, GREEN)], run_time=1.6 * s)
            self.play(Transform(grid[B.TRIED[k]], final[B.TRIED[k]], rate_func=motion.SPRING), run_time=0.5 * s)
            self.clear_transients()
            self.add(grid)
        self.play(LaggedStart(*[Transform(grid[i], final[i], rate_func=motion.SPRING) for i in B.TRIED[2:]], lag_ratio=0.3),
                  run_time=1.2 * s)
        untried = [d for i, d in enumerate(grid) if i not in B.TRIED]
        self.play(LaggedStart(*[Indicate(d, color=ORANGE, scale_factor=1.8) for d in untried], lag_ratio=0.01), run_time=2.0 * s)
        self.clear_transients()
        self.settle("tried")


class B_5_2(Part5Beat):
    beat_id = "5.2"

    def animate_beat(self):
        s = self.step(16)
        self.erase("twins", "tried", style="fall", run_time=1.0)
        space = B.space()
        final = B.space()
        for i in (B.HIT, B.MOST_NEGATIVE):
            space.cells[i].set_fill(DIM, 0.55)
        n = B.SPACE
        self.play(LaggedStart(*[FadeIn(VGroup(*space.cells[r * n:(r + 1) * n])) for r in range(n)], lag_ratio=0.06),
                  run_time=2.0 * s)
        self.write("c32", anim=Write, run_time=1.5 * s)
        self.play(Transform(space.cells[B.HIT], final.cells[B.HIT]), GrowFromCenter(space.hit_ring, rate_func=motion.ELASTIC),
                  run_time=1.0 * s)
        self.write("share", anim=Write, run_time=1.2 * s)
        self.write("c64", anim=Write, run_time=1.5 * s)
        start = B.negate_strip(B.most_negative_bits())
        flipped = B.negate_strip([1 - b for b in B.most_negative_bits()])
        back = B.negate_strip(B.most_negative_bits())
        self.play(LaggedStart(*[pop_in(c) for c in start.cells], lag_ratio=0.02), run_time=1.0 * s)
        self.play(LaggedStart(*[Transform(c, f) for c, f in zip(start.cells, flipped.cells)], lag_ratio=0.03), run_time=1.5 * s)
        ripple = list(zip(start.cells, back.cells))[::-1]
        self.play(LaggedStart(*[Transform(c, f, rate_func=motion.SPRING) for c, f in ripple], lag_ratio=0.08), run_time=2.0 * s)
        self.play(Transform(space.cells[B.MOST_NEGATIVE], final.cells[B.MOST_NEGATIVE]),
                  GrowFromCenter(space.corner_ring, rate_func=motion.ELASTIC), run_time=0.8 * s)
        eq = B.negate()[1]
        self.play(Write(eq), run_time=1.2 * s)
        self.clear_transients()
        self.settle("space")
        self.settle("negate")


class B_5_3(Part5Beat):
    beat_id = "5.3"

    def animate_beat(self):
        s = self.step(8)
        self.erase("space", "c32", "share", "c64", "negate", style="swipe", run_time=1.2)
        final = B.evens()
        a, plus, b, eq, total = final
        self.play(pop_in(a.copy()), run_time=1.0 * s)
        self.play(FadeIn(plus.copy(), scale=1.5), pop_in(b.copy()), run_time=1.0 * s)
        self.play(FadeIn(eq.copy()), Create(total[0].copy()), run_time=0.5 * s)
        pairs = list(a.pairs) + list(b.pairs)
        self.play(LaggedStart(*[TransformFromCopy(p, q, path_arc=-0.8) for p, q in zip(pairs, total.pairs)], lag_ratio=0.15),
                  run_time=2.0 * s)
        self.clear_transients()
        self.settle("evens")
        self.write("algebra", anim=Write, run_time=2.0 * s)
        self.play(Indicate(self.items["algebra"], color=GREEN, scale_factor=1.08), run_time=1.0 * s)


class B_5_4(Part5Beat):
    beat_id = "5.4"

    def animate_beat(self):
        s = self.step(11)
        self.erase("evens", "algebra", style="pop", run_time=0.6)
        states = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
        states = states[:states.index(B.SAT_BITS) + 1]
        cur = B.sat_at(states[0])
        self.play(FadeIn(cur[0], shift=DOWN * 0.3), LaggedStart(*[pop_in(m) for m in cur[1]], lag_ratio=0.2), run_time=1.2 * s)
        for st in states[1:]:
            self.play(Transform(cur, B.sat_at(st), rate_func=motion.SPRING), run_time=3.0 * s / len(states))
        self.play(Indicate(cur.lamp, color=ORANGE, scale_factor=1.4), run_time=0.8 * s)
        self.clear_transients()
        self.settle("sat")
        self.write("chip", anim=pop_in, run_time=1.0 * s)
        bits = B.bits()
        self.play(FadeIn(bits[0], scale=1.5), run_time=0.5 * s)
        self.play(LaggedStart(*[TransformFromCopy(bits[0], c) for c in bits[1].cells], lag_ratio=0.03), run_time=1.8 * s)
        self.clear_transients()
        self.settle("bits")
        gates = B.gates()
        self.play(pop_in(gates[0]), run_time=0.6 * s)
        self.play(FadeIn(gates[1], shift=RIGHT * 0.3), LaggedStart(*[Create(g) for g in gates[2]], lag_ratio=0.25), run_time=1.6 * s)
        self.clear_transients()
        self.settle("gates")


class B_5_5(Part5Beat):
    beat_id = "5.5"

    def animate_beat(self):
        s = self.step(9)
        self.erase("sat", "chip", "bits", "gates", style="fall", run_time=1.0)
        q = B.query()
        self.play(LaggedStart(*[pop_in(m) for m in q.pair], lag_ratio=0.3), run_time=1.5 * s)
        self.play(Create(q[1]), GrowFromCenter(q.ne, rate_func=motion.ELASTIC), run_time=1.0 * s)
        self.play(Create(q[3]), pop_in(q.box), run_time=1.0 * s)
        pulses = [pics.marble(BLUE, 0.12).move_to(w.get_start()) for w in q[1]]
        self.play(*[MoveAlongPath(p, w) for p, w in zip(pulses, q[1])], run_time=0.8 * s)
        last = pics.marble(ORANGE, 0.12).move_to(q[3].get_start())
        self.play(MoveAlongPath(last, q[3]), run_time=0.6 * s)
        self.play(Indicate(q.box, color=BLUE, scale_factor=1.12), run_time=1.0 * s)
        self.clear_transients()
        self.settle("query")
        self.write("unsat", anim=slam, run_time=0.8 * s)
        self.write("forall", anim=Write, run_time=1.5 * s)


class B_5_6(Part5Beat):
    beat_id = "5.6"

    def animate_beat(self):
        s = self.step(15)
        self.erase("query", "forall", style="pop", run_time=0.6)
        t = B.tree_at(0)
        self.play(Create(t.edges), LaggedStart(*[pop_in(n) for n in t.nodes], lag_ratio=0.04), run_time=2.0 * s)
        final = B.tree()
        rules = B.learned()
        for k, leaf in enumerate(B.CONFLICTS):
            path = [leaf]
            while path[-1]:
                path.append((path[-1] - 1) // 2)
            path.reverse()
            self.play(LaggedStart(*[Indicate(t.nodes[i], color=ORANGE, scale_factor=1.6) for i in path], lag_ratio=0.5),
                      run_time=1.3 * s)
            mark = final[1][k].copy()
            self.play(GrowFromCenter(mark, rate_func=motion.ELASTIC), run_time=0.4 * s)
            self.play(TransformFromCopy(mark, rules[k]), run_time=0.8 * s)
            self.play(Transform(t, B.tree_at(k + 1)), run_time=0.9 * s)
        self.play(Transform(t, final.t), run_time=0.5 * s)
        self.play(Indicate(self.items["unsat"], color=GREEN, scale_factor=1.15), run_time=0.8 * s)
        self.clear_transients()
        self.settle("tree")
        self.settle("learned")


class B_5_7(Part5Beat):
    beat_id = "5.7"

    def animate_beat(self):
        s = self.step(10)
        self.erase("tree", "learned", "unsat", style="fall", run_time=1.0)
        c = B.counter()
        before = B._twin(r"x \ll 1", 3.4).move_to(c.pair[1])
        self.play(pop_in(c.pair[0]), pop_in(before), run_time=1.2 * s)
        self.play(Transform(before.face, c.pair[1].face, rate_func=motion.SPRING), run_time=0.8 * s)
        self.feed(c.pair, "1", [("2", GREEN), ("4", ORANGE)], run_time=2.0 * s)
        self.clear_transients()
        self.settle("counter")
        self.write("sat_stamp", anim=lambda g: AnimationGroup(slam(g[0]), Write(g[1])), run_time=1.2 * s)
        self.write("summary", anim=lambda g: LaggedStart(*[pop_in(part) for row in g for part in row], lag_ratio=0.2),
                   run_time=2.4 * s)
