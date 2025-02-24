import time
import unittest

from diff3 import diff


class TestDiffPerformance(unittest.TestCase):

    def test_large_diff_performance(self):
        str_a = 'A'*1000
        str_b = 'B'*1000
        str_c = 'C'*1000

        large_seq1 = [str_a]*250 + [str_b]*500 + [str_c]*500 + [str_a]*250
        large_seq2 = [str_a]*250 + [str_c]*500 + [str_b]*500 + [str_a]*250

        start_time = time.time()
        _ = diff(large_seq1, large_seq2)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Performance test duration: {duration:.2f} seconds")
        self.assertLess(duration, 12, "Performance test took too long")


if __name__ == "__main__":
    unittest.main()
