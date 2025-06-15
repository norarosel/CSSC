# -*- coding: utf-8 -*-
"""
    TargetGroup.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports
from enum import StrEnum

# Third-party app imports

# Imports from your apps


class TargetGroup(StrEnum):
    adult = 'adult'
    child = 'child'
    man = 'man'
    woman = 'woman'
