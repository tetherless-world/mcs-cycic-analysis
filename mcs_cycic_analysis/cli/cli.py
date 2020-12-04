import logging
from argparse import ArgumentParser
from pathlib import Path

from mcs_cycic_analysis.cli.commands.create_spreadsheet_command import CreateSpreadsheetCommand


class Cli:
    __COMMAND_CLASSES = {
        "create-spreadsheet": CreateSpreadsheetCommand,
    }

    def __init__(self):
        self.__arg_parser = ArgumentParser()
        self.__logger = logging.getLogger(self.__class__.__name__)

    def __add_arguments(self):
        arg_parsers = [self.__arg_parser]

        subparsers = self.__arg_parser.add_subparsers(dest="command")
        for command_name, command_class in self.__COMMAND_CLASSES.items():
            command_arg_parser = subparsers.add_parser(command_name)
            command_class.add_arguments(command_arg_parser)
            arg_parsers.append(command_arg_parser)

        for arg_parser in arg_parsers:
            # arg_parser.add_argument("-c", is_config_file=True, help="config file path")
            arg_parser.add_argument(
                '--debug',
                action='store_true',
                help='turn on debugging'
            )
            arg_parser.add_argument(
                '--logging-level',
                help='set logging-level level (see Python logging module)'
            )

    def __configure_logging(self, args):
        if args.debug:
            logging_level = logging.DEBUG
        elif args.logging_level is not None:
            logging_level = getattr(logging, args.logging_level.upper())
        else:
            logging_level = logging.INFO
        logging.basicConfig(
            format='%(asctime)s:%(processName)s:%(module)s:%(lineno)s:%(name)s:%(levelname)s: %(message)s',
            level=logging_level
        )

    def main(self):
        self.__add_arguments()
        args = self.__arg_parser.parse_args()
        self.__configure_logging(args)

        command_class = self.__COMMAND_CLASSES[args.command]
        command_kwds = vars(args).copy()
        # command_kwds.pop("c")
        command_kwds.pop("logging_level")
        command = command_class(**command_kwds)

        command()


def main():
    Cli().main()


if __name__ == '__main__':
    main()
