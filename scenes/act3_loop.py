from manim import DOWN, LEFT, RIGHT, UP, UR, Dot, FadeIn, FadeOut, Indicate, Line, MoveAlongPath, RoundedRectangle, Transform, VGroup

from theme import BLUE, DIM, INK, ORANGE, PROOF, VideoScene, loop_diagram, mono

CHIP_W = 0.5
CHIP_H = 0.3
EXAMPLES_ROUND1 = ["3", "7"]
COUNTEREXAMPLE = "12"


def make_chip() -> RoundedRectangle:
    return RoundedRectangle(
        corner_radius=0.05, width=CHIP_W, height=CHIP_H, stroke_color=INK, stroke_width=1.5, fill_color=INK, fill_opacity=0.12
    )


class GuessAndCheck(VideoScene):
    def construct(self) -> None:
        title = mono("guess and check", size=30, color=INK)
        title.to_edge(UP, buff=0.7)
        self.play(FadeIn(title), run_time=0.6)
        self.wait(0.6)

        diagram = loop_diagram()
        diagram.move_to([0, 0.4, 0])
        self.play(FadeIn(diagram), run_time=1.0)
        self.wait(1.2)

        examples = VGroup(*[mono(v, size=22, color=BLUE) for v in EXAMPLES_ROUND1]).arrange(DOWN, buff=0.25)
        examples.next_to(diagram.guess_node, LEFT, buff=0.9)
        self.play(FadeIn(examples, lag_ratio=0.2), run_time=0.6)
        self.wait(1.0)

        round_counter = mono("round 1", size=16, color=DIM).to_corner(UR, buff=0.6)
        self.play(FadeIn(round_counter), run_time=0.3)
        self.wait(0.3)

        chip1 = make_chip().move_to(diagram.forward_arrow.get_start())
        self.play(FadeIn(chip1, scale=0.6), run_time=0.3)
        self.play(MoveAlongPath(chip1, diagram.forward_arrow), run_time=0.9)
        self.wait(0.4)

        self.play(Indicate(diagram.check_node, color=ORANGE, scale_factor=1.15), FadeOut(chip1), run_time=0.7)
        self.wait(0.2)

        counter_dot = Dot(radius=0.09, color=ORANGE).move_to(diagram.back_arrow.get_start())
        self.play(FadeIn(counter_dot, scale=0.5), run_time=0.3)
        self.play(MoveAlongPath(counter_dot, diagram.back_arrow), run_time=0.9)

        new_example = mono(COUNTEREXAMPLE, size=22, color=ORANGE)
        new_example.next_to(examples, DOWN, buff=0.25)
        plus_one = mono("+1", size=15, color=ORANGE).next_to(new_example, RIGHT, buff=0.2)
        self.play(FadeOut(counter_dot), FadeIn(new_example), run_time=0.4)
        examples.add(new_example)
        self.play(FadeIn(plus_one, shift=UP * 0.1), run_time=0.3)
        self.wait(0.3)
        self.play(FadeOut(plus_one), run_time=0.3)

        round2_counter = mono("round 2", size=16, color=DIM).move_to(round_counter.get_center())
        self.play(Transform(round_counter, round2_counter), run_time=0.4)
        self.wait(0.5)

        chip2 = make_chip().move_to(diagram.forward_arrow.get_start())
        self.play(FadeIn(chip2, scale=0.6), run_time=0.3)
        self.play(MoveAlongPath(chip2, diagram.forward_arrow), run_time=0.9)
        self.wait(0.2)

        self.play(Indicate(diagram.check_node, color=PROOF, scale_factor=1.15), run_time=0.7)
        self.wait(0.5)

        pedestal_y = diagram.get_bottom()[1] - 0.9
        pedestal = Line([-1.0, pedestal_y, 0], [1.0, pedestal_y, 0], stroke_color=DIM, stroke_width=2)
        self.play(FadeIn(pedestal), run_time=0.3)
        self.play(
            chip2.animate.move_to(pedestal.get_center()).set_stroke(PROOF).set_fill(PROOF, opacity=0.3), run_time=0.8
        )
        self.wait(0.8)

        final_rounds = mono("2 rounds", size=18, color=PROOF).move_to(round_counter.get_center())
        self.play(Transform(round_counter, final_rounds), run_time=0.5)
        self.wait(17.7)
