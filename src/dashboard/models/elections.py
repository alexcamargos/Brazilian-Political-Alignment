#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: elections.py
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

import pandas as pd


class Election():
    """Class to represent a municipal election."""

    def __init__(self, data: pd.DataFrame, position: str = 'Prefeito') -> None:
        self.__data = data
        self.__position = position

        # Filter the dataset by elected position.
        self.__filter_data = self.__filter_elected_position()

    def __filter_position(self) -> pd.DataFrame:
        """Filter the dataset by a specific position.

        Returns:
            - DataFrame with only the selected position.
        """

        return self.__data[self.__data['DS_CARGO'] == self.__position]

    def __filter_elected_position(self) -> pd.DataFrame:
        """Filter only elected mayors from the dataset.

        Returns:
            - DataFrame with only elected mayors.
        """

        position_df = self.__filter_position()
        elected_position_df = position_df[position_df['DS_SIT_TOT_TURNO'] == 'ELEITO']
        drop_elected_position_df = elected_position_df.drop_duplicates(subset=['SQ_CANDIDATO'])

        return drop_elected_position_df

    @property
    def filter_data(self) -> pd.DataFrame:
        """Return the filtered dataset."""

        return self.__filter_data

    def count_by_party(self) -> pd.DataFrame:
        """Count the number of mayors elected by party.

        Returns:
            - DataFrame with the number of mayors elected by party.
        """

        party_counts = self.__filter_data['SG_PARTIDO'].value_counts().reset_index()
        party_counts.columns = ['Partido', 'Quantidade']
        party_counts = party_counts.sort_values(by='Quantidade', ascending=False)

        return party_counts

    def top5_states_by_party(self) -> dict:
        """Get the top 5 states with the highest number of mayors elected per party.

        Returns:
            - Dictionary where keys are party codes and values are DataFrames with top 5 states and their counts.
        """

        parties = self.__filter_data['SG_PARTIDO'].unique()

        top5_dict = {}
        for party in parties:
            party_data = self.__filter_data[self.__filter_data['SG_PARTIDO'] == party]
            state_counts = party_data['SG_UF'].value_counts().nlargest(5).reset_index()
            state_counts.columns = ['Estado', 'Quantidade']
            top5_dict[party] = state_counts

        return top5_dict
