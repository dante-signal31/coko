import os.path
import unittest

import coko.classes.configuration as configuration
import coko.classes.exceptions as exceptions
import tests.tools as tools


class TestConfiguration(unittest.TestCase):

    def test_create_configuration(self):
        """ All parameters right, we should get a correct object
        """
        correct_path = os.getcwd()
        correct_permissions = [1, 10, 777, True]
        try:
            config = configuration.Configuration(correct_path, correct_path,
                                                 correct_permissions)
        except Exception as e:
            self.fail(f"Test failed with exception {e}")
        self.assertEqual(correct_path, config.source_folder)
        self.assertEqual(correct_path, config.destination_folder)
        self.assertEqual(configuration.FileOwnership(*correct_permissions),
                         config.default_ownership)

    def test_incorrect_paths(self):
        """ Check an exceptions is raised if any incorrect path is entered.
        """
        incorrect_path = os.path.join(os.getcwd(), tools.get_random_string(8))
        correct_path = os.getcwd()
        correct_permissions = [1, 10, 777, True]
        try:
            _ = configuration.Configuration(incorrect_path, correct_path,
                                            correct_permissions)
        except exceptions.FolderNotFound as e:
            self.assertEqual(incorrect_path, e.incorrect_path)
        else:
            self.fail("FileNotFound exception not raised for wrong "
                      "source folder.")
        try:
            _ = configuration.Configuration(correct_path, incorrect_path,
                                            correct_permissions)
        except exceptions.FolderNotFound as e:
            self.assertEqual(incorrect_path, e.incorrect_path)
        else:
            self.fail("FileNotFound exception not raised for wrong "
                      "destination folder.")


if __name__ == '__main__':
    unittest.main()
