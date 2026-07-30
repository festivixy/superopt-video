from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    UP,
    UL,
    UR,
    DecimalNumber,
    FadeIn,
    FadeOut,
    ValueTracker,
    always_redraw,
    linear,
    rate_functions,
)

from theme import BLUE, C_KEYWORDS, DIM, INK, VideoScene, mono

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def load_c_source() -> str:
    return (ASSETS / "clear_lowest_bit.c").read_text().strip()


def load_asm_lines() -> list[str]:
    lines = []
    for raw in (ASSETS / "clang_clear_lowest_bit.s").read_text().splitlines():
        line = raw.split("#", 1)[0].replace("\t", "    ").rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith(".") or stripped.endswith(":"):
            if stripped.endswith(":") and not stripped.startswith("."):
                lines.append(stripped)
            continue
        lines.append("        " + stripped)
    return lines


class TheScroll(VideoScene):
    def construct(self):
        code = mono(load_c_source(), size=26, t2c=C_KEYWORDS, line_spacing=0.9)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=1.5)
        self.wait(2.0)

        self.play(
            code.animate.scale(0.45).to_corner(UL, buff=0.4).set_opacity(0.5),
            run_time=1.0,
        )

        asm_lines = load_asm_lines()
        asm = mono("\n".join(asm_lines), size=20, color=DIM, line_spacing=0.7)
        asm.move_to(DOWN * (asm.height / 2 + 5))

        tracker = ValueTracker(0)
        counter = always_redraw(
            lambda: mono(f"{int(tracker.get_value())}", size=64, color=INK)
            .to_corner(UR, buff=0.6)
        )
        label = mono("instructions", size=24, color=DIM).to_corner(UR, buff=0.6)
        label.shift(DOWN * 1.1)

        self.add(asm, counter, label)
        total_shift = asm.height + 10
        self.play(
            asm.animate(rate_func=rate_functions.ease_in_quad).shift(
                UP * total_shift
            ),
            tracker.animate(rate_func=rate_functions.ease_in_quad).set_value(98),
            run_time=7.0,
        )
        self.remove(asm)
        self.wait(0.3)

        big = mono("98 instructions.", size=72, color=INK)
        self.play(FadeOut(counter), FadeOut(label), FadeIn(big), run_time=0.6)
        self.wait(1.5)

        self.remove(big, code)
        self.wait(0.5)

        answer = mono(
            "lea     eax, [rdi - 1]\nand     eax, edi",
            size=40,
            color=BLUE,
            line_spacing=1.1,
        )
        two = mono("2.", size=96, color=INK)
        two.next_to(answer, DOWN, buff=1.0)
        self.play(FadeIn(answer, lag_ratio=0.3), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(two, scale=0.8), run_time=0.8)
        self.wait(2.0)
