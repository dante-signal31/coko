import contextlib
import dataclasses
import os
import random
import string
import tempfile
from typing import List

import coko.classes.sync as sync


@dataclasses.dataclass
class TestBed:
    source_folder: str
    destination_folder: str
    source_files: List[sync.FileInfo]
    destination_files: List[sync.FileInfo]


def get_random_string(length: int) -> str:
    """ Create a random string with given length.

    Got from:  https://stackoverflow.com/questions/47073453/how-to-generate-a-random-string-with-symbols

    :param length: Desired length for generated 4random string.
    """
    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for _ in range(length)])


def create_file_tree(root_folder: str, files: List[sync.FileInfo])-> None:
    """ Create a dummy file structure defined by files parameter using
    root folder as base point.

    :param root_folder: Base folder created files will hang from.
    :param files: A list of files to be created inside root folder.
    :return: None
    """
    for file in files:
        absolute_file_path = os.path.join(root_folder,
                                          file.relative_filename_path)
        os.makedirs(os.path.dirname(absolute_file_path), exist_ok=True)
        with open(absolute_file_path, "w+") as f:
            f.write(get_random_string(12))
            sync.set_ownership(absolute_file_path, file.ownership)


@contextlib.contextmanager
def create_test_bed(source_files: List[sync.FileInfo],
                    destination_files: List[sync.FileInfo])-> TestBed:
    """ Create two random folder populated with dummy files structure defined
    in source_files and destination_files list.

    :param source_files: List of files to be created at source folder.
    :param destination_files: List of files to be created at destination folder.
    :return: A TestBed object about your generated context.
    """
    source_folder: str = tempfile.mkdtemp()
    destination_folder: str = tempfile.mkdtemp()
    create_file_tree(source_folder, source_files)
    create_file_tree(destination_folder, destination_files)
    yield TestBed(source_folder, destination_folder,
                  source_files, destination_files)