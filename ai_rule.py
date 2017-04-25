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

    def __init__(self,team,weights=[1,0.8,1,1,1]):
        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = team
        self.weights = weights
        self.input_ratio = [4, 2, 2]  # teeny, big, speedy
        self.desired_ratio = []
        for unit_type in self.input_ratio:
            self.desired.ratio.append(unit_type/sum(self.input_ratio))

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

        teenies = [unit for unit in self.units if unit.species == 'teenie']
        speedies = [unit for unit in self.units if unit.species == 'speedie']
        heavies = [unit for unit in self.units if unit.species == 'heavie']
        n = len(self.units)
        self.ratio = [len(teenies)/n, len(speedies)/n, len(heavies)/n]

    def unit_command(self):
        """ DOCSTRING:
            Given list of units on team, returns direction for movement of each
            units
            """

        for unit in self.units:  # Orders for all units

            if unit.mission == 'attack': # If unit is attacking
                if self.flag.pickedup == True: # If enemy flag is obtained
                    if unit == self.flag.unit: # Flag unit returns to base
                        dir_1 = self.get_direction(self.base.pos,unit.pos,True)
                    else: # Other units follow flag unit
                        dir_1 = self.get_direction(self.flag.unit.pos,unit.pos,True)
            elif unit.mission == 'defend':  # If unit is defending
                dir_destination = self.get_direction(self.flag, unit.pos, True)
                force_list = []
                for other_unit in self.other_units:
                    other_unit_dir = get_direction(other_unit.pos, unit.pos)  # straight line between units
                    predict_dir = other_unit_dir + other_unit.direction     # leading the units
                    force_hat = np.linalg.norm(predict_dir)
                    unit_weight =
            elif unit.mission == 'return':  # If unit is returning
                f1 = self.get_direction(self.base.pos,unit.pos,True) # f1 towards base
                for enemy in self.other_units:
                    f2 += self.get_direction(self.enemy.pos,unit.pos,False)



            # Weights based on enemy flag position
            if (self.flag.pickedup == True): # If flag is obtained
                if unit == self.flag.unit: # Flag unit returns to base
                    dir_1 = self.get_direction(self.base.pos,unit.pos,True)
                else: # Other units follow flag unit
                    dir_1 = self.get_direction(self.flag.unit.pos,unit.pos,True)
            else: # All units go for flag
                dir_1 = self.get_direction(self.flag.pos,unit.pos,True)

            # Weights based on team flag position
            dir_2 = self.get_direction([0,0],[0,0])
            for other_unit in self.other_units:
                distance = np.linalg.norm(self.get_direction(other_unit.pos,self.other_flag.pos))
                if distance < 300:
                    if self.other_flag.unit != None:
                        dir_2 = self.get_direction(self.other_flag.unit.pos,unit.pos,True)
                    else:
                        dir_2 = self.get_direction(self.other_flag.pos,unit.pos,True)

                    break


            # Adds all force vectors; calculates movement vector
            direction = f1 + f2 + f3 + f4

            # Moves unit
            unit.move_direction(direction[0], direction[1])

                unit.directioin = direction


    def get_direction(self,pt1,pt2,norm=False):
        """ DOCSTRING:
            Given two points, returns normalized vector from pt1 towards pt2
            """

        direction = np.array([pt1[0]-pt2[0],pt1[1]-pt2[1]]) # Build vector
        mag = np.linalg.norm(direction)
        if norm and mag > 0: direction = direction/mag # normalize
        return direction

    def get_weight(unit, other_unit, mission):
        """ DOCSTRING:
            Given a unit opposing unit and mission, returns the coreect weight to
            give the unit force.
            """
        i = None    # our unit type index
        j = None    # other unit index
        if unit.species == 'teenie':
            i = 0
        elif unit.species == 'speedie':
            i = 1
        elif unit.species == 'heavie':
            i = 2

        if other_unit.species == 'teenie':
            j = 0
        elif other_unit.species == 'speedie':
            j = 1
        elif other_unit.species == 'heavie':
            j = 2

        if mission == 'attack':
            return Weights[1][j][i]
        elif mission == 'defend':
            return Weights[2][j][i]

    def get_distance(self,pt1,pt2):
        """ DOCSTRING:
            Given two points, returns distance btw pts
            """

        direction = np.array([])
