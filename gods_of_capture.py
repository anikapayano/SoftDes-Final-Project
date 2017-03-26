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
    def __init__(self):
        # TODO: Initialize attributes like . . . position?
        pass

    def draw(self):
        # TODO draw sprite at location
        pass

    # TODO more methods here!


class Base():
    """ The base class for the game"""
    def __init__(self):
        # TODO: Initialize attributes like position, type of unit selected
        pass

    def draw(self):
        # TODO draw sprite at location
        pass

    # TODO more methods here!


# The Big Cheese, the main loop!
if __name__ == "__main__":
    game = CaptureGame()
    game.run()
