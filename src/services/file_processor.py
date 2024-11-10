#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: file_processor.py
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

import glob

import pandas as pd

from src.interfaces.processor import FileProcessorInterface
from src.utils.political_parties import (incorporated_parties,
                                         merged_parties,
                                         parties_that_changed_names)


class FileProcessor(FileProcessorInterface):

    def __get_csv_files(self, source_directory: str, extension: str = '*.csv',) -> list:
        """Get all CSV files in the source directory."""

        return glob.glob(f'{source_directory}/{extension}')

    def __load_csv_file(self, file_path: str) -> pd.DataFrame:
        """Load a CSV file into a pandas DataFrame."""

        return pd.read_csv(file_path, sep=';', encoding='latin1')

    def __fetch_brazilian_party_positions(self) -> pd.DataFrame:
        """Load positions of Brazilian parties."""

        return pd.read_csv('data/positions_brazilian_parties.csv')

    def __process_incorporated_parties(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Incorporate parties that were incorporated."""

        dataframe['SG_PARTIDO'].map(incorporated_parties)

        return dataframe

    def __process_merged_parties(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Merge parties that were merged."""
        dataframe['SG_PARTIDO'].map(merged_parties)

        return dataframe

    def __process_parties_that_changed_names(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Rename parties that changed names."""

        dataframe['SG_PARTIDO'].map(parties_that_changed_names)

        return dataframe

    def __apply_new_maps_for_parties(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Apply new maps for parties."""

        # Apply maps for parties that were incorporated.
        dataframe = self.__process_incorporated_parties(dataframe)

        # Apply maps for parties that were merged.
        dataframe = self.__process_merged_parties(dataframe)

        # Apply maps for parties that changed names.
        dataframe = self.__process_parties_that_changed_names(dataframe)

        return dataframe

    def __integrate_brazilian_party_roles(self, dataframe: pd.DataFrame) -> pd.DataFrame:

        # Load positions of Brazilian parties.
        positions_brazilian_parties_df = self.__fetch_brazilian_party_positions()

        # Merge positions of Brazilian parties with the DataFrame.
        dataframe = pd.merge(dataframe,
                             positions_brazilian_parties_df,
                             left_on='SG_PARTIDO',
                             right_on='Partido',
                             how='left')

        return dataframe

    def __save_processed_data(self,
                              dataframe: pd.DataFrame,
                              data_directory: str,
                              file_name: str,
                              file_type: str = 'parquet') -> None:
        """Save the processed DataFrame."""

        try:
            if file_type == 'parquet':
                dataframe.to_parquet(f'{data_directory}/{file_name}.parquet', index=False)
            else:
                dataframe.to_csv(f'{data_directory}/{file_name}.csv',
                                 index=False,
                                 sep=';',
                                 encoding='utf-8')
        except IOError as error:
            print(f'Error saving the processed data: {file_name}.{file_type}')
            print(f'Error: {error}')

    def process_file(self, source_directory: str) -> None:
        """Process a file with voting data."""

        for file_path in self.__get_csv_files(source_directory):
            # Get the file name to save the processed data.
            file_name = file_path.split('\\')[-1].split('.')[0]
            print(f'Processing file: {file_path}.csv')

            # Load the CSV file with the voting data.
            voting_df = self.__load_csv_file(file_path)

            # Apply new maps for parties in the DataFrame.
            voting_df = self.__apply_new_maps_for_parties(voting_df)

            # Merge positions of Brazilian parties with the DataFrame.
            voting_df = self.__integrate_brazilian_party_roles(voting_df)

            # Save the processed election data.
            self.__save_processed_data(voting_df, 'data', file_name, file_type='parquet')
