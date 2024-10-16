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

from os import path

import requests

from src.interfaces.file_handler import FileDownloaderInterface


class FileDownloader(FileDownloaderInterface):

    def download_file(self, url: str, file_path: str):
        """Download a file from a URL and save it to a local file path."""

        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            if path.exists(file_path):
                file_size_local = path.getsize(file_path)
                file_size_remote = int(response.headers.get('content-length', 0))

                if file_size_remote == file_size_local:
                    print(f'{file_path} already exists and has the same size as the remote file.')
                    return

            with open(file_path, 'wb') as file:
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
