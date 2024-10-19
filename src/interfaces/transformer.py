#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: transformer.py
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


class CVSTransformerInterface(ABC):
    """Transform a CSV file with TSE data."""

    @abstractmethod
    def merge_csv_files(self) -> None:
        """Merge all CSV files in the source directory into a single file."""

        raise NotImplementedError("Method 'merge_csv_files' must be implemented.")
