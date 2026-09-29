from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

RATE = 2.1
HEAD = re.compile(r"^### (\S+) · .*$", re.M)
HOLD = re.compile(r"hold (\d+(?:\.\d+)?)s")
WORD = re.compile(r"[A-Za-z0-9'-]+")
END_OF_BEATS = "## Sources for the numbers"
NO_VOICE = "no voice"


@dataclass(frozen=True)
class Beat:
    id: str
    words: int
    hold: float


def parse(text: str) -> list[Beat]:
    body = text.split(END_OF_BEATS, 1)[0]
    for line in body.splitlines():
        if line.startswith("###") and not HEAD.match(line):
            raise ValueError(f"malformed beat header (expected '### <id> · <title>'): {line!r}")
    pieces = HEAD.split(body)
    beats: list[Beat] = []
    seen: set[str] = set()
    for beat_id, block in zip(pieces[1::2], pieces[2::2]):
        if beat_id in seen:
            raise ValueError(f"duplicate beat id {beat_id}")
        seen.add(beat_id)
        holds = HOLD.findall(block)
        if not holds:
            raise ValueError(f"beat {beat_id} has no 'hold Ns' on its Scene line")
        if len(holds) > 1:
            raise ValueError(f"beat {beat_id} has more than one 'hold Ns' (two beats merged?)")
        hold = HOLD.search(block)
        narration = " ".join(
            line[1:].strip() for line in block.splitlines() if line.startswith(">")
        )
        if not narration and NO_VOICE not in block:
            raise ValueError(f"beat {beat_id} has no narration lines (mark pictures-only beats '{NO_VOICE}')")
        beats.append(Beat(beat_id, len(WORD.findall(narration)), float(hold.group(1))))
    return beats


def durations(beats: list[Beat], rate: float = RATE) -> dict[str, float]:
    return {b.id: round(b.words / rate + b.hold, 1) for b in beats}


def module_source(timing: dict[str, float]) -> str:
    lines = "".join(f"    {beat_id!r}: {seconds},\n" for beat_id, seconds in timing.items())
    return "TIMING: dict[str, float] = {\n" + lines + "}\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    script = Path(args[0] if args else "script/script.md")
    out = Path(args[1] if len(args) > 1 else "video/timing.py")
    timing = durations(parse(script.read_text(encoding="utf-8")))
    out.write_text(module_source(timing), encoding="utf-8")
    print(f"wrote {len(timing)} beats to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
