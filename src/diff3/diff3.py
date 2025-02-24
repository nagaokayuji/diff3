from dataclasses import dataclass
from typing import Generic, Optional, Sequence, TypeVar

from .diff import DiffOperation, DiffType, diff

T = TypeVar('T')


@dataclass
class Chunk(Generic[T]):
    base: Sequence[T]
    a: Sequence[T]
    b: Sequence[T]

    @property
    def merged_str(self) -> str:
        sep1 = "<<<<<<<"
        sep2 = "======="
        sep3 = ">>>>>>>"

        if self.a == self.b:  # stable or falsely conflicting
            return '\n'.join(map(str, self.a))
        if self.base == self.a:  # changed in b
            return '\n'.join(map(str, self.b))
        if self.base == self.b:  # changed in a
            return '\n'.join(map(str, self.a))

        # truly conflicting
        return "\n".join((sep1, *map(str, self.a), sep2, *map(str, self.b), sep3))


class MappingsHelper(Generic[T]):
    def __init__(self,
                 base_lines: Sequence[T],
                 a_lines: Sequence[T],
                 b_lines: Sequence[T],
                 diff_ops_a: Sequence[DiffOperation[T]],
                 diff_ops_b: Sequence[DiffOperation[T]]):
        self.base_lines = base_lines
        self.a_lines = a_lines
        self.b_lines = b_lines
        self.matches_a = self.build_matches(diff_ops_a)
        self.matches_b = self.build_matches(diff_ops_b)

        assert (self.base_lines[k] == self.a_lines[v]
                for k, v in self.matches_a.items())
        assert (self.base_lines[k] == self.b_lines[v]
                for k, v in self.matches_b.items())

        assert len(self.matches_a) == len([
            d for d in diff_ops_a if d.type == DiffType.KEEP])
        assert len(self.matches_b) == len([
            d for d in diff_ops_b if d.type == DiffType.KEEP])

    @staticmethod
    def build_matches(diff_ops: Sequence[DiffOperation[T]]) -> dict[int, int]:
        """
        Returns the non-crossing matches from the diff operations.
        """
        mapping: dict[int, int] = {}
        index_base = 0
        index_mod = 0
        for op in diff_ops:
            if op.type == DiffType.KEEP:
                mapping[index_base] = index_mod
                index_base += 1
                index_mod += 1
            elif op.type == DiffType.REMOVE:
                index_base += 1
            elif op.type == DiffType.INSERT:
                index_mod += 1
        return mapping

    def next_mismatch(self, index_base: int, index_a: int, index_b: int) -> Optional[int]:
        """
        Returns the first index where a mismatch is found between the base and both
        modified texts from the current position (index_base).
        """
        max_len = len(self.base_lines)
        for i in range(0, max_len + 1):
            a_val = self.matches_a.get(index_base + i)
            b_val = self.matches_b.get(index_base + i)
            if a_val != index_a + i or b_val != index_b + i:
                return i

        return None

    def next_match(self, index_base: int) -> Optional[tuple[int, int, int]]:
        """
        Returns the first index where a match is found between the base and both
        modified texts after the current position (index_base).
        """
        for i in range(index_base, len(self.base_lines)):
            a_val = self.matches_a.get(i)
            b_val = self.matches_b.get(i)
            if a_val is not None and b_val is not None:
                return i, a_val, b_val

        return None


def diff3(base_lines: Sequence[T], a_lines: Sequence[T], b_lines: Sequence[T]) -> list[Chunk]:
    """
    3-way merge algorithm to combine changes from two modified texts (A and B)
    with respect to a common base text.
    """
    diff_ops_a = diff(base_lines, a_lines)
    diff_ops_b = diff(base_lines, b_lines)

    helper = MappingsHelper(base_lines, a_lines,
                            b_lines, diff_ops_a, diff_ops_b)

    result_chunks: list[Chunk[T]] = []
    index_base = 0
    index_a = 0
    index_b = 0

    while index_base < len(base_lines):
        offset = helper.next_mismatch(index_base, index_a, index_b)
        if offset is None:
            break  # skip and output the final stable chunk

        if offset == 0:  # unstable chunk
            next_match = helper.next_match(index_base)
            if next_match is None:
                break
            o, a, b = next_match
        else:  # stable chunk
            o = index_base + offset
            a = index_a + offset
            b = index_b + offset

        result_chunks.append(Chunk(
            base_lines[index_base:o], a_lines[index_a:a], b_lines[index_b:b]))

        index_base, index_a, index_b = o, a, b

    result_chunks.append(
        Chunk(base_lines[index_base:], a_lines[index_a:], b_lines[index_b:]))

    return result_chunks


def merge(base_lines: Sequence[T], a_lines: Sequence[T], b_lines: Sequence[T]) -> str:
    chunks = diff3(base_lines, a_lines, b_lines)
    return '\n'.join((chunk.merged_str for chunk in chunks if chunk.merged_str))
