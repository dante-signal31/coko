import os.path
from typing import List

import coko.classes.exceptions as exceptions


class Folder(object):
    """A descriptor that sets and returns system folders checking folder
    actually exists.
    """
    def __init__(self):
        self._folder_path = None

    def __get__(self, obj, objtype)-> str:
        return self._folder_path

    def __set__(self, obj, value):
        absolute_path = os.path.abspath(value)
        if os.path.isdir(absolute_path):
            self._folder_path = os.path.abspath(value)
        else:
            raise exceptions.FolderNotFound(absolute_path)


class Configuration:
    source_folder: Folder = Folder()
    destination_folder: Folder = Folder()

    def __init__(self, source_folder: str, destination_folder: str,
                 permissions: List):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        # TODO: self.permissions is just a placeholder, I don't know yet its final form.
        self.permissions = permissions

