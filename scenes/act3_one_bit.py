from manim import AnimationGroup, FadeIn, FadeOut, Indicate, Square, Transform

from theme import BLUE, DIM, INK, ORANGE, VideoScene, bit_register, mono

VALUE = 0b00000000000000000110110000000000
SET_INDICES = [17, 18, 20, 21]
LOWEST_INDEX = 21
CLEAR_INDICES = [17, 18, 20]


class OneBitSurvives(VideoScene):
    def construct(self) -> None:
        register = bit_register(32, value=VALUE, cell=0.38, color=INK)
        register.move_to([0, 0, 0])
        self.play(FadeIn(register), run_time=1.0)
        self.wait(1.6)

        set_digits = [register.digits[i] for i in SET_INDICES]
        self.play(
            AnimationGroup(*[Indicate(d, color=BLUE, scale_factor=1.6) for d in set_digits], lag_ratio=0.15),
            run_time=1.0,
        )
        self.wait(0.5)
        self.play(
            AnimationGroup(*[Indicate(d, color=BLUE, scale_factor=1.6) for d in set_digits], lag_ratio=0.15),
            run_time=1.0,
        )
        self.wait(1.0)

        crosshair = Square(side_length=0.62, stroke_color=ORANGE, stroke_width=3, fill_opacity=0)
        crosshair.move_to(register.digits[SET_INDICES[0]].get_center())
        self.play(FadeIn(crosshair, scale=1.6), run_time=0.4)
        for i in SET_INDICES[1:]:
            self.play(crosshair.animate.move_to(register.digits[i].get_center()), run_time=0.4)
            self.wait(0.15)
        self.play(Indicate(crosshair, color=ORANGE, scale_factor=1.3), run_time=0.6)
        self.wait(0.8)

        clears = []
        for i in CLEAR_INDICES:
            digit = register.digits[i]
            new_digit = mono("0", size=register.digit_size, color=DIM).move_to(digit.get_center())
            clears.append(Transform(digit, new_digit))
        self.play(*clears, run_time=0.8)
        self.wait(1.0)

        lowest_digit = register.digits[LOWEST_INDEX]
        new_lowest = mono("1", size=register.digit_size, color=BLUE).move_to(lowest_digit.get_center())
        self.play(Transform(lowest_digit, new_lowest), run_time=0.5)
        self.play(Indicate(lowest_digit, color=BLUE, scale_factor=1.8), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(crosshair), run_time=0.5)
        self.wait(12.6)
