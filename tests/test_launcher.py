import unittest

import coko.launcher as launcher

class TestLauncher(unittest.TestCase):

    def test_launcher_no_create(self)-> None:
        """ Test application syncronizing a source folder over a destination
        folder but without creating new files at destination.

        :return: None
        """
        self.assertEqual(True, False)

    def test_launcher_create(self)-> None:
        """ Test aplication synchcronizing a source file over a destination
        folder but this time creating at destination every file present at
        source but not already present at destination one.

        :return: None
        """
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
