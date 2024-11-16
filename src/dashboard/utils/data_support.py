#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: data_support.py
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

import geopandas as gpd
import pandas as pd
import streamlit as st


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


@st.cache_data
def load_election_data(file_path: str) -> pd.DataFrame:
    """Load the election data from a parquet file.

    Arguments:
        - file_path: Path to the parquet file.

    Returns:
        - DataFrame with the election data.
    """

    return pd.read_parquet(file_path)


@st.cache
def load_shapefile_data(shapefile_path: str) -> pd.DataFrame:
    """Load shapefile data.

    Parameters:
        - shapefile_path: Path to the shapefile.

    Returns:
        - DataFrame with the shapefile data.
    """

    return gpd.read_file(shapefile_path)
