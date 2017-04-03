"""
This is a capture the flag game made to perform evolutionary algorithms on an
AI.
@authors Colvin Chapman, Sophia Nielsen, Connor Novak,
         Emily Lepert, Anika Payano
         """
import pygame
import unittest
import math


# UNIT TESTS
class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = Model([1840, 920])

    def test_set_up(self):
        starting_units = 5
        self.model.set_up(starting_units=starting_units)
        self.assertTrue(len(self.model.unit_list), starting_units*2)
        self.assertTrue(len(self.model.flag_list), 2)
        self.assertTrue(len(self.model.base_list), 2)


class TestUnit(unittest.TestCase):
    def setUp(self):
        self.red_unit = Unit()

    def test_move(self):
        self.red_unit.move((10, 20))
        self.assertTrue(self.red_unit.position, (10, 20))

    def test_move_direction(self):
        pass

    def test_attack(self):
        pass


class CaptureGame():
    """Class that defines a game of capture the flag.
       Creates instancese of other important classes,
       Uses Model View Controller Architecture"""
    def __init__(self):
        pygame.init()                   # initialize pygame
        self.screen_size = [1840, 920]  # size of screen
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen_sprite = pygame
        # Add background sprite

        # Initialize MVC classes
        self.model = Model(self.screen_size)
        self.view = View(self.model)
        self.control = Controller(self.model)

        self.running = True

    def run(self):

        # Eventually add pre-game setup stuff somewhere here

        while self.running:
            """runs the game loop"""
            # TODO Check wincase (Controller)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # quits
                    self.running = False
            # User Input May Eventually go here
            # AI Input WILL Go here


class Model(object):
    """DOCSTRING:
        Provides model of the current game state that is changed by the
        Controller and shown by the Viewer; holds lists of all entities on the
        field"""

    def __init__(self, screen_size):
        '''DOCSTRING:
            Initializes Model for initial game stages
            '''
        # Lists of objects
        self.unit_list = []
        self.wall_list = []
        self.flag_list = []
        self.base_list = []
        self.screen_size = screen_size  # Need this to place obj rel. to screen

    def set_up(self, starting_units):
        # Add units
        for i in range(starting_units):
            self.unit_list.append(Teenie(10, 20 + i*10, 'team1'))
            self.unit_list.append(Teenie(self.screen_size[0]-10,
                                  self.screen_size[1]-(20 + i*10), 'team2'))
        # Sets up initial team positions
        self.base_list.append(Base(10, 10), 'team1')
        self.base_list.append(Base(self.screen_size[0]-10,
                              self.screen_size[1]-10), 'team2')
        # TODO: set up flag positions


class View(object):
    """Makes the draw methods for all of the classes with"""

    def __init__(self, model):
        """DOCSTRING
            Initializes View object to allow references to model"""
        self.model = model

    # Draw single object function (This is written wrong, I think)
    def draw(self, object):
        surface.blit(self.model.icon, (self.model.x, self.model.y))

    # Draw entire model function


class Controller(object):
    """DOCSTRING
        Holds functions for manipulating the model
        """

    def __init__(self, model):
        """DOCSTRING
            Initializes Controller object to allow manipulation of Model
            """

        self.model = model

    def generate_new_unit(time, unit_type):
        #for each team, if time = 5s
            #new_unit = Unit(x,y,team) => x, y would be set for each team
            #new_unit.draw(x,y)
            #team_base.unit_generation()
        pass

    def update():
        # Tells base class to update their personal timecounters
        pass


class Unit():
    # TODO Make uninstantiable

    def __init__(self, x, y, team, stats):  # TODO set to position of the base
        """
        DOCSTRING:
        attributes:
        TEAM: 'team1' or 'team2'
        """
        self.position = x, y
        self.team = team
        self.is_selected = False
        self.strength = stats[0]
        self.speed = stats[1]
        self.health = stats[2]
        self.attack = stats[3]
        self.cooldown = stats[4]
        self.range_sprite = "sprite/unitradius.png"
        if team == 'team1':
            self.sprite = "sprites/redunit.png"
        elif team == 'team2':
            self.sprite = "sprites/blueuuit.png"
        else:
            self.sprite = "sprite/unitradius.png"

    def move(self, pos):
        """moves unit to pos = x, y"""
        self.position = pos

    def move_direction(self, direction):
        """moves unit at self.speed in direction = x, y"""
        x, y = self.position
        x_2, y_2 = direction
        # new_x

    def attack(self, unit):
        # TODO make unit attack other unit
        pass


# Example specific unit for later use
class Teenie(Unit):
    """ The base unit in the game"""
    def __init__(self, x, y, team):
        Unit.__init__(self, x, y, team, [5, 6, 10, 2, 2])


class Speedie(Unit):
    """ The fast unit in the game"""
    def __init__(self, x, y, team):
        Unit.__init__(self, x, y, team, [])


class Heavie(Unit):
    """The strong unit in the game"""


class Flag():
    """ The flag class for the game"""
    def __init__(self, x, y, color):
        # TODO: Initialize attributes like position, color
        self.position = x , y #should define the position based off of mouse position
        self.color = color #One basic color for each side of team
        self.pickedup = False # Bool for flag picked up
        # has to be removeable
        pass

    def update(self):
        # TODO updates flag position to unit carrying position, or home position
        # if not carried
        pass

    # TODO more methods here!


class Base():
    """ The base class for the game"""
    def __init__(self, x, y, color):
        # TODO: Initialize attributes like position, type of unit selected
        self.position = x, y #pixel position (idk if it's center or corner)
            # would need to see about pygame shapes
        self.color = color # pygame command (imagine that this would change depending
            # on the type of unit being produced or could be a time indicator)
        self.unit_type = unit_type #this is just a placeholder, I imagine that
            # we'd pass this into a fxn or something like that rather than have it
            # be an attribute
        # Add counter for unit generation
        # Add method that increments the counter and makes selected unit if applicable


    #TODO has to do with animations
    def unit_generation():
        # when a unit is generated, have some visual effect
        pass

    # TODO more methods here!


# The Big Cheese, the main loop!
if __name__ == "__main__":
    # game = CaptureGame()
    # game.run()
    unittest.main()
