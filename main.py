import re
import logging
import argparse

from lib.problem import Problem
from lib.language import Cpp


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
    Cpp.generate(p)

main()
