""" DOCSTRING
If-tree based Artificial Intelligence designed to play capture the flag

@author Connor Novak
         """
import pygame
import unittest
import math
import objects as obj
import mvc
from objects import TestUnit

class AIRule(object):
    """ DOCSTRING:
        Class defining AI to play game based on rules of game and if-tree
        """

    def __init__(self,weights):
        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = 1
        self.other_team = 2
        self.weights = weights

    def update(self, units, flags):
        """ DOCSTRING:
            Updates info that AI knows of game
            """
        self.all_units = units
        self.units = [unit if unit.team == self.team for unit in self.all_units]
        self.other_units = [unit if unit.team == self.other_team for unit in self.all_units]
        self.flag = [flag if flag.team == self.team for flag in self.flags]
        self.other_flag = [flag if flag.team == self.other_team for flag in self.flags]

    def unit_command(self):
        """ DOCSTRING:
            Given list of units on team, returns direction for movement of each
            units
            """

        for unit in self.units:
            unit.move_direction(flag.position[0] - unit.position[0],flag.position[1] - unit.position[1])
