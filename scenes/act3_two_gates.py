import random

from manim import DOWN, UP, FadeIn, FadeOut, Indicate, LaggedStart, Line, RoundedRectangle, VGroup

from theme import DIM, INK, PROOF, VideoScene, mono

CHIP_W = 0.5
CHIP_H = 0.3
TRACK_Y = 0
GATE1_X = -2.2
GATE2_X = 2.2
GATE_W = 0.3
GATE_H = 3.0
START_X = -6.0
PEDESTAL_X = 5.2


def make_gate(x: float) -> RoundedRectangle:
    gate = RoundedRectangle(
        corner_radius=0.1, width=GATE_W, height=GATE_H, stroke_color=INK, stroke_width=2, fill_opacity=0
    )
    gate.move_to([x, TRACK_Y, 0])
    return gate


def make_chip(x: float, y: float) -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.05, width=CHIP_W, height=CHIP_H, stroke_color=INK, stroke_width=1.5, fill_color=INK, fill_opacity=0.12
    ).move_to([x, y, 0])


class TwoGates(VideoScene):
    def construct(self) -> None:
        gate1 = make_gate(GATE1_X)
        gate2 = make_gate(GATE2_X)
        label1 = mono("the proof", size=20, color=DIM).next_to(gate1, DOWN, buff=0.4)
        label2 = mono("the second opinion", size=20, color=DIM).next_to(gate2, DOWN, buff=0.4)
        self.play(FadeIn(gate1), FadeIn(gate2), FadeIn(label1), FadeIn(label2), run_time=0.8)
        self.wait(0.6)

        chip = make_chip(START_X, TRACK_Y)
        self.play(FadeIn(chip, scale=0.6), run_time=0.3)
        self.wait(0.3)

        self.play(chip.animate.move_to([GATE1_X, TRACK_Y, 0]), run_time=0.9)
        self.wait(0.2)

        self.play(Indicate(gate1, color=PROOF, scale_factor=1.15), run_time=0.6)
        self.wait(0.4)

        self.play(chip.animate.move_to([GATE2_X, TRACK_Y, 0]), run_time=0.9)
        self.wait(0.2)

        rng = random.Random(5)
        drops = VGroup()
        for _ in range(6):
            val = str(rng.randint(10, 99))
            x = GATE2_X + rng.uniform(-0.5, 0.5)
            label = mono(val, size=14, color=DIM)
            label.move_to([x, TRACK_Y + 1.7, 0])
            drops.add(label)
        self.play(
            LaggedStart(*[d.animate.move_to([d.get_center()[0], TRACK_Y + 0.28, 0]) for d in drops], lag_ratio=0.15),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[Indicate(d, color=PROOF, scale_factor=1.3) for d in drops], lag_ratio=0.1), run_time=0.8
        )
        self.play(FadeOut(drops), run_time=0.4)
        self.wait(0.3)

        self.play(chip.animate.move_to([PEDESTAL_X, TRACK_Y, 0]), run_time=0.9)

        pedestal = Line([PEDESTAL_X - 0.9, TRACK_Y - 0.35, 0], [PEDESTAL_X + 0.9, TRACK_Y - 0.35, 0], stroke_color=DIM, stroke_width=2)
        self.play(FadeIn(pedestal), run_time=0.3)
        self.play(chip.animate.set_stroke(PROOF).set_fill(PROOF, opacity=0.3), run_time=0.5)

        optimal_label = mono("optimal", size=20, color=INK)
        optimal_label.next_to(chip, UP, buff=0.3)
        self.play(FadeIn(optimal_label), run_time=0.5)
        self.wait(16.0)
