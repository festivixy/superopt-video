from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, RoundedRectangle, VGroup

from theme import DIM, INK, PROOF, VideoScene, mono

CARD_WIDTH = 10.6
CARD_HEIGHT = 3.2
CARD_Y = 0.6


def make_pill(text: str) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.18, width=1.05, height=0.4, stroke_color=PROOF, stroke_width=2, fill_opacity=0
    )
    label = mono(text, size=15, color=PROOF).move_to(box.get_center())
    return VGroup(box, label)


class TheFiledIssue(VideoScene):
    def construct(self) -> None:
        card = RoundedRectangle(
            corner_radius=0.15,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            stroke_color=INK,
            stroke_width=1.5,
            fill_opacity=0,
        )
        card.move_to([0, CARD_Y, 0])
        self.play(Create(card), run_time=1.2)
        self.wait(0.3)

        title = VGroup(
            mono("Missed optimization:", size=24, color=INK),
            mono("bit-scan loops are not folded to x & (x-1)", size=24, color=INK),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        title.move_to(card.get_center() + [0, 0.7, 0])
        self.play(FadeIn(title), run_time=0.7)
        self.wait(0.6)

        pill = make_pill("Open")
        subtitle = mono("llvm/llvm-project  ·  issue #212908", size=18, color=DIM)
        meta_row = VGroup(pill, subtitle).arrange(RIGHT, buff=0.35)
        meta_row.next_to(title, DOWN, buff=0.5)
        meta_row.align_to(title, LEFT)
        self.play(FadeIn(meta_row), run_time=0.6)
        self.wait(11.8)

        everything = VGroup(card, title, meta_row)
        self.play(everything.animate.shift(UP * 9).set_opacity(0), run_time=1.8)
        self.wait(1.2)
