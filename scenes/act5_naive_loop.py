from manim import DOWN, LEFT, Arrow, FadeIn, Indicate, Transform, VGroup

from theme import BLUE, C_KEYWORDS, DIM, INK, PROOF, VideoScene, bit_register, mono

LOOP_LINES = [
    "for (int i = 0; i < 32; i++) {",
    "    if (x & (1u << i))",
    "        return x ^ (1u << i);",
    "}",
]

REGISTER_VALUE = 0b00101000
FOUND_BIT = 3
REG_CELL = 0.6

CODE_X = -3.6
REG_X = 2.6
REG_Y = 0.6


def make_code_card() -> VGroup:
    lines = VGroup(*[mono(line, size=22, color=DIM, t2c=C_KEYWORDS) for line in LOOP_LINES])
    lines.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    return lines


def make_pointer(cell) -> Arrow:
    x = cell.get_center()[0]
    bottom = cell.get_bottom()[1]
    return Arrow(
        start=[x, bottom - 0.55, 0],
        end=[x, bottom - 0.1, 0],
        color=BLUE,
        stroke_width=5,
        max_tip_length_to_length_ratio=0.5,
        buff=0,
    )


class TheObviousWay(VideoScene):
    def construct(self) -> None:
        code = make_code_card()
        code.move_to([CODE_X, REG_Y, 0])
        self.play(FadeIn(code, lag_ratio=0.15), run_time=1.0)
        self.wait(0.8)

        register = bit_register(8, value=REGISTER_VALUE, cell=REG_CELL, color=INK)
        register.move_to([REG_X, REG_Y, 0])
        label = mono("x", size=20, color=DIM).next_to(register, LEFT, buff=0.35)
        self.play(FadeIn(register), FadeIn(label), run_time=0.7)
        self.wait(0.4)

        cell_index = register.n_bits - 1
        pointer = make_pointer(register.cells[cell_index])
        counter = mono("i = 0", size=18, color=BLUE).next_to(register.cells[cell_index], DOWN, buff=0.75)
        self.play(FadeIn(pointer, scale=0.6), FadeIn(counter), run_time=0.5)
        self.wait(0.5)

        for i in range(1, FOUND_BIT + 1):
            cell_index = register.n_bits - 1 - i
            cell = register.cells[cell_index]
            new_counter = mono(f"i = {i}", size=18, color=BLUE).next_to(cell, DOWN, buff=0.75)
            self.play(
                Transform(pointer, make_pointer(cell)),
                Transform(counter, new_counter),
                run_time=0.5,
            )
            self.wait(0.2)

        found_cell = register.n_bits - 1 - FOUND_BIT
        self.play(
            Indicate(register.digits[found_cell], color=PROOF, scale_factor=1.6),
            Indicate(pointer, color=PROOF, scale_factor=1.4),
            run_time=0.7,
        )
        self.wait(1.0)
        self.play(Indicate(code, color=DIM, scale_factor=1.05), run_time=0.6)
        self.wait(16.5)
