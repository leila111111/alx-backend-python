#!/usr/bin/env python3
"""function of task8"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''takes a float multiplier as argument and returns a function
    that multiplies a float by multiplier'''
    return lambda a: a * multiplier
