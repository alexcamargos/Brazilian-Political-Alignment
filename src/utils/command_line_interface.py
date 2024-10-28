#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: command_line_interface.py
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

import argparse


def get_arguments() -> argparse.Namespace:
    """Get command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """

    # Create the parser.
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='Este projeto busca identificar tendencias políticas nos municípios '
                    'brasileiros ao longo do tempo, classificando os prefeitos eleitos '
                    'em direita, esquerda ou centro, com base no diagrama de Nolan.'
    )

    # Add the arguments.
    parser.add_argument('-i',
                        '--initialize',
                        action='store_true',
                        help='Run the initialization step.'
                        )

    parser.add_argument('-d',
                        '--download',
                        action='store_true',
                        help='Run the download step.'
                        )

    parser.add_argument('-e',
                        '--extract',
                        action='store_true',
                        help='Run the extraction step.'
                        )

    parser.add_argument('-m',
                        '--merge',
                        action='store_true',
                        help='Run the merge step.'
                        )

    parser.add_argument('-g',
                        '--aggregate',
                        action='store_true',
                        help='Run the aggregation step.'
                        )

    parser.add_argument('-a',
                        '--all',
                        action='store_true',
                        help='Run all steps.'
                        )

    # Parse the arguments.
    return parser.parse_args()
