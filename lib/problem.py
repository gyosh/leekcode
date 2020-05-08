import re
import logging

from .phrase_iterator import PhraseIterator
from .vtype import VType
from .io_spec import IoSpec
from .testcase import TestCase

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
            output_s = it.seek_one(['<strong>', '</pre>'])

            if title in seen_title:
                continue
            seen_title.add(title)

            input_s = input_s.strip()
            output_s = output_s.strip()

            input_vars = self.__extract_variables(input_s)
            output = self.__extract_variables(output_s, value_only=True)[0]

            if io_spec is None:
                io_spec = IoSpec(
                    input_names=[v[0] for v in input_vars],
                    input_vtypes=[v[1] for v in input_vars],
                    output_vtype=output[1]
                )

            tcs.append(TestCase(
                title,
                io_spec,
                inputs=[v[2] for v in input_vars],
                output=output[2]
            ))
        return io_spec, tcs


    def __extract_variables(self, s, value_only=False):
        result = []
        it = PhraseIterator(s + ',')

        def parse_type_and_value():
            c = it.current_char()

            vtype = None
            value = None
            if c == '"':
                vtype = VType(VType.STRING)
                it.skip('"')
                value = it.skip_r(r'[^"]+')
                it.skip('"')
            elif c in 'tf':
                vtype = VType(VType.BOOLEAN)
                value = True if c == 't' else False
                it.skip(str(value).lower())
            elif (c == '-') or (('0' <= c) and (c <= '9')):
                vtype = VType(VType.INTEGER)
                value = int(it.skip_r(r'[-0-9]+'))
            else:
                vtype = VType(VType.LIST)
                value = []
                it.skip('[')
                element_type = None
                while True:
                    element_type, element_value = parse_type_and_value()
                    value.append(element_value)
                    if not it.can_skip(','):
                        break
                    it.skip(',')
                vtype.set_child(element_type)
                it.skip(']')
            return vtype, value

        while not it.end():
            name = None
            if not value_only:
                name = it.skip_r(r'[_a-zA-Z0-9]+').strip()
                logging.info('Found variable name: `%s`', name)

                it.skip_r(r'\s*')
                it.skip_r('=')
                it.skip_r(r'\s*')
            vtype, value = parse_type_and_value()
            logging.info('Found variable type : value: `%s`: `%s`', vtype, value)
            result.append((name, vtype, value))
            it.skip_r(r'\s*')
            it.skip_r(r',')
            it.skip_r(r'\s*')
        return result


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
        s = re.findall(r'(?s)class Solution\(object\):\n\sdef ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        

        raise Exception('Unknown solution method name!')
