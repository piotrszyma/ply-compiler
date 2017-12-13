#!/usr/bin/env python
import argparse

from lib.lexer import Lexer


def parse_args():
    parser = argparse.ArgumentParser(description="PLYC compiler")
    parser.add_argument('input')
    parser.add_argument('--output', "-o", help="specify output filename (default a.out)", default="a.out")
    return parser.parse_args()


def run_compiler(input_name, output_name):
    lexer = Lexer()

    with open(input_name, 'r') as f:
        source_code = f.read()

    tokens = lexer.tokenize(source_code)
    for t in list(tokens):
        print(t)
    # generate tokens using lexer
    # group tokens into syntactical units using parser
    # perform semantic analyze
    # optimize
    # generate source code


def main():
    args = parse_args()
    run_compiler(args.input, args.output)


main()
