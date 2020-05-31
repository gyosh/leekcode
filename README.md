![A sign with leek in it](https://github.com/gyosh/leekcode/blob/master/logo.png "Leekcode")

# About

Ease the coding & testing phase during [Leetcode](https://leetcode.com/)'s contest by generating skeleton for execution against all sample cases, so you can focus on writing your solution.

With single run, all testcases will be executed and compared against your solution's output. Server side testing in Leetcode and retyping custom testcases over & over again is effectively eliminated.


# Example Template

From [1431. Kids With the Greatest Number of Candies](https://leetcode.com/contest/biweekly-contest-25/problems/kids-with-the-greatest-number-of-candies/).

```python
# Kids With the Greatest Number of Candies - LeetCode Contest
from collections import *
import math

# ----- BEGIN CUT HERE -----

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

# Dependency

Python 3.

# How To

1. Download the most [recent release](https://github.com/gyosh/leekcode/releases) or clone this repository.
2. Open the problem page you're trying to solve in the browser, like [this one](https://leetcode.com/contest/biweekly-contest-25/problems/kids-with-the-greatest-number-of-candies/).
3. Save the html page, say that the saved file is prob.html.
4. On your terminal, run
```
$ python3 /path/to/cloned/repository/main.py -l py /path/to/saved/problem/prob.html > solution.py
```
Here, we are generating template for Python3. See next section for list of supported languages.

5. Code your solution in `solution.py`.
6. When done, run `python3 solution.py` to test your code against all sample testcases. The script will tell you if there is no error or there is failing case(s).
7. When ready for submission, cut the class portion of `solution.py` and submit it to Leetcode.

See help for more complex use cases.
```
$ python3 /path/to/cloned/repository/main.py -h
usage: main.py [-h] -l {cpp,py} [-e HEADER] [-t BINARY_TREE] [-x] input

Generate template for Leetcode's contest problem, to ease coding & testing.

positional arguments:
  input                 The html file for downloaded problem page

optional arguments:
  -h, --help            show this help message and exit
  -l {cpp,py}, --language {cpp,py}
                        Language of the template to generate.
  -e HEADER, --header HEADER
                        A .txt file to be included in the generated code as
                        header (commonly for defining constants or common
                        functions).
  -t BINARY_TREE, --binary-tree BINARY_TREE
                        Comma separated indexes of the input parameters/output
                        to be treated as binary tree. Use 'i' prefix for input
                        followed by one based index, and 'o' for output. E.g:
                        "i2,o" means 2nd input parameter and output is binary
                        tree. You need to give this information since binary
                        tree is provided as list in Leetcode's testcase.
  -x, --skip-check      If set, will not check output with expected output.
                        Use this for multiple possible output problems.

```

# Supported Language

- Python3
- C++


# Disclaimer

Tested only on recent contest problems.
No guarantee it works for future contests, especially if the HTML format changes or if the problem uses complicated objects in the parameter/return type.

Use at your own risk!

# Contributing

Contributions as issue or pull request are welcome.

Be sure to add and run unit test if making any changes.
```
python -m unittest discover test
```

# License

MIT.
