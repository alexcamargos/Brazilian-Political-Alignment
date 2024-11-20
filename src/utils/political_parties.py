#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: political_parties.py
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


# Mapping of mergers, acquisitions and name changes made based on the list
# available on the TSE website.
# URL: https://www.tse.jus.br/partidos/partidos-registrados-no-tse/registrados-no-tse
# Data da consulta: 11/11/2024.

# Mapping of brazilians merged parties.
parties_merged_mapping = {
    'PP': 'PPB',
    'PPR': 'PPB',
    'PRONA': 'PR',
    'PL': 'PR',
    'PSL': 'UNIÃO',
    'DEM': 'UNIÃO',
    'PTB': 'PRD',
    'PATRIOTA': 'PRD'
}


# Mapping of brazilians incorporated parties.
parties_incorporated_mapping = {
    'PGT': 'PL',
    'PST': 'PL',
    'PSD': 'PTB',
    'PAN': 'PTB',
    'PRP': 'PEN',
    'PPL': 'PC do B',
    'PHS': 'PODE',
    'PROS': 'SOLIDARIEDADE',
    'PSC': 'PODE'
}

# Mapping of brazilians parties that changed their name.
parties_changed_names_mapping = {
    'PSN': 'PHS',
    'PRN': 'PTC',
    'PPB': 'PP',
    'PFL': 'DEM',
    'PMR': 'PRB',
    'PTN': 'PODE',
    'PT do B': 'AVANTE',
    'PMDB': 'MDB',
    'PEN': 'PATRI',
    'PSDC': 'DC',
    'SD': 'SOLIDARIEDADE',
    'PR': 'PL',
    'PATRI': 'PATRIOTA',
    'PRB': 'REPUBLICANOS',
    'PPS': 'CIDADANIA',
    'PTC': 'AGIR',
    'PMN': 'MOBILIZA'
}
