import argparse
import tempfile
import unittest
import coko.classes.console_parser as console_parser


class TestConsoleParser(unittest.TestCase):

    _source_folder = None
    _destination_folder = None

    @classmethod
    def setUpClass(cls):
        cls._source_folder = tempfile.mkdtemp()
        cls._destination_folder = tempfile.mkdtemp()

    def test_correct_input(self):
        parsed_arguments = console_parser.parse_arguments(f"{self.__class__._source_folder} "
                                                          f"{self.__class__._destination_folder}".split())
        self.assertEqual(self.__class__._source_folder,
                         parsed_arguments["source_folder"])
        self.assertEqual(self.__class__._destination_folder,
                         parsed_arguments["destination_folder"])

    def test_incorrect_input(self):
        self.assertRaises(argparse.ArgumentTypeError,
                          console_parser.parse_arguments,
                          f"{self.__class__._source_folder}X ",
                          f"{self.__class__._destination_folder}")
        self.assertRaises(argparse.ArgumentTypeError,
                          console_parser.parse_arguments,
                          f"{self.__class__._source_folder} ",
                          f"{self.__class__._destination_folder}X")

    def test_create_correct_arguments(self):
        parsed_arguments = console_parser.parse_arguments(f"{self.__class__._source_folder} "
                                                          f"{self.__class__._destination_folder} "
                                                          f"--create 10 50 775".split())
        self.assertEqual([10, 50, 775], parsed_arguments["default_ownership"])


if __name__ == '__main__':
    unittest.main()
