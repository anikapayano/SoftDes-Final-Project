""" DOCSTRING
If-tree based Artificial Intelligence designed to play capture the flag

@author Connor Novak
         """
import random
import numpy as np
import unittest
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
            Initializes AI w/ weights (default random weights)
            """

        self.tick = 0
        self.team = team
        # if now weights are given, generate random weights
        if weights == []:
            self.weights = []
            for i in range(26):
                random_weight = random.randint(-100, 100)
                random_weight = float(random_weight/100)
                self.weights.append(random_weight)
        else:
            self.weights = weights

        weights = self.weights
        self.attack_weights = [weights[0:3], weights[3:6], weights[6:9]]
        self.defend_weights = [weights[9:12], weights[12:15], weights[15:18]]
        self.flag_weights = [abs(weights[18]), abs(weights[19])]
        self.attack_ratio = abs(weights[20])
        produce_ratio = weights[21:24]
        self.sensitivity_weights =[abs(weights[24]), abs(weights[25])]
        s = sum(produce_ratio)
        self.input_ratio = [produce_ratio[0]/s, produce_ratio[1]/s,
                            produce_ratio[2]/s]  # teeny, big, speedy
        self.desired_ratio = []
        self.convert = 10
        for unit_type in self.input_ratio:
            self.desired_ratio.append(unit_type/sum(self.input_ratio))
        self.desired_ratio = np.array(self.desired_ratio)
        #print(self.desired_ratio)

        # this is necessary for DEAP to run 
        self.fitness = FitnessMaxSingle()

        # fitness number
        self.state_evaluation = (0,)

        # initialize empty list of all of AI's units
        self.all_units = []
        # initialize empty list of all of AI's opponent's units
        self.all_other_units = []

        # attributes for changing the fitness function 
        # used for taking ratio of AI's unit loss to opponent's unit loss
        self.loss = 0
        self.other_loss = 0
        self.previous_units = []
        self.other_previous_units = []
        


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

        teenies = [unit for unit in self.units if unit.species == 'teenie']
        speedies = [unit for unit in self.units if unit.species == 'speedie']
        heavies = [unit for unit in self.units if unit.species == 'heavie']
        n = len(self.units)
        if n == 0:
            self.ratio = np.array([0, 0, 0])
        else:
            self.ratio = np.array([len(teenies)/n, len(speedies)/n, len(heavies)/n])

        #self.evaluate_loss_during_game()

    def end_game(self):
        """ DOCSTRING:
            DEAP pickles the AIs at the end of the game
            since it cannot pickle pygame objects, set all pygame objects
            to None
            """

        self.all_units = None
        self.units = None
        self.other_units = None
        self.flag = None
        self.other_flag = None
        self.base = None
        self.other_base = None
        self.previous_units = []
        self.other_previous_units = []

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
                #print('Gave unit mission: ' + unit.mission)
            if unit.mission == 'attack': # If unit is attacking
                if self.flag.pickedup == True: # If enemy flag is obtained
                    if unit == self.flag.unit: # Flag unit returns to base
                        f1 = self.get_direction(self.base.pos, unit.pos, "Normal")
                    else: # Other units follow flag unit
                        f1 = (self.get_direction(self.flag.unit.pos,
                                unit.pos, "Normal") + self.flag.unit.direction*self.sensitivity_weights[1]*15 )  # leading unit
                else:  # normal find flag
                    flag_weight = self.flag_weights[0] # charging weight
                    f1 = self.get_direction(self.flag.pos, unit.pos,"Normal")*flag_weight
                    force_list = []
                    for other_unit in self.other_units:
                        other_unit_dir = self.get_direction(other_unit.pos, unit.pos,"Inverse")  # straight line between units
                        predict_dir = other_unit_dir + other_unit.direction*self.sensitivity_weights[1]*15     # leading the units    # leading the units
                        unit_weight = self.get_weight(unit, other_unit)
                        unit_force = predict_dir * unit_weight
                        force_list.append(unit_force)
                    f2 = sum(force_list)
                    all_force.append(f2)
                all_force.append(f1)
                # f2 = np.array([0, 0])

            elif unit.mission == 'defend':  # If unit is defending
                if self.other_flag.pickedup:  # get flag back!
                    f1 = self.get_direction(self.other_flag.unit.pos, unit.pos, "Normal") + self.other_flag.unit.direction*self.sensitivity_weights[1]*15
                else:  # normal find flag
                    flag_weight = self.flag_weights[1]  # puppy guarding weight
                    f1 = self.get_direction(self.other_flag.pos, unit.pos,"Normal")*flag_weight
                    force_list = []
                    for other_unit in self.other_units:
                        other_unit_dir = self.get_direction(other_unit.pos, unit.pos,"Inverse")  # straight line between units
                        predict_dir = other_unit_dir + other_unit.direction*self.sensitivity_weights[1]*15     # leading the units
                        unit_weight = self.get_weight(unit, other_unit)
                        unit_force = predict_dir * unit_weight
                        force_list.append(unit_force)
                    f2 = sum(force_list)
                    all_force.append(f2)
                if self.flag.pickedup == True: # If enemy flag is obtained
                    if unit == self.flag.unit: # Flag unit returns to base
                        f1 = self.get_direction(self.base.pos, unit.pos, "Normal")
                all_force.append(f1)

            elif unit.mission == 'return':  # If unit is returning
                f1 = self.get_direction(self.base.pos,unit.pos,"Normal")# f1 towards base
                for enemy in self.other_units:
                    f2 += self.convert/self.get_distance(self.enemy.pos,unit.pos) * self.get_direction(self.enemy.pos,unit.pos,"Inverse")

            # Adds all force vectors; calculates movement vector
            direction = sum(all_force)
            direction = direction / np.linalg.norm(direction)

            # Moves unit if it's not the one being used for debugging
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
        direction = np.array([pt1[0]-pt2[0], pt1[1]-pt2[1]]) # Build vector
        location_sense = self.sensitivity_weights[0]*1000 # correct order of mag
        mag = np.linalg.norm(direction)/location_sense

        if norm == "Normal" and mag > 0: direction = direction/mag # normalize
        if norm == "Inverse" and mag > 0: direction = direction/mag/mag+.01 # invert
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

    def evaluate_loss_during_game(self):
        """ DOCSTRING:
            evaluates the losses of each team while the game runs
            """
        if len(self.previous_units) > len(self.units):
            self.loss += len(self.previous_units) - len(self.units)
        elif len(self.other_previous_units) > len(self.other_units):
            self.other_loss += len(self.other_previous_units) - len(self.other_units)

        self.previous_units = self.units
        self.other_previous_units = self.other_units

    def evaluate_state(self, winning=False):
        """ DOCSTRING:
            evaluates AI at the end of game
            """
        lst = list(self.state_evaluation)

        #final_total_own = len(self.units)
        #final_total_rival = len(self.other_units)
        won = 0
        if winning==True:
            won = 5000

        ''' ratio of losses code
        #lst[0] = won*50-self.loss*5+self.other_loss*5
        if self.other_loss == 0:
            self.other_loss = 1
        lst[0] = float(won*50-float(self.loss/self.other_loss)*10)
        self.state_evaluation = tuple(lst)
        '''
        # if it wins, add 5000 but subtract time. this prevents the ai from 
        # taking forever to win
        lst[0] = won-self.tick
        self.state_evaluation = tuple(lst)
        
        return(self.state_evaluation)

