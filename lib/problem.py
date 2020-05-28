import re
import html
import logging

from .phrase_iterator import PhraseIterator
from .vtype import VType
from .io_spec import IoSpec
from .testcase import TestCase
from .util import extract_variables

# <p><strong>Example 1:</strong></p>

# <pre><strong>Input:</strong> s1 = "abc", s2 = "xya"
# <strong>Output:</strong> true
# <strong>Explanation:</strong> "ayx" is a permutation of s2="xya" which can break to string "abc" which is a permutation of s1="abc".
# </pre>

class Problem:
    def __init__(self, problem_html):
        self.html = problem_html
        self.title = re.findall(r'<title>(.*?)</title>', problem_html)[0]
        self.io_spec, self.testcases = self.__unpack_testcases(problem_html)
        self.method_name = self.__extract_method_name(problem_html)
        logging.info(self.method_name)

    def __unpack_testcases(self, problem_html):
        io_spec = None
        tcs = []
        seen_title = set()
        tc_strs = re.findall(r'(?s)(<p><strong>Example.+?</pre>)', problem_html)
        for tc_str in tc_strs:
            it = PhraseIterator(tc_str)
            it.skip('<p><strong>')
            title = it.seek('</strong></p>')

            it.seek('<pre><strong>Input:</strong>')
            input_s = it.seek('<strong>Output:</strong>')
            output_s = it.seek_one(['<strong>', '<b>', '</pre>'])

            if title in seen_title:
                continue
            seen_title.add(title)

            input_s = html.unescape(input_s).strip()
            output_s = html.unescape(output_s).strip()

            input_vars = extract_variables(input_s)
            output = extract_variables(output_s, value_only=True)[0]

            if io_spec is None:
                io_spec_candidate = IoSpec(
                    input_names=[v[0] for v in input_vars],
                    input_vtypes=[v[1] for v in input_vars],
                    output_vtype=output[1]
                )
                if not io_spec_candidate.is_ambiguous():
                    io_spec = io_spec_candidate

            tcs.append(TestCase(
                title,
                io_spec,
                inputs=[v[2] for v in input_vars],
                output=output[2]
            ))
        return io_spec, tcs


    def __extract_method_name(self, problem_html):
        # Try C++
        s = re.findall(r'(?s)public:\n\s+[^ ]+ ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        

        # Try Python3
        s = re.findall(r'(?s)class Solution:\n\s+def ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        

        # Try Python
        s = re.findall(r'(?s)class Solution\(object\):\n\s+def ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        

        raise Exception('Unknown solution method name!')
