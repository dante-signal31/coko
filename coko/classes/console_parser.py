import argparse
import os.path
from typing import Dict


def _check_folder_exists(_string: str) -> str:
    if os.path.isdir(_string):
        return _string
    else:
        raise argparse.ArgumentTypeError("{0} file does "
                                         "not exists.".format(_string))


def parse_arguments(args: list=None) -> Dict[str, str]:
    arg_parser = argparse.ArgumentParser(description="A Tool to overwrite directories "
                                                     "using files from a different "
                                                     "owners but keeping original "
                                                     "owners and permissions.\n",
                                         epilog="Follow coko development at: "
                                                "<https://github.com/dante-signal31/coko>")
    arg_parser.add_argument(dest="source_folder",
                            metavar="SOURCE_FOLDER",
                            nargs=1, type=_check_folder_exists, default=None,
                            help="Source folder where you want copy files from.")
    arg_parser.add_argument(dest="destination_folder",
                            metavar="DESTINATION_FOLDER",
                            nargs=1, type=_check_folder_exists, default=None,
                            help="Destination folder where you want copy "
                                 "files to.")
    arg_parser.add_argument("-c", "--create", dest="default_ownership",
                            nargs=3, metavar="UID GUID PERMISSION", default=[],
                            help="Copy over files not present at destination "
                                 "folder yet and set for them given uid and guid " \
                                 "and permission.")
    parsed_arguments = {item: (value[0] if value!=[] else None)
                        for (item, value) in vars(arg_parser.parse_args(args)).items()}
    return parsed_arguments