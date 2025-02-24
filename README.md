# diff & diff3 in Python

A simple implementation of Myers' diff algorithm and a three-way merge algorithm (diff3) in Python.

## Features
- Implements **Myers' diff algorithm** for calculating differences between two sequences.
- Implements **diff3 algorithm** for three-way merging based on the following reference:
  - https://www.cis.upenn.edu/~bcpierce/papers/diff3-short.pdf
- **Minimal implementation** with no external dependencies.
- **Tested on Python 3.13**.
- **No guarantees** on correctness or robustness – use at your own risk.
- **MIT License**.

## Installation

To install the package, you can use `pip` to install directly from the GitHub repository:

```sh
pip install git+https://github.com/nagaokayuji/diff3.git
```

## Usage

### diff
```python
from diff3 import diff

original = list("ABCABBA")
target = list("CBABAC")
diff_result = diff(original, target)
print(diff_result)
# Output:
# [- A, - B,   C, + B,   A,   B, - B,   A, + C]
```

### diff3 (Three-way Merge)
```python
from diff3 import merge

base = ['a', 'b', 'c', 'd', 'e']
a = ['a', 'b', 'c', 'cc', 'd', 'e']
b = ['a', 'c', 'd', 'dd', 'e', 'f']

merged = merge(base, a, b)
print(merged)
# Output:
# a
# c
# cc
# d
# dd
# e
# f
```

## Running Tests
Unit tests are included. To run all tests, use:
```sh
PYTHONPATH=src python -m unittest discover test
```

## License
This project is licensed under the MIT License.

