from manim import DOWN, LEFT, RIGHT, UL, FadeIn, Text, Transform, VGroup

from theme import DIM, INK, VideoScene, mono, proof_check

NAMES = [
    "test_synthesizes_isolate_rmb_at_32_bit",
    "test_synthesizes_branchless_absval_at_32_bit",
    "test_no_absval_program_of_length_two_or_less",
    "test_recovers_mask_constant_in_wiring",
    "test_no_isolate_rmb_program_of_length_one_or_less",
    "test_synthesized_program_passes_independent_fuzzer",
]

COUNTER_ANCHOR = [6.3, -3.3, 0]


def counter_label(text: str, color: str) -> Text:
    return mono(text, size=28, color=color).move_to(COUNTER_ANCHOR, aligned_edge=RIGHT)


class GreenSuite(VideoScene):
    def construct(self) -> None:
        rows = VGroup(*[mono(name, size=20, color=DIM) for name in NAMES])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.to_corner(UL, buff=0.8)
        self.play(FadeIn(rows), run_time=1.0)
        self.wait(0.4)

        counter = counter_label("0", DIM)
        self.play(FadeIn(counter), run_time=0.4)
        self.wait(0.3)

        check_x = rows.get_right()[0] + 0.7
        for i, row in enumerate(rows):
            check = proof_check(size=0.35).move_to([check_x, row.get_y(), 0])
            new_counter = counter_label(str(i + 1), DIM)
            self.play(FadeIn(check, scale=1.3), Transform(counter, new_counter), run_time=0.35)
            self.wait(0.12)

        self.wait(0.4)
        final_counter = counter_label("all green", INK)
        self.play(Transform(counter, final_counter), run_time=0.7)
        self.wait(18.9)
