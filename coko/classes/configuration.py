import dataclasses
import os.path

import coko.classes.exceptions as exceptions

@dataclasses.dataclass
class Configuration:
    _source_folder_path: str = None
    _destination_folder_path: str = None

    @property
    def source_folder(self)-> str:
        return self._source_folder_path

    @source_folder.setter
    def source_folder(self, value: str)-> None:
        absolute_path = os.path.abspath(value)
        if os.path.isdir(absolute_path):
            self._source_folder_path = os.path.abspath(value)
        else:
            raise exceptions.FolderNotFound(absolute_path)
