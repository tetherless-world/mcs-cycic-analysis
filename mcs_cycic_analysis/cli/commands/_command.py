import logging
from abc import ABC, abstractmethod, abstractclassmethod

from configargparse import ArgParser


class _Command(ABC):
    def __init__(self, **kwds):
        self._logger = logging.getLogger(self.__class__.__name__)

    @classmethod
    def add_arguments(cls, arg_parser: ArgParser):
        """
        Add arguments to the given argparser.
        The parsed arguments are passed to the subclass's constructor as **kwds.
        """

    def __call__(self):
        pass
