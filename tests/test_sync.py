import unittest

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
        with tools.create_test_bed(DUMMY_SOURCE_FOLDER,
                                   DUMMY_DESTINATION_FOLDER) as test_bed:


        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
