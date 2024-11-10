#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: commands.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

from typing import List

from src.interfaces.controller import CommandInterface
from src.services.download_manager import DownloadManager
from src.services.extractor_manager import ExtractionManager
from src.services.file_aggregator import FileAggregator
from src.services.file_processor import FileProcessor
from src.services.transformer_csv import CVSTransformer
from src.utils.helpers import make_directory


class InitializeCommand(CommandInterface):
    """Initialize the project and download the data."""

    def __init__(self, output_dir: list):
        self.__output_dir = output_dir

    def execute(self) -> None:
        """Execute the initialize command."""

        for directory in self.__output_dir:
            make_directory(directory)


class DownloadCommand(CommandInterface):
    """Initialize the project and download the data."""

    def __init__(self,
                 download_manager: DownloadManager,
                 output_dir: str):

        self.__download_manager = download_manager
        self.__output_dir = output_dir

    def execute(self) -> None:
        """Execute the download command."""

        self.__download_manager.run(self.__output_dir)


class ExtractDataCommand(CommandInterface):
    """Extract the data from the downloaded files."""

    def __init__(self,
                 extractor: ExtractionManager,
                 output_dir: str,
                 extraction_dir: str):
        self.__extractor = extractor
        self.__output_dir = output_dir
        self.__extraction_dir = extraction_dir

    def execute(self) -> None:
        """Execute the extract data command."""

        self.__extractor.extract_all_files(self.__output_dir, self.__extraction_dir)


class MergeDataCommand(CommandInterface):
    """Merge the extracted data."""

    def __init__(self, transformers: List[CVSTransformer]):
        self.transformers = transformers

    def execute(self) -> None:
        """Execute the merge data command."""

        for transformer in self.transformers:
            transformer.transform()


class FileAggregateCommand(CommandInterface):
    """Aggregate the data."""

    def __init__(self, aggregator: FileAggregator):
        self.__aggregator = aggregator

    def execute(self) -> None:
        """Execute the file aggregation command."""

        self.__aggregator.aggregate_files()


class FileProcessorCommand(CommandInterface):
    """Process the data."""

    def __init__(self, file_processor: FileProcessor, aggregation_dir: str):
        self.__file_processor = file_processor
        self.__aggregation_dir = aggregation_dir

    def execute(self) -> None:
        """Execute the file processor command."""

        self.__file_processor.process_file(self.__aggregation_dir)
