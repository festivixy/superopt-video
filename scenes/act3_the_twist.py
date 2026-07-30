from manim import DOWN, LEFT, UP, FadeIn, FadeOut, Transform, VGroup

from theme import BLUE, DIM, INK, ORANGE, PROOF, VideoScene, bit_register, mono


class TheBitWrap(VideoScene):
    def construct(self):
        register = bit_register(2, value=0, cell=1.0, color=BLUE)
        register.move_to(DOWN * 0.3)
        width_label = mono("loc_width = 2", size=28, color=DIM)
        width_label.next_to(register, DOWN, buff=0.7)

        self.play(FadeIn(register), FadeIn(width_label), run_time=1.0)

        decimal = mono("0", size=48, color=BLUE)
        decimal.next_to(register, buff=1.0)
        self.play(FadeIn(decimal), run_time=0.4)
        self.wait(0.8)

        for v in (1, 2, 3):
            new_decimal = mono(str(v), size=48, color=BLUE).move_to(decimal)
            bits = format(v, "02b")
            new_digit_mobs = [
                mono(bit, size=register.digit_size, color=BLUE).move_to(cell.get_center())
                for bit, cell in zip(bits, register.cells)
            ]
            self.play(
                Transform(decimal, new_decimal),
                *[Transform(d, nd) for d, nd in zip(register.digits, new_digit_mobs)],
                run_time=0.5,
            )
            self.wait(0.45)

        self.wait(1.0)

        constraint = mono("ULT(var, n_lines)", size=34, color=INK)
        constraint.to_edge(UP, buff=1.0)
        self.play(FadeIn(constraint), run_time=0.8)
        self.wait(1.0)

        constraint_4 = mono("ULT(var, 4)", size=34, color=INK).move_to(constraint)
        self.play(Transform(constraint, constraint_4), run_time=0.8)
        self.wait(1.2)

        cell0 = register.cells[0].get_center()
        cell1 = register.cells[1].get_center()
        pitch = cell1[0] - cell0[0]

        incoming = VGroup(
            mono("1", size=register.digit_size, color=BLUE),
            mono("0", size=register.digit_size, color=BLUE),
            mono("0", size=register.digit_size, color=BLUE),
        )
        start_offset = UP * 1.8
        incoming[0].move_to(cell0 + LEFT * pitch + start_offset)
        incoming[1].move_to(cell0 + start_offset)
        incoming[2].move_to(cell1 + start_offset)

        self.play(FadeIn(incoming), run_time=0.6)
        self.wait(0.6)

        self.play(
            FadeOut(register.digits),
            incoming.animate.shift(DOWN * 1.8),
            run_time=1.0,
        )

        falling = incoming[0]
        landed = VGroup(incoming[1], incoming[2])

        falling_orange = mono("1", size=register.digit_size, color=ORANGE).move_to(falling.get_center())
        self.play(Transform(falling, falling_orange), run_time=0.3)
        self.play(falling.animate.shift(DOWN * 1.6).set_opacity(0), run_time=0.6)
        self.remove(falling)

        new_decimal_0 = mono("0", size=48, color=BLUE).move_to(decimal)
        self.play(Transform(decimal, new_decimal_0), run_time=0.5)
        self.wait(0.8)

        constraint_0 = mono("ULT(var, 0)", size=34, color=ORANGE).move_to(constraint)
        self.play(Transform(constraint, constraint_0), run_time=0.8)
        self.wait(0.6)

        annotation = mono("no unsigned value is less than zero", size=22, color=DIM)
        annotation.next_to(constraint, DOWN, buff=0.5)
        self.play(FadeIn(annotation), run_time=0.6)
        self.wait(2.5)

        unsat = mono("unsat", size=100, color=ORANGE)
        unsat.move_to(constraint.get_center())
        self.play(FadeOut(annotation), run_time=0.3)
        self.play(FadeIn(unsat, scale=1.3), run_time=0.8)
        self.wait(3.5)

        self.play(
            FadeOut(unsat),
            FadeOut(register),
            FadeOut(landed),
            FadeOut(decimal),
            run_time=0.8,
        )
        self.wait(0.3)

        new_label = mono("loc_width = 3", size=28, color=DIM).move_to(width_label)
        self.play(Transform(width_label, new_label), run_time=0.6)

        register3 = bit_register(3, value=0, cell=1.0, color=INK)
        register3.move_to(register.get_center())
        self.play(FadeIn(register3), run_time=0.8)
        self.wait(1.2)

        cellA = register3.cells[0].get_center()
        cellB = register3.cells[1].get_center()
        cellC = register3.cells[2].get_center()

        incoming2 = VGroup(
            mono("1", size=register3.digit_size, color=BLUE),
            mono("0", size=register3.digit_size, color=BLUE),
            mono("0", size=register3.digit_size, color=BLUE),
        )
        start_offset2 = UP * 1.8
        incoming2[0].move_to(cellA + start_offset2)
        incoming2[1].move_to(cellB + start_offset2)
        incoming2[2].move_to(cellC + start_offset2)

        self.play(FadeIn(incoming2), run_time=0.6)
        self.wait(0.4)
        self.play(
            FadeOut(register3.digits),
            incoming2.animate.shift(DOWN * 1.8),
            run_time=1.0,
        )
        self.wait(1.5)

        constraint_final = mono("ULT(var, 4)", size=34, color=INK).move_to(constraint)
        self.play(Transform(constraint, constraint_final), run_time=0.8)
        self.wait(0.8)

        sat = mono("sat", size=48, color=PROOF)
        sat.next_to(constraint, DOWN, buff=0.5)
        self.play(FadeIn(sat, scale=1.2), run_time=0.7)
        self.wait(2.0)
