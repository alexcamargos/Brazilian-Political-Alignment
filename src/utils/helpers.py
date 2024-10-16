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


def make_directory(path: str, exist_ok: bool = True) -> None:
    """Create a directory if it does not exist."""

    os.makedirs(path, exist_ok=exist_ok)


def delete_file(file_path: str) -> None:
    """Delete a file."""

    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)


def generate_election_years(start_year: int, end_year: int, interval: int = 4) -> list:
    """Generate a list of election years."""

    known_municipal_election = 2024

    offset = (start_year - known_municipal_election) % interval
    first_municipal_election_year = start_year - offset

    if first_municipal_election_year < start_year:
        first_municipal_election_year += interval

    return list(range(first_municipal_election_year, end_year + 1, interval))


def extract_year_from_zip_file_name(file_name: str) -> str:
    """Extract the year from a zip file name."""

    base_name = os.path.basename(file_name)
    name_parts = base_name.split('_')
    year = name_parts[-1]

    return year.replace('.zip', '')
