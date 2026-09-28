from __future__ import annotations

import importlib

from kit.beat import BeatScene

MODULES = ("beats.intro", "beats.part1", "beats.part2")


def all_beats() -> dict[str, type[BeatScene]]:
    found: dict[str, type[BeatScene]] = {}
    for name in MODULES:
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as err:
            if err.name == name:  # that Part isn't built yet; its coverage test will say so
                continue
            raise
        for obj in vars(module).values():
            if isinstance(obj, type) and issubclass(obj, BeatScene) and obj is not BeatScene and obj.beat_id:
                if obj.beat_id in found:
                    raise ValueError(f"two scenes for beat {obj.beat_id}")
                found[obj.beat_id] = obj
    return found
