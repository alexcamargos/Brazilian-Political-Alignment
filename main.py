#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: main.py
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

import os

import requests


class ElectionYear:

    BASE_URL = 'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/'

    def __init__(self, year):
        self.year = year

    def generate_url(self):
        return f'{self.BASE_URL}votacao_candidato_munzona_{self.year}.zip'

    def file_name(self):
        return f'votacao_candidato_munzona_{self.year}.zip'


class DownloadManager:

    def __init__(self, start_year, end_year, download_dir):
        self.start_year = start_year
        self.end_year = end_year
        self.download_dir = download_dir

        self.__make_directory()

    def __make_directory(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def __populate_election_years(self):

        return list(range(self.start_year, self.end_year + 1, 4))

    def __download_file(self, url, path):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            with open(path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        except requests.exceptions.HTTPError as http_error:
            print(f'HTTP Error: {http_error}')
        except requests.exceptions.RequestException as request_exception:
            print(f'Request Exception: {request_exception}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')
        except Exception as error:  # pylint: disable=broad-except
            print(f'Unexpected error: {error}')

            raise error

    def run(self):
        election_years = self.__populate_election_years()

        for year in election_years:
            election_year = ElectionYear(year)
            url = election_year.generate_url()
            path = os.path.join(self.download_dir, election_year.file_name())
            self.__download_file(url, path)


if __name__ == '__main__':
    START_YEAR = 2020
    END_YEAR = 2024

    manager = DownloadManager(START_YEAR, END_YEAR, 'downloads')
    manager.run()
