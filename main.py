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

from src.pipeline import Pipeline


if __name__ == '__main__':
    START_YEAR = 1990
    END_YEAR = 2024
    DOWNLOADS_DIR = 'downloads'
    EXTRACTION_DIR = 'data'
    TRANSFORMER_DIR = f'{EXTRACTION_DIR}/2024'
    OUTPUT_FILE = 'output_merge.csv'

    pipeline = Pipeline(START_YEAR,
                        END_YEAR,
                        DOWNLOADS_DIR,
                        EXTRACTION_DIR,
                        TRANSFORMER_DIR,
                        OUTPUT_FILE)
    pipeline.run()
