import dataclasses
from typing import List

import coko.classes.configuration as configuration


@dataclasses.dataclass
class FileOwnershipInfo:
    relative_filename_path: str
    uid: int
    guid: int
    permissions: int


def register_destination_files(config: configuration.Configuration)-> List[FileOwnershipInfo]:
    """

    :param config:
    :return:
    """
    pass


def copy_files(config: configuration.Configuration,
               destination_ownerships: List[FileOwnershipInfo])-> None:
    pass

