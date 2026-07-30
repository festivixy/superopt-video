from manim import DOWN, LEFT, RIGHT, UL, FadeIn, FadeOut, Indicate, VGroup

from act4_green_suite import NAMES
from theme import DIM, INK, PROOF, VideoScene, mono, proof_check

TIMES = ["1.2s", "4.8s", "0.9s", "2.3s", "5.1s", "1.7s"]
HARD_ROW = 4


class TheHonestRerun(VideoScene):
    def construct(self) -> None:
        rows = VGroup(*[mono(name, size=20, color=DIM) for name in NAMES])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        rows.to_corner(UL, buff=0.8)
        self.play(FadeIn(rows), run_time=1.0)
        self.wait(0.4)

        check_x = rows.get_right()[0] + 0.7
        checks = VGroup()
        time_labels = VGroup()
        for i, (row, value) in enumerate(zip(rows, TIMES)):
            self.wait(float(value[:-1]))

            check = proof_check(size=0.35).move_to([check_x, row.get_y(), 0])
            time_label = mono(value, size=16, color=DIM).next_to(check, RIGHT, buff=0.3)
            self.play(FadeIn(check, scale=1.3), FadeIn(time_label), run_time=0.3)
            if i == HARD_ROW:
                self.play(Indicate(time_label, color=PROOF, scale_factor=1.2), run_time=0.4)
            self.wait(0.2)
            checks.add(check)
            time_labels.add(time_label)

        self.wait(0.5)
        all_green = mono("all green", size=32, color=INK).move_to([0, -3.2, 0])
        self.play(FadeIn(all_green), run_time=0.6)
        self.wait(3.4)
        self.play(FadeOut(all_green), run_time=0.4)

        self.play(
            FadeOut(rows),
            FadeOut(checks),
            FadeOut(time_labels),
            run_time=0.8,
        )

        final_line = mono("a fast no is a suspicious no", size=34, color=INK)
        self.play(FadeIn(final_line), run_time=0.8)
        self.wait(8.6)
