from manim import RIGHT, UP, FadeIn, FadeOut, Transform

from theme import DIM, INK, ORANGE, VideoScene, mono, proof_check


class TheSmell(VideoScene):
    def construct(self) -> None:
        row = mono("rule out every one-step program", size=28, color=INK)
        row.move_to(UP * 0.3)
        label = mono("the hardest proof in the suite", size=22, color=DIM)
        label.next_to(row, UP, buff=0.5)

        self.play(FadeIn(label), FadeIn(row), run_time=0.8)
        self.wait(0.8)

        timer = mono("0.00s", size=32, color=DIM)
        timer.next_to(row, RIGHT, buff=1.0)
        self.play(FadeIn(timer), run_time=0.5)
        self.wait(0.3)

        for value in ("0.01s", "0.02s"):
            new_timer = mono(value, size=32, color=DIM).move_to(timer.get_center())
            self.play(Transform(timer, new_timer), run_time=0.35)
            self.wait(0.2)

        check = proof_check(size=0.4).next_to(timer, RIGHT, buff=0.3)
        self.play(FadeIn(check, scale=1.3), run_time=0.3)
        self.wait(1.3)

        grown = mono("0.02s", size=48, color=ORANGE).move_to(timer.get_center())
        self.play(Transform(timer, grown), FadeOut(check), run_time=0.8)
        self.wait(17.5)
