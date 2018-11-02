import os
import unittest
from typing import List, Dict

import coko.classes.sync as sync
import coko.classes.configuration as configuration
import tests.tools as tools

# Permissions octals cheatsheet:
# from: https://stackoverflow.com/questions/5337070/how-can-i-get-a-files-permission-mask
#
#
# The upper parts determine the filetype, e.g.:
#
# S_IFMT  0170000 bitmask for the file type bitfields
# S_IFSOCK    0140000 socket
# S_IFLNK 0120000 symbolic link
# S_IFREG 0100000 regular file
# S_IFBLK 0060000 block device
# S_IFDIR 0040000 directory
# S_IFCHR 0020000 character device
# S_IFIFO 0010000 FIFO
# S_ISUID 0004000 set UID bit
# S_ISGID 0002000 set-group-ID bit (see below)
# S_ISVTX 0001000 sticky bit (see below)
#
# The lower parts are what you use to change with chmod:
#
# S_IRWXU 00700   mask for file owner permissions
# S_IRUSR 00400   owner has read permission
# S_IWUSR 00200   owner has write permission
# S_IXUSR 00100   owner has execute permission
# S_IRWXG 00070   mask for group permissions
# S_IRGRP 00040   group has read permission
# S_IWGRP 00020   group has write permission
# S_IXGRP 00010   group has execute permission
# S_IRWXO 00007   mask for permissions for others (not in group)
# S_IROTH 00004   others have read permission
# S_IWOTH 00002   others have write permission
# S_IXOTH 00001   others have execute permission

DUMMY_DESTINATION_FOLDER = [
    sync.FileInfo("executable",
                  configuration.FileOwnership(10,
                                              30,
                                              100755,
                                              True)),
    sync.FileInfo("config",
                  configuration.FileOwnership(10,
                                              30,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/data1",
                  configuration.FileOwnership(10,
                                              30,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/data2",
                  configuration.FileOwnership(10,
                                              30,
                                              100644,
                                              True)),
    sync.FileInfo("folder2/data3",
                  configuration.FileOwnership(10,
                                              30,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/folder2/data4",
                  configuration.FileOwnership(10,
                                              30,
                                              100644,
                                              True))
    ]

DUMMY_SOURCE_FOLDER = [
    sync.FileInfo("executable",
                  configuration.FileOwnership(20,
                                              40,
                                              100755,
                                              True)),
    sync.FileInfo("new_file1",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("config",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/data1",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/data2",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/new_file2",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("folder2/data3",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True)),
    sync.FileInfo("folder1/folder2/data4",
                  configuration.FileOwnership(20,
                                              40,
                                              100644,
                                              True))
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
                                                 [10, 30, 644, True])
            stored_file_list: List[sync.FileInfo] = sync.register_destination_files(config)
            stored_file_dict: Dict[str, configuration.FileOwnership] = {item.relative_filename_path: item.ownership
                                                                        for item in stored_file_list}
            for original in DUMMY_DESTINATION_FOLDER:
                if original.relative_filename_path in stored_file_dict:
                    self.assertEqual(original.ownership,
                                     stored_file_dict[original.relative_filename_path],
                                     "Permissions not properly registered.")
                else:
                    self.fail(f"One of the dummy files at destination folder "
                              f"was not registered "
                              f"right: {original.relative_filename_path}")

    @staticmethod
    def _copy_files(config: configuration.Configuration)-> List[sync.FileInfo]:
        stored_file_list: List[sync.FileInfo] = sync.register_destination_files(config)
        sync.copy_files(config, stored_file_list)
        return stored_file_list

    def _check_ownership(self, absolute_file_path: str,
                         ownership: configuration.FileOwnership):
        file_stat = os.stat(absolute_file_path)
        self.assertEqual(ownership.uid, file_stat.st_uid,
                         "Destination file uid property not properly preserved.")
        self.assertEqual(ownership.guid, file_stat.st_gid,
                         "Destination file gid property not properly preserved.")
        self.assertEqual(ownership.permissions, file_stat.st_mode,
                         "Destination file permissions property not properly preserved.")

    def _check_destination_files_are_properly_updated(self, stored_file_list: List[sync.FileInfo],
                                                      test_bed: tools.TestBed):
        # Check all files formerly present at destination have updated their
        # contents but not their metadata.
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
                    source_contents = f.read()
                self.assertEqual(source_contents, destination_contents,
                                 "Destination file content not properly updated.")
                # Check ownership data has been preserved.
                self._check_ownership(destination_file_path, stored_file.ownership)

    def _check_new_files_at_destination(self, source_files: List[sync.FileInfo],
                                        destination_files: List[sync.FileInfo],
                                        config: configuration.Configuration,
                                        test_bed: tools.TestBed,
                                        may_exist_new_files: bool):
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
                self.assertEqual(config.default_ownership, actual_ownership,
                                 "Default permissions not properly set for new "
                                 "file at destination")
            else:
                # Check there is not at destination a file not formerly present there.
                self.assertFalse(os.path.exists(absolute_path),
                                 "Not allowed file creation at destination "
                                 "folder")

    def test_copy_files_default(self):
        """ Test default case when you only copy files from source folder
        to destination folder if they are already present at destination.

        At the end no new files should be present at destination.
        """
        with tools.create_test_bed(DUMMY_SOURCE_FOLDER,
                                   DUMMY_DESTINATION_FOLDER) as test_bed:
            config = configuration.Configuration(test_bed.source_folder,
                                                 test_bed.destination_folder,
                                                 None)
            updated_file_list: List[sync.FileInfo] = TestSync._copy_files(config)
            self._check_destination_files_are_properly_updated(updated_file_list,
                                                               test_bed)
            self._check_new_files_at_destination(DUMMY_SOURCE_FOLDER,
                                                 DUMMY_DESTINATION_FOLDER,
                                                 config,
                                                 test_bed,
                                                 may_exist_new_files=False)

    def test_copy_files_create(self):
        """ Test case were creation of new files at destination is allowed.

        At the end new files should have been properly created at destination.
        """
        with tools.create_test_bed(DUMMY_SOURCE_FOLDER,
                                   DUMMY_DESTINATION_FOLDER) as test_bed:
            config = configuration.Configuration(test_bed.source_folder,
                                                 test_bed.destination_folder,
                                                 [10, 20, 100644, True])
            updated_file_list: List[sync.FileInfo] = TestSync._copy_files(config)
            self._check_destination_files_are_properly_updated(updated_file_list,
                                                               test_bed)
            self._check_new_files_at_destination(DUMMY_SOURCE_FOLDER,
                                                 DUMMY_DESTINATION_FOLDER,
                                                 config,
                                                 test_bed,
                                                 may_exist_new_files=True)


if __name__ == '__main__':
    unittest.main()
