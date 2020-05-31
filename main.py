import re
import logging
import argparse

from lib.problem import Problem
from lib.language.cpp import Cpp
from lib.language.python3 import Python3

LANGUAGE_MAPPING = {
    'cpp': Cpp,
    'py': Python3,
}

def parse_binary_tree_param_indexes(binary_tree_arg):
    tokens = binary_tree_arg.split(',')
    ret = []
    for s in tokens:
        if s.startswith('i'):
            ret.append(int(s[1:])-1)
        elif s == 'o':
            ret.append(-1)
        elif len(s) > 0:
            raise Exception('Invalid parameter for binary tree argument {}.'.format(s))
    return ret


def main():
    parser = argparse.ArgumentParser(description='Generate template for Leetcode\'s contest problem, to ease coding & testing.')
    parser.add_argument('input', help='The html file for downloaded problem page');
    parser.add_argument('-l', '--language', choices=LANGUAGE_MAPPING.keys(), required=True, help='Language of the template to generate.')
    parser.add_argument('-e', '--header', help='A .txt file to be included in the generated code as header (commonly for defining constants or common functions).')
    parser.add_argument('-t', '--binary-tree', default='', help='Comma separated indexes of the input parameters/output to be treated as binary tree. Use \'i\' prefix for input followed by one based index, and \'o\' for output. E.g: "i2,o" means 2nd input parameter and output is binary tree. You need to give this information since binary tree is provided as list in Leetcode\'s testcase.')
    parser.add_argument('-x', '--skip-check', action='store_true', help='If set, will not check output with expected output. Use this for multiple possible output problems.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    content = ''
    with open(args.input) as f:
        content = f.read()

    header = ''
    if args.header is not None:
        logging.info('Loading header from %s', args.header)
        with open(args.header) as f:
            header = f.read()

    if args.skip_check:
        logging.info('Using skip check mode')

    language_class = LANGUAGE_MAPPING[args.language]
    try:
        p = Problem(content, binary_tree_param_indexes=parse_binary_tree_param_indexes(args.binary_tree))
        print(language_class.generate(p, skip_check=args.skip_check, header=header))
    except Exception as e:
        msg = 'Unable to generate template due to {}, PLEASE USE LEETCODE\'S EDITOR ON YOUR BROWSER'.format(str(e))
        logging.error(msg)
        print(msg)

main()
