import os.path
import random
import string
import unittest

import coko.classes.configuration as configuration
import coko.classes.exceptions as exceptions


def _get_random_string(length: int) -> str:
    """ Create a random string with given length.

    Got from:  https://stackoverflow.com/questions/47073453/how-to-generate-a-random-string-with-symbols
    """
    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for n in range(length)])


class TestConfiguration(unittest.TestCase):

    def test_create_configuration(self):
        """ All parameters right, we should get a correct object
        """
        correct_path = os.getcwd()
        try:
            config = configuration.Configuration(correct_path, correct_path)
        except Exception as e:
            self.fail(f"Test failed with exception {e}")
        self.assertEqual(correct_path, config.source_folder)
        self.assertEqual(correct_path, config.destination_folder_path)

    def test_incorrect_paths(self):
        """ Check an exceptions is raised if any incorrect path is entered.
        """
        incorrect_path = _get_random_string(8)
        with self.assertRaises(exceptions.FolderNotFound) as e:
            self.assertEqual(e.exception.msg, incorrect_path)


if __name__ == '__main__':
    unittest.main()
