#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: standard_elements.py
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

import streamlit as st


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

