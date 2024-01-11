#!/usr/bin/env python3
"""function of task11"""
from typing import Any, Mapping, Union, TypeVar


T = TypeVar('T')
R = Union[Any, T]


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> R:
    '''extract a value from a dictionnary'''
    if key in dct:
        return dct[key]
    else:
        return default
