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

from src.models.election_year import ElectionYear
from src.services.download_manager import DownloadManager
from src.services.file_downloader import FileDownloader
from src.utils.helpers import make_directory

if __name__ == '__main__':
    START_YEAR = 2020
    END_YEAR = 2024
    OUTPUT_DIR = 'downloads'

    election_year = ElectionYear()
    downloader = FileDownloader()

    make_directory(OUTPUT_DIR)

    manager = DownloadManager(election_year, downloader, START_YEAR, END_YEAR)
    manager.run(OUTPUT_DIR)
