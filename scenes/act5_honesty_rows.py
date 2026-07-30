from manim import DOWN, FadeIn, Indicate, RoundedRectangle, VGroup

from theme import DIM, INK, PROOF, VideoScene, mono

LABEL_X = -5.9
CHIP_X = -3.0
COMPILER_COUNT_X = -0.9
MACHINE_COUNT_X = 2.4
ROW1_Y = 1.2
ROW2_Y = -1.2
HEADER_Y = 2.6

ROWS = [
    ("rotate", "rol", "1", "3", "proven", PROOF, ROW1_Y),
    ("byte swap", "bswap", "2", "9", "best, not proven", DIM, ROW2_Y),
]


def make_chip(text: str) -> VGroup:
    box = RoundedRectangle(
        corner_radius=0.1, width=1.4, height=0.6, stroke_color=INK, stroke_width=2, fill_color=INK, fill_opacity=0.12
    )
    label = mono(text, size=20, color=INK).move_to(box.get_center())
    return VGroup(box, label)


class TheHonestyRows(VideoScene):
    def construct(self) -> None:
        compiler_header = mono("compiler", size=18, color=DIM).move_to([COMPILER_COUNT_X, HEADER_Y, 0])
        machine_header = mono("superopt", size=18, color=DIM).move_to([MACHINE_COUNT_X, HEADER_Y, 0])
        self.play(FadeIn(compiler_header), FadeIn(machine_header), run_time=0.6)
        self.wait(0.4)

        for label_text, chip_text, compiler_count, machine_count, tag_text, tag_color, y in ROWS:
            label = mono(label_text, size=22, color=DIM).move_to([LABEL_X, y, 0])
            chip = make_chip(chip_text).move_to([CHIP_X, y, 0])
            compiler_number = mono(compiler_count, size=28, color=INK).move_to([COMPILER_COUNT_X, y, 0])
            self.play(FadeIn(label), FadeIn(chip), FadeIn(compiler_number), run_time=0.7)
            self.play(Indicate(chip, color=PROOF, scale_factor=1.15), run_time=0.6)
            self.wait(0.3)

            machine_number = mono(machine_count, size=28, color=INK).move_to([MACHINE_COUNT_X, y, 0])
            tag = mono(tag_text, size=15, color=tag_color).next_to(machine_number, DOWN, buff=0.2)
            self.play(FadeIn(machine_number), run_time=0.6)
            self.play(FadeIn(tag), run_time=0.4)
            self.wait(0.8)

        self.wait(21.6)
