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

import glob

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.models.elections import Election


@st.cache_resource
def create_bar_chart_party_counts(party_counts: pd.DataFrame, year: str) -> go.Figure:
    """Create a bar chart with the number of mayors elected by party.

    Parameters:
        - party_counts: DataFrame with the number of mayors elected by party.
        - year: Year of the election.

    Returns:
        - Bar chart with the number of mayors elected by party.
    """

    fig = px.bar(party_counts,
                 x='Partido',
                 y='Quantidade',
                 title=f'Quantidade de Prefeitos Eleitos por Partido - {year}',
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
    """Load the election data from a parquet file.

    Arguments:
        - file_path: Path to the parquet file.

    Returns:
        - DataFrame with the election data.
    """

    return pd.read_parquet(file_path)


def setup_dashboard_configuration() -> None:
    st.set_page_config(page_title='Alinhamento Político Brasileiro',
                       page_icon=':chart_with_upwards_trend:',
                       layout='wide',
                       initial_sidebar_state='auto')


@st.cache_resource
def dashboard_banner() -> None:
    st.title(
        'Alinhamento Político Brasileiro (Direita, Esquerda ou Centro): Análise dos Prefeitos Eleitos de 1992 a 2024'
        )
    st.write('Este projeto de análise de dados tem como objetivo comparar, desde 1992 até as eleições de 2024,'
             'o espectro político dos candidatos a prefeito eleitos em cada município do Brasil. Através desta',
             'análise histórica, busca-se compreender as tendências políticas municipais ao longo dos anos,',
             'identificando padrões e mudanças no alinhamento político brasileiro. Para isso, serão utilizados os',
             'conceitos do Diagrama de Nolan, que oferece uma visão bidimensional do espectro político,',
             'considerando tanto a liberdade econômica quanto as liberdades pessoais.')


@st.cache_resource
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


@st.cache_data
def list_all_elections_files(data_directory: str,
                             file_extension: str = 'parquet') -> list[glob.glob]:
    """List all election data files from a directory.

    Arguments:
        - data_directory: Path to the directory with the election data files.
        - file_extension: Extension of the election data files.

    Returns:
        - List with the available election data files.
    """

    # Find all file matching the pattern in the data directory.
    file_pattern = f'{data_directory}/*.{file_extension}'

    # Return the list of files in reverse order.
    return glob.glob(file_pattern)[::-1]


def main_page() -> None:
    """Default page of the dashboard."""
    
    # Set the page configuration.
    setup_dashboard_configuration()

    # Display the page banner.
    dashboard_banner()

    # Display the header of the analysis.
    st.subheader('Análise dos Prefeitos Eleitos por Partido Político')

    # List all election data files.
    data_directory = 'data'
    parquet_data_files = list_all_elections_files(data_directory)

    # Load the election data from the parquet files.
    all_elections_data = [load_election_data(file) for file in parquet_data_files]

    # Create containers separated into tabs for each election year.
    election_years = [year.split('.')[0].split('_')[-1] for year in parquet_data_files]
    tabs = st.tabs(election_years)

    # Display the graphs of elected mayors by party for each election.
    for index, election_data in enumerate(all_elections_data):
        with tabs[index]:
            if election_data.empty:
                st.write('Os dados não foram carregados. Contate o administrador do sistema.')
                continue
            else:
                # Create an Election object for the mayoral election.
                election = Election(election_data, position='Prefeito')
                party_counts = election.count_by_party()
                chart = create_bar_chart_party_counts(party_counts, election_years[index])
                
                # Display the bar chart with the number of mayors elected by party.
                st.plotly_chart(chart)
    
    # Display the project footer.
    dasboard_footer()
