import random

from manim import DOWN, UP, FadeIn, FadeOut, Indicate, LaggedStart, Line, RoundedRectangle, VGroup

from act3_two_gates import GATE1_X, GATE2_X, START_X, TRACK_Y, make_chip, make_gate
from theme import DIM, INK, ORANGE, PROOF, VideoScene, mono


class TheSaboteur(VideoScene):
    def construct(self) -> None:
        gate1 = make_gate(GATE1_X)
        gate2 = make_gate(GATE2_X)
        label1 = mono("the proof", size=20, color=DIM).next_to(gate1, DOWN, buff=0.4)
        label2 = mono("the second opinion", size=20, color=DIM).next_to(gate2, DOWN, buff=0.4)
        self.play(FadeIn(gate1), FadeIn(gate2), FadeIn(label1), FadeIn(label2), run_time=0.8)
        self.wait(0.6)

        rule_plate = RoundedRectangle(
            corner_radius=0.08, width=0.8, height=0.45, stroke_color=INK, stroke_width=1.5, fill_opacity=0
        )
        rule_plate.move_to(gate1.get_top() + UP * 0.6)
        rule_text = mono(">>", size=22, color=INK).move_to(rule_plate.get_center())
        self.play(FadeIn(rule_plate), FadeIn(rule_text), run_time=0.5)
        self.wait(0.4)

        rule_text_bad = mono(">>", size=22, color=ORANGE).move_to(rule_plate.get_center())
        self.play(rule_text.animate.become(rule_text_bad), run_time=0.4)
        self.wait(1.0)

        chip = make_chip(START_X, TRACK_Y)
        self.play(FadeIn(chip, scale=0.6), run_time=0.3)
        self.wait(0.3)

        self.play(chip.animate.move_to([GATE1_X, TRACK_Y, 0]), run_time=0.9)
        self.wait(0.2)

        flash1 = mono("impossible to beat", size=16, color=PROOF)
        flash1.move_to([GATE1_X, TRACK_Y + 1.0, 0])
        self.play(FadeIn(flash1, scale=0.7), run_time=0.3)
        self.wait(0.4)
        self.play(FadeOut(flash1), run_time=0.3)

        crack = VGroup(
            Line(gate1.get_center() + [-0.12, 0.35, 0], gate1.get_center() + [0.08, 0.05, 0], stroke_color=ORANGE, stroke_width=1.5),
            Line(gate1.get_center() + [0.08, 0.05, 0], gate1.get_center() + [-0.1, -0.35, 0], stroke_color=ORANGE, stroke_width=1.5),
        )
        self.play(FadeIn(crack), run_time=0.3)
        self.wait(0.3)

        self.play(chip.animate.move_to([GATE2_X, TRACK_Y, 0]), run_time=0.9)
        self.wait(0.2)

        rng = random.Random(9)
        drops = VGroup()
        for _ in range(4):
            val = str(rng.randint(10, 99))
            x = GATE2_X + rng.uniform(-0.5, 0.5)
            label = mono(val, size=14, color=DIM)
            label.move_to([x, TRACK_Y + 1.7, 0])
            drops.add(label)
        self.play(
            LaggedStart(*[d.animate.move_to([d.get_center()[0], TRACK_Y + 0.28, 0]) for d in drops], lag_ratio=0.15),
            run_time=1.1,
        )
        self.play(
            LaggedStart(*[Indicate(d, color=PROOF, scale_factor=1.3) for d in drops[:-1]], lag_ratio=0.15),
            run_time=0.7,
        )
        self.wait(0.2)

        big_x = mono("X", size=60, color=ORANGE)
        big_x.move_to([GATE2_X, TRACK_Y, 0])
        count_label = mono(f"{len(drops)} random inputs", size=13, color=DIM)
        count_label.next_to(big_x, DOWN, buff=1.1)
        self.play(FadeIn(big_x, scale=1.6), FadeOut(drops), run_time=0.4)
        self.play(FadeIn(count_label), run_time=0.4)
        self.wait(0.5)

        self.play(chip.animate.shift(UP * 0.5), FadeOut(big_x), run_time=0.3)
        self.play(chip.animate.shift(DOWN * 5).set_opacity(0), FadeOut(count_label), run_time=0.8)
        self.wait(18.0)
