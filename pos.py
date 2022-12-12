from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from vec import Vec


@dataclass
@total_ordering
class Pos:
    x: int
    y: int

    def __hash__(self):
        return 1009 * self.x + self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __add__(self, other: Vec):
        return Pos(self.x + other.dx, self.y + other.dy)