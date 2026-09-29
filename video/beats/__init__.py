from __future__ import annotations

import importlib

from kit.beat import BeatScene

MODULES = ("beats.intro", "beats.part1", "beats.part2", "beats.part3", "beats.part4", "beats.part5",
           "beats.part6", "beats.part7", "beats.part8", "beats.part9", "beats.part10")


def _class_name(beat_id: str) -> str:
    return "B_" + beat_id.replace(".", "_")


def all_beats(modules: tuple[str, ...] = MODULES) -> dict[str, type[BeatScene]]:
    found: dict[str, type[BeatScene]] = {}
    for name in modules:
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as err:
            if err.name == name:
                continue
            raise
        for obj in vars(module).values():
            if isinstance(obj, type) and issubclass(obj, BeatScene) and obj is not BeatScene and obj.beat_id:
                if obj.__name__ != _class_name(obj.beat_id):
                    raise ValueError(f"scene class {obj.__name__} has beat_id {obj.beat_id}; "
                                     f"expected class {_class_name(obj.beat_id)}")
                if obj.beat_id in found:
                    raise ValueError(f"two scenes for beat {obj.beat_id}")
                found[obj.beat_id] = obj
    return found
