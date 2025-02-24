import unittest

from diff3 import merge


class TestDiff3(unittest.TestCase):
    def test_no_conflict(self):
        # When both modified texts are the same as the base,
        # the merge result should simply reproduce the base.
        base = "a\nb\nc".split()
        a = "a\nb\nc".split()
        b = "a\nb\nc".split()
        expected = "a\nb\nc"
        self.assertEqual(merge(base, a, b), expected)

    def test_changed_in_a(self):
        # When a modifies the base, the merge result should reflect the changes.
        base = "a\nb\nc".split()
        a = "X\nc\nfoo\nbar".split()
        b = "a\nb\nc".split()
        expected = "X\nc\nfoo\nbar"
        self.assertEqual(merge(base, a, b), expected)

    def test_changed_in_b(self):
        # When b modifies the base, the merge result should reflect the changes.
        base = "a\nb\nc\nd".split()
        a = "a\nb\nc\nd".split()
        b = "X\nc\nfoo\nbar\nxxx\nzzz".split()
        expected = "X\nc\nfoo\nbar\nxxx\nzzz"
        self.assertEqual(merge(base, a, b), expected)

    def test_changed_in_both_without_conflict_1(self):
        # When a and b modify the base in the same way, the merge result should reflect the changes.
        base = "a\nb\nc\nd\ne_removed\nf".split()
        a = "a_changed\na_added\nb\nc\nd\nf".split()
        b = "a\nb\nc_changed\nd\nf".split()
        expected = "a_changed\na_added\nb\nc_changed\nd\nf"
        self.assertEqual(merge(base, a, b), expected)

    def test_changed_in_both_without_conflict_2(self):
        base = ['a', 'b', 'c', 'd', 'e']
        a = ['a', 'b', 'c', 'cc', 'd', 'e']
        b = ['a', 'c', 'd', 'dd', 'e', 'f']
        expected = '\n'.join(('a', 'c', 'cc', 'd', 'dd', 'e', 'f'))
        self.assertEqual(
            merge(base, a, b), expected
        )

    def test_conflict(self):
        # When a and b modify the base differently, a conflict marker is expected.
        base = "a\nb\nc\n".split()
        a = "a\nX\nX2\nX3\nc\n".split()
        b = "a\ny\nc\n".split()
        expected = "a\n<<<<<<<\nX\nX2\nX3\n=======\ny\n>>>>>>>\nc"
        self.assertEqual(merge(base, a, b), expected)


if __name__ == "__main__":
    unittest.main()
