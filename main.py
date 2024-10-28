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

from src.pipeline import Pipeline
from src.utils.command_line_interface import get_arguments


if __name__ == '__main__':

    # Get the command-line arguments.
    args = get_arguments()

    START_YEAR = 1996
    END_YEAR = 2024
    DOWNLOADS_DIR = 'downloads'
    EXTRACTION_DIR = 'extractions'
    TRANSFORMER_DIR = EXTRACTION_DIR
    AGGREGATED_DIR = 'aggregated'
    OUTPUT_FILE = 'merge_votacao_candidato_munzona_{}.csv'

    pipeline = Pipeline(START_YEAR,
                        END_YEAR,
                        DOWNLOADS_DIR,
                        EXTRACTION_DIR,
                        TRANSFORMER_DIR,
                        AGGREGATED_DIR,
                        OUTPUT_FILE)

    # All available commands.
    available_commands = ['initialize', 'download', 'extract', 'merge', 'aggregate']
    # Get the commands to run.
    commands_to_run = [command for command in available_commands if getattr(args, command)]

    # Run the corresponding commands.
    if commands_to_run:
        pipeline.run(commands_to_run)
    elif args.all:
        pipeline.run()
    else:
        print('No command was given. Please, use --help to see the available commands.')
