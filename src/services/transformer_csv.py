#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: transformer.py
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

import csv
import glob
import os

from src.interfaces.transformer import CVSTransformerInterface
from src.utils.helpers import TSECVSDialect


class CVSTransformer(CVSTransformerInterface):
    """Transform a CSV file with TSE data."""

    def __init__(self, source_directory: str, output_file: str) -> None:
        self.source_directory = source_directory
        self.output_file = output_file

    def __get_csv_files(self,
                        extension: str = '*[0-9][0-9][0-9][0-9]_[A-Z][A-Z].csv',
                        scenario_filter: str = 'uf') -> list:
        """Get all CSV files in the source directory."""

        if scenario_filter == 'uf':
            return glob.glob(f'{self.source_directory}/{extension}')

        return glob.glob(f'{self.source_directory}/*.cvs')

    def __read_csv_rows(self, file_path: str, file_encoding: str = 'latin-1') -> list:
        """Read a CSV file and return its content."""

        try:
            with open(file_path, mode='r', encoding=file_encoding) as file_object:
                csv_reader = csv.reader(file_object, dialect=TSECVSDialect)

                yield from csv_reader

        except csv.Error as csv_error:
            print(f'File not found: {csv_error}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')

    def __write_csv__rows(self, data: list,  file_encoding: str = 'latin-1') -> None:
        """Write data to a CSV file."""

        try:
            with open(self.output_file,
                      mode='a',
                      encoding=file_encoding,
                      newline='') as file_object:
                csv_writer = csv.writer(file_object, dialect=TSECVSDialect)
                csv_writer.writerows(data)

        except csv.Error as csv_error:
            print(f'CSV Error: {csv_error}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')

    def merge_csv_files(self) -> None:
        """Merge all CSV files in the source directory into a single file."""

        if not os.path.exists(self.source_directory) and not os.path.isdir(self.source_directory):
            raise FileNotFoundError(f'{self.source_directory} does not exist or is not a directory.')

        csv_files = self.__get_csv_files()
        if not csv_files:
            raise FileNotFoundError(f'No CSV files found in {self.source_directory}.')

        for index, csv_file in enumerate(csv_files):
            csv_data = self.__read_csv_rows(csv_file, 'latin-1')

            if index > 0:
                continue

            self.__write_csv__rows(csv_data)
