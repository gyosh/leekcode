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

def main():
    parser = argparse.ArgumentParser(description='Generate template for Leetcode\'s contest problem, to ease coding & testing.')
    parser.add_argument('input', help='The html file for downloaded problem page');
    parser.add_argument('-l', '--language', choices=LANGUAGE_MAPPING.keys(), required=True, help='Language of the template to generate.')
    parser.add_argument('-e', '--header', help='A .txt file to be included in the generated code as header (commonly for defining constants or common functions).')
    parser.add_argument('-t', '--binary-tree', nargs='+', type=int, default=[], help='Indexes of the input parameters to be treated as binary tree, zero based. Use -1 if is for output.')
    parser.add_argument('-x', '--skip-check', action='store_true', help='If set, will not check output with expected output. Use this for multiple possible output problems.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    content = ''
    with open(args.input) as f:
        content = f.read()

    header = ''
    if args.header is not None:
        with open(args.header) as f:
            header = f.read()

    p = Problem(content, binary_tree_param_indexes=args.binary_tree)

    if args.skip_check:
        logging.info('Using skip check mode')

    language_class = LANGUAGE_MAPPING[args.language]
    try:
        print(language_class.generate(p, skip_check=args.skip_check, header=header))
    except Exception as e:
        msg = 'Unable to generate template due to {}, PLEASE USE LEETCODE\'S EDITOR ON YOUR BROWSER'.format(str(e))
        logging.error(msg)
        print(msg)

main()
