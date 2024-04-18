"""Enum definition for different options that are possible with COMP 227"""

from enum import Enum

__authors__ = ["Ben Goulet, Abdulaziz Al-Shayef"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class Comp227(Enum):
    COMPENSATION = 0
    CREDIT = 1
    BOTH = 2
