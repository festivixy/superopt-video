from manim import RIGHT, FadeIn, Indicate, VGroup

from theme import INK, PROOF, VideoScene, mono, proof_check


class TheSuite(VideoScene):
    def construct(self) -> None:
        result = mono("109 passed, 3 deselected", size=34, color=INK)
        check = proof_check(size=0.6)
        row = VGroup(check, result).arrange(RIGHT, buff=0.4)
        row.move_to([0, 0.3, 0])
        self.play(FadeIn(check, scale=1.3), FadeIn(result), run_time=0.8)
        self.wait(1.5)
        self.play(Indicate(row, color=PROOF, scale_factor=1.06), run_time=0.6)
        self.wait(12.2)
