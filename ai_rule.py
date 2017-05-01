""" DOCSTRING
If-tree based Artificial Intelligence designed to play capture the flag

@author Connor Novak
         """
import random
import numpy as np
import unittest
import math
import objects as obj
import mvc
from deap import algorithms, base, tools, creator


class FitnessMaxSingle(base.Fitness):
    """
    Class representing the fitness of a given individual, with a single
    objective that we want to minimize (weight = -1)
    """
    weights = (1.0, )

class AIRule(object):
    """ DOCSTRING:
        Class defining AI to play game based on rules of game and if-tree
        """

    def __init__(self,team=1,weights=[]):

        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = team
        if weights == []:
            self.weights = []
            for i in range(5):
                random_weight = random.randint(0, 100)
                random_weight = float(random_weight/100)
                self.weights.append(random_weight)
        else:
            self.weights = weights

        self.fitness = FitnessMaxSingle()
        self.state_evaluation = (0,)
        self.all_units = []
        self.all_other_units = []
        self.loss = 0
        self.other_loss = 0
        self.previous_units = []
        self.other_previous_units = []
        self.tick = 0


    def update(self, units, flags, bases, tick):
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
        self.tick = tick

        self.evaluate_during_game()

    def end_game(self):
        self.all_units = None
        self.units = None
        self.other_units = None
        self.flag = None
        self.other_flag = None
        self.base = None
        self.other_base = None
        self.previous_units = []
        self.other_previous_units = []

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
            dir_2 = self.get_direction([0,0],[0,0])
            for other_unit in self.other_units:
                distance = np.linalg.norm(self.get_direction(other_unit.pos,self.other_flag.pos))
                if distance < 300:
                    if self.other_flag.unit != None:
                        dir_2 = self.get_direction(self.other_flag.unit.pos,unit.pos,True)
                    else:
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
        mag = np.linalg.norm(direction)
        if norm and mag > 0: direction = direction/mag # normalize
        return direction

    def evaluate_during_game(self):
        if len(self.previous_units) > len(self.units):
            self.loss += len(self.previous_units) - len(self.units)
        elif len(self.other_previous_units) > len(self.other_units):
            self.other_loss += len(self.other_previous_units) - len(self.other_units)

        self.previous_units = self.units
        self.other_previous_units = self.other_units

    def evaluate_state(self, winning=False):
        lst = list(self.state_evaluation)

        #final_total_own = len(self.units)
        #final_total_rival = len(self.other_units)
        won = 0
        if winning==True:
            won = 5000

        '''
        #lst[0] = won*50-self.loss*5+self.other_loss*5
        if self.other_loss == 0:
            self.other_loss = 1
        lst[0] = float(won*50-float(self.loss/self.other_loss)*10)
        self.state_evaluation = tuple(lst)
        '''
        lst[0] = won-self.tick
        self.state_evaluation = tuple(lst)
        return(self.state_evaluation)

    def final_state(self, ai_state):
        self.state_evaluation = ai_state
        #print(self.state_evaluation, self.tick)
        return(self.state_evaluation)



'''
for unit in self.unit:
                if (unit not in self.all_units) and (unit not in self.all_other_units):
                    if unit.team == self.team:
                        self.all_units.append(unit)
                    else:
                        self.all_other_units(unit)
'''
