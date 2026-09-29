from __future__ import annotations

from manim import tempconfig


def render_dry(scene_cls):
    with tempconfig({"dry_run": True, "quality": "low_quality", "disable_caching": True}):
        scene = scene_cls()
        scene.render()
    return scene
