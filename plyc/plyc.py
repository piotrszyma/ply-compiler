#!/bin/python
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="PLYC compiler")
    parser.add_argument('input')
    parser.add_argument('--output', "-o", help="specify output filename (default a.out)", default="a.cf")
    return parser.parse_args()


def run_compiler(input_name, output_name):

    with open(input_name, 'r') as f:
        source_code = f.read()
    print(source_code)

    # generate tokens using lexer
    # group tokens into syntactical units using parser
    # perform semantic analyze
    # optimize
    # generate source code



def main():
    args = parse_args()
    run_compiler(args.input, args.output)


if __name__ == '__main__':
    main()
