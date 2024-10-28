#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: file_aggregator.py
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

import shutil
import glob

from src.interfaces.aggregator import FileAggregatorInterface


class FileAggregator(FileAggregatorInterface):

    def __init__(self, input_dir: str, output_dir: str) -> None:
        self.__input_dir = input_dir
        self.__output_dir = output_dir

    def __get_all_aggregated_files(self,
                                   pattern: str = 'merge_votacao_candidato_munzona_????.csv') -> list:
        """Get all aggregated files in the output directory.

        Arguments:
            pattern {str} -- Pattern to search for files. Defaults to 'merge_votacao_candidato_munzona_????.csv'.
        """

        return glob.glob(f'{self.__input_dir}/**/{pattern}', recursive=True)

    def aggregate_files(self) -> None:
        """Aggregate all CSV files in the input directory in output directory.

        Raises:
            FileNotFoundError: If no CSV files are found in the input directory.
        """

        agregated_files = self.__get_all_aggregated_files()

        if not agregated_files:
            raise FileNotFoundError(f'No CSV files found in {self.__input_dir}.')

        for file in agregated_files:
            try:
                shutil.copy(file, self.__output_dir)
            except shutil.Error as error:
                print(f'Error copying file: {error}')
