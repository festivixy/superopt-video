from manim import DOWN, RIGHT, FadeIn, FadeOut, Indicate, RoundedRectangle

from theme import DIM, INK, PROOF, VideoScene, mono, proof_check


class TheRegressionTest(VideoScene):
    def construct(self) -> None:
        card = RoundedRectangle(
            corner_radius=0.15, width=9.4, height=3.6, stroke_color=INK, stroke_width=2, fill_opacity=0
        )
        card.move_to([0, 0.2, 0])
        self.play(FadeIn(card), run_time=0.6)

        name = mono("test_synthesizes_when_line_count_is_a_power_of_two", size=22, color=INK)
        name.move_to(card.get_center() + [0, 1.1, 0])
        self.play(FadeIn(name), run_time=0.6)
        self.wait(0.3)

        subtitle = mono("the shape that failed", size=20, color=DIM)
        subtitle.next_to(name, DOWN, buff=0.35)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.8)

        running = mono("running", size=18, color=DIM)
        running.move_to(card.get_center() + [0, -0.9, 0])
        self.play(FadeIn(running), run_time=0.3)
        self.play(Indicate(running, color=INK, scale_factor=1.15), run_time=0.6)
        self.wait(0.2)
        self.play(FadeOut(running), run_time=0.3)
        self.wait(0.2)

        check = proof_check(size=0.9, stroke_width=10).move_to(card.get_center() + [-0.9, -0.9, 0])
        passes = mono("passes", size=32, color=PROOF)
        passes.next_to(check, RIGHT, buff=0.5)
        self.play(FadeIn(check, scale=1.3), FadeIn(passes, scale=1.2), run_time=0.7)
        self.wait(19.9)
