#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: maps.py
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
import streamlit as st
import matplotlib.pyplot as plt
from plotly import express as px
from plotly import graph_objects as go

from src.dashboard.models.elections import Election
from src.dashboard.utils.data_support import (list_all_elections_files,
                                              load_election_data,
                                              load_shapefile_data)
from src.dashboard.utils.standard_elements import (dasboard_footer,
                                                   dashboard_banner,
                                                   setup_dashboard_configuration)


@st.cache_resource
def create_political_alignment_map(_political_geospatial_data:pd.DataFrame,
                                   year: str) -> plt.Figure:
    """Create a map with the political alignment of the mayors elected in the election year.
    
    Arguments:
        - election_data: DataFrame with the election data.
        - year: Year of the election.
        
    Returns:
        - Map with the political alignment of the mayors elected in the election year.
    """

    fig, ax = plt.subplots(figsize=(18, 8))
    _political_geospatial_data.plot(column='Espectro',
                                    ax=ax,
                                    legend=True,
                                    cmap='coolwarm',
                                    aspect=1)

    ax.set_title(f'Alinhamento Político dos Prefeitos Eleitos em {year}', fontsize=14)

    return fig


def comparison_political_alignment_page() -> None:
    """Display the cloroopleth map with the political alignment."""

    # Set the page configuration.
    setup_dashboard_configuration()

    # Display the page banner.
    dashboard_banner()

    # Display the header of the analysis.
    st.subheader('Comparação do Alinhamento Político dos Prefeitos Eleitos nas Eleições Municipais')

    # List all election data files.
    data_directory = 'data'
    parquet_data_files = list_all_elections_files(data_directory)

    # Load the election data from the parquet files.
    all_elections_data = [load_election_data(file) for file in parquet_data_files]

    # Create containers separated into tabs for each election year.
    election_years = [year.split('.')[0].split('_')[-1] for year in parquet_data_files]
    tabs = st.tabs(election_years)

    # Load the geospatial simplifed data.
    shapefile_directory = 'data/shapefiles'
    geospatial_municipal_mesh = load_shapefile_data(shapefile_directory)

    # Display the maps of the political alignment of the mayors elected in each election year.
    for index, election_data in enumerate(all_elections_data):
        with tabs[index]:
            # Check if the election data is empty.
            if election_data.empty:
                st.write('Os dados não foram carregados. Contate o administrador do sistema.')
                continue

            # Create an Election object for the mayoral election.
            election = Election(election_data, position='Prefeito')
            election_data = election.filter_data

            # Set the municipality name to uppercase.
            election_data['NM_MUNICIPIO'] = election_data['NM_UE'].str.upper()

            # Merge the geospatial data with the election data.
            geospatial_data = geospatial_municipal_mesh.merge(election_data,
                                                              left_on='NM_MUN',
                                                              right_on='NM_MUNICIPIO')

            # Display the cloroopleth map with the political alignment.
            fig = create_political_alignment_map(geospatial_data, election_years[index])
            st.pyplot(fig)

    # Display the project footer.
    dasboard_footer()
