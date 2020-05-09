# About

Ease the coding & testing phase during [Leetcode](https://leetcode.com/)'s contest.
With single run, all testcases will be executed and compared against your code's output.

# Dependency

Python 3.

# How To

1. Clone this repository.
2. Open the problem page you're trying to solve, like [this one](https://leetcode.com/contest/weekly-contest-187/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/).
3. Save the html page.
4. On your terminal, run `python3 /path/to/cloned/repository/main.py -l py /path/to/saved/problem/html > solution.py` (see next section for list of supported languages).
5. Code your solution in `solution.py`.
6. When done, run `python3 solution.py` to test your code against all sample testcases.
7. When ready for submission, cut the class portion of `solution.py` and submit it to Leetcode.

# Supported Language

- Python3
- C++

# Example Template

From [Problem 1438: Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit](https://leetcode.com/contest/weekly-contest-187/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/).

```python
from collections import *

# ----- BEGIN CUT HERE -----

class Solution:
    def longestSubarray(self, nums, limit):
      # Code your solution here

# ------ END CUT HERE ------

solution = Solution()

nTc = 0
passing = 0


nTc += 1
nums = [8,2,4,7];
limit = 4;
__expected = 2
__answer = solution.longestSubarray(nums, limit)
if __expected == __answer:
    passing += 1
else:
    print('Error at `Example 1:`')
    print('__expected: {}'.format(str(__expected)))
    print('Got     : {}'.format(str(__answer)))


nTc += 1
nums = [10,1,2,4,7,2];
limit = 5;
__expected = 4
__answer = solution.longestSubarray(nums, limit)
if __expected == __answer:
    passing += 1
else:
    print('Error at `Example 2:`')
    print('__expected: {}'.format(str(__expected)))
    print('Got     : {}'.format(str(__answer)))


nTc += 1
nums = [4,2,2,2,4,4,2,2];
limit = 0;
__expected = 3
__answer = solution.longestSubarray(nums, limit)
if __expected == __answer:
    passing += 1
else:
    print('Error at `Example 3:`')
    print('__expected: {}'.format(str(__expected)))
    print('Got     : {}'.format(str(__answer)))


if passing == nTc:
    print('No error!')
else:
    print('FAIL!!!')
```

# Disclaimer

Tested only on recent contest problems.
No guarantee it works all the time, especially when the problem's HTML format changes.


# License

MIT.


