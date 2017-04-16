""" DOCSTRING
If-tree based Artificial Intelligence designed to play capture the flag

@author Connor Novak
         """
import pygame
import unittest
import math
import objects as obj
import mvc

class AIRule(object):
    """ DOCSTRING:
        Class defining AI to play game based on rules of game and if-tree
        """

    def __init__(self,weights):
        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = 1
        self.weights = weights

    def update(self, units, flags):
        """ DOCSTRING:
            Updates info that AI knows of game
            """
        self.all_units = units
        self.units = [unit for unit in self.all_units if unit.team == self.team]
        self.other_units = [unit for unit in self.all_units if unit.team != self.team]
        self.flag = [flag for flag in flags if flag.team == self.team]
        self.flag = self.flag[0]
        self.other_flag = [flag for flag in flags if flag.team != self.team]
        self.other_flag = self.other_flag[0]

    def unit_command(self):
        """ DOCSTRING:
            Given list of units on team, returns direction for movement of each
            units
            """

        for unit in self.units:
            unit.move_direction(self.flag.pos[0] - unit.pos[0],self.flag.pos[1] - unit.pos[1])
