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
            self.unit_list.append(obj.Teenie((500, 500), 1))
            self.unit_list.append(obj.Teenie((500, 600), 2))

        # Sets up initial team positions
        self.base_list.append(obj.Base((10, 10), 1))
        self.base_list.append(obj.Base((self.screen_size[0]-10,
            self.screen_size[1]-10), 2))
        # Sets up flag positions
        self.flag_list.append(obj.Flag((200, 200), 1))
        self.flag_list.append(obj.Flag((300, 300), 2))



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
        self.selected_obj = []  # Keeps track of currently selected objects

    def click_object(self, mouse_pos):
        for flag in self.model.flag_list:  # Loop through flags
            value = flag.rect.collidepoint(mouse_pos)
            # If flag clicked on and no other flag selected
            if value == 1:
                if self.selected_obj == []:

                    # Select flag; add to selected obj list; stop searching
                    flag.select()
                    self.selected_obj.append(flag)
                    return

                else:
                    for thing in self.selected_obj:
                        thing.select()
                    self.selected_obj = []
                    return

        for unit in self.model.unit_list:  # Loop through units
            value = unit.rect.collidepoint(mouse_pos)
            if value == 1:
                if not any(isinstance(x, obj.Unit) for x in self.selected_obj):
                    unit.select()
                    self.selected_obj.append(unit)
                    return
                else:
                    print(type(unit))
                    unit = next(thing for thing in self.selected_obj if type(thing) == obj.Teenie or type(thing) == obj.Speedie or type(thing) == obj.Heavie)
                    unit.select()
                    self.selected_obj.pop(self.selected_obj.index(unit))
                    return

    def move_object(self, mouse_pos):
        for flag in self.model.flag_list:
            if flag.is_selected is True:
                flag.move(mouse_pos)
                pygame.display.update(flag.rect)

    def updates(self, tick):
        self.update_flags()
        self.update_base(tick)
        self.check_collisions(tick)

    def update_unit_type(self, key):
        if key == '1' or key == '2' or key == '3':
            self.model.base_list[0].update_unit(key)
        elif key == 'q' or key == 'w' or key == 'e':
            self.model.base_list[1].update_unit(key)

    def update_base(self, tick):
        # Tells base class to update their personal timecounters
        for base in self.model.base_list:

            unit = base.update(tick)
            if unit is False:
                pass
            else:
                self.model.unit_list.append(unit)

    def update_flags(self):
        # moves flag. (flag is already picked up)
        for flag in self.model.flag_list:
                if flag.pickedup is True:
                    flag.position = flag.unit.position

    def check_attacks(self, tick, unit):
        """checks if attack range collides with body sprite of opposing units"""
        # initiates attacks
        for sec_unit in self.model.unit_list:
            pass

    def check_unit_bumps(self, unit):
        """Optional! checks if unit is bumping into any other units"""
        pass

    def check_wall_bump(self, unit):
        """checks if unit is trying to go through a wall, and
        changes position accordingly"""
        pass

    def check_flag_pickup(self, unit):
        """checks whether an offensive unit is touching the flag"""
        for flag in self.model.flag_list:
            if flag.is_selected is False and unit.team == flag.team:
                if pygame.sprite.collide_rect(flag, unit):
                    flag.be_picked_up(unit)

    def check_map_bump(self, unit):
        """checks if unit is trying to go off the screen and
        changes position accordingly"""
        pass

    def check_collisions(self, tick):
        for unit in self.model.unit_list:
            self.check_unit_bumps(unit)
            self.check_attacks(tick, unit)
            self.check_flag_pickup(unit)
            self.check_wall_bump(unit)
            self.check_map_bump(unit)
