#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: download_manager.py
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

from os import path
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.interfaces.handler import DownloadManagerInterface
from src.models.election_year import ElectionYear
from src.services.file_downloader import FileDownloader
from src.utils.helpers import generate_election_years


class DownloadManager(DownloadManagerInterface):

    def __init__(self,
                 election_year: ElectionYear,
                 file_downloader: FileDownloader,
                 start_year,
                 end_year,
                 max_threads=5):

        if start_year > end_year:
            raise ValueError("start_year must be less than or equal to end_year")

        self.__election_year = election_year
        self.__file_downloader = file_downloader

        self.__start_year = start_year
        self.__end_year = end_year
        self.__max_threads = max_threads

    def run(self, output_dir: str = 'downloads'):

        with ThreadPoolExecutor(max_workers=self.__max_threads) as executor:
            futures = {}
            for year in generate_election_years(self.__start_year, self.__end_year):
                election_year_instance = self.__election_year(year)
                url = election_year_instance.generate_url()
                file_path = path.join(output_dir, election_year_instance.file_name())
                future = executor.submit(self.__file_downloader.download_file, url, file_path)
                futures[future] = year

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as error:
                    year = futures[future]
                    print(f"An unexpected error occurred {year}: {error}")
