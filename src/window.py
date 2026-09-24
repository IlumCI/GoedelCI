"""A fixed-size window over a stream of numbers.

Small on purpose. The loop's first milestones will be about this file, and a
milestone is only judgeable if what it asks for is small enough to be observed
in one test.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable


class Window:
    """The last `size` values pushed, and cheap summaries of them."""

    def __init__(self, size: int) -> None:
        if size < 1:
            raise ValueError("a window of no values summarises nothing")
        self.size = size
        self._values: deque[float] = deque(maxlen=size)

    def push(self, value: float) -> None:
        self._values.append(float(value))

    def extend(self, values: Iterable[float]) -> None:
        for v in values:
            self.push(v)

    @property
    def values(self) -> list[float]:
        return list(self._values)

    @property
    def full(self) -> bool:
        return len(self._values) == self.size

    def mean(self) -> float:
        if not self._values:
            raise ValueError("an empty window has no mean")
        return sum(self._values) / len(self._values)

    def peak(self) -> float:
        if not self._values:
            raise ValueError("an empty window has no peak")
        return max(self._values)
