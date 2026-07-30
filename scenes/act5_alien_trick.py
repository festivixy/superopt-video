from manim import DOWN, RIGHT, Circle, Create, FadeIn, Line, RoundedRectangle, VGroup

from theme import DIM, MAGENTA, ORANGE, PROOF, VideoScene, mono, proof_check

CARD_Y = 1.1
BOUNDARY_RADIUS = 2.6


class TheAlienTrick(VideoScene):
    def construct(self) -> None:
        line_top = mono("m = x >> x", size=32, color=MAGENTA)
        line_mid = mono("y = x ^ m", size=28, color=DIM)
        line_bottom = mono("r = y - m", size=28, color=DIM)
        lines = VGroup(line_top, line_mid, line_bottom).arrange(DOWN, buff=0.3)
        lines.move_to([0, CARD_Y, 0])

        self.play(FadeIn(line_top), FadeIn(line_bottom), run_time=0.7)
        self.wait(0.7)
        self.play(FadeIn(line_mid, scale=1.3), run_time=0.7)
        self.wait(0.5)

        glow = RoundedRectangle(
            corner_radius=0.35,
            width=lines.width + 1.0,
            height=lines.height + 0.6,
            stroke_color=MAGENTA,
            stroke_width=4,
            fill_color=MAGENTA,
            fill_opacity=0.05,
        )
        glow.move_to(lines.get_center())
        glow.set_stroke(opacity=0.0)
        self.add(glow)
        self.play(glow.animate.set_stroke(opacity=0.6), run_time=0.8)
        self.play(glow.animate.set_stroke(opacity=0.15), run_time=0.8)
        self.play(glow.animate.set_stroke(opacity=0.6), run_time=0.8)
        self.play(glow.animate.set_stroke(opacity=0.15), run_time=0.8)

        boundary = Circle(radius=BOUNDARY_RADIUS, stroke_color=DIM, stroke_width=2, fill_opacity=0)
        boundary.move_to(lines.get_center())
        self.play(Create(boundary), run_time=1.0)
        self.wait(0.3)

        check = proof_check(size=0.3, color=PROOF).next_to(lines, DOWN, buff=0.5)
        self.play(glow.animate.set_stroke(color=PROOF, opacity=0.7), FadeIn(check, scale=1.2), run_time=0.7)
        self.wait(1.0)

        copy_card = lines.copy().scale(0.32)
        copy_glow = glow.copy().scale(0.32)
        copy_group = VGroup(copy_glow, copy_card)
        copy_group.move_to(lines.get_center())
        edge_point = boundary.get_right()
        self.play(copy_group.animate.move_to(edge_point), run_time=1.0)
        self.wait(0.2)

        outside_point = edge_point + RIGHT * 2.2
        self.play(
            copy_group.animate.move_to(outside_point),
            copy_glow.animate.set_stroke(color=ORANGE, opacity=0.0),
            run_time=1.0,
        )
        crack = VGroup(
            Line(outside_point + [-0.35, 0.28, 0], outside_point + [0.05, 0.0, 0], stroke_color=ORANGE, stroke_width=2),
            Line(outside_point + [0.05, 0.0, 0], outside_point + [-0.28, -0.32, 0], stroke_color=ORANGE, stroke_width=2),
        )
        self.play(FadeIn(crack), run_time=0.4)
        self.wait(16.4)
