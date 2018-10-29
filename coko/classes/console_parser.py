import argparse
import sys
from typing import Dict

import coko.classes.configuration as configuration
import coko.classes.exceptions as exceptions


def parse_arguments(args: list=None) -> configuration.Configuration:
    """ Parse console arguments to generate a Configuration object we
    can work with.
    """
    arg_parser = argparse.ArgumentParser(description="A Tool to overwrite directories "
                                                     "using files from a different "
                                                     "owners but keeping original "
                                                     "owners and permissions.\n",
                                         epilog="Follow coko development at: "
                                                "<https://github.com/dante-signal31/coko>")
    arg_parser.add_argument(dest="source_folder",
                            metavar="SOURCE_FOLDER",
                            nargs=1, default=None,
                            help="Source folder where you want copy files from.")
    arg_parser.add_argument(dest="destination_folder",
                            metavar="DESTINATION_FOLDER",
                            nargs=1, default=None,
                            help="Destination folder where you want copy "
                                 "files to.")
    # TODO: Update help when default ownership is ready.
    arg_parser.add_argument("-c", "--create", dest="default_ownership",
                            nargs=3, metavar="UID GUID PERMISSION", default=None,
                            help="Copy over files not present at destination "
                                 "folder yet and set for them given uid and guid " \
                                 "and permission. (DOES NOT WORK. PENDING)")
    # Parse_args returns each parameter in a list. We must take them out.
    parsed_arguments = {item: (value[0] if item != "default_ownership"
                               else value)
                        for (item, value) in vars(arg_parser.parse_args(args)).items()}
    try:
        config = configuration.Configuration(parsed_arguments["source_folder"],
                                             parsed_arguments["destination_folder"],
                                             parsed_arguments["default_ownership"])
    except exceptions.FolderNotFound as e:
        print(f"Folder not found: {e.incorrect_path}")
        sys.exit(1)
    return config
