from manim import FadeIn, FadeOut, Indicate, ManimColor, RoundedRectangle, Transform, interpolate_color

from theme import DIM, INK, ORANGE, VideoScene, mono

TASK_Y = 2.6
TIMER_Y = 0.6

VALUES = ["0.06s", "0.1s", "3.9s", "11s", "27s"]
SIZES = [22, 26, 32, 40, 50]


class WhatItStillCant(VideoScene):
    def construct(self) -> None:
        card = RoundedRectangle(
            corner_radius=0.15, width=3.6, height=0.9, stroke_color=INK, stroke_width=1.5, fill_opacity=0
        )
        card.move_to([0, TASK_Y, 0])
        task = mono("count the 1s", size=24, color=INK).move_to(card.get_center())
        self.play(FadeIn(card), FadeIn(task), run_time=0.7)
        self.wait(0.8)

        timer = mono(VALUES[0], size=SIZES[0], color=DIM).move_to([0, TIMER_Y, 0])
        self.play(FadeIn(timer), run_time=0.5)
        self.wait(0.3)

        for i in range(1, len(VALUES)):
            t = i / (len(VALUES) - 1)
            color = interpolate_color(ManimColor(DIM), ManimColor(ORANGE), t)
            new_timer = mono(VALUES[i], size=SIZES[i], color=color).move_to([0, TIMER_Y, 0])
            self.play(Transform(timer, new_timer), run_time=0.5)
            self.wait(0.35)

        dots = mono("...", size=50, color=ORANGE).move_to([0, TIMER_Y, 0])
        self.play(Transform(timer, dots), run_time=0.5)
        self.wait(0.8)

        self.play(FadeOut(timer), run_time=0.7)
        self.wait(0.5)
        self.play(Indicate(card, color=ORANGE, scale_factor=1.08), run_time=0.7)
        self.wait(13.8)
