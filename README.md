![A sign with leek in it](https://github.com/gyosh/leekcode/blob/master/logo.png "Leekcode")

# About

Ease the coding & testing phase during [Leetcode](https://leetcode.com/)'s contest.

With single run, all testcases will be executed and compared against your code's output.

Say no to server side execution!

# Dependency

Python 3.

# How To

1. Clone this repository.
2. Open the problem page you're trying to solve, like [this one](https://leetcode.com/contest/biweekly-contest-25/problems/kids-with-the-greatest-number-of-candies/).
3. Save the html page.
4. On your terminal, run
```
python3 /path/to/cloned/repository/main.py -l py /path/to/saved/problem/html > solution.py
```
(see next section for list of supported languages).

5. Code your solution in `solution.py`.
6. When done, run `python3 solution.py` to test your code against all sample testcases.
7. When ready for submission, cut the class portion of `solution.py` and submit it to Leetcode.

# Supported Language

- Python3
- C++

# Example Template

From [1431. Kids With the Greatest Number of Candies](https://leetcode.com/contest/biweekly-contest-25/problems/kids-with-the-greatest-number-of-candies/).

```python
# Kids With the Greatest Number of Candies - LeetCode Contest
from collections import *
import math

# ----- BEGIN CUT HERE -----

MOD = 1000000007
INF = 2123123123
EPS = 1e-9

class Solution:
    def kidsWithCandies(self, candies, extraCandies):
        # Your code goes here

# ------ END CUT HERE ------

nTc = 0
passing = 0

def runTc(_name, candies, extraCandies, _expected):
    global nTc
    nTc += 1

    _answer = Solution().kidsWithCandies(candies, extraCandies)
    if _expected == _answer:
        return 1
    print('Error at `{}`'.format(_name))
    print('Expected: {}'.format(str(_expected)))
    print('Got     : {}\n'.format(str(_answer)))
    return 0

candies = [2,3,5,1,3]
extraCandies = 3
_expected = [True,True,True,False,True]
passing += runTc('Example 1:', candies, extraCandies, _expected)

candies = [4,2,1,1,2]
extraCandies = 1
_expected = [True,False,False,False,False]
passing += runTc('Example 2:', candies, extraCandies, _expected)

candies = [12,1,12]
extraCandies = 10
_expected = [True,False,True]
passing += runTc('Example 3:', candies, extraCandies, _expected)


if passing == nTc:
    print('No error!')
else:
    print('FAIL!!!')

```

# Disclaimer

Tested only on recent contest problems.
No guarantee it works all the time, especially when the problem's HTML format changes, or if the problem uses objects in the IO.


# Contributing

Contributions as issue or pull request are welcome.

Be sure to add and run unit test if making any changes.
```
python -m unittest discover test
```

# License

MIT.
