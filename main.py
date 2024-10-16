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
from src.services.extractor_manager import ExtractionManager
from src.services.file_downloader import FileDownloader
from src.utils.helpers import make_directory

if __name__ == '__main__':
    START_YEAR = 1990
    END_YEAR = 2024
    OUTPUT_DIR = 'downloads'
    DATA_DIR = 'data'

    downloader = FileDownloader()
    extractor = ExtractionManager()

    make_directory(OUTPUT_DIR)

    manager = DownloadManager(ElectionYear, downloader, START_YEAR, END_YEAR)
    manager.run(OUTPUT_DIR)

    extractor.extract_all_files(OUTPUT_DIR, DATA_DIR)
