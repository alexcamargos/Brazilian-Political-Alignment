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

        # Filter the dataset by the selected position.
        position_df = self.__filter_position()
        elected_position_df = position_df[position_df['DS_SIT_TOT_TURNO'] == 'ELEITO']

        # Convert the 'Espectro' column to a categorical and ordered type.
        spectrum_type = pd.CategoricalDtype(categories=['Esquerda', 'Centro', 'Direita'], ordered=True)
        elected_position_df['Espectro'] = elected_position_df.loc[:, 'Espectro'].astype(spectrum_type)

        # Group the dataset by candidate and aggregate the votes.
        aggregated_elected_candidates_df = (
            elected_position_df.groupby('SQ_CANDIDATO')
            .agg({'SG_UF': 'first',
                  'SG_UE': 'first',
                  'NM_UE': 'first',
                  'CD_MUNICIPIO': 'first',
                  'NM_MUNICIPIO': 'first',
                  'SG_PARTIDO': 'first',
                  'NR_PARTIDO': 'first',
                  'NM_PARTIDO': 'first',
                  'NR_CANDIDATO': 'first',
                  'NM_CANDIDATO': 'first',
                  'NM_URNA_CANDIDATO': 'first',
                  'Espectro': 'first',
                  'Espectro_Detalhado': 'first',
                  'Posicionamento': 'first',
                  'QT_VOTOS_NOMINAIS': 'sum'})
            .reset_index())

        return aggregated_elected_candidates_df

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
