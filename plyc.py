#!/usr/bin/env python3
import argparse
import logging

from lib.code_generator import CodeGenerator
from lib.error import CompilerError
from lib.flow_graph import FlowGraph
from lib.parser import Parser
from lib.static_analysis import StaticAnalyzer


def parse_args():
    parser = argparse.ArgumentParser(description="PLYC compiler")
    parser.add_argument('input')
    parser.add_argument('--output', "-o", help="specify output filename (default a.out)", default="a.out")
    return parser.parse_args()


def run_compiler(input_name, output_name):
    parser = Parser()
    analyzer = StaticAnalyzer()
    flow_generator = FlowGraph()
    code_generator = CodeGenerator()

    source_code = ''

    try:
        with open(input_name, 'r') as f:
            source_code = f.read()
    except FileNotFoundError:
        logging.error("File not found")
        exit(1)

    try:
        # group tokens into syntactical units using parser
        parse_tree = parser.parse(source_code)
        # perform semantic analyze
        symtab, ast = analyzer.analyze(parse_tree)
        # generate flow graph
        flow_graph = flow_generator.generate(ast)
        # generate code
        code = code_generator.generate(flow_graph, symtab)

        with open(output_name, 'w') as f:
            f.write(str(code))

    except CompilerError as error:
        if str(error):
            logging.error("COMPILER_ERROR: {0}".format(str(error)))
        exit(1)


def main():
    args = parse_args()
    run_compiler(args.input, args.output)


if __name__ == '__main__':
    main()
