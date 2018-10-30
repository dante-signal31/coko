import os
import unittest
from typing import List, Dict

import coko.classes.sync as sync
import coko.classes.configuration as configuration
import tests.tools as tools

DUMMY_DESTINATION_FOLDER = [
    sync.FileInfo("executable",
                  configuration.FileOwnership(10,
                                              30,
                                              755)),
    sync.FileInfo("config",
                  configuration.FileOwnership(10,
                                              30,
                                              644)),
    sync.FileInfo("folder1/data1",
                  configuration.FileOwnership(10,
                                              30,
                                              644)),
    sync.FileInfo("folder1/data2",
                  configuration.FileOwnership(10,
                                              30,
                                              644)),
    sync.FileInfo("folder2/data3",
                  configuration.FileOwnership(10,
                                              30,
                                              644)),
    sync.FileInfo("folder1/folder2/data4",
                  configuration.FileOwnership(10,
                                              30,
                                              644))
    ]

DUMMY_SOURCE_FOLDER = [
    sync.FileInfo("executable",
                  configuration.FileOwnership(20,
                                              40,
                                              755)),
    sync.FileInfo("new_file1",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("config",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("folder1/data1",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("folder1/data2",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("folder1/new_file2",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("folder2/data3",
                  configuration.FileOwnership(20,
                                              40,
                                              644)),
    sync.FileInfo("folder1/folder2/data4",
                  configuration.FileOwnership(20,
                                              40,
                                              644))
    ]


class TestSync(unittest.TestCase):

    def test_register_destination_files(self):
        """ Test all info from destination folder is properly stored to
        apply it copied over folders from source folder.
        """
        with tools.create_test_bed(DUMMY_SOURCE_FOLDER,
                                   DUMMY_DESTINATION_FOLDER) as test_bed:
            config = configuration.Configuration(test_bed.source_folder,
                                                 test_bed.destination_folder,
                                                 configuration.FileOwnership(10,
                                                                             30,
                                                                             644))
            stored_file_list: List[sync.FileInfo] = sync.register_destination_files(config)
            stored_file_dict: Dict[str, configuration.FileOwnership] = {item.relative_filename_path: item.ownership
                                                                        for item in stored_file_list}
            for original in DUMMY_DESTINATION_FOLDER:
                if original.relative_filename_path in stored_file_dict:
                    self.assertEqual(original.ownership,
                                     stored_file_dict[original.relative_filename_path])
                else:
                    self.fail(f"One of the dummy files at destination folder "
                              f"was not registered "
                              f"right: {original.relative_filename_path}")

    def test_copy_files_default(self):
        """ Test default case when you only copy files from source folder
        to destination folder if they are already present at destination.
        """
        with tools.create_test_bed(DUMMY_SOURCE_FOLDER,
                                   DUMMY_DESTINATION_FOLDER) as test_bed:
            config = configuration.Configuration(test_bed.source_folder,
                                                 test_bed.destination_folder,
                                                 configuration.FileOwnership(10,
                                                                             30,
                                                                             644))
            stored_file_list: List[sync.FileInfo] = sync.register_destination_files(config)
            sync.copy_files(config, stored_file_list)
            for stored_file in stored_file_list:
                destination_file_path = os.path.join(test_bed.destination_folder,
                                                     stored_file.relative_filename_path)
                try:
                    with open(destination_file_path) as f:
                        destination_contents = f.read()
                except FileNotFoundError:
                    self.fail(f"A file was not found at "
                              f"destination folder: {destination_file_path}")
                else:
                    # Check contents have actually changed.
                    source_file_path = os.path.join(test_bed.source_folder,
                                                    stored_file.relative_filename_path)
                    with open(source_file_path) as f:
                        source_contents = f.read
                    self.assertEqual(source_contents, destination_contents)
                    # Check ownership data has been preserved.
                    file_stat = os.stat(destination_file_path)
                    self.assertEqual(stored_file.ownership.uid, file_stat.st_uid)
                    self.assertEqual(stored_file.ownership.guid, file_stat.st_gid)
                    self.assertEqual(stored_file.ownership.permissions, file_stat.st_mode)


if __name__ == '__main__':
    unittest.main()
