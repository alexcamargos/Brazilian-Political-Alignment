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

from src.interfaces.handler import DownloadManagerInterface
from src.models.election_year import ElectionYear
from src.services.file_downloader import FileDownloader
from src.utils.helpers import generate_election_years


class DownloadManager(DownloadManagerInterface):

    def __init__(self,
                 election_year: ElectionYear,
                 file_downloader: FileDownloader,
                 start_year,
                 end_year):

        if start_year > end_year:
            raise ValueError("start_year must be less than or equal to end_year")

        self.__url_generator = election_year
        self.__file_downloader = file_downloader

        self.__start_year = start_year
        self.__end_year = end_year

    def run(self, output_dir: str = 'downloads'):

        for year in generate_election_years(self.__start_year, self.__end_year):
            self.__url_generator.year = year
            file_path = path.join(output_dir, self.__url_generator.file_name())
            self.__file_downloader.download_file(self.__url_generator.generate_url(),
                                                 file_path)
