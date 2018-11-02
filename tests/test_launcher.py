import unittest
import os.path
from typing import List

import coko.launcher as launcher
import coko.classes.sync as sync
import coko.classes.configuration as configuration
import tests.tools as tools
import tests.test_sync as test_sync


class TestLauncher(unittest.TestCase):

    def _check_ownership(self, absolute_file_path: str,
                         ownership: configuration.FileOwnership):
        file_stat = os.stat(absolute_file_path)
        self.assertEqual(ownership.uid, file_stat.st_uid,
                         "Destination file uid property not properly preserved.")
        self.assertEqual(ownership.guid, file_stat.st_gid,
                         "Destination file gid property not properly preserved.")
        self.assertEqual(ownership.permissions, file_stat.st_mode,
                         "Destination file permissions property not properly preserved.")

    def _check_destination_files_are_properly_updated(self, updated_file_list: List[sync.FileInfo],
                                                      test_bed: tools.TestBed):
        # Check all files formerly present at destination have updated their
        # contents but not their metadata.
        for updated_file in updated_file_list:
            destination_file_path = os.path.join(test_bed.destination_folder,
                                                 updated_file.relative_filename_path)
            try:
                with open(destination_file_path) as f:
                    destination_contents = f.read()
            except FileNotFoundError:
                self.fail(f"A file was not found at "
                          f"destination folder: {destination_file_path}")
            else:
                # Check contents have actually changed.
                source_file_path = os.path.join(test_bed.source_folder,
                                                updated_file.relative_filename_path)
                with open(source_file_path) as f:
                    source_contents = f.read()
                self.assertEqual(source_contents, destination_contents,
                                 "Destination file content not properly updated.")
                # Check ownership data has been preserved.
                self._check_ownership(destination_file_path, updated_file.ownership)

    def _check_new_files_at_destination(self, source_files: List[sync.FileInfo],
                                        destination_files: List[sync.FileInfo],
                                        ownership: List[int],
                                        test_bed: tools.TestBed,
                                        may_exist_new_files: bool):
        default_ownership = configuration.FileOwnership(ownership[0],
                                                        ownership[1],
                                                        int(f"100{str(ownership[2])}"),
                                                        True)
        source_file_names = {file.relative_filename_path
                             for file in source_files}
        destination_file_names = {file.relative_filename_path
                                  for file in destination_files}
        files_not_at_destination = source_file_names - destination_file_names
        for file_name in files_not_at_destination:
            absolute_path = os.path.join(test_bed.destination_folder,
                                         file_name)
            if may_exist_new_files:
                # Check at destination that a file not formerly present there has
                # been properly created.
                self.assertTrue(os.path.exists(absolute_path),
                                "Source file not created at destination.")
                file_metadata = os.stat(absolute_path)
                actual_ownership = configuration.FileOwnership(file_metadata.st_uid,
                                                               file_metadata.st_gid,
                                                               file_metadata.st_mode,
                                                               False)
                self.assertEqual(default_ownership, actual_ownership,
                                 "Default permissions not properly set for new "
                                 "file at destination")
            else:
                # Check there is not at destination a file not formerly present there.
                self.assertFalse(os.path.exists(absolute_path),
                                 "Not allowed file creation at destination "
                                 "folder")

    def test_launcher_no_create(self)-> None:
        """ Test application syncronizing a source folder over a destination
        folder but without creating new files at destination.

        :return: None
        """
        with tools.create_test_bed(test_sync.DUMMY_SOURCE_FOLDER,
                                   test_sync.DUMMY_DESTINATION_FOLDER) as test_bed:
            default_ownership = [10, 20, 644]
            launcher.main([test_bed.source_folder,
                           test_bed.destination_folder])
            self._check_destination_files_are_properly_updated(test_sync.DUMMY_DESTINATION_FOLDER,
                                                               test_bed)
            self._check_new_files_at_destination(test_sync.DUMMY_SOURCE_FOLDER,
                                                 test_sync.DUMMY_DESTINATION_FOLDER,
                                                 default_ownership,
                                                 test_bed,
                                                 may_exist_new_files=False)

    def test_launcher_create(self)-> None:
        """ Test aplication synchcronizing a source file over a destination
        folder but this time creating at destination every file present at
        source but not already present at destination one.

        :return: None
        """
        with tools.create_test_bed(test_sync.DUMMY_SOURCE_FOLDER,
                                   test_sync.DUMMY_DESTINATION_FOLDER) as test_bed:
            default_ownership = [10, 20, 644]
            launcher.main([test_bed.source_folder,
                           test_bed.destination_folder,
                           "--create", *[str(value) for value in default_ownership]])
            self._check_destination_files_are_properly_updated(test_sync.DUMMY_DESTINATION_FOLDER,
                                                               test_bed)
            self._check_new_files_at_destination(test_sync.DUMMY_SOURCE_FOLDER,
                                                 test_sync.DUMMY_DESTINATION_FOLDER,
                                                 default_ownership,
                                                 test_bed,
                                                 may_exist_new_files=True)


if __name__ == '__main__':
    unittest.main()
