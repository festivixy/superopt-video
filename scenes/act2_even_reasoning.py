from manim import DOWN, RIGHT, AnimationGroup, Dot, FadeIn, FadeOut, Indicate, VGroup

from theme import DIM, INK, VideoScene, mono

ROW_Y = 1.0
PAIR_BUFF = 0.22
GROUP_BUFF = 0.55


def make_pair() -> VGroup:
    d1 = Dot(radius=0.09, color=DIM)
    d2 = Dot(radius=0.09, color=DIM)
    return VGroup(d1, d2).arrange(RIGHT, buff=PAIR_BUFF)


def make_row(n_pairs: int) -> VGroup:
    pairs = [make_pair() for _ in range(n_pairs)]
    return VGroup(*pairs).arrange(RIGHT, buff=GROUP_BUFF)


class EvenPlusEven(VideoScene):
    def construct(self) -> None:
        row_a = make_row(3)
        row_a.move_to([-3.8, ROW_Y, 0])
        row_b = make_row(4)
        row_b.move_to([3.8, ROW_Y, 0])

        label_a = mono("even", size=22, color=DIM).next_to(row_a, DOWN, buff=0.4)
        label_b = mono("even", size=22, color=DIM).next_to(row_b, DOWN, buff=0.4)

        self.play(FadeIn(row_a), FadeIn(label_a), run_time=0.6)
        self.play(FadeIn(row_b), FadeIn(label_b), run_time=0.6)
        self.wait(1.8)

        pairs = list(row_a) + list(row_b)
        layout = VGroup(*[p.copy() for p in pairs])
        layout.arrange(RIGHT, buff=GROUP_BUFF)
        layout.move_to([0, ROW_Y, 0])
        self.play(
            *[p.animate.move_to(t.get_center()) for p, t in zip(pairs, layout)],
            FadeOut(label_a),
            FadeOut(label_b),
            run_time=1.3,
        )
        self.wait(1.0)

        self.play(
            AnimationGroup(*[Indicate(p, color=INK, scale_factor=1.4) for p in pairs], lag_ratio=0.1),
            run_time=1.4,
        )
        self.wait(2.0)

        digits = VGroup()
        fades_out = []
        fades_in = []
        for i, pair in enumerate(pairs):
            for j, dot in enumerate(pair):
                bit = "1" if (i + j) % 2 == 0 else "0"
                digit = mono(bit, size=16, color=INK).move_to(dot.get_center())
                digits.add(digit)
                fades_out.append(FadeOut(dot))
                fades_in.append(FadeIn(digit))

        self.play(*fades_out, *fades_in, run_time=1.0)
        self.wait(14.3)
