#!/usr/bin/env python
import argparse

from lib.error import CompilerError
from lib.lexer import Lexer
from lib.parser import Parser
from lib.static_analysis import StaticAnalyzer


def parse_args():
    parser = argparse.ArgumentParser(description="PLYC compiler")
    parser.add_argument('input')
    parser.add_argument('--output', "-o", help="specify output filename (default a.out)", default="a.out")
    return parser.parse_args()


def run_compiler(input_name, output_name):
    lexer = Lexer()
    parser = Parser()
    analyzer = StaticAnalyzer()

    with open(input_name, 'r') as f:
        source_code = f.read()

    try:
        # group tokens into syntactical units using parser
        parse_tree = parser.parse(source_code)
        # perform semantic analyze
        ast = analyzer.analyze(parse_tree)
        # optimize
        # generate source code
    except CompilerError:
        exit(1)


def main():
    args = parse_args()
    run_compiler(args.input, args.output)


if __name__ == '__main__':
    main()
