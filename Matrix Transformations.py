inp = """
#@#
@@#
@@@
"""
print("before: ", inp)
inp = inp.strip().split("\n")

from copy import deepcopy
n = len(inp)
before = []
after = []
for i in range(n):
    before.append([s for s in inp[i]])
def rotate_90(pattern):
    pattern_ = deepcopy(pattern)
    for i in range(n):
        for j in range(n):
            pattern_[j][n-1-i] = pattern[i][j]
    return pattern_
def rotate_180(pattern):
    pattern_ = deepcopy(pattern)
    for i in range(n):
        for j in range(n):
            pattern_[n-1-i][n-1-j] = pattern[i][j]
    return pattern_
def rotate_270(pattern):
    pattern_ = deepcopy(pattern)
    for i in range(n):
        for j in range(n):
            pattern_[n-1-j][i] = pattern[i][j]
    return pattern_
def reflect_horizontal(pattern):
    pattern_ = deepcopy(pattern)
    for i in range(n):
        for j in range(n):
            pattern_[i][n-1-j] = pattern[i][j]
    return pattern_
def reflect_vertical(pattern):
    pattern_ = deepcopy(pattern)
    for i in range(n):
        for j in range(n):
            pattern_[n-1-i][j] = pattern[i][j]
    return pattern_
def print_pattern(pattern):
    print("after: ")
    for row in pattern:
        print("".join(row))
    print("")
print_pattern(rotate_90(before))
print_pattern(rotate_180(before))
print_pattern(rotate_270(before))
print_pattern(reflect_horizontal(before))
print_pattern(reflect_vertical(before))