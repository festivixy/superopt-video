from __future__ import annotations

import re

import pytest
from manim import MarkupText, Text

from boards.intro import BOARD as INTRO
from boards.part1 import BOARD as PART1
from boards.part2 import BOARD as PART2
from boards.part3 import BOARD as PART3
from boards.part4 import BOARD as PART4
from boards.part5 import BOARD as PART5
from boards.part6 import BOARD as PART6
from boards.part7 import BOARD as PART7
from boards.part8 import BOARD as PART8
from boards.part9 import BOARD as PART9
from boards.part10 import BOARD as PART10
from kit import style
from kit.beat import Write

MAX_WORDS = 2


def _texts(m):
    for x in m.get_family():
        if isinstance(x, (Text, MarkupText)):
            yield x


def _is_prose(t) -> bool:
    if getattr(t, "font", None) == style.MONO:
        return False
    plain = re.sub(r"<[^>]+>", "", t.original_text)
    words = [w for w in plain.split() if any(c.isalpha() for c in w)]
    return len(words) > MAX_WORDS


RECORDS = [(board.name, r) for board in (INTRO, PART1, PART2, PART3, PART4, PART5,
                                              PART6, PART7, PART8, PART9, PART10) for r in board.records if isinstance(r, Write)]


@pytest.mark.parametrize("board_name,record", RECORDS, ids=[f"{b}:{r.key}" for b, r in RECORDS])
def test_no_sentences_on_the_board(board_name, record):
    prose = [t.original_text for t in _texts(record.build()) if _is_prose(t)]
    assert not prose, f"{board_name}:{record.key} puts words on screen, draw it instead: {prose}"
