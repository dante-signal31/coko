import sys
from typing import Dict, List
import coko.classes.console_parser as console_parser

def main(args: List=sys.argv[1:])-> None:
    console_arguments = console_parser.parse_arguments(args)


if __name__ == "__main__":
    main()

