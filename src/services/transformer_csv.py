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
from typing import Iterator, List

from src.interfaces.transformer import CVSTransformerInterface
from src.utils.helpers import TSECVSDialect


class CVSTransformer(CVSTransformerInterface):
    """Transform a CSV file with TSE data."""

    def __init__(self, source_directory: str, output_dir: str, output_file: str) -> None:
        self.__source_directory = source_directory
        self.__output_dir = output_dir
        self.__output_file = output_file
        self.__output_file_path = f'{self.__output_dir}/{self.__output_file.format(output_dir.split('/')[-1])}'

    def __get_csv_files(self,
                        extension: str = '*[0-9][0-9][0-9][0-9]_[A-Z][A-Z].csv',
                        scenario_filter: str = 'uf') -> list:
        """Get all CSV files in the source directory."""

        if scenario_filter == 'uf':
            return glob.glob(f'{self.__source_directory}/{extension}')

        return glob.glob(f'{self.__source_directory}/*.cvs')

    def __read_csv_rows(self,
                        file_path: str,
                        file_encoding: str = 'latin-1') -> Iterator[List[str]]:
        """Read a CSV file and return its content."""

        try:
            with open(file_path, mode='r', encoding=file_encoding) as file_object:
                csv_reader = csv.reader(file_object, dialect=TSECVSDialect)

                yield from csv_reader

        except csv.Error as csv_error:
            print(f'File not found: {csv_error}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')

    def __skip_csv_header(self, data: Iterator[List[str]]) -> Iterator[List[str]]:
        """Skip the header of a CSV file."""

        return (row for index, row in enumerate(data) if index > 0)

    def __write_csv_rows(self, data: Iterator[List[str]],  file_encoding: str = 'latin-1') -> None:
        """Write data to a CSV file."""

        # Checking if the target file already exists and has no content.
        output_file_exists = os.path.exists(self.__output_file_path)
        output_file_not_empty = output_file_exists and os.path.getsize(self.__output_file_path) > 0

        try:
            with open(self.__output_file_path,
                      mode='a',
                      encoding=file_encoding,
                      newline='') as file_object:
                csv_writer = csv.writer(file_object, dialect=TSECVSDialect)

                if output_file_not_empty:
                    data = self.__skip_csv_header(data)

                csv_writer.writerows(data)

        except csv.Error as csv_error:
            print(f'CSV Error: {csv_error}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')

    def merge_csv_files(self) -> None:
        """Merge all CSV files in the source directory into a single file."""

        if not os.path.exists(self.__source_directory) and not os.path.isdir(self.__source_directory):
            raise FileNotFoundError(f'{self.__source_directory} does not exist or is not a directory.')

        csv_files = self.__get_csv_files()
        if not csv_files:
            raise FileNotFoundError(f'No CSV files found in {self.__source_directory}.')

        for csv_file in csv_files:
            csv_data = self.__read_csv_rows(csv_file, 'latin-1')
            self.__write_csv_rows(csv_data)
