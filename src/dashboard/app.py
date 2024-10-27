#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: app.py
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
import plotly.express as px
import streamlit as st


def filter_position(data: pd.DataFrame, position: str) -> pd.DataFrame:
    """Filter the dataset by a specific position.

    Parameters:
        - data: DataFrame with election data.
        - position: Position to filter the dataset.

    Returns:
        - DataFrame with only the selected position.
    """

    return data[data['DS_CARGO'] == position]


def filter_position_by_situation(data: pd.DataFrame,
                                 position: str,
                                 situation: str) -> pd.DataFrame:
    """Filter only elected mayors from the dataset.

    Parameters:
        - data: DataFrame with election data.
        - position: Position to filter the dataset.
        - situation: Situation to filter the dataset.

    Returns:
        - DataFrame with only elected mayors.
    """

    elected_position_df = data[data[position] == situation]

    # Drop duplicates to keep only one row per candidate.
    elected_position_df = elected_position_df.drop_duplicates(subset=['SQ_CANDIDATO'])

    return elected_position_df


def count_mayors_by_party(data: pd.DataFrame) -> pd.DataFrame:
    """Count the number of mayors elected by party.

    Parameters:
        - data: DataFrame with election data.

    Returns:
        - DataFrame with the number of mayors elected by party.
    """

    party_counts = data['SG_PARTIDO'].value_counts().reset_index()
    party_counts.columns = ['Partido', 'Quantidade']
    party_counts = party_counts.sort_values(by='Quantidade', ascending=False)

    return party_counts


@st.cache_resource
def create_bar_chart_party_counts(party_counts: pd.DataFrame) -> px.bar:
    """Create a bar chart with the number of mayors elected by party.

    Parameters:
        - party_counts: DataFrame with the number of mayors elected by party.

    Returns:
        - Bar chart with the number of mayors elected by party.
    """

    fig = px.bar(party_counts,
                 x='Partido',
                 y='Quantidade',
                 title='Quantidade de Prefeitos Eleitos por Partido',
                 labels={'Partido': 'Partido',
                         'Quantidade': 'Número de Prefeitos Eleitos'},
                 color='Partido',
                 text='Quantidade')

    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title='Partido',
                      yaxis_title='Número de Prefeitos Eleitos',
                      uniformtext_minsize=8,
                      uniformtext_mode='hide')

    return fig


@st.cache_data
def load_election_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path,
                       encoding='latin1',
                       sep=';', decimal=',')


def set_page_config() -> None:
    st.set_page_config(page_title='Alinhamento Político Brasileiro',
                       page_icon=':chart_with_upwards_trend:',
                       layout='wide',
                       initial_sidebar_state='auto')


def dashboard_banner() -> None:
    st.title('Alinhamento Político Brasileiro (Direita, Esquerda ou Centro): Análise dos Prefeitos Eleitos de 1992 a 2024')
    st.write('Este projeto de análise de dados tem como objetivo comparar, desde 1992 até as eleições de 2024, o',
             'espectro político dos candidatos a prefeito eleitos em cada município do Brasil. Através desta',
             'análise histórica, busca-se compreender as tendências políticas municipais ao longo dos anos,',
             'identificando padrões e mudanças no alinhamento político brasileiro. Para isso, serão utilizados os',
             'conceitos do Diagrama de Nolan, que oferece uma visão bidimensional do espectro político,',
             'considerando tanto a liberdade econômica quanto as liberdades pessoais.')


def dasboard_footer() -> None:
    st.markdown(
        """
        <div style="text-align: center;">
            <p>Copyright © 2024 - Alexsander Lopes Camargos</p>
            <p>Feito com Streamlit, Plotly e Pandas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def main_page() -> None:

    DATA_FILE_PATH = 'extractions/2024/merge_votacao_candidato_munzona_2024.csv'

    # Set the page configuration.
    set_page_config()

    # Display the project banner.
    dashboard_banner()

    # Load and filter the election data.
    datafame = load_election_data(DATA_FILE_PATH)

    if not datafame.empty:
        mayors_df = filter_position(datafame, 'Prefeito')
        elected_mayors_df = filter_position_by_situation(mayors_df,
                                                         'DS_SIT_TOT_TURNO',
                                                         'ELEITO')
        party_counts_df = count_mayors_by_party(elected_mayors_df)

        # Display the project content.
        st.subheader('Prefeitos eleitos em 2024')
        chart = create_bar_chart_party_counts(party_counts_df)

        st.plotly_chart(chart)

        st.write('---')
        st.subheader('Dados utilizados')
        st.write(
            'Abaixo, você pode conferir os dados utilizados para a análise dos prefeitos eleitos em 2024.')
        st.write(elected_mayors_df)
    else:
        st.write('Os dados não foram carregados. Contate o administrador do sistema.')

    # Display the project footer.
    dasboard_footer()
