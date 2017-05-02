""" DOCSTRING:
    If-tree based Artificial Intelligence designed to play capture the flag

    @author Connor Novak, Colvin Chapman
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


    def __init__(self, team, weights=[.5, 0.8, .5, .5, .5, .5, 0.8, .5, .5, .5,
                                      .5, 0.8, .5, .5, .5, .5, 0.8, .5, .5, .5,
                                      .5, 0.8, .5, .5]):  # 24 weights

        """ DOCSTRING:
            Initializes AI w/ weights (default weights implicit)
            """
        self.team = team
        self.attack_weights = [weights[0:3], weights[3:6], weights[6:9]]
        self.defend_weights = [weights[9:12], weights[12:15], weights[15:18]]
        self.flag_weights = weights[18:20]
        self.attack_ratio = weights[20]
        produce_ratio = weights[21:24]
        s = sum(produce_ratio)
        self.input_ratio = [produce_ratio[0]/s, produce_ratio[1]/s,
                            produce_ratio[2]/s]  # teeny, big, speedy
        self.desired_ratio = []
        self.convert = 10
        for unit_type in self.input_ratio:
            self.desired_ratio.append(unit_type/sum(self.input_ratio))
        self.desired_ratio = np.array(self.desired_ratio)

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
        if n == 0:
            self.ratio = np.array([0, 0, 0])
        else:
            self.ratio = np.array([len(teenies)/n, len(speedies)/n, len(heavies)/n])

    def base_command(self):
        """ DOCSTRING:
            Returns unit type for base to generate
            """
        ratio_diff = self.desired_ratio - self.ratio
        unit_index = np.argmax(ratio_diff)
        if unit_index == 0:
            if self.team == 1: return '1'
            else: return 'q'
        elif unit_index == 1:
            if self.team == 1: return '2'
            else: return 'w'
        else:
            if self.team == 1: return '3'
            else: return 'e'

    def unit_command(self, control):
        """ DOCSTRING:
            Returns direction for movement of each unit on team
            """
        for unit in self.units:  # Orders for all units
            all_force = []
            f1 = []
            f2 = []
            if unit.mission == None:
                unit.mission = self.get_mission(self.attack_ratio, self.units)
                print('Gave unit mission: ' + unit.mission)
            if unit.mission == 'attack': # If unit is attacking
                if self.flag.pickedup == True: # If enemy flag is obtained
                    if unit == self.flag.unit: # Flag unit returns to base
                        f1 = self.get_direction(self.base.pos, unit.pos, "Normal")
                    else: # Other units follow flag unit
                        f1 = (self.get_direction(self.flag.unit.pos,
                                unit.pos, "Normal") + .5*self.flag.unit.direction)  # leading unit
                else:  # normal find flag
                    flag_weight = self.flag_weights[0] # charging weight
                    f1 = self.get_direction(self.flag.pos, unit.pos,"Normal")*flag_weight
                    force_list = []
                    for other_unit in self.other_units:
                        other_unit_dir = self.get_direction(other_unit.pos, unit.pos,"Inverse")  # straight line between units
                        predict_dir = other_unit_dir + other_unit.direction     # leading the units
                        unit_weight = self.get_weight(unit, other_unit)
                        unit_force = predict_dir * unit_weight
                        force_list.append(unit_force)
                    f2 = sum(force_list)
                    all_force.append(f2)
                all_force.append(f1)
                # f2 = np.array([0, 0])

            elif unit.mission == 'defend':  # If unit is defending
                if self.other_flag.pickedup:
                    f1 = self.get_direction(self.other_flag.unit.pos, unit.pos, "Normal")
                else:  # normal find flag
                    flag_weight = self.flag_weights[1]  # puppy guarding weight
                    f1 = self.get_direction(self.other_flag.pos, unit.pos,"Normal")*flag_weight
                    force_list = []
                    for other_unit in self.other_units:
                        other_unit_dir = self.get_direction(other_unit.pos, unit.pos,"Inverse")  # straight line between units
                        predict_dir = other_unit_dir + other_unit.direction     # leading the units
                        unit_weight = self.get_weight(unit, other_unit)
                        unit_force = predict_dir * unit_weight
                        force_list.append(unit_force)
                    f2 = sum(force_list)
                    print(f2)
                    all_force.append(f2)
                all_force.append(f1)

            elif unit.mission == 'return':  # If unit is returning
                f1 = self.get_direction(self.base.pos,unit.pos,"Normal") # f1 towards base
                for enemy in self.other_units:
                    f2 += self.convert/self.get_distance(self.enemy.pos,unit.pos) * self.get_direction(self.enemy.pos,unit.pos,False)

            # Adds all force vectors; calculates movement vector
            direction = sum(all_force)

            # Moves unit if it's not the debugging unit
            if unit != control.driven_unit:
                unit.move_direction(direction[0], direction[1])
                unit.direction = direction

    def get_mission(self, weight, units):
        """ DOCSTRING:
            Given weight representing ratio of missions & list of units, returns
            mission for new unit
            """
        ratio = abs(weight)
        att_units = len([unit for unit in units if unit.mission == 'attack'])
        def_units = len([unit for unit in units if unit.mission == 'defend'])
        if def_units == 0: curr_ratio = 1
        else: curr_ratio = att_units/def_units
        if def_units == 0: new_ratio_1 = 1
        else: new_ratio_1 = (att_units+1)/def_units
        new_ratio_2 = att_units/(def_units + 1)
        if abs(ratio - new_ratio_1) < abs(ratio - new_ratio_2): return 'attack'
        else: return 'defend'

    def get_direction(self, pt1, pt2, norm="Regular"):
        """ DOCSTRING:
            Given two points, returns normalized vector from pt1 towards pt2
            """
        direction = np.array([pt1[0]-pt2[0],pt1[1]-pt2[1]]) # Build vector
        mag = np.linalg.norm(direction)

        if norm == "Normal" and mag > 0: direction = direction/mag # normalize
        if norm == "Inverse" and mag > 0: direction = direction/mag/mag # invert
        return direction

    def get_weight(self, unit, other_unit):
        """ DOCSTRING:
            Given a unit opposing unit and mission, returns the correct weight to
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
        if unit.mission == 'attack':
            return self.attack_weights[j][i]
        elif unit.mission == 'defend':
            return self.defend_weights[j][i]

    def get_distance(self, pt1, pt2):
        """ DOCSTRING:
            Given two points, returns distance btw pts
            """

        direction = np.array([pt1[0]-pt2[0], pt1[1]-pt2[1]])  # Build vector
        return np.linalg.norm(direction)
