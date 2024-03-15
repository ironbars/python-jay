import argparse
import json
import io
import atexit
import sys
from typing import TextIO

import ruamel.yaml


def yaml2json(stuff: TextIO) -> str:
    yaml = ruamel.yaml.YAML(typ="safe", pure=True)

    return json.dumps(yaml.load(stuff), indent=2)


def json2yaml(stuff: TextIO) -> str:
    yaml = ruamel.yaml.YAML()
    yaml.explicit_start = True
    yaml.indent(sequence=4, offset=2)
    data = json.load(stuff, object_pairs_hook=ruamel.yaml.comments.CommentedMap)
    buffer = io.StringIO()

    ruamel.yaml.scalarstring.walk_tree(data)
    yaml.dump(data, buffer)

    return buffer.getvalue()


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o", "--output", help="File to write to (default is to write to stdout)"
    )
    parser.add_argument(
        "--j2y",
        action="store_true",
        help="Convert JSON to YAML (default is YAML to JSON)",
    )
    parser.add_argument(
        "input_file", nargs="?", help="Read from file (default is to read from stdin)"
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    op = json2yaml if args.j2y else yaml2json
    istream = open(args.input_file, "r") if args.input_file else sys.stdin
    ostream = open(args.output, "w") if args.output else sys.stdout

    def cleanup():
        if istream is not sys.stdin:
            istream.close()

        if ostream is not sys.stdout:
            ostream.close()

    atexit.register(cleanup)

    # The try/except block is for the case where a user opens a file for output but is
    # waiting for input from stdin
    try:
        print(op(istream).strip(), file=ostream)
    except (KeyboardInterrupt, EOFError):
        sys.exit()


if __name__ == "__main__":
    sys.exit(main())
