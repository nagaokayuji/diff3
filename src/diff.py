from dataclasses import dataclass
from enum import Enum
from typing import Generic, Sequence, TypeVar

T = TypeVar('T')


class DiffType(Enum):
    KEEP = 'keep'
    INSERT = 'insert'
    REMOVE = 'remove'


@dataclass
class DiffOperation(Generic[T]):
    """
    Represents a single diff operation.

    Attributes:
        type: A DiffType, one of DiffType.KEEP, DiffType.INSERT, or DiffType.REMOVE.
        value: The element involved in the operation.
    """
    type: DiffType
    value: T

    def __str__(self) -> str:
        prefix = (
            ' ' if self.type == DiffType.KEEP
            else '+' if self.type == DiffType.INSERT
            else '-'  # DiffType.REMOVE
        )
        return f"{prefix} {self.value}"

    def __repr__(self) -> str:
        return str(self)


@dataclass
class EndpointAndHistory(Generic[T]):
    """
    Represents the furthest reaching point on a given diagonal and
    the corresponding diff operations (history) required to reach that point.

    Attributes:
        x: The index in sequence a reached so far.
        history: The list of DiffOperation objects representing the edit script.
    """
    x: int
    history: list[DiffOperation[T]]


def diff(a: Sequence[T], b: Sequence[T]) -> list[DiffOperation[T]]:
    """
    Compute the diff between sequences a and b using Myers' algorithm.

    Args:
        a: The original sequence.
        b: The target sequence.

    Returns:
        A list of DiffOperation objects representing the edit script to transform a into b.
    """
    n = len(a)
    m = len(b)
    max_length = n + m
    # frontier maps diagonal index k to the furthest EndpointAndHistory reached.
    frontier = {1: EndpointAndHistory(0, [])}  # fictitious endpoint (0, -1)

    for d in range(max_length + 1):  # Iterate over edit distances
        for k in range(-d, d + 1, 2):  # Iterate over diagonals
            # Decide whether to take an insertion (moving downwards in b)
            # or a deletion (moving rightwards in a)
            take_insertion = k == - \
                d or (k != d and frontier[k - 1].x < frontier[k + 1].x)
            prev = frontier[k + 1] if take_insertion else frontier[k - 1]
            current_history = prev.history[:]

            # Determine starting coordinates based on the chosen operation.
            x, y = (prev.x, prev.x -
                    k) if take_insertion else (prev.x + 1, prev.x - k + 1)
            if take_insertion and 0 <= y-1 < m:
                current_history.append(
                    DiffOperation(DiffType.INSERT, b[y - 1]))
            elif 0 <= x - 1 < n:
                current_history.append(
                    DiffOperation(DiffType.REMOVE, a[x - 1]))

            while x < n and y < m and a[x] == b[y]:
                current_history.append(DiffOperation(DiffType.KEEP, a[x]))
                x, y = x+1, y+1

            frontier[k] = EndpointAndHistory(x, current_history)

            if x >= n and y >= m:
                return current_history

    raise RuntimeError("Unreachable")
