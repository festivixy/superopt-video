from manim import DOWN, Create, Dot, FadeIn, FadeOut, Line, ReplacementTransform

from theme import BLUE, DIM, INK, VideoScene, mono


class EndCard(VideoScene):
    def construct(self) -> None:
        title = mono("github.com/smiles0527/superopt", size=36, color=INK)
        title.move_to([0, 0.4, 0])
        self.play(FadeIn(title), run_time=0.9)
        self.wait(0.5)

        underline = Line(
            title.get_left() + DOWN * 0.35,
            title.get_right() + DOWN * 0.35,
            color=BLUE,
            stroke_width=3,
        )
        self.play(Create(underline), run_time=1.2)
        self.wait(0.4)

        subtitle = mono("the code, the proofs, the mistakes", size=22, color=DIM)
        subtitle.next_to(underline, DOWN, buff=0.45)
        self.play(FadeIn(subtitle), run_time=0.7)
        self.wait(8.6)

        dot = Dot(radius=0.06, color=BLUE).move_to(underline.get_center())
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            ReplacementTransform(underline, dot),
            run_time=0.8,
        )
        self.wait(0.5)

        self.play(dot.animate.scale(0.001).set_opacity(0), run_time=1.0)
        self.wait(0.4)
