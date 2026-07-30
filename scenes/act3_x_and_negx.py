from manim import DOWN, LEFT, FadeIn, Indicate, Line, VGroup

from theme import BLUE, DIM, INK, PROOF, VideoScene, bit_register, mono

X_VALUE = 0b01101100
NEGX_VALUE = 0b10010100
R_VALUE = 0b00000100
R_BLUE_INDEX = 5

CARD_Y = 3.0
ROW_X_Y = 1.0
ROW_NEGX_Y = -0.1
ROW_R_Y = -1.5
REG_CELL = 0.5


def make_card() -> VGroup:
    lines = ["t = -x", "r = x & t"]
    program = VGroup(*[mono(line, size=28, color=INK) for line in lines]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
    label = mono("2 instructions", size=18, color=PROOF).next_to(program, DOWN, buff=0.2)
    return VGroup(program, label)


class XAndNegX(VideoScene):
    def construct(self) -> None:
        card = make_card()
        card.move_to([0, CARD_Y, 0])
        self.play(FadeIn(card), run_time=0.8)
        self.wait(1.6)

        register_x = bit_register(8, value=X_VALUE, cell=REG_CELL, color=INK)
        register_x.move_to([0.4, ROW_X_Y, 0])
        label_x = mono("x", size=20, color=DIM).next_to(register_x, LEFT, buff=0.35)
        self.play(FadeIn(register_x), FadeIn(label_x), run_time=0.6)
        self.wait(1.0)

        register_negx = bit_register(8, value=NEGX_VALUE, cell=REG_CELL, color=INK)
        register_negx.move_to([0.4, ROW_NEGX_Y, 0])
        label_negx = mono("-x", size=20, color=DIM).next_to(register_negx, LEFT, buff=0.35)
        self.play(FadeIn(register_negx), FadeIn(label_negx), run_time=0.6)
        self.wait(0.6)

        and_symbol = mono("&", size=26, color=INK)
        and_symbol.move_to([register_x.get_left()[0], (ROW_X_Y + ROW_NEGX_Y) / 2, 0])
        self.play(FadeIn(and_symbol, scale=0.6), run_time=0.5)
        self.wait(0.8)

        divider = Line(
            [register_negx.get_left()[0], (ROW_NEGX_Y + ROW_R_Y) / 2, 0],
            [register_negx.get_right()[0], (ROW_NEGX_Y + ROW_R_Y) / 2, 0],
            stroke_color=DIM,
            stroke_width=1.5,
        )
        self.play(FadeIn(divider), run_time=0.3)
        self.wait(0.5)

        register_r = bit_register(8, value=R_VALUE, cell=REG_CELL, color=INK)
        register_r.move_to([0.4, ROW_R_Y, 0])
        register_r.digits[R_BLUE_INDEX].set_color(BLUE)
        label_r = mono("r", size=20, color=DIM).next_to(register_r, LEFT, buff=0.35)
        self.play(FadeIn(register_r), FadeIn(label_r), run_time=0.6)
        self.play(Indicate(register_r.digits[R_BLUE_INDEX], color=BLUE, scale_factor=1.8), run_time=0.8)
        self.wait(1.5)
        self.play(Indicate(card, color=PROOF, scale_factor=1.08), run_time=0.7)
        self.wait(19.0)
