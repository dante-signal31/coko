import tempfile
import unittest

import coko.classes.console_parser as console_parser
import coko.classes.configuration as configuration


class TestConsoleParser(unittest.TestCase):

    _source_folder = None
    _destination_folder = None

    @classmethod
    def setUpClass(cls):
        cls._source_folder = tempfile.mkdtemp()
        cls._destination_folder = tempfile.mkdtemp()

    def test_input(self):
        """ Test a correct input of two folders are properly parsed.
        """
        config = console_parser.parse_arguments(f"{self.__class__._source_folder} "
                                                f"{self.__class__._destination_folder}".split())
        self.assertEqual(self.__class__._source_folder,
                         config.source_folder)
        self.assertEqual(self.__class__._destination_folder,
                         config.destination_folder)

    def test_optional_arguments(self):
        """ Test correct optional parameters are properly parsed.
        """
        config = console_parser.parse_arguments(f"{self.__class__._source_folder} "
                                                          f"{self.__class__._destination_folder} "
                                                          f"--create 10 50 775".split())
        self.assertEqual(configuration.FileOwnership(10, 50, 775, True),
                         config.default_ownership)


if __name__ == '__main__':
    unittest.main()
