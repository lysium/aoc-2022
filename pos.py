from __future__ import annotations

from dataclasses import dataclass
from vec import Vec


@dataclass(frozen=True, eq=True, order=True, repr=True)
class Pos:
    x: int
    y: int

    def __add__(self, other: Vec):
        return Pos(self.x + other.dx, self.y + other.dy)