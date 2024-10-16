#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: election_year.py
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

from src.models.election_year_interface import ElectionYearInterface


class ElectionYear(ElectionYearInterface):

    def __init__(self, year: int = 2024):
        self.__year = year

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        self.__year = year

    def generate_url(self):
        return f'{self.BASE_URL}votacao_candidato_munzona_{self.year}.zip'

    def file_name(self):
        return f'votacao_candidato_munzona_{self.year}.zip'
