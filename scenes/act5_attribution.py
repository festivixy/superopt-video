from manim import DOWN, FadeIn, VGroup

from theme import DIM, INK, VideoScene, mono

LINES = [
    ("Massalin", "Massalin — 1987 — the idea"),
    ("Solar-Lezama", "Solar-Lezama — 2006 — guess and check (CEGIS)"),
    ("Jha, Gulwani, Seshia, Tiwari", "Jha, Gulwani, Seshia, Tiwari — 2010 — the wiring"),
]


class StandingOn(VideoScene):
    def construct(self) -> None:
        rows = VGroup(*[mono(text, size=26, color=DIM, t2c={name: INK}) for name, text in LINES])
        rows.arrange(DOWN, buff=0.55)
        rows.move_to([0, 0.5, 0])

        self.wait(0.3)
        for row in rows:
            self.play(FadeIn(row, shift=DOWN * 0.15), run_time=0.7)
            self.wait(1.2)

        self.wait(12.2)
