from manim import DOWN, LEFT, RIGHT, AnimationGroup, Dot, FadeIn, FadeOut, RoundedRectangle, Transform, VGroup, Wiggle

from theme import DIM, INK, MAGENTA, ORANGE, VideoScene, mono

CODE_LINES_TEXT = [
    "t = x * 2",
    "u = t + 0",
    "v = u",
    "w = v",
    "result = w",
]


class TidyUpEditor(VideoScene):
    def construct(self) -> None:
        code_lines = [mono(t, size=24, color=DIM) for t in CODE_LINES_TEXT]
        code = VGroup(*code_lines).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        code.move_to([-4.1, 0.0, 0])

        compiler_box = RoundedRectangle(
            corner_radius=0.25, width=3.0, height=1.6, stroke_color=INK, stroke_width=2, fill_opacity=0
        )
        compiler_box.move_to([2.4, 0.7, 0])
        compiler_label = mono("compiler", size=26, color=INK).move_to(compiler_box.get_center())

        bag_shape = RoundedRectangle(
            corner_radius=0.3, width=1.1, height=0.85, stroke_color=DIM, stroke_width=2, fill_opacity=0
        )
        bag_shape.move_to(compiler_box.get_corner(DOWN + RIGHT) + [0.15, -0.25, 0])
        bag_dots = VGroup(*[Dot(radius=0.06, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        bag_dots.move_to(bag_shape.get_center())
        bag = VGroup(bag_shape, bag_dots)

        self.play(FadeIn(code, lag_ratio=0.15), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(compiler_box), FadeIn(compiler_label), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(bag), run_time=0.6)
        self.wait(1.5)

        chip1 = mono("x*2 -> x<<1", size=20, color=MAGENTA)
        chip1.move_to(bag.get_center())
        self.play(FadeIn(chip1, scale=0.5), run_time=0.3)
        self.wait(0.3)
        target1 = code_lines[0].get_right() + RIGHT * 0.7
        self.play(chip1.animate.move_to(target1), run_time=0.7)
        self.wait(0.3)
        new_line0 = mono("t = x << 1", size=24, color=DIM).move_to(code_lines[0], aligned_edge=LEFT)
        self.play(
            FadeOut(chip1),
            Transform(code_lines[0], new_line0),
            FadeOut(code_lines[4]),
            run_time=0.7,
        )
        self.wait(1.8)

        chip2 = mono("t+0 -> t", size=20, color=MAGENTA)
        chip2.move_to(bag.get_center())
        self.play(FadeIn(chip2, scale=0.5), run_time=0.3)
        self.wait(0.3)
        target2 = code_lines[1].get_right() + RIGHT * 0.7
        self.play(chip2.animate.move_to(target2), run_time=0.7)
        self.wait(0.3)
        new_line1 = mono("u = t", size=24, color=DIM).move_to(code_lines[1], aligned_edge=LEFT)
        self.play(
            FadeOut(chip2),
            Transform(code_lines[1], new_line1),
            FadeOut(code_lines[3]),
            run_time=0.7,
        )
        self.wait(1.8)

        flicker = Dot(radius=0.08, color=MAGENTA).move_to(bag.get_center())
        self.play(FadeIn(flicker, scale=0.4), run_time=0.15)
        self.play(flicker.animate.move_to(code_lines[2].get_center()), run_time=0.35)
        self.play(FadeOut(flicker), FadeOut(code_lines[2]), run_time=0.4)
        self.wait(1.3)

        dust = VGroup(*[Dot(radius=0.03, color=DIM) for _ in range(5)])
        for i, d in enumerate(dust):
            d.move_to(bag.get_center() + DOWN * 0.5 + RIGHT * (i - 2) * 0.15)
        self.play(
            Wiggle(bag),
            AnimationGroup(*[FadeIn(d, shift=DOWN * 0.3) for d in dust], lag_ratio=0.1),
            run_time=1.0,
        )
        self.wait(0.4)
        self.play(FadeOut(dust), run_time=0.4)
        self.wait(1.0)

        remaining = VGroup(code_lines[0], code_lines[1])
        ghost = mono("u = x << 1", size=22, color=DIM)
        ghost.set_opacity(0.0)
        ghost.next_to(remaining, DOWN, buff=0.7, aligned_edge=LEFT)
        self.add(ghost)
        self.play(ghost.animate.set_opacity(0.3), run_time=1.0)
        self.wait(0.8)
        self.play(ghost.animate.set_opacity(0.08), run_time=1.0)
        self.wait(0.5)
        self.play(ghost.animate.set_opacity(0.28), run_time=1.0)
        self.wait(2.5)

        hover = mono("shortest?", size=22, color=ORANGE)
        hover.set_opacity(0.55)
        hover.next_to(remaining, RIGHT, buff=0.9)
        self.play(FadeIn(hover), run_time=0.7)
        self.wait(18.0)
