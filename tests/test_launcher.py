import unittest
import os.path

import coko.launcher as launcher
import tests.tools as tools
import tests.test_sync as test_sync


class TestLauncher(unittest.TestCase):

    def test_launcher_no_create(self)-> None:
        """ Test application syncronizing a source folder over a destination
        folder but without creating new files at destination.

        :return: None
        """
        with tools.create_test_bed(test_sync.DUMMY_SOURCE_FOLDER,
                                   test_sync.DUMMY_DESTINATION_FOLDER) as test_bed:
            launcher.main(["coko",
                           test_bed.source_folder,
                           test_bed.destination_folder])
            # TODO: Refactoring needed. Too much code repeated with test_sync.test_copy_files_default
            for synced_file in test_sync.DUMMY_DESTINATION_FOLDER:
                destination_file_path = os.path.join(test_bed.destination_folder,
                                                     synced_file.relative_filename_path)
                try:
                    with open(destination_file_path) as f:
                        destination_contents = f.read()
                except FileNotFoundError:
                    self.fail(f"A file was not found at "
                              f"destination folder: {destination_file_path}")
                else:
                    # Check contents have actually changed to the ones in source
                    # folder.
                    source_file_path = os.path.join(test_bed.source_folder,
                                                    synced_file.relative_filename_path)
                    with open(source_file_path) as f:
                        source_contents = f.read
                    self.assertEqual(source_contents, destination_contents)
                    # Check ownership data has been preserved.
                    file_stat = os.stat(destination_file_path)
                    self.assertEqual(synced_file.ownership.uid, file_stat.st_uid)
                    self.assertEqual(synced_file.ownership.guid, file_stat.st_gid)
                    self.assertEqual(synced_file.ownership.permissions, file_stat.st_mode)



    def test_launcher_create(self)-> None:
        """ Test aplication synchcronizing a source file over a destination
        folder but this time creating at destination every file present at
        source but not already present at destination one.

        :return: None
        """
        # TODO: Pending.
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
