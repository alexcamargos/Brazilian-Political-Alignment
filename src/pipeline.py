#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: pipeline.py
#  Version: 0.0.1
#
#  Summary: Alinhamento Político Brasileiro
#           Este projeto busca identificar tendencias políticas nos municípios
#           brasileiros ao longo do tempo, classificando os prefeitos eleitos
#           em direita, esquerda ou centro, com base no diagrama de Nolan.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

from typing import List

from src.models.election_year import ElectionYear
from src.services.commands import (DownloadCommand,
                                   ExtractDataCommand,
                                   InitializeCommand,
                                   MergeDataCommand)
from src.services.download_manager import DownloadManager
from src.services.extractor_manager import ExtractionManager
from src.services.file_downloader import FileDownloader
from src.services.transformer_csv import CVSTransformer


class Pipeline:
    """Pipeline to download, extract, and transform data."""

    def __init__(self,
                 start_year: int,
                 end_year: int,
                 downloads_dir: str,
                 extraction_dir: str,
                 transformer_dir: str,
                 output_file: str) -> None:

        self.__start_year = start_year
        self.__end_year = end_year
        self.__downloads_dir = downloads_dir
        self.__extraction_dir = extraction_dir
        self.__transformer_dir = transformer_dir
        self.__output_file = output_file

        self.__file_downloader = FileDownloader()

        self.__download_manager = DownloadManager(ElectionYear,
                                                  self.__file_downloader,
                                                  self.__start_year,
                                                  self.__end_year)
        self.__extractor = ExtractionManager()

        self.__transformer = CVSTransformer(self.__transformer_dir,
                                            self.__transformer_dir,
                                            self.__output_file)

        # Defining all available commands.
        self.__commands = {
            'initialize': InitializeCommand([self.__downloads_dir,
                                             self.__extraction_dir,
                                             self.__transformer_dir]),
            'download': DownloadCommand(self.__download_manager,
                                        self.__downloads_dir),
            'extract': ExtractDataCommand(self.__extractor,
                                          self.__downloads_dir,
                                          self.__extraction_dir),
            'merge': MergeDataCommand(self.__transformer)
        }

    def run(self, commands_to_run: List[str] = None) -> None:
        """Executes one of the steps in the data pipeline.

        Args:
            command (str, optional): The command to be executed. Defaults to 'initialize'.

        Raises:
            ValueError: If the command is not valid.
        """

        print('Running pipeline...')

        # If not command to run, run all commands.
        if commands_to_run is None:
            commands_to_run = list(self.__commands.keys())

        # Validating the commands.
        for command in commands_to_run:
            if command not in self.__commands:
                raise ValueError(f'Command "{command}" is not valid. Available commands: {list(self.__commands.keys())}')

        # Running the commands.
        for command in commands_to_run:

            try:
                print(f'Running command: {command}')
                self.__commands[command].execute()
            except Exception as error:
                print(f'Error in command "{command}": {error}')
                raise

        print('Pipeline executed successfully.')
