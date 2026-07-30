from manim import DOWN, UP, AddTextLetterByLetter, FadeIn, FadeOut, Indicate, RoundedRectangle, Square, Transform, VGroup

from theme import INK, MAGENTA, VideoScene, bit_register, mono

HOLE_SIDE = 0.4
SOLVER_POS = [0, 2.7, 0]
SOLVER_W = 1.6
SOLVER_H = 0.9
FILL_VALUE = 0xAAAAAAAA
CHUNK_SIZE = 8


def fill_chunk(register: VGroup, start: int, end: int, bits: str, color: str) -> list:
    anims = []
    for i in range(start, end):
        digit = register.digits[i]
        new_digit = mono(bits[i], size=register.digit_size, color=color)
        new_digit.move_to(digit.get_center())
        anims.append(Transform(digit, new_digit))
    return anims


class TheFill(VideoScene):
    def construct(self) -> None:
        solver = RoundedRectangle(
            corner_radius=0.2, width=SOLVER_W, height=SOLVER_H, stroke_color=INK, stroke_width=2, fill_opacity=0
        )
        solver.move_to(SOLVER_POS)
        solver_label = mono("logic", size=20, color=INK).move_to(solver.get_center())
        hole = Square(side_length=HOLE_SIDE, stroke_color=MAGENTA, stroke_width=2, fill_opacity=0)
        hole.move_to(solver.get_top() + UP * 0.35)

        self.play(FadeIn(solver), FadeIn(solver_label), FadeIn(hole), run_time=0.6)
        self.wait(0.5)

        self.play(Indicate(solver, color=MAGENTA, scale_factor=1.08), run_time=0.6)
        self.play(Indicate(solver, color=MAGENTA, scale_factor=1.08), run_time=0.6)
        self.wait(0.3)

        self.play(FadeOut(solver), FadeOut(solver_label), FadeOut(hole), run_time=0.5)
        self.wait(0.3)

        register = bit_register(32, value=0, cell=0.38, color=INK)
        register.move_to([0, 0.3, 0])
        self.play(FadeIn(register), run_time=0.8)
        self.wait(0.6)

        bits = format(FILL_VALUE, "032b")
        for start in range(0, 32, CHUNK_SIZE):
            end = start + CHUNK_SIZE
            self.play(*fill_chunk(register, start, end, bits, MAGENTA), run_time=0.5)
            self.wait(0.2)
        self.wait(0.4)

        hex_text = mono("0xAAAAAAAA", size=30, color=MAGENTA)
        hex_text.next_to(register, DOWN, buff=0.6)
        self.play(AddTextLetterByLetter(hex_text), run_time=0.9)
        self.wait(0.6)
        self.play(Indicate(hex_text, color=MAGENTA, scale_factor=1.15), run_time=0.7)
        self.wait(17.4)
