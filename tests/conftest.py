from __future__ import annotations

from manim import tempconfig


def render_dry(scene_cls):
    """Run a scene's construct without writing video; return the finished scene."""
    with tempconfig({"dry_run": True, "quality": "low_quality", "disable_caching": True}):
        scene = scene_cls()
        scene.render()
    return scene
