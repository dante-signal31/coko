import dataclasses
import os
from typing import List

import coko.classes.configuration as configuration


@dataclasses.dataclass
class FileInfo:
    relative_filename_path: str
    ownership: configuration.FileOwnership


def get_files(root_folder: str)-> str:
    """ Iterator to get all files inside a nested folder tree.

    :param root_folder: Base folder where to star getting files from.
    :return: Iterator return files path names relatives to root folder.
    """
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            absolute_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(absolute_path, root_folder)
            yield relative_path


def set_ownership(file_path: str, file_info: configuration.FileOwnership)-> None:
    """ Set file for uid, guid and permissions given through a FileOwnership
    object.

    To use this function application should be run as sudo, otherwise the only
    you'll get is an "Operation not permitted" error.

    :param file_path: Absolute file path whose permissions we want to set.
    :param file_info: UID, GUID and access permission to set for this file.
    :return: None
    """
    os.chown(file_path, file_info.uid, file_info.guid)
    os.chmod(file_path, file_info.permissions)


def register_destination_files(config: configuration.Configuration)-> List[FileInfo]:
    """ Walk through destination folder taking note of relative path and
    permissions of every file it meets.

    :param config: Configuration generated from console parameters.
    :return: A list with a FileInfo object for every file in destination folder.
    """
    destination_files = []
    for destination_file in get_files(config.destination_folder):
        file_info = os.stat(os.path.join(config.destination_folder, destination_file))
        permissions = configuration.FileOwnership(file_info.st_uid,
                                                  file_info.st_gid,
                                                  file_info.st_mode)
        destination_files.append(FileInfo(destination_file,
                                          permissions))
    return destination_files


def copy_files(config: configuration.Configuration,
               destination_ownerships: List[FileInfo])-> None:
    """ Walks through original folder copying into destination but keeping
    original destination folder files permissions.

    It won't copy a file into destination folder if that folder was not already
    present unless Configuration.ownership was other than None. If
    Configuration.ownership wasn't None then ownership would be a
    configuration.FileOwnership object with permissions every newly created
    file at destination will have by default.

    :param config: configuration generated from console parameters.
    :param destination_ownerships: A list with ownership info for every file at
    destination folder.
    :return: None
    """
    pass

