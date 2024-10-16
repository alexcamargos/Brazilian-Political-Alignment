#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: election_year_interface.py
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

from abc import ABC, abstractmethod


class ElectionYearInterface(ABC):

    BASE_URL = 'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/'

    @abstractmethod
    def generate_url(self):
        raise NotImplementedError('Method "generate_url" must be implemented.')

    @abstractmethod
    def file_name(self):
        raise NotImplementedError('Method "file_name" must be implemented.')
