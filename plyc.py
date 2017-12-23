#!/usr/bin/env python
import argparse

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

    with open(input_name, 'r') as f:
        source_code = f.read()

    try:
        # group tokens into syntactical units using parser
        parse_tree = parser.parse(source_code)
        # perform semantic analyze
        symtab, ast = analyzer.analyze(parse_tree)
        # generate flow graph
        import pdb; pdb.set_trace()
        flow_graph = flow_generator.generate(ast, main=True)
        # generate code
        code = code_generator.generate(flow_graph, symtab)

        with open(output_name, 'w') as f:
            f.write(str(code))

    except CompilerError:
        exit(1)


def main():
    args = parse_args()
    run_compiler(args.input, args.output)


if __name__ == '__main__':
    main()
