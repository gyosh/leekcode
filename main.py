import re
import logging
import argparse

from util import template_cpp, template_testcases_cpp

class VType:
    INTEGER = 'INTEGER'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    LIST = 'LIST'
    def __init__(self, vtype, inner_vtype=None):
        self.vtype = vtype
        self.inner_vtype = inner_vtype

    def __str__(self):
        if self.inner_vtype is None:
            return self.vtype
        return '{}<{}>'.format(self.vtype, self.inner_vtype)

    def set_inner_vtype(self, inner_vtype):
        self.inner_vtype = inner_vtype

    def is_type(self, vtype):
        return self.vtype == vtype

    def as_cpp(self):
        if self.vtype == self.INTEGER:
            return 'int'
        if self.vtype == self.BOOLEAN:
            return 'bool'
        if self.vtype == self.STRING:
            return 'string'
        if self.vtype == self.LIST:
            return 'vector<{}>'.format(self.inner_vtype.as_cpp())
        return '?'


class Variable:
    def __init__(self, name, vtype, value):
        self.name = name
        self.vtype = vtype
        self.value = value

    def as_param_cpp(self):
        if self.vtype.is_type(VType.LIST):
            return '{} &{}'.format(self.vtype.as_cpp(), self.name)
        return '{} {}'.format(self.vtype.as_cpp(), self.name)

    def as_init_cpp(self):
        return '{} {} = {};'.format(self.vtype.as_cpp(), self.name, self.value_as_cpp(self.value))

    @staticmethod
    def value_as_cpp(v):
        if type(v) is bool:
            return str(v).lower()
        if type(v) is str:
            return '"' + v + '"'
        if type(v) is list:
            return '{' +  ','.join([Variable.value_as_cpp(x) for x in v]) + '}'
        return str(v);


class TestCase:
    def __init__(self, title, input_params, output):
        self.title = title
        self.input_params = input_params
        self.output = output

    def get_params(self):
        return [Variable(v.name, v.vtype, None) for v in self.input_params]

    def get_output_type(self):
        return self.output.vtype

    def generate_cpp(self, method_name):
        return template_testcases_cpp.format(
            tc_name=self.title,
            inputs_init='\n    '.join([v.as_init_cpp() for v in self.input_params]),
            output_type=self.output.vtype.as_cpp(),
            output_value=Variable.value_as_cpp(self.output.value),
            method_name=method_name,
            param_names=', '.join([v.name for v in self.input_params])
        )


class PhraseIterator:
    def __init__(self, s):
        self.s = s
        self.p = 0
        self.len = len(s)

    def find_next(self, phrase):
        d = 0
        l_phrase = len(phrase)
        while self.p + d + l_phrase - 1 < self.len:
            match = True
            for i in range(l_phrase):
                if phrase[i] != self.s[self.p + d + i]:
                    match = False
                    break
            if match:
                return d
            d += 1
        return -1

    # Forward phrase
    def skip(self, phrase):
        if self.find_next(phrase) != 0:
            raise Exception('Unable to skip {}: `{}`'.format(phrase, self.__look_ahead()))
        self.p += len(phrase)

    def skip_r(self, rgx):
        cur_s = ''
        pattern = re.compile('^' + rgx + '$')
        while (self.p < self.len) and bool(re.match(pattern, cur_s + self.s[self.p])):
            cur_s += self.s[self.p]
            self.p += 1
        return cur_s

    def can_skip(self, phrase):
        return self.find_next(phrase) == 0

    # Find right after phrase
    def seek(self, phrase):
        d = self.find_next(phrase)
        if d == -1:
            raise Exception('Unable to seek {}: `{}`'.format(phrase, self.__look_ahead()))
        e_idx = self.p + d
        between = self.s[self.p:e_idx]
        self.p = e_idx + len(phrase)
        return between

    def seek_one(self, phrases):
        for p in phrases:
            if self.find_next(p) != -1:
                return self.seek(p)
        return -1

    def next_char(self):
        ret = self.s[self.p]
        self.p += 1
        return ret

    def prev_char(self):
        self.p -= 1
        ret = self.s[self.p]
        return ret

    def end(self):
        return self.p == self.len

    def __look_ahead(self, size=50):
        e_idx = min(self.p + size, self.len)
        return self.s[self.p:e_idx] + '...'


class Problem:
    def __init__(self, problem_html):
        self.html = problem_html
        self.testcases = self.__extract_testcases(problem_html)
        self.params = self.testcases[0].get_params()
        self.output_type = self.testcases[0].get_output_type()
        self.method_name = self.__extract_method_name(problem_html)

        logging.info(self.method_name)

# <p><strong>Example 1:</strong></p>

# <pre><strong>Input:</strong> s1 = "abc", s2 = "xya"
# <strong>Output:</strong> true
# <strong>Explanation:</strong> "ayx" is a permutation of s2="xya" which can break to string "abc" which is a permutation of s1="abc".
# </pre>
    def __extract_testcases(self, problem_html):
        tcs = []
        seen_title = set()
        tc_strs = re.findall(r'(?s)(<p><strong>Example.+?</pre>)', problem_html)
        for tc_str in tc_strs:
            it = PhraseIterator(tc_str)
            it.skip('<p><strong>')
            title = it.seek('</strong></p>')

            it.seek('<pre><strong>Input:</strong>')
            input_s = it.seek('<strong>Output:</strong>')

            output_s = ''
            if it.find_next('<strong>') != -1:
                output_s = it.seek('<strong>')
            else:
                output_s = it.seek('</pre>')

            if title in seen_title:
                continue
            seen_title.add(title)

            input_s = input_s.strip()
            output_s = output_s.strip()

            input_vars = self.__extract_variables(input_s)
            output = self.__extract_variables(output_s, value_only=True)[0]
            tcs.append(TestCase(title, input_vars, output))
        return tcs

    def __extract_variables(self, s, value_only=False):
        result = []
        it = PhraseIterator(s + ',')

        def parse_type_and_value():
            c = it.next_char()
            it.prev_char()

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
            elif ('0' <= c) and (c <= '9'):
                vtype = VType(VType.INTEGER)
                value = int(it.skip_r(r'[0-9]+'))
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
                vtype.set_inner_vtype(element_type)
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
            result.append(Variable(name, vtype, value))
            it.skip_r(r'\s*')
            it.skip_r(r',')
            it.skip_r(r'\s*')

        return result

    def __extract_method_name(self, problem_html):
        # Try C++
        s = re.findall(r'(?s)public:\n    [^ ]+ ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        

        # Try Python
        s = re.findall(r'(?s)class Solution:\n    def ([_a-zA-Z0-9]+)', problem_html)
        if s:
            return s[0]        
        raise Exception('Unknown solution method name!')

    def generate_cpp(self):
        testcases = '\n'.join([tc.generate_cpp(self.method_name) for tc in self.testcases])
        method_params = ', '.join([p.as_param_cpp() for p in self.params])
        result = template_cpp.format(
                return_type=self.output_type.as_cpp(),
                method_name=self.method_name,
                params=method_params,
                n_testcases=len(self.testcases),
                testcases=testcases
            )
        print(result)


def main():
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('input');
    parser.add_argument('-l', '--language', choices=['cpp', 'py'], required=True);
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    content = ''
    with open(args.input) as f:
        content = f.read()

    p = Problem(content)
    p.generate_cpp()


main()
