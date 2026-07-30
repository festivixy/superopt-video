from manim import DOWN, PI, RIGHT, CurvedArrow, Line, RoundedRectangle, Scene, Square, Text, Triangle, VGroup, config

BG = "#000000"
INK = "#ECECEC"
DIM = "#6E7681"
BLUE = "#58A6FF"
ORANGE = "#FFB86B"
MAGENTA = "#FF7EE3"
PROOF = "#7EE787"
MONO = "Consolas"

C_KEYWORDS = {
    "#include": BLUE,
    "uint32_t": BLUE,
    "for": BLUE,
    "if": BLUE,
    "return": BLUE,
}

config.background_color = BG


class VideoScene(Scene):
    def setup(self):
        self.camera.background_color = BG


def mono(text: str, size: float = 24, color: str = INK, **kwargs) -> Text:
    return Text(text, font=MONO, font_size=size, color=color, **kwargs)


def machine(code_lines: list[str] | None = None, n_stations: int = 3, width: float = 3.2) -> VGroup:
    height = width * 0.55
    body = RoundedRectangle(corner_radius=0.18, width=width, height=height, stroke_color=INK, stroke_width=2.5, fill_opacity=0)

    chute = Triangle(stroke_color=INK, stroke_width=2, fill_color=INK, fill_opacity=0.25)
    chute.scale_to_fit_height(height * 0.32)
    chute.rotate(-PI / 2)
    inlet = chute.copy().move_to(body.get_left())
    outlet = chute.copy().move_to(body.get_right())

    unit = VGroup(body, inlet, outlet)
    unit.body = body
    unit.inlet = inlet
    unit.outlet = outlet

    if code_lines:
        code = VGroup(*[mono(t, size=22, color=INK) for t in code_lines])
        if len(code) > 1:
            code.arrange(DOWN, buff=0.15)
        if code.width > width * 0.78:
            code.scale_to_fit_width(width * 0.78)
        code.move_to(body.get_center())
        unit.add(code)
        unit.code = code
    else:
        station_size = height * 0.3
        stations = VGroup(
            *[Square(side_length=station_size, stroke_color=INK, stroke_width=1.5, fill_color=DIM, fill_opacity=0.4) for _ in range(n_stations)]
        )
        stations.arrange(RIGHT, buff=station_size * 0.7)
        stations.move_to(body.get_center())
        unit.add(stations)
        unit.stations = stations

    return unit


def bit_register(n_bits: int, value: int = 0, cell: float = 0.55, color: str = INK) -> VGroup:
    cells = VGroup(
        *[Square(side_length=cell, stroke_color=INK, stroke_width=2, fill_opacity=0) for _ in range(n_bits)]
    )
    cells.arrange(RIGHT, buff=0)
    digits = VGroup(*[mono("0", size=cell * 70) for _ in range(n_bits)])
    register = VGroup(cells, digits)
    register.cells = cells
    register.digits = digits
    register.n_bits = n_bits
    register.digit_size = cell * 70
    register.digit_color = color
    set_bits(register, value)
    return register


def loop_diagram(node_width: float = 2.6, node_height: float = 1.1, gap: float = 3.6) -> VGroup:
    guess_rect = RoundedRectangle(
        corner_radius=0.15, width=node_width, height=node_height, stroke_color=INK, stroke_width=2, fill_opacity=0
    )
    guess_rect.move_to([-gap / 2, 0, 0])
    guess_text = mono("guess", size=28, color=INK).move_to(guess_rect.get_center())
    guess_node = VGroup(guess_rect, guess_text)

    check_rect = RoundedRectangle(
        corner_radius=0.15, width=node_width, height=node_height, stroke_color=INK, stroke_width=2, fill_opacity=0
    )
    check_rect.move_to([gap / 2, 0, 0])
    check_text = mono("check", size=28, color=INK).move_to(check_rect.get_center())
    check_node = VGroup(check_rect, check_text)

    forward_arrow = CurvedArrow(
        guess_rect.get_top() + RIGHT * 0.3, check_rect.get_top() + RIGHT * -0.3, angle=-1.0, color=DIM, stroke_width=3
    )
    back_arrow = CurvedArrow(
        check_rect.get_bottom() + RIGHT * -0.3, guess_rect.get_bottom() + RIGHT * 0.3, angle=-1.0, color=DIM, stroke_width=3
    )

    diagram = VGroup(guess_node, check_node, forward_arrow, back_arrow)
    diagram.guess_node = guess_node
    diagram.check_node = check_node
    diagram.forward_arrow = forward_arrow
    diagram.back_arrow = back_arrow
    return diagram


def verdict(word: str, color: str, size: float = 72) -> Text:
    return mono(word.upper(), size=size, color=color)


def proof_check(size: float = 1.0, color: str = PROOF, stroke_width: float = 6) -> VGroup:
    check = VGroup(
        Line([-0.5, 0.0, 0], [-0.15, -0.4, 0], stroke_color=color, stroke_width=stroke_width),
        Line([-0.15, -0.4, 0], [0.55, 0.5, 0], stroke_color=color, stroke_width=stroke_width),
    )
    check.scale(size)
    return check


def set_bits(register: VGroup, value: int, color: str | None = None) -> VGroup:
    if color is not None:
        register.digit_color = color
    bits = format(value & ((1 << register.n_bits) - 1), f"0{register.n_bits}b")
    for cell, digit, bit in zip(register.cells, register.digits, bits):
        new_digit = mono(bit, size=register.digit_size, color=register.digit_color)
        new_digit.move_to(cell.get_center())
        digit.become(new_digit)
    return register
