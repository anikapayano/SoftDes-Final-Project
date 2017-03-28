"""
This is a capture the flag game made to perform evolutionary algorithms on an
AI.
@authors Colvin Chapman, Sophia Nielsen, Connor Novak,
         Emily Lepert, Anika Payano
         """
import pygame


class CaptureGame():
    """Class that defines a game of capture the flag.
       Creates instancese of other important classes,
       Uses Model View Controller Architecture"""
    def __init__(self):
        pygame.init()                   # initialize pygame
        self.screen_size = [1840, 920]  # size of screen
        self.screen = pygame.display.set_mode(self.screen_size)
        self.model = Model()
        self.view = View()
        self.control = Control()
        self.running = True

    def run(self):
        while self.run:
            """runs the game loop"""
            # TODO Check wincase (Controller)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # quits
                    self.running = False
            # TODO Escape key
            # User Input May Eventually go here
            # AI Input WILL Go here


class Model():
    """Makes all starter objects,
    - Field, Bases, Flags, Units..."""


class View():
    """Makes the draw methods for all of the classes with"""

    def main.unit.draw():
        pass


class Controller():
    """Holds functions for manipulating the model"""
    def generate_new_unit(time, unit_type):
        #for each team, if time = 5s
            #new_unit = Unit(x,y,team) => x, y would be set for each team
            #new_unit.draw(x,y)
            #team_base.unit_generation()
        pass


class Unit():  # TODO Make uninstantiable

    def __init__(self, x, y, team):  # TODO set to position of the base
        self.position = x, y
        self.team = team
        self.is_selected = False

    def draw():
        pass


# Example specific unit for later use
class Teenie(Unit):
    """ The base unit in the game"""
    def __init__(self, strength=4, speed=8, health=12, attack=2, cooldown=3):
        self.strength = strength
        self.speed = speed
        self.health = health
        self.attack = attack
        self.cooldown = cooldown
        self.sprite = sprite  # TODO: put Teenie sprite here


class Flag():
    """ The flag class for the game"""
    def __init__(self, x, y, color):
        # TODO: Initialize attributes like position, color
        self.position = x , y #should define the position based off of mouse position
        self.color = color #One basic color for each side of team
        # has to be removeable
        pass

    def draw(self):
        # TODO draw sprite at location
        pass

    # TODO more methods here!


class Base():
    """ The base class for the game"""
    def __init__(self, x, y, color, current_time):
        # TODO: Initialize attributes like position, type of unit selected
        self.position = x, y #pixel position (idk if it's center or corner)
            # would need to see about pygame shapes
        self.color = color # pygame command (imagine that this would change depending
            # on the type of unit being produced or could be a time indicator)
        self.unit_type = unit_type #this is just a placeholder, I imagine that
            # we'd pass this into a fxn or something like that rather than have it
            # be an attribute
        self.time = current_time # what time is it in the game?
            # i'm imagigining that theres a time module in python so this would
            # keep track of the seconds (ie: is it 5s or 6s)



    def draw(self):
        # TODO draw sprite at location

        pass

    def change_color():
        # change the self.color depending on the unit type
        pass

    def unit_generation():
        # when a unit is generated, have some visual effect
        pass

    # TODO more methods here!


# The Big Cheese, the main loop!
if __name__ == "__main__":
    game = CaptureGame()
    game.run()
