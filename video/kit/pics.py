from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Circle, Dot, Group, ImageMobject, Line, Polygon, Rectangle, RoundedRectangle, Square,
    Triangle, VGroup, VMobject,
)

from kit import style
from kit.style import BLUE, DIM, GREEN, INK, MAGENTA, ORANGE, STROKE

THIN = STROKE * 0.7
BG_BAR = "#1C2128"


def switch(on: bool, h: float = 0.8) -> VGroup:
    track = RoundedRectangle(corner_radius=h * 0.27, width=h * 0.55, height=h).set_stroke(INK, THIN).set_fill(BLUE, 0)
    r = h * 0.2
    knob = Circle(radius=r).move_to(track.get_center() + (UP if on else DOWN) * (h / 2 - r - h * 0.06))
    if on:
        knob.set_fill(BLUE, 1).set_stroke(BLUE, THIN)
        track.set_fill(BLUE, 0.12)
    else:
        knob.set_fill(BLUE, 0).set_stroke(DIM, THIN)
    s = VGroup(track, knob)
    s.on, s.h = on, h
    return s


def flipped(s: VGroup) -> VGroup:
    return switch(not s.on, s.h).move_to(s[0].get_center())


def switch_row(value: int, n: int = 8, h: float = 0.8, place_values: bool = False) -> VGroup:
    if not 0 <= value < (1 << n):
        raise ValueError(f"{value} does not fit in {n} switches")
    bits = format(value, f"0{n}b")
    switches = VGroup(*[switch(b == "1", h) for b in bits]).arrange(RIGHT, buff=h * 0.18)
    places = VGroup()
    if place_values:
        for s, p in zip(switches, range(n - 1, -1, -1)):
            places.add(style.mono(str(1 << p), h * 26, DIM).next_to(s, UP, buff=0.14))
    row = VGroup(switches, places)
    row.switches, row.places, row.value, row.n = switches, places, value, n

    def bit(i: int) -> VGroup:
        return switches[n - 1 - i]

    row.bit = bit
    return row


def pointer(color: str = ORANGE, size: float = 0.32) -> Triangle:
    return Triangle().rotate(np.pi).scale_to_fit_width(size).set_fill(color, 1).set_stroke(color, THIN)


def marble(color: str = ORANGE, r: float = 0.13) -> Circle:
    return Circle(radius=r).set_fill(color, 1).set_stroke(color, THIN)


def tile(name: str = "", color: str = INK, w: float = 1.1, h: float = 0.55) -> VGroup:
    body = RoundedRectangle(corner_radius=0.1, width=w, height=h).set_stroke(color, STROKE).set_fill(color, 0.08)
    label = style.mono(name, h * 42, color).move_to(body) if name else VGroup()
    t = VGroup(body, label)
    t.body, t.label = body, label
    return t


def tile_strip(names: Sequence[str], color: str = INK) -> VGroup:
    return VGroup(*[tile(n, color) for n in names]).arrange(RIGHT, buff=0.12)


def press_machine(w: float = 2.8) -> VGroup:
    h = w * 0.6
    body = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(INK, STROKE).set_fill(opacity=0)
    top = body.get_top()
    hopper = Polygon(top + LEFT * w * 0.28 + UP * 0.55, top + RIGHT * w * 0.28 + UP * 0.55,
                     top + RIGHT * w * 0.12, top + LEFT * w * 0.12).set_stroke(INK, STROKE).set_fill(opacity=0)
    chute = Rectangle(width=w * 0.18, height=h * 0.3).set_stroke(INK, STROKE).set_fill(opacity=0)
    chute.next_to(body, RIGHT, buff=0).align_to(body, DOWN).shift(UP * h * 0.12)
    plate = Line(LEFT * w * 0.34, RIGHT * w * 0.34).set_stroke(ORANGE, STROKE * 1.6).move_to(body.get_top() + DOWN * h * 0.22)
    rod = Line(plate.get_center(), body.get_top()).set_stroke(DIM, THIN)
    m = VGroup(body, hopper, chute, rod, plate)
    m.body, m.hopper, m.chute, m.plate = body, hopper, chute, plate
    return m


def bit_strip(bits: Sequence[int], cell: float = 0.2) -> VGroup:
    cells = VGroup()
    for b in bits:
        sq = Square(side_length=cell).set_stroke(DIM, THIN)
        sq.set_fill(BLUE, 0.9 if b else 0)
        sq.on = bool(b)
        cells.add(sq)
    cells.arrange(RIGHT, buff=0.03)
    strip = VGroup(cells)
    strip.cells = cells
    return strip


def dot_grid(rows: int, cols: int, color: str = DIM, gap: float = 0.28) -> VGroup:
    dots = VGroup(*[Dot(radius=0.045, color=color) for _ in range(rows * cols)])
    return dots.arrange_in_grid(rows=rows, cols=cols, buff=gap - 0.09)


def book_open(rows: Sequence[int] = (108, 104, 4, 111)) -> VGroup:
    left = RoundedRectangle(corner_radius=0.06, width=2.4, height=3.0).set_stroke(INK, STROKE).set_fill(opacity=0)
    right = left.copy().next_to(left, RIGHT, buff=0)
    spine = Line(left.get_corner(UP + RIGHT), left.get_corner(DOWN + RIGHT)).set_stroke(DIM, THIN)
    pages = VGroup()
    for page, values in ((left, rows[:2]), (right, rows[2:])):
        block = VGroup(*[bit_strip([int(b) for b in format(v, "08b")], cell=0.21) for v in values])
        block.arrange(DOWN, buff=0.55).move_to(page)
        pages.add(block)
    return VGroup(left, right, spine, pages)


def magnifier(size: float = 0.6) -> VGroup:
    ring = Circle(radius=size * 0.32).set_stroke(INK, STROKE)
    handle = Line(ring.point_at_angle(-np.pi / 4), ring.point_at_angle(-np.pi / 4) + np.array([size * 0.3, -size * 0.3, 0]))
    return VGroup(ring, handle.set_stroke(INK, STROKE * 1.4))


def loop_icon(size: float = 0.6) -> VGroup:
    arc = Arc(radius=size * 0.32, start_angle=0.3, angle=np.pi * 1.6).set_stroke(INK, STROKE)
    head = Triangle().scale_to_fit_width(size * 0.22).set_fill(INK, 1).set_stroke(INK, THIN)
    head.move_to(arc.get_end()).rotate(np.pi * 0.55)
    return VGroup(arc, head)


def bug(size: float = 0.6) -> VGroup:
    body = Circle(radius=size * 0.22).stretch(1.3, 1).set_stroke(ORANGE, STROKE)
    legs = VGroup(*[Line(body.get_center() + np.array([s * size * 0.2, y, 0]),
                         body.get_center() + np.array([s * size * 0.42, y + 0.06, 0])).set_stroke(ORANGE, THIN)
                    for s in (-1, 1) for y in (-0.1, 0.0, 0.1)])
    return VGroup(body, legs)


def bars_icon(size: float = 0.6) -> VGroup:
    bars = VGroup(*[Rectangle(width=size * 0.16, height=size * f).set_stroke(width=0).set_fill(c, 0.9)
                    for f, c in ((0.9, ORANGE), (0.55, DIM), (0.2, GREEN))])
    return bars.arrange(RIGHT, buff=size * 0.08, aligned_edge=DOWN)


def check(size: float = 0.5, color: str = GREEN) -> VMobject:
    m = VMobject().set_points_as_corners([np.array([-0.5, 0.0, 0]), np.array([-0.15, -0.4, 0]), np.array([0.55, 0.5, 0])])
    return m.scale(size).set_stroke(color, STROKE * 1.6)


def flag(size: float = 0.6) -> VGroup:
    pole = Line(DOWN * size * 0.4, UP * size * 0.4).set_stroke(INK, STROKE)
    cloth = Polygon(pole.get_top(), pole.get_top() + np.array([size * 0.45, -size * 0.12, 0]),
                    pole.get_top() + DOWN * size * 0.26).set_fill(BLUE, 0.8).set_stroke(BLUE, THIN)
    return VGroup(pole, cloth)


def mini_game(w: float = 3.2) -> VGroup:
    ground = Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(DIM, THIN).shift(DOWN * w * 0.22)
    blocks = VGroup(*[Square(side_length=w * 0.08).set_stroke(MAGENTA, THIN).set_fill(MAGENTA, 0.25)
                      .move_to(ground.get_center() + np.array([x * w, w * 0.04, 0])) for x in (0.1, 0.3)])
    head = Circle(radius=w * 0.035).set_fill(INK, 1).set_stroke(width=0)
    body = Line(UP * w * 0.02, DOWN * w * 0.07).set_stroke(INK, STROKE)
    legs = VMobject().set_points_as_corners([np.array([-w * 0.03, -w * 0.13, 0]), np.array([0, -w * 0.07, 0]),
                                             np.array([w * 0.03, -w * 0.13, 0])]).set_stroke(INK, STROKE)
    runner = VGroup(head.shift(UP * w * 0.055), body, legs).move_to(ground.get_center() + np.array([-w * 0.25, w * 0.08, 0]))
    coin = Circle(radius=w * 0.03).set_fill(ORANGE, 1).set_stroke(width=0).move_to(ground.get_center() + np.array([w * 0.3, w * 0.28, 0]))
    game = VGroup(ground, blocks, coin, runner)
    game.runner, game.coin = runner, coin
    return game


def program_machine(n_stations: int = 3, face: str | None = None, w: float = 3.0, covered: bool = True) -> VGroup:
    from kit.style import BG

    h = w * 0.45
    body = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(INK, STROKE).set_fill(opacity=0)
    inlet = Triangle().rotate(-np.pi / 2).scale_to_fit_height(h * 0.32).set_stroke(INK, THIN).set_fill(opacity=0)
    inlet.move_to(body.get_left())
    outlet = inlet.copy().move_to(body.get_right())
    stations = VGroup(*[Square(side_length=h * 0.34).set_stroke(DIM, THIN).set_fill(DIM, 0.25) for _ in range(n_stations)])
    stations.arrange(RIGHT, buff=h * 0.2).move_to(body)
    cover = RoundedRectangle(corner_radius=0.1, width=w * 0.8, height=h * 0.7).move_to(body)
    cover.set_fill(BG, 1 if covered else 0).set_stroke(INK if covered else DIM, THIN if covered else 0)
    parts = [body, inlet, outlet, stations, cover]
    face_m = None
    if face:
        face_m = style.math(face, 40).move_to(body)
        parts.append(face_m)
    m = VGroup(*parts)
    m.body, m.inlet, m.outlet, m.stations, m.cover, m.face = body, inlet, outlet, stations, cover, face_m
    return m


def and_gate(size: float = 0.7, color: str = INK) -> VGroup:
    left = Line(UP * size / 2, DOWN * size / 2).set_stroke(color, STROKE)
    top = Line(left.get_top(), left.get_top() + RIGHT * size * 0.45).set_stroke(color, STROKE)
    bottom = Line(left.get_bottom(), left.get_bottom() + RIGHT * size * 0.45).set_stroke(color, STROKE)
    arc = Arc(radius=size / 2, start_angle=-np.pi / 2, angle=np.pi).set_stroke(color, STROKE)
    arc.move_to(top.get_end() + DOWN * size / 2, aligned_edge=LEFT)
    ins = VGroup(*[Line(left.get_center() + np.array([-size * 0.35, y, 0]), left.get_center() + np.array([0, y, 0]))
                   .set_stroke(color, THIN) for y in (size * 0.22, -size * 0.22)])
    out = Line(arc.get_right(), arc.get_right() + RIGHT * size * 0.35).set_stroke(color, THIN)
    g = VGroup(left, top, bottom, arc, ins, out)
    g.inputs, g.output = ins, out
    return g


def lamp(on: bool = False, size: float = 0.9) -> VGroup:
    bulb = Circle(radius=size * 0.32).set_stroke(ORANGE if on else INK, STROKE)
    bulb.set_fill(ORANGE, 0.85 if on else 0)
    base = VGroup(*[Line(LEFT * size * 0.14, RIGHT * size * 0.14).set_stroke(INK, THIN).shift(DOWN * (size * 0.36 + k * 0.08))
                    for k in range(3)])
    rays = VGroup()
    if on:
        for a in np.linspace(0.3, np.pi - 0.3, 5):
            d = np.array([np.cos(a), np.sin(a), 0])
            rays.add(Line(d * size * 0.42, d * size * 0.62).set_stroke(ORANGE, THIN))
    g = VGroup(rays, bulb, base)
    g.bulb, g.on = bulb, on
    return g


def x_mark(size: float = 0.4, color: str = ORANGE) -> VGroup:
    return VGroup(Line(UP * size / 2 + LEFT * size / 2, DOWN * size / 2 + RIGHT * size / 2),
                  Line(UP * size / 2 + RIGHT * size / 2, DOWN * size / 2 + LEFT * size / 2)).set_stroke(color, STROKE * 1.4)


def paper(w: float = 1.8) -> VGroup:
    h = w * 1.3
    fold = w * 0.22
    outline = Polygon(np.array([-w / 2, h / 2, 0]), np.array([w / 2 - fold, h / 2, 0]), np.array([w / 2, h / 2 - fold, 0]),
                      np.array([w / 2, -h / 2, 0]), np.array([-w / 2, -h / 2, 0])).set_stroke(INK, STROKE).set_fill(opacity=0)
    lines = VGroup(*[Line(LEFT * w * 0.35, RIGHT * w * (0.35 if k % 3 else 0.15)).set_stroke(DIM, THIN) for k in range(6)])
    lines.arrange(DOWN, buff=h * 0.08).move_to(outline).shift(DOWN * h * 0.08)
    return VGroup(outline, lines)


def stamp(word: str, color: str = GREEN) -> VGroup:
    label = style.mono(word, 56, color)
    frame = RoundedRectangle(corner_radius=0.12, width=label.width + 0.5, height=label.height + 0.4).set_stroke(color, STROKE * 1.8)
    g = VGroup(frame.move_to(label), label).rotate(0.08)
    g.label = label
    return g


def domino(n_pairs: int, color: str = BLUE, gap: float = 0.32) -> VGroup:
    pairs = VGroup(*[VGroup(Dot(radius=0.09, color=color), Dot(radius=0.09, color=color)).arrange(DOWN, buff=0.14)
                     for _ in range(n_pairs)]).arrange(RIGHT, buff=gap)
    frame = RoundedRectangle(corner_radius=0.12, width=pairs.width + 0.35, height=pairs.height + 0.3).move_to(pairs)
    frame.set_stroke(DIM, THIN)
    g = VGroup(frame, pairs)
    g.dots = [d for p in pairs for d in p]
    g.pairs = pairs
    return g


def tree(depth: int = 3, width: float = 7.0, level_gap: float = 1.0) -> VGroup:
    nodes = VGroup()
    edges = VGroup()
    positions = []
    for level in range(depth + 1):
        count = 2 ** level
        for k in range(count):
            x = -width / 2 + width * (k + 0.5) / count
            positions.append(np.array([x, -level * level_gap, 0.0]))
    for p in positions:
        nodes.add(Circle(radius=0.13).set_stroke(INK, THIN).set_fill(BLUE, 0.35).move_to(p))
    for i in range(1, len(positions)):
        edges.add(Line(positions[(i - 1) // 2], positions[i], buff=0.13).set_stroke(DIM, THIN))
    t = VGroup(edges, nodes)
    t.nodes, t.edges = nodes, edges
    t.leaves = nodes[2 ** depth - 1:]

    def subtree(i: int) -> list[int]:
        out, frontier = [], [i]
        while frontier:
            j = frontier.pop()
            if j < len(nodes):
                out.append(j)
                frontier += [2 * j + 1, 2 * j + 2]
        return out

    t.subtree = subtree
    return t


def screenshot(filename: str, url: str, width: float = 8.0) -> Group:
    import facts

    path = facts.ASSETS / "web" / filename
    if not path.exists():
        raise FileNotFoundError(f"no screenshot at {path}")
    image = ImageMobject(str(path)).scale_to_fit_width(width)
    bar_h = 0.42
    bar = RoundedRectangle(corner_radius=0.12, width=width, height=bar_h + 0.12).set_stroke(DIM, THIN).set_fill(BG_BAR, 1)
    bar.next_to(image, UP, buff=0)
    dots = VGroup(*[Circle(radius=0.06).set_stroke(width=0).set_fill(c, 1) for c in (MAGENTA, ORANGE, GREEN)])
    dots.arrange(RIGHT, buff=0.08).move_to(bar.get_left() + RIGHT * 0.4 + UP * 0.03)
    address = style.mono(url, 16, DIM)
    address.move_to(bar).shift(UP * 0.03).align_to(dots, LEFT).shift(RIGHT * 0.55)
    border = Rectangle(width=image.width, height=image.height).move_to(image).set_stroke(DIM, THIN).set_fill(opacity=0)
    g = Group(bar, dots, address, image, border)
    g.image, g.bar, g.url = image, bar, address
    return g
