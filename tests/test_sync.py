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



if __name__ == '__main__':
    unittest.main()
