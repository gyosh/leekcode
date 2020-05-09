import re
import logging
import argparse

from lib.problem import Problem
from lib.language import Cpp, Py

LANG_CPP = 'cpp'
LANG_PYTHON = 'py'

def main():
    parser = argparse.ArgumentParser(description='Generate template for Leetcode\'s contest problem, to ease coding & testing.')
    parser.add_argument('input', help='The html file for downloaded problem page');
    parser.add_argument('-l', '--language', choices=[LANG_PYTHON, LANG_CPP], required=True, help='Language of the template to generate');
    parser.add_argument('-x', '--skip-check', action='store_true', help='If set, will not check output with expected output. Use this for multiple possible output problems.');
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    content = ''
    with open(args.input) as f:
        content = f.read()

    p = Problem(content)

    if args.skip_check:
        logging.info('Using skip check mode')

    if args.language == LANG_CPP:
        print(Cpp.generate(p, args.skip_check))
    else:
        print(Py.generate(p, args.skip_check))

main()
