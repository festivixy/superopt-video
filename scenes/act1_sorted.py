from manim import DOWN, LEFT, AnimationGroup, Brace, Create, FadeIn, VGroup

from theme import BLUE, DIM, INK, ORANGE, VideoScene, mono

SHORT_PROGRAMS = [
    (["x + x"], "1 instruction"),
    (["x * 2"], "1 instruction"),
    (["x << 1"], "1 instruction"),
]
LONG_PROGRAM = (["a = x * 4", "b = a - x", "c = b - x"], "3 instructions")

SCATTER = [
    [-4.6, 2.2, 0],
    [3.9, 2.6, 0],
    [-3.4, -2.3, 0],
    [4.3, -1.9, 0],
]


def make_card(lines: list, count_label: str, color: str) -> VGroup:
    if len(lines) == 1:
        program = mono(lines[0], size=30, color=color)
    else:
        program = VGroup(*[mono(line, size=24, color=color) for line in lines])
        program.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    label = mono(count_label, size=16, color=DIM)
    label.next_to(program, DOWN, buff=0.18)
    return VGroup(program, label)


class SortedByLength(VideoScene):
    def construct(self) -> None:
        cards = [make_card(lines, count, INK) for lines, count in SHORT_PROGRAMS]
        for card, pos in zip(cards, SCATTER):
            card.move_to(pos)

        self.play(
            AnimationGroup(*[FadeIn(c, scale=0.8) for c in cards], lag_ratio=0.35),
            run_time=1.6,
        )
        self.wait(1.4)

        long_card = make_card(LONG_PROGRAM[0], LONG_PROGRAM[1], DIM)
        long_card.move_to(SCATTER[3])
        self.play(FadeIn(long_card, scale=0.8), run_time=0.8)
        self.wait(1.3)

        order = [*cards, long_card]
        layout = VGroup(*[c.copy() for c in order])
        layout.arrange(DOWN, buff=0.35)
        layout.move_to([-1.6, 0.4, 0])
        self.play(
            *[c.animate.move_to(t.get_center()) for c, t in zip(order, layout)],
            run_time=1.8,
        )
        self.wait(1.0)

        tier = VGroup(*cards)
        bracket = Brace(tier, direction=LEFT, color=BLUE)
        self.play(Create(bracket), run_time=0.9)
        self.wait(1.1)

        question = mono("shortest?", size=30, color=ORANGE)
        question.move_to([4.2, 0.4, 0])
        self.play(FadeIn(question, scale=0.7), run_time=0.6)
        self.wait(14.2)
