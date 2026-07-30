from manim import RIGHT, UP, FadeIn, Indicate, RoundedRectangle, Square, VGroup

from theme import INK, MAGENTA, VideoScene, mono

HOLE_SIDE = 0.4
CARD_Y = 1.5
SOLVER_POS = [3.8, -1.3, 0]
SOLVER_W = 2.0
SOLVER_H = 1.1


class TheHole(VideoScene):
    def construct(self) -> None:
        prefix = mono("r = x & ", size=36, color=INK)
        hole = Square(side_length=HOLE_SIDE, stroke_color=MAGENTA, stroke_width=2, fill_opacity=0)
        hole.next_to(prefix, RIGHT, buff=0.1)
        card = VGroup(prefix, hole)
        card.move_to([-1.0, CARD_Y, 0])

        self.play(FadeIn(card), run_time=0.7)
        self.wait(1.0)
        self.play(Indicate(hole, color=MAGENTA, scale_factor=1.6), run_time=0.7)
        self.wait(1.3)

        solver = RoundedRectangle(
            corner_radius=0.25, width=SOLVER_W, height=SOLVER_H, stroke_color=INK, stroke_width=2, fill_opacity=0
        )
        solver.move_to(SOLVER_POS)
        solver_label = mono("logic", size=26, color=INK).move_to(solver.get_center())
        self.play(FadeIn(solver), FadeIn(solver_label), run_time=0.6)
        self.wait(0.8)

        self.play(hole.animate.shift(UP * 0.6), run_time=0.5)
        self.wait(0.3)
        hover = solver.get_top() + UP * 0.35
        self.play(hole.animate.move_to(hover), run_time=1.1)
        self.wait(0.2)

        self.play(Indicate(hole, color=MAGENTA, scale_factor=1.8), run_time=0.8)
        self.play(Indicate(hole, color=MAGENTA, scale_factor=1.8), run_time=0.8)
        self.wait(15.8)
