import pygame
import unittest
import math


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.red_unit = Teenie((10, 10), 1)
        self.blue_unit = Teenie((50, 50), 2)

    def test_move(self):
        self.red_unit.move((10, 20))
        self.assertTrue(self.red_unit.position == (10, 20))

    def test_move_direction(self):
        self.red_unit.move_direction(math.sqrt(3), 1)
        x, y = self.red_unit.position
        self.assertTrue(x == 10 + 3*math.sqrt(3))
        self.assertTrue(y == 10 + 3)

    def test_attack(self):
        health = self.blue_unit.health
        self.red_unit.attack(self.blue_unit, 40)
        self.assertTrue(self.blue_unit.health ==
                        health - self.red_unit.attack_/4)
        health = self.blue_unit.health
        self.red_unit.attack(self.blue_unit, 41)
        self.assertTrue(self.blue_unit.health == health)

    def test_pick_up_flag(self):
        flag = Flag((300, 300), 2)
        self.red_unit.pick_up_flag(flag)
        self.assertTrue(flag.position == self.red_unit.position)
        self.red_unit.move(400, 400)
        self.assertTrue(flag.position == self.red_unit.position)


class Unit(object):  # TODO Make uninstantiable
    def __init__(self, position, team, stats):  # TODO set to position of the base
        """
        DOCSTRING:
        attributes:
        TEAM: 1 or 2
        """
        self.position = x, y = position
        self.team = team
        self.is_selected = False
        self.strength = stats[0]
        self.speed = stats[1]
        self.health = stats[2]
        self.attack_ = stats[3]
        self.cooldown = stats[4]
        self.rect = pygame.Rect(self.position[0], self.position[1], 50, 50)
        # TODO: make sure this picture is here
        # self.range_sprite = pygame.image.load("sprites/unitradius.png")
        if team == 1:
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/redunit1.png"), 10, 10)
        elif team == 2:
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/blueunit1.png"), 10, 10)
        else:
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/unitradius.png"), 10, 10)

    def move(self, pos):
        """moves unit to pos = x, y"""
        self.position = pos

    def move_direction(self, x_d, y_d):
        """moves unit at self.speed in direction = x, y"""
        x, y = self.position
        mag = math.sqrt(x_d**2 + y_d**2)
        x = x + (x_d*self.speed)/mag
        y = y + (y_d*self.speed)/mag
        self.position = x, y

    def attack(self, unit, tick):
        if (tick % self.cooldown) == 0:
            unit.health = unit.health - self.attack_/4

    def pick_up_flag(self, flag):
        pass


class Teenie(Unit):
    """ The base unit in the game"""

    def __init__(self, position, team):
        Unit.__init__(self, position, team, [5, 6, 10, 2, 2])


class Speedie(Unit):
    """ The fast unit in the game"""
    def __init__(self, x, y, team):
        Unit.__init__(self, x, y, team, [])


class Heavie(Unit):
    """The strong unit in the game"""


class Flag(object):
    """ The flag class for the game"""
    def __init__(self, position, team):
        # TODO: Initialize attributes like position, color
        # should define the position based off of mouse position
        self.position = x, y = position
        # One basic color for each side of team
        self.team = team
        self.sprite = pygame.image.load("sprites/team"+str(team)+"flag.png")
        self.oldsprite = self.sprite
        self.is_selected = False
        self.rect = pygame.Rect(self.position[0], self.position[1], 40, 60)
        self.pickedup = False  # Bool for flag picked up
        # has to be removeable

    def select(self):
        if self.is_selected is False:
            self.is_selected = True
            self.sprite = pygame.image.load("sprites/yellowflag.png")
        else:
            self.is_selected = False
            self.sprite = self.oldsprite

    def move(self, mouse_pos):
        self.position = (mouse_pos[0], mouse_pos[1])
        self.rect = pygame.Rect(self.position[0], self.position[1], 40, 60)

    def update(self):
        # TODO updates flag position to unit carrying position, or home position
        # if not carried
        pass

    # TODO more methods here!


class Base(object):
    """ The base class for the game"""

    def __init__(self, position, team):
        # TODO: Initialize attributes like position, type of unit selected

        self.position = x, y = position#pixel position
        self.cycle_count = 0 #initial cycle count
        self.size = [50,50]
        self.team = team


        self.sprite = pygame.image.load("sprites/base_"+str(team)+".png")
        # Add counter for unit generation
        # Add method that increments the counter and makes selected unit if applicable
        self.width = 20
        self.height = 20
        self.unit_cycles = [30, 50] #number of cycles for a unit to generate (10 - teenie, 20 - speedie)
        self.current_unit_cycle = 30
        self.unit_type = 0

    def update(self, tick, unit_type):
        self.cycle_count +=1
        self.unit_type = unit_type
        self.current_unit_cycle = self.unit_cycles[self.unit_type]
        if self.cycle_count == self.current_unit_cycle:
            new_unit = self.unit_generation(self.unit_type)
            self.cycle_count = 0
            return(new_unit)
        else:
            return(False)

    #TODO has to do with animations
    def unit_generation(self, unit_type):
        new_unit = Teenie((self.position[0]+70, self.position[1]+20), self.team)
        return(new_unit)


    # TODO more methods here!

if __name__ == "__main__":
    unittest.main()
