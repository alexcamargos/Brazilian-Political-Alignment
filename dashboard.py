#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: dashboard.py
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

from src.dashboard.app import main_page
from src.dashboard.pages.maps import comparison_political_alignment_page

if __name__ == '__main__':
    # Create paginated navigation bar.
    pages = st.navigation(
        [
            st.Page(main_page,
                    title='Página Inicial',
                    icon=':material/home:',),
            st.Page(comparison_political_alignment_page,
                    title='Comparação de Alinhamento Político',
                    icon=':material/map:'),
        ]
    )

    # Run the application.
    pages.run()
