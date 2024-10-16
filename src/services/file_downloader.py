#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: file_downloader.py
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
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

import requests

from src.interfaces.downloader import FileDownloaderInterface


class FileDownloader(FileDownloaderInterface):

    def download_file(self, url: str, path: str):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            with open(path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        except requests.exceptions.HTTPError as http_error:
            print(f'HTTP Error: {http_error}')
        except requests.exceptions.RequestException as request_exception:
            print(f'Request Exception: {request_exception}')
        except IOError as io_error:
            print(f'Input/Output Error: {io_error}')
        except Exception as error:  # pylint: disable=broad-except
            print(f'Unexpected error: {error}')
            raise error
