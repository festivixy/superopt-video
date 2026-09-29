from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Circle, DashedLine, Group, Line, Rectangle, RoundedRectangle, VGroup

import facts
from boards.part8 import BOARD as PART8
from kit import board, draw, pics, style
from kit.beat import Board, Erase, Write
from kit.pics import THIN
from kit.style import BLUE, DIM, GREEN, INK, MAGENTA, ORANGE, STROKE

BEATS = ("9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7", "9.8")

JOBS = ("absval", "avg_ceil", "avg_floor", "bswap32", "clear_lowest_bit", "flp2", "isolate_lowest_zero",
        "isolate_rmb", "popcount", "rotl5", "sign", "smear_lowest_bit", "times_nine", "turn_off_trailing_ones")
PROVEN = 7
SCORES = (("clear_lowest_bit", 18, 98, 2), ("smear_lowest_bit", 19, 97, 2), ("isolate_rmb", 14, 97, 2))
BIT_SCAN = tuple(name for name, *_ in SCORES)
TRICK = ("m = x >> x", "y = x ^ m", "r = y - m")


def chip_label(text: str, color: str = INK, size: float = 24) -> VGroup:
    t = style.mono(text, size, color)
    frame = RoundedRectangle(corner_radius=0.1, width=t.width + 0.35, height=t.height + 0.28).set_stroke(color, THIN)
    g = VGroup(frame.move_to(t), t)
    g.frame, g.text = frame, t
    return g


def chip(name: str, w: float = 2.4, color: str = INK) -> VGroup:
    body = RoundedRectangle(corner_radius=0.12, width=w, height=w * 0.7).set_stroke(color, STROKE).set_fill(opacity=0)
    pins = VGroup()
    for k in range(4):
        y = body.get_top()[1] - body.height * (k + 0.8) / 4.6
        for x, d in ((body.get_left()[0], -1), (body.get_right()[0], 1)):
            pins.add(Line([x, y, 0], [x + d * 0.22, y, 0]).set_stroke(DIM, THIN))
    g = VGroup(pins, body, style.mono(name, w * 20, color).move_to(body))
    g.body = body
    return g


def _dash_card(lengths, color: str) -> VGroup:
    rows = VGroup(*[Line(LEFT * 0, RIGHT * n * 0.32).set_stroke(color, STROKE) for n in lengths])
    rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    for r, n in zip(rows, lengths):
        r.shift(RIGHT * 0.25 * (n % 2))
    frame = RoundedRectangle(corner_radius=0.12, width=rows.width + 0.6, height=rows.height + 0.5).set_stroke(DIM, THIN)
    card = VGroup(frame.move_to(rows), rows)
    card.rows = rows
    return card


def hackers_book():
    return pics.book_open().scale_to_fit_width(3.4).move_to([-5.2, 0.9, 0])


def jobs():
    chips = VGroup(*[chip_label(n, INK, 22) for n in JOBS])
    cols = VGroup(VGroup(*chips[:7]).arrange(DOWN, buff=0.2, aligned_edge=LEFT),
                  VGroup(*chips[7:]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)).arrange(RIGHT, buff=0.6, aligned_edge=UP)
    cols.move_to([1.5, 1.05, 0])
    cols.chips = chips
    return cols


def pair():
    lengths = (4, 6, 5, 3)
    py = _dash_card(lengths, BLUE)
    c = _dash_card(lengths, ORANGE)
    VGroup(py, c).arrange(RIGHT, buff=2.2)
    links = VGroup(*[DashedLine(a.get_right() + RIGHT * 0.1, b.get_left() + LEFT * 0.1, dash_length=0.08).set_stroke(DIM, THIN)
                     for a, b in zip(py.rows, c.rows)])
    tags = VGroup(style.mono(".py", 30, BLUE).next_to(py, LEFT, buff=0.3), style.mono(".c", 30, ORANGE).next_to(c, RIGHT, buff=0.3))
    g = VGroup(py, c, links, tags).move_to([1.5, -2.75, 0])
    g.py, g.c, g.links, g.tags = py, c, links, tags
    return g


def rigs():
    gcc = VGroup(draw.laptop_icon(), style.mono("gcc", 30, INK)).arrange(DOWN, buff=0.2)
    clang = VGroup(draw.browser_window(), style.mono("clang", 30, ORANGE)).arrange(DOWN, buff=0.2)
    return VGroup(gcc, clang).arrange(RIGHT, buff=1.2).move_to([-4.4, 2.3, 0])


ASM_SHOWN = 6


def _asm_rows():
    body = [l for l in facts.CLANG_ASM_LINES if not l.endswith(":")]
    shown = VGroup(*[style.mono(l, 22, INK) for l in body[:ASM_SHOWN]])
    dots = style.math(r"\vdots", 36, DIM)
    ret = style.mono("ret", 22, DIM)
    rows = VGroup(*shown, dots, ret).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    dots.shift(RIGHT * 0.9)
    return rows, shown, dots, ret


def asm():
    rows, shown, dots, ret = _asm_rows()
    ticks = VGroup(*[Line(LEFT * 0.12, RIGHT * 0.12).set_stroke(GREEN, STROKE).next_to(r, LEFT, buff=0.3) for r in shown])
    no = pics.x_mark(0.3).next_to(ret, LEFT, buff=0.22)
    frame = RoundedRectangle(corner_radius=0.14, width=rows.width + 1.3, height=rows.height + 0.5).set_stroke(DIM, THIN)
    frame.move_to(rows).shift(LEFT * 0.3)
    count = style.mono(str(facts.CLANG_CLEAR_LOWEST_BIT), 56, ORANGE).next_to(frame, RIGHT, buff=0.45)
    g = VGroup(frame, rows, ticks, no, count).move_to([-3.4, -1.25, 0])
    g.rows, g.ticks, g.no, g.count, g.dots = rows, ticks, no, count, dots
    return g


def badges():
    icons = (pics.check(0.45), pics.magnifier(0.55), style.math(r"\le", 44, BLUE), style.mono("—", 36, DIM))
    names = (("proven", GREEN), ("best found", INK), ("upper bound", BLUE), ("no result", DIM))
    rows = VGroup()
    for icon, (name, color) in zip(icons, names):
        slot = VGroup(icon).set_width(0.5) if icon.width > 0.5 else VGroup(icon)
        rows.add(VGroup(slot, style.serif(name, 32, color)).arrange(RIGHT, buff=0.35))
    rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    return rows.move_to([4.3, 1.55, 0])


def seven():
    dots = VGroup(*[Circle(radius=0.15).set_stroke(GREEN if i < PROVEN else DIM, THIN)
                    .set_fill(GREEN if i < PROVEN else DIM, 0.85 if i < PROVEN else 0.2) for i in range(len(JOBS))])
    dots.arrange_in_grid(rows=2, cols=7, buff=0.2)
    count = style.math(r"7 / 14", 52, GREEN).next_to(dots, RIGHT, buff=0.45)
    g = VGroup(dots, count).move_to([4.1, -1.9, 0])
    g.dots = dots
    return g


BAR_X = -2.4
BAR_MAX = 7.2
COLORS = (DIM, ORANGE, GREEN)


def legend():
    items = VGroup()
    for name, color in zip(("gcc", "clang", "superopt"), COLORS):
        sw = Rectangle(width=0.4, height=0.24).set_stroke(width=0).set_fill(color, 0.9)
        items.add(VGroup(sw, style.mono(name, 26, color)).arrange(RIGHT, buff=0.18))
    return items.arrange(RIGHT, buff=0.8).move_to([1.2, 3.35, 0])


def score_row(k: int):
    name, *values = SCORES[k]
    y = 1.9 - k * 2.1
    label = style.mono(name, 30, INK).move_to([BAR_X - 0.35, y, 0], aligned_edge=RIGHT)
    bars, nums = VGroup(), VGroup()
    for i, (v, color) in enumerate(zip(values, COLORS)):
        bar = Rectangle(width=max(0.08, BAR_MAX * v / 98), height=0.36).set_stroke(width=0).set_fill(color, 0.9)
        bar.move_to([BAR_X, y + 0.5 - i * 0.5, 0], aligned_edge=LEFT)
        bars.add(bar)
        nums.add(style.mono(str(v), 28, color).next_to(bar, RIGHT, buff=0.2))
    proof = pics.check(0.4).next_to(nums[2], RIGHT, buff=0.25)
    g = VGroup(label, bars, nums, proof)
    g.label, g.bars, g.nums, g.proof = label, bars, nums, proof
    return g


LOOP_STEPS = ("i++", "shl", "test", "jne")


def gcc_loop():
    tiles = VGroup(*[pics.tile(n, INK, w=1.2, h=0.6) for n in LOOP_STEPS])
    corners = ([-1.4, 0.9, 0], [1.4, 0.9, 0], [1.4, -0.9, 0], [-1.4, -0.9, 0])
    for t, p in zip(tiles, corners):
        t.move_to(p)
    arrows = VGroup(*[Line(tiles[i].get_center(), tiles[(i + 1) % 4].get_center(), buff=0.7)
                      .add_tip(tip_length=0.16).set_stroke(DIM if i < 3 else ORANGE, THIN) for i in range(4)])
    for a in arrows:
        a.get_tip().set_fill(a.get_color(), 1).set_stroke(a.get_color(), THIN)
    times = style.mono("×32", 44, ORANGE).move_to([0, 0, 0])
    name = style.mono("gcc", 32, INK).next_to(VGroup(tiles), UP, buff=0.45)
    strip = pics.bit_strip([0] * 8, cell=0.3).next_to(VGroup(tiles), DOWN, buff=0.5)
    g = VGroup(name, arrows, tiles, times, strip).move_to([-3.6, 0.65, 0])
    g.tiles, g.arrows, g.strip, g.times = tiles, arrows, strip, times
    return g


def clang_unrolled():
    copies = VGroup(*[VGroup(*[pics.tile("", DIM, w=0.28, h=0.2) for _ in range(3)]).arrange(RIGHT, buff=0.04)
                      for _ in range(32)]).arrange_in_grid(rows=8, cols=4, buff=(0.22, 0.14))
    name = style.mono("clang", 32, ORANGE).next_to(copies, UP, buff=0.45)
    times = style.mono("32×", 30, ORANGE).next_to(copies, RIGHT, buff=0.3)
    g = VGroup(name, copies, times).move_to([3.5, 0.75, 0])
    g.copies = copies
    return g


def blsr():
    t = pics.tile("blsr", GREEN, w=1.5, h=0.7)
    eq = style.math(r"= x \mathbin{\&} (x-1)", 44, GREEN)
    return VGroup(t, eq).arrange(RIGHT, buff=0.35).move_to([0, -2.9, 0])


def unused(loop, unrolled, target):
    links = VGroup()
    for src in (loop, unrolled):
        a = DashedLine(src.get_bottom() + DOWN * 0.1, target[0].get_top() + UP * 0.05, dash_length=0.1).set_stroke(DIM, THIN)
        links.add(VGroup(a, pics.x_mark(0.34).move_to(a.get_center())))
    return links


def unused_links():
    return unused(gcc_loop()[4], clang_unrolled()[1], blsr())


COL_X86, COL_MINE = -1.2, 3.2


def headers():
    x86 = chip("x86", 1.3).move_to([COL_X86, 2.75, 0])
    mine = style.mono("superopt", 30, GREEN).move_to([COL_MINE, 2.75, 0])
    return VGroup(x86, mine)


def _row(y: float, name: str, theirs, mine, mine_count):
    label = style.mono(name, 30, INK).move_to([-5.2, y, 0])
    theirs.move_to([COL_X86, y, 0])
    mine.move_to([COL_MINE, y, 0])
    mine_count.next_to(mine, RIGHT, buff=0.3)
    return VGroup(label, theirs, mine, mine_count)


def rotate_row():
    theirs = VGroup(pics.tile("rol", ORANGE), style.mono("1–2", 30, ORANGE)).arrange(RIGHT, buff=0.25)
    mine = pics.tile_strip(["shl", "lshr", "or"], GREEN)
    count = VGroup(style.mono("3", 36, GREEN), pics.check(0.4)).arrange(RIGHT, buff=0.2)
    return _row(1.0, "rotl5", theirs, mine, count)


def bswap_row():
    theirs = pics.tile("bswap", ORANGE, w=1.4)
    mine = VGroup(*[pics.tile("", BLUE, w=0.34, h=0.5) for _ in range(9)]).arrange(RIGHT, buff=0.06)
    count = style.math(r"\le 9", 44, BLUE)
    return _row(-0.9, "bswap32", theirs, mine, count)


def instruction_set():
    tiles = VGroup(*[pics.tile(op, DIM, w=0.95, h=0.46) for op in facts.OPS]).arrange(RIGHT, buff=0.08)
    box = RoundedRectangle(corner_radius=0.15, width=tiles.width + 0.4, height=tiles.height + 0.4).set_stroke(GREEN, THIN)
    box.move_to(tiles)
    reject = VGroup(pics.tile("rol", ORANGE, w=0.95, h=0.46), pics.x_mark(0.34)).next_to(box, RIGHT, buff=0.35)
    reject[1].move_to(reject[0])
    g = VGroup(box, tiles, reject).scale_to_fit_width(13.0).move_to([0, -2.95, 0])
    g.box, g.tiles, g.reject = box, tiles, reject
    return g


def trick():
    card = board.program_card(TRICK, size=34, colors={0: MAGENTA})
    return card.move_to([-4.3, 1.7, 0])


NEG_BITS = [1, 1, 1, 1, 1, 0, 1, 1] * 4
POS_BITS = [0, 0, 0, 1, 0, 1, 1, 0] * 4


def _case(y: float, sign: str, bits, fill: int, color: str, extra: str | None):
    x = pics.bit_strip(bits, cell=0.17)
    x.cells[0].set_stroke(color, STROKE)
    res = pics.bit_strip([fill] * 32, cell=0.17)
    for c in res.cells:
        c.set_fill(color, 0.9 if fill else 0).set_stroke(color if fill else DIM, THIN)
    lab_x = style.math(sign, 46)
    lab_r = style.math(r"x \gg x", 46, MAGENTA)
    top = VGroup(lab_x, x).arrange(RIGHT, buff=0.35)
    bottom = VGroup(lab_r, res).arrange(RIGHT, buff=0.35)
    bottom.next_to(top, DOWN, buff=0.35).align_to(top, RIGHT)
    g = VGroup(top, bottom)
    if extra:
        g.add(style.math(extra, 36, DIM).next_to(bottom, DOWN, buff=0.2).align_to(bottom, RIGHT))
    g.move_to([2.65, y, 0])
    g.x, g.res = x, res
    return g


def neg_case():
    return _case(1.75, r"x < 0", NEG_BITS, 1, ORANGE, None)


def pos_case():
    return _case(-1.25, r"x > 0", POS_BITS, 0, BLUE, r"x < 2^{x}")


def ring():
    card = trick()
    circle = Circle(radius=2.35).set_stroke(DIM, THIN).move_to(card)
    ok = pics.check(0.5).next_to(card, DOWN, buff=0.35)
    return VGroup(circle, ok)


def x86():
    return chip("x86", 2.4, INK).move_to([4.4, 2.1, 0])


def five():
    amount = pics.bit_strip([0] * 26 + [1, 0, 0, 0, 0, 0], cell=0.17)
    low = VGroup(*amount.cells[27:])
    box = RoundedRectangle(corner_radius=0.06, width=low.width + 0.14, height=low.height + 0.14).set_stroke(ORANGE, STROKE)
    box.move_to(low)
    lab = style.math("32", 40, BLUE).next_to(amount, LEFT, buff=0.3)
    zero = style.mono("0", 40, ORANGE).next_to(box, DOWN, buff=0.3)
    g = VGroup(lab, amount, box, zero).move_to([2.2, -0.55, 0])
    g.amount, g.box, g.zero = amount, box, zero
    return g


def wrong():
    eq = style.math(r"|32| \to -32", 56, ORANGE)
    return VGroup(eq, pics.x_mark(0.45).next_to(eq, RIGHT, buff=0.35)).move_to([3.0, -2.6, 0])


def writeup():
    doc = pics.paper(1.3)
    flag = pics.flag(0.7).set_color(ORANGE).next_to(doc, RIGHT, buff=0.05).align_to(doc, UP)
    return VGroup(doc, flag).move_to([-4.6, -2.45, 0])


def held():
    rows = VGroup(*[VGroup(pics.check(0.4), style.mono(n, 30, INK)).arrange(RIGHT, buff=0.3) for n in BIT_SCAN])
    return rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-3.6, 2.75, 0])


ISSUE_URL = "github.com/llvm/llvm-project/issues/212908"
NUMBER_BOX = (0.488, 0.395, 0.575, 0.485)


def issue():
    shot = pics.screenshot("llvm_issue.png", ISSUE_URL, width=11.4).move_to([0, -1.05, 0])
    img = shot.image
    left, top, right, bottom = NUMBER_BOX
    corner = img.get_corner(UP + LEFT)
    x0, x1 = corner[0] + left * img.width, corner[0] + right * img.width
    y0, y1 = corner[1] - top * img.height, corner[1] - bottom * img.height
    ring = RoundedRectangle(corner_radius=0.1, width=x1 - x0 + 0.25, height=y0 - y1 + 0.2).set_stroke(ORANGE, STROKE)
    ring.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    g = Group(shot, ring)
    g.shot, g.ring = shot, ring
    return g


BOARD = Board("part9", BEATS, (
    Write("9.1", "book", hackers_book),
    Write("9.1", "jobs", jobs),
    Write("9.1", "pair", pair),
    Erase("9.2", "book"),
    Erase("9.2", "jobs"),
    Erase("9.2", "pair"),
    Write("9.2", "rigs", rigs),
    Write("9.2", "asm", asm),
    Write("9.2", "badges", badges),
    Write("9.2", "seven", seven),
    Erase("9.3", "rigs"),
    Erase("9.3", "asm"),
    Erase("9.3", "badges"),
    Erase("9.3", "seven"),
    Write("9.3", "legend", legend),
    Write("9.3", "row0", lambda: score_row(0)),
    Write("9.3", "row1", lambda: score_row(1)),
    Write("9.3", "row2", lambda: score_row(2)),
    Erase("9.4", "legend"),
    Erase("9.4", "row0"),
    Erase("9.4", "row1"),
    Erase("9.4", "row2"),
    Write("9.4", "gcc_loop", gcc_loop),
    Write("9.4", "clang_unrolled", clang_unrolled),
    Write("9.4", "blsr", blsr),
    Write("9.4", "unused", unused_links),
    Erase("9.5", "gcc_loop"),
    Erase("9.5", "clang_unrolled"),
    Erase("9.5", "blsr"),
    Erase("9.5", "unused"),
    Write("9.5", "headers", headers),
    Write("9.5", "rotate_row", rotate_row),
    Write("9.5", "instruction_set", instruction_set),
    Write("9.5", "bswap_row", bswap_row),
    Erase("9.6", "headers"),
    Erase("9.6", "rotate_row"),
    Erase("9.6", "instruction_set"),
    Erase("9.6", "bswap_row"),
    Write("9.6", "trick", trick),
    Write("9.6", "neg_case", neg_case),
    Write("9.6", "pos_case", pos_case),
    Erase("9.7", "neg_case"),
    Erase("9.7", "pos_case"),
    Write("9.7", "ring", ring),
    Write("9.7", "x86", x86),
    Write("9.7", "five", five),
    Write("9.7", "wrong", wrong),
    Write("9.7", "writeup", writeup),
    Erase("9.8", "trick"),
    Erase("9.8", "ring"),
    Erase("9.8", "x86"),
    Erase("9.8", "five"),
    Erase("9.8", "wrong"),
    Erase("9.8", "writeup"),
    Write("9.8", "held", held),
    Write("9.8", "issue", issue),
), previous=PART8, wipe="swipe")
