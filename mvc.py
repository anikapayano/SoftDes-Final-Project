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
            self.unit_list.append(obj.Teenie((100, 100), 1))
            self.unit_list.append(obj.Teenie((1800, 800), 2))

        # Sets up initial team positions
        self.base_list.append(obj.Base((10, 10), 1))
        self.base_list.append(obj.Base((self.screen_size[0]-110,
            self.screen_size[1]-110), 2))
        # Sets up flag positions
        self.flag_list.append(obj.Flag((50, 460), 1))
        self.flag_list.append(obj.Flag((1790, 460), 2))


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
        try:
            self.screen.blit(thing.sprite, (thing.pos[0], thing.pos[1]))
        except TypeError:
            pass

    def draw_all(self):
        """DOCSTRING:
        Draws all units, walls, flags, and bases in model
        """

        self.screen.blit(self.screen_sprite, (0,0))

        for base in self.model.base_list:
            self.draw(base)
        for wall in self.model.wall_list:
            self.draw(wall)
        for unit in self.model.unit_list:
            self.draw(unit)
        for flag in self.model.flag_list:
            self.draw(flag)
        pygame.display.update()


class Controller(object):
    """ DOCSTRING:
        Holds functions for manipulating model
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
                if unit in self.selected_obj:
                    unit.select()
                    self.selected_obj.pop(self.selected_obj.index(unit))
                    return
                else:
                    if not any(unit.team != u.team for u in self.selected_obj):
                        print(unit.team for u in self.selected_obj)
                        unit.select()
                        self.selected_obj.append(unit)
                        return

        # If no object is clicked, set mouse pos as goal for all selected units
        for thing in self.selected_obj:
            if isinstance(thing, obj.Unit):
                thing.goal_pos = mouse_pos

    def move_object(self, mouse_pos):
        for flag in self.model.flag_list:
            if flag.is_selected is True:
                flag.move(mouse_pos)
                pygame.display.update(flag.rect)


    def updates(self, tick):
        self.update_flags()
        self.update_base(tick)
        self.check_collisions(tick)
        self.update_units()

    def update_unit_type(self, key):
        """ DOCSTRING:
            Given key btw 1-3 or q-e, changes unit type spawned at base 1 or 2.
            """
        if key == '1' or key == '2' or key == '3':
            self.model.base_list[0].update_unit(key)
        elif key == 'q' or key == 'w' or key == 'e':
            self.model.base_list[1].update_unit(key)

    def update_base(self, tick):
        # Tells base class to update their personal timecounters
        for base in self.model.base_list:
            units = self.model.unit_list
            unit = base.update(tick, units)
            if unit is False:
                pass
            else:
                self.model.unit_list.append(unit)

    def update_flags(self):
        # moves flag. (flag is already picked up)
        for flag in self.model.flag_list:
                if flag.pickedup is True:
                    flag.pos = (flag.unit.pos[0] + 10, flag.unit.pos[1] - 50)

    def update_units(self):
        """ KILLs units that have no health
            Updates the collision rectangle for those that are alive"""
        for unit in self.model.unit_list:
            if unit.health <= 0:
                for flag in self.model.flag_list:
                    if flag.unit is unit:
                        flag.pickedup = False
                        flag.unit = None
                self.model.unit_list.remove(unit)
                print('death takes us all')
                try:
                    self.selected_obj.remove(unit)
                except:
                    pass
            else:
                unit.update(self.model.screen_size)

    def check_attacks(self, tick, unit):
        """checks if attack range collides with body sprite of opposing units
            """
        # TODO Make attack range sprite
        for sec_unit in self.model.unit_list:
            if unit.team != sec_unit.team:
                if pygame.sprite.collide_rect(unit, sec_unit):
                    unit.attack(sec_unit, tick)  # initiates attack

    def check_unit_bumps(self, unit):
        """Optional! checks if unit is bumping into any other units"""
        pass

    def check_wall_bump(self, unit):
        """checks if unit is trying to go through a wall, and
        changes position accordingly"""
        pass

    def check_flag_pickup(self, unit):
        """ DOCSTRING:
            Given unit, checks whether unit is touching opponents flag; picks up
            flag if true
            """
        for flag in self.model.flag_list:
            if flag.is_selected is False and unit.team != flag.team and flag.pickedup is False:
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

    def check_win(self):
        """ DOCSTRING:
            Checks if flag in enemy base; moves to win case if so
            """
        for flag in self.model.flag_list:
            for base in self.model.base_list:

                if flag.unit != None:
                    if pygame.sprite.collide_rect(flag.unit, base) and base.team == flag.unit.team:
                        print('MSG: Team ' + str(base.team) + ' is the winner!')
                        return (True, base.team)

        return (False,)

    def drive_unit(self, event):
        # Moves selected object with arrow keys
        try:
            unit = self.model.unit_list[1]
        except IndexError:
            print('ERR: No unit to drive!')
            return
        x = unit.pos[0]
        y = unit.pos[1]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            x += unit.speed
        if keys[pygame.K_LEFT]:
            x -= unit.speed
        if keys[pygame.K_UP]:
            y -= unit.speed
        if keys[pygame.K_DOWN]:
            y += unit.speed

        self.model.unit_list[1].pos = x, y
        pass
