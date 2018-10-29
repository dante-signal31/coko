import sys
from typing import Dict, List
import coko.classes.console_parser as console_parser


def main(args: List=sys.argv[1:])-> None:
    config = console_parser.parse_arguments(args)
    destination_ownerships = register_destination_files(config)
    copy_files(config, destination_ownerships)


if __name__ == "__main__":
    main()

