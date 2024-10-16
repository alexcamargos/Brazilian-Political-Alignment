#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: helpers.py
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
# pylint: disable=missing-module-docstring, missing-function-docstring

import os


def make_directory(path: str):
    """Create a directory if it does not exist."""

    if not os.path.exists(path):
        os.makedirs(path)


def generate_election_years(start_year: int, end_year: int, interval: int = 4) -> list:
    """Generate a list of election years."""

    known_municipal_election = 2024

    offset = (start_year - known_municipal_election) % interval
    first_municipal_election_year = start_year - offset

    if first_municipal_election_year < start_year:
        first_municipal_election_year += interval

    return list(range(first_municipal_election_year, end_year + 1, interval))
