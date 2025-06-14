# -*- coding: utf-8 -*-
"""
    CancerType.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""

# Stdlib imports
from enum import StrEnum

# Third-party app imports

# Imports from your apps


class CancerType(StrEnum):
    all = 'all'
    breast = 'breast'
    prostate = 'prostate'
    colorectal = 'colorectal'
    hodgkins = 'hodgkins_lymphoma'
    paedriatic = 'paedriatic'
