# Common functions used by ci scripts.

import sys
import subprocess
import contextlib
if sys.version_info.major < 3:
    import ConfigParser as configparser
else:
    import configparser


@contextlib.contextmanager
def read_configuration(configuration_file):
    parser = _get_config_parser()
    parser.read(configuration_file)
    yield parser


def get_current_version(configuration_file):
    with read_configuration(configuration_file) as parser:
        version = _get_version(parser)
        return version


def get_python_version_to_package(configuration_file):
    with read_configuration(configuration_file) as parser:
        python_version = _get_python_version(parser)
        return python_version


def _get_config_parser():
    if sys.version_info[0] == 3:
        parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
    else:
        parser = configparser.ConfigParser()
    return parser


def _get_value(parser, section, parameter):
    if sys.version_info[0] == 3:
        value = parser[section][parameter]
    else:
        value = parser.get(section, parameter)
    return value


def _get_version(parser):
    return _get_value(parser, "DEFAULT", "version")


def _get_python_version(parser):
    return _get_value(parser, "DEFAULT", "python_version")


def run_console_command(command):
    if sys.version_info.major < 3:
        subprocess.call(command, shell=True)
    else:
        subprocess.run(command, shell=True, check=True)


