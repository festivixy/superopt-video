from manim import DOWN, LEFT, RIGHT, Create, FadeIn, Indicate, Line, RoundedRectangle, VGroup

from theme import DIM, INK, ORANGE, VideoScene, bit_register, mono


class DoesNotWork(VideoScene):
    def construct(self) -> None:
        card = RoundedRectangle(
            corner_radius=0.15, width=4.4, height=2.0, stroke_color=DIM, stroke_width=1.5, fill_opacity=0
        )
        card.move_to([-2.0, 0.4, 0])

        old_line = mono("n_constants=1", size=24, color=INK)
        old_line.move_to(card.get_center() + [0, 0.45, 0])
        strike = Line(
            old_line.get_left() + LEFT * 0.15,
            old_line.get_right() + RIGHT * 0.15,
            stroke_color=DIM,
            stroke_width=2,
        )

        new_line = mono("n_constants=2", size=24, color=INK)
        new_line.move_to(card.get_center() + [0, -0.45, 0])

        tag = RoundedRectangle(
            corner_radius=0.12, width=3.1, height=0.8, stroke_color=ORANGE, stroke_width=2, fill_opacity=0
        )
        tag.next_to(card, RIGHT, buff=0.7)
        tag_text = mono('"does not work"', size=20, color=ORANGE).move_to(tag.get_center())
        tag_group = VGroup(tag, tag_text)

        self.play(FadeIn(card), FadeIn(old_line), FadeIn(new_line), run_time=0.9)
        self.wait(0.4)
        self.play(Create(strike), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(tag_group), run_time=0.6)
        self.wait(1.3)

        self.wait(0.6)
        self.play(Indicate(tag_group, color=ORANGE, scale_factor=1.12), run_time=0.8)
        self.wait(0.6)

        ghost = bit_register(2, value=0, cell=0.35, color=DIM)
        ghost.cells.set_stroke(color=DIM)
        ghost.move_to([-5.5, -3.0, 0])
        ghost.cells.set_stroke(opacity=0)
        ghost.digits.set_fill(opacity=0)
        self.add(ghost)

        connector = Line(
            tag.get_bottom() + DOWN * 0.05,
            ghost.get_top() + [0, 0.1, 0],
            stroke_color=DIM,
            stroke_width=1.5,
        )
        self.play(Create(connector), run_time=1.1)
        self.wait(0.3)
        self.play(
            ghost.cells.animate.set_stroke(opacity=0.32),
            ghost.digits.animate.set_fill(opacity=0.3),
            run_time=1.0,
        )
        self.wait(3.0)

        self.wait(1.0)
        self.play(Indicate(ghost, color=ORANGE, scale_factor=1.15), run_time=1.8)
        self.wait(4.0)
