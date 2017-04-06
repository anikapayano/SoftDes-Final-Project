import pygame
import unittest
import math
import objects as obj


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


class Model(object):
    """DOCSTRING:
        Provides model of the current game state that is changed by the
        Controller and shown by the Viewer; holds lists of all entities on the
        field"""

    def __init__(self, screen_size):
        '''DOCSTRING:
            Initializes Model for initial game stages
            '''

        self.unit_list = []
        self.wall_list = []
        self.flag_list = []
        self.base_list = []

        self.screen_size = screen_size  # Need this to place obj rel. to screen

    def set_up(self, starting_units):
        # Add units
        for i in range(starting_units):
            self.unit_list.append(obj.Teenie((10, 20 + i*10), 1))
            self.unit_list.append(obj.Teenie((self.screen_size[0]-10,
                                  self.screen_size[1]-(20 + i*10)), 2))

        # Sets up initial team positions
        self.base_list.append(obj.Base((10, 10), 1))
        self.base_list.append(obj.Base((self.screen_size[0]-10,
                              self.screen_size[1]-10), 2))
        # Sets up flag positions
        self.flag_list.append(obj.Flag((300, 300), 2))
        self.flag_list.append(obj.Flag((200, 200), 1))


class View(object):
    """DOCSTRING
        Class for viewing a model. Contains methods to draw single object and
        to draw all objects
        """

    def __init__(self, model, screen, sprite):
        """DOCSTRING
        Given a model to show and a screen upon which to show it, creates
        attributes for each
        """

        self.model = model
        self.screen = screen
        self.screen_sprite = sprite

    def draw(self, thing):
        """DOCSTRING
        Given a thing, draws thing on screen
        """

        self.screen.blit(thing.sprite, (thing.position[0], thing.position[1]))

    def draw_all(self):
        """DOCSTRING:
        Draws all units, walls, flags, and bases in model
        """

        self.screen.blit(self.screen_sprite, (0,0))

        for unit in self.model.unit_list:
            self.draw(unit)
        for wall in self.model.wall_list:
            self.draw(wall)
        for flag in self.model.flag_list:
            self.draw(flag)
        for base in self.model.base_list:
            self.draw(base)
        pygame.display.update()


class Controller(object):
    """DOCSTRING
    Holds functions for manipulating the model
    """

    def __init__(self, model):
        """DOCSTRING
        Initializes Controller object to allow manipulation of Model
        """

        self.model = model

    def click_object(self, mouse_pos):
        for flag in self.model.flag_list:
            value = flag.rect.collidepoint(mouse_pos)
            if value == 1:
                flag.select()
                break

    def move_object(self, mouse_pos):
        for flag in self.model.flag_list:
            if flag.is_selected == True:
                flag.move(mouse_pos)
                pygame.display.update(flag.rect)

    def updates(self, tick):
        self.update_flags()
        self.update_base(tick)
        self.check_collisions()

    def update_base(self, tick):
        # Tells base class to update their personal timecounters
        for base in self.model.base_list:
            unit = base.update(tick, 0)
            if unit is False:
                pass
            else:
                self.model.unit_list.append(unit)

    def update_flags(self):
        # moves flag. (flag is already picked up)
        for flag in self.model.flag_list:
                if flag.picked_up:
                    flag.position = flag.unit.position

    def check_attacks(self, tick):
        """checks if attack range collides with body sprite of opposing units"""
        #initiates attacks

    def check_unit_bumps():
        """Optional! checks if unit is bumping into any other units"""
        pass

    def check_wall_bump():
        """checks if unit is trying to go through a wall, and
        changes position accordingly"""
        pass

    def check_flag_pickup():
        """checks whether an offensive unit is touching the flag"""
        pass

    def check_map_bump():
        """checks if unit is trying to go off the screen and
        changes position accordingly"""
        pass

    def check_collisions(self, tick):
        for unit in self.model.unit_list:
            self.check_unit_bumps()
            self.check_attacks(tick)
            self.check_flag_pickup()
            self.check_wall_bump()
            self.check_map_bump()
