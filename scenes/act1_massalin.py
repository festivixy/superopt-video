from manim import DOWN, UP, FadeIn, VGroup

from theme import DIM, INK, ORANGE, VideoScene, mono


class Massalin1987(VideoScene):
    def construct(self) -> None:
        year = mono("1987", size=90, color=INK)
        year.move_to([0, 1.0, 0])
        self.play(FadeIn(year, shift=UP * 0.2), run_time=0.9)
        self.wait(1.0)

        title = mono("Superoptimizer — a look at the smallest program", size=22, color=DIM)
        title.next_to(year, DOWN, buff=0.5)
        self.play(FadeIn(title), run_time=0.7)
        self.wait(1.8)

        top = VGroup(year, title)
        self.play(top.animate.shift(UP * 0.6).set_opacity(0), run_time=1.0)
        self.wait(0.3)

        shortest = mono("shortest?", size=30, color=ORANGE)
        shortest.move_to([0, 0, 0])
        self.play(FadeIn(shortest, scale=0.7), run_time=0.7)
        self.wait(12.9)
