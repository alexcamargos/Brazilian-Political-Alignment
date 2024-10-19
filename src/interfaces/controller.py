#!/usr/bin/env python
# encoding: utf-8

# ------------------------------------------------------------------------------
#  Name: controller.py
#  Version: 0.0.1
#
#  Summary: Project Name
#           Quick description of the project.
#
#  Author: Alexsander Lopes Camargos
#  Author-email: alcamargos@vivaldi.net
#
#  License: MIT
# ------------------------------------------------------------------------------
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring

from abc import ABC, abstractmethod


class CommandInterface(ABC):

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError('Method "execute" must be implemented.')
