import pygame
import unittest
import math


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.red_unit = Teenie((10, 10), 1)
        self.blue_unit = Teenie((50, 50), 2)

    def test_move(self):
        self.red_unit.move((10, 20))
        self.assertTrue(self.red_unit.pos == (10, 20))

    def test_move_direction(self):
        self.red_unit.move_direction(math.sqrt(3), 1)
        x, y = self.red_unit.pos
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


class TestFlag(unittest.TestCase):
    def setUp(self):
        self.flag = Flag((300, 300), 2)

    def test_be_picked_up(self):
        self.red_unit = Teenie((10, 10), 1)
        self.flag.be_picked_up(self.red_unit)
        #self.assertTrue(self.flag.pos == self.red_unit.pos)
        self.red_unit.move((400, 400))
        #self.assertTrue(self.flag.pos == self.red_unit.pos)


class Unit(object):  # TODO Make uninstantiable

    def __init__(self, position, team, stats):
        """ DOCSTRING:
            Given pos, team, & stat list, provides init template for more specific
            units such as Teenie, Speedie, & Heavie.
            """
        self.pos = x, y = position
        self.goal_pos = [None,None]
        self.team = team
        self.is_selected = False

        # Sets stats
        self.strength = stats[0]
        self.speed = stats[1]
        self.health = stats[2]
        self.attack_ = stats[3]
        self.cooldown = stats[4]
        self.size = stats[5]
        self.radius = float(stats[5][1]/2)
        self.cooled = 0       # tick at which unit's attack is enabled again

        # Sets sprite(s)
        self.range_sprite = pygame.image.load("sprites/unitradius.png")
        if team == 1:
            self.sprite = pygame.image.load("sprites/redunit1.png")
        elif team == 2:
            self.sprite = pygame.image.load("sprites/blueunit1.png")
        self.old_sprite = self.sprite # Stores unit sprite when using selected unit sprite

    def update(self):
        """ DOCSTRING:
            updates unit attributes/methods that take more than one tick to run
            """

        # Sets rect pos to unit pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        # If there is goal and unit isn't there, move towards goal
        if self.goal_pos != [None,None] and self.pos != self.goal_pos:
            self.move_direction(self.goal_pos[0] - self.pos[0], self.goal_pos[1]-self.pos[1])

            # If unit arrived at goal, turn off goal
            if abs(math.sqrt((self.pos[0]-self.goal_pos[0])**2 + (self.pos[1]-self.goal_pos[1])**2)) < self.speed:
                self.goal_pos = [None,None]

    def select(self):
        """DOCSTRING:
            flips selection state of unit and changes sprite
            """
        if self.is_selected is False:
            self.is_selected = True
            self.sprite = pygame.transform.scale(pygame.image.load("sprites/unit_3.png"), self.size)
        else:
            self.is_selected = False
            self.sprite = self.old_sprite

    def move(self, pos):
        """moves unit to pos = x, y"""
        self.pos = pos

    def move_direction(self, x_d, y_d):
        """moves unit at self.speed in direction = x, y"""
        x, y = self.pos
        mag = math.sqrt(x_d**2 + y_d**2)
        x = x + (x_d*self.speed)/mag
        y = y + (y_d*self.speed)/mag
        self.pos = x, y

    def attack(self, unit, tick):
        if tick > self.cooled:
            unit.health = unit.health - self.attack_
            self.cooled = tick + self.cooldown
            print(unit.health)


class Teenie(Unit):
    """ The base unit in the game"""
    def __init__(self, position, team):
        Unit.__init__(self, position, team, [4, 4, 10, 2, 50, [20,20]])
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

class Speedie(Unit):
    """ The fast unit in the game"""
    def __init__(self, position, team):
        Unit.__init__(self, position, team, [4, 6, 10, 2, 50, [30,30]])
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

class Heavie(Unit):
    """The strong unit in the game"""
    def __init__(self, position, team):
        Unit.__init__(self, position, team, [8, 2, 14, 4, 75, [40,40]])
        self.sprite = pygame.transform.scale(self.sprite, self.size)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


class Flag(object):
    """ DOCSTRING:
        Contains attributes and methods for Flag obj of Capture the Flag
        """
    def __init__(self, position, team):
        # TODO: Initialize attributes like position, color
        # should define the position based off of mouse position
        self.pos = x, y = position
        # One basic color for each side of team
        self.team = team
        self.sprite = pygame.image.load("sprites/team"+str(team)+"flag.png")
        self.oldsprite = self.sprite
        self.is_selected = False
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 60)
        self.pickedup = False  # Bool for flag picked up
        # has to be removeable
        self.unit = None     # remembers which unit is carying the flag

    def select(self):
        if self.is_selected is False:
            self.is_selected = True
            self.sprite = pygame.image.load("sprites/yellowflag.png")
        else:
            self.is_selected = False
            self.sprite = self.oldsprite

    def move(self, mouse_pos):
        self.pos = (mouse_pos[0], mouse_pos[1])
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 60)

    def be_picked_up(self, unit):
        if self.pickedup is False:
            self.pickedup = True
            self.unit = unit
            self.pos = (unit.pos[0] + 10, unit.pos[1] - 50)
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 40, 60)
        else:
            self.pickedup = False

    # TODO more methods here!


class Base(object):
    """ DOCSTRING:
        Contains attributes and methods for Base object in Capture the Flag
        (spawns units, need to get flag to base to win)
        """
    def __init__(self, position, team):
        self.pos = x, y = position  # pixel position
        self.cycle_count = 0  # initial cycle count
        self.size = [50, 50]
        self.team = team

        self.sprite = pygame.image.load("sprites/base_"+str(team)+".png")
        # Add counter for unit generation
        self.width = 20
        self.height = 20
        self.unit_cycles = [30, 50, 80]  # number of cycles for a unit to generate (10 - teenie, 20 - speedie)
        self.current_unit_cycle = 30
        self.unit_type = 0
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 100, 100)

    def update(self, tick):
        self.cycle_count += 1
        self.current_unit_cycle = self.unit_cycles[self.unit_type]
        if self.cycle_count == self.current_unit_cycle:
            new_unit = self.unit_generation()

            self.cycle_count = 0
            return(new_unit)
        else:
            return(False)

    def update_unit(self, key):
        """DOCSTRING
            given pressed key, changes currently spawning unit type based on
            which key is pressed"""
        print(key)
        if key == '1' or key =='q':
            self.unit_type = 0
            print("MSG: Unit type changed to Teenie on base " + str(self.team))
        elif key == '2' or key == 'w':
            self.unit_type = 1
            print("MSG: Unit type changed to Speedie on base " + str(self.team))
        elif key == '3' or key == 'e':
            self.unit_type = 2
            print("MSG: Unit type changed to Heavie on base " + str(self.team))

    #TODO has to do with animations
    def unit_generation(self):
        """DOCSTRING
            Checks unit type to spawn, creates new unit of current type
            close to self, then passes message if verbose is true (TODO)"""
        if self.unit_type == 0:
            new_unit = Teenie((self.pos[0]+300, self.pos[1]+300), self.team)
            #print("MSG: New Teenie Unit on base " + str(self.team))
        elif self.unit_type == 1:
            new_unit = Speedie((self.pos[0]+200, self.pos[1]+200), self.team)
            #print("MSG: New Speedie Unit on base " + str(self.team))
        else:
            new_unit = Heavie((self.pos[0]+200, self.pos[1]+200), self.team)
            #print("MSG: New Heavie Unit on base " + str(self.team))
        return(new_unit)


    # TODO more methods here!

if __name__ == "__main__":
    unittest.main()
