from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vec:
    dx: int
    dy: int


UP = Vec(0, -1)
DOWN = Vec(0, 1)
LEFT = Vec(-1, 0)
RIGHT = Vec(1, 0)
