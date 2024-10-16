#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: extractor_manager.py
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from zipfile import BadZipFile, ZipFile

from src.interfaces.extractor import ExtractionManagerInterface
from src.utils.helpers import (
    delete_file,
    extract_year_from_zip_file_name,
    make_directory,
)


class ExtractionManager(ExtractionManagerInterface):

    def __init__(self, max_workers: int = 3) -> None:
        self.__max_workers = max_workers

    def __extract_and_clean(self, zip_file: str, output_directory: str) -> None:

        try:
            make_directory(output_directory)

            with ZipFile(zip_file, 'r') as zip_ref:
                print(f'Extracting {zip_file} to {output_directory}...')
                zip_ref.extractall(output_directory)

            readme_files = glob.glob(f'{output_directory}/*.pdf')
            if readme_files:
                for file in readme_files:
                    print(f'Removing {file}...')
                    delete_file(file)
        except BadZipFile as error:
            print(f'The file {zip_file} is corrupt or invalid.')
            print(error)
            raise
        except Exception as error:
            print(f'An error occurred while extracting {zip_file}.')
            print(error)
            raise

    def extract_all_files(self, source_directory: str, output_directory: str) -> None:

        zip_files = glob.glob(f'{source_directory}/*.zip')

        if not zip_files:
            print(f'No compressed files found in {source_directory}.')
            return

        with ThreadPoolExecutor(max_workers=self.__max_workers) as executor:
            futures = {
                executor.submit(
                    self.__extract_and_clean,
                    zip_file,
                    f'{output_directory}/{extract_year_from_zip_file_name(zip_file)}',
                ): zip_file for zip_file in zip_files
            }

            for future in as_completed(futures):
                year = futures[future]
                future.result()
                print(f'Extraction of {year} completed successfully.')

        print('All files extracted successfully.')
