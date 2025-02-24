import unittest

from diff3.diff import DiffOperation, DiffType, diff


class TestDiff(unittest.TestCase):
    def _common_assertion(self, original: list, target: list):
        diff_ops = diff(original, target)
        self.assertEqual(self.apply_diff(diff_ops), target)
        edit_distance = sum(op.type != DiffType.KEEP for op in diff_ops)
        lcs_length = self.naive_lcs_len(original, target)
        self.assertEqual(edit_distance, len(original) +
                         len(target) - 2 * lcs_length)

    def apply_diff(self, diff_ops: list[DiffOperation]):
        result = []
        for op in diff_ops:
            if op.type == DiffType.KEEP:
                result.append(op.value)
            elif op.type == DiffType.INSERT:
                result.append(op.value)
            # DiffType.REMOVE: do nothing
        return result

    def naive_lcs_len(self, a: list, b: list):
        """
        Naive implementation of the Longest Common Subsequence (LCS) algorithm.
        """
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    def test_no_change(self):
        # When both sequences are identical, the diff should consist of KEEP operations.
        original = list("abcdef")
        target = list("abcdef")
        self._common_assertion(original, target)

    def test_insertion(self):
        # When target has an extra element, the diff should include an INSERT op.
        original = list("abc")
        target = list("axbc")
        self._common_assertion(original, target)

    def test_deletion(self):
        # When target removes an element, the diff should include a REMOVE op.
        original = list("abc")
        target = list("ac")
        self._common_assertion(original, target)

    def test_complex_cases(self):
        test_cases = [
            ([], []),
            (list("abc\nafads\ndef"), list("azcfasd\nfsa\ndef")),
            (list("AAAAAXXXXXXXYYYYYY"), list("AABXXEE<<CYIYYYYY")),
            (list("XYXYXYY"), [])
        ]
        for original, target in test_cases:
            self._common_assertion(original, target)

        if __name__ == "__main__":
            unittest.main()
