""" DOCSTRING
If-tree based Artificial Intelligence designed to play capture the flag

@author Connor Novak
         """
import pygame
import numpy as np
import unittest
import math
import objects as obj
import mvc

class AIRule(object):
    """ DOCSTRING:
        Class defining AI to play game based on rules of game and if-tree
        """

    def __init__(self,team,weights=[1,1,1,1,1]):
        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = team
        self.weights = weights

    def update(self, units, flags, bases):
        """ DOCSTRING:
            Updates info that AI knows of game; pos of units, base, flag
            """
        self.all_units = units
        self.units = [unit for unit in self.all_units if unit.team == self.team]
        self.other_units = [unit for unit in self.all_units if unit.team != self.team]

        self.flag = [flag for flag in flags if flag.team != self.team]
        self.flag = self.flag[0]
        self.other_flag = [flag for flag in flags if flag.team == self.team]
        self.other_flag = self.other_flag[0]

        self.base = [base for base in bases if base.team == self.team]
        self.base = self.base[0]
        self.other_base = [base for base in bases if base.team != self.team]
        self.other_base = self.other_base[0]

    def unit_command(self):
        """ DOCSTRING:
            Given list of units on team, returns direction for movement of each
            units
            """

        for unit in self.units: # Orders for all units

            # Weights based on enemy flag position
            if (self.flag.pickedup == True): # If flag is obtained
                if unit == self.flag.unit: # Flag unit returns to base
                    dir_1 = self.get_direction(self.base.pos,unit.pos,True)
                else: # Other units follow flag unit
                    dir_1 = self.get_direction(self.flag.unit.pos,unit.pos,True)
            else: # All units go for flag
                dir_1 = self.get_direction(self.flag.pos,unit.pos,True)

            # Weights based on team flag position
            dir_2 = self.get_direction([0,0],[0,0]) # Default no force
            for other_unit in self.other_units: # Check enemy unit pos rel to flag
                distance = np.linalg.norm(self.get_direction(other_unit.pos,self.other_flag.pos))
                if distance < 500: # If an enemy unit is close
                    if self.other_flag.unit != None: # If flag not taken, guard flag
                        dir_2 = self.get_direction(self.other_flag.unit.pos,unit.pos,True)
                    else: # If flag taken, chase unit
                        dir_2 = self.get_direction(self.other_flag.pos,unit.pos,True)
                    break

            # Adds and weights all vectors; calculates movement vector
            direction = self.weights[0] * dir_1 + self.weights[1] * dir_2

            # Moves unit
            unit.move_direction(direction[0],direction[1])

    def get_direction(self,pt1,pt2,norm=False):
        """ DOCSTRING:
            Given two points, returns normalized vector from pt1 towards pt2
            """

        direction = np.array([pt1[0]-pt2[0],pt1[1]-pt2[1]]) # Build vector
        norm_dir = np.linalg.norm(direction)
        if norm and norm_dir != 0: direction = direction/np.linalg.norm(direction) # normalize
        return direction
