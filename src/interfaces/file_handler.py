#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: file_handler.py
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


class FileDownloaderInterface(ABC):

    @abstractmethod
    def download_file(self, url: str, file_path: str):
        raise NotImplementedError('Method "download_file" must be implemented.')