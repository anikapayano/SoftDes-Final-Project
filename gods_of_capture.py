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
        self.screen_size = [920,460] #[1840, 920]  # size of screen
        self.screen = pygame.display.set_mode(self.screen_size)
        # Add background sprite

        # Initialize MVC classes
        self.model = Model()
        self.view = View(self.model)
        self.control = Controller(self.model)

        self.running = True

    def run(self):
        while self.running:
            """runs the game loop"""
            # TODO Check wincase (Controller)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # quits
                    self.running = False
            # User Input May Eventually go here
            # AI Input WILL Go here


class Model(object):
    """Makes all starter objects,
    - Field, Bases, Flags, Units..."""

    def __init__(self):
        '''DOCSTRING
            Initializes Model for initial game stages
            '''



class View(object):
    """Makes the draw methods for all of the classes with"""

    def __init__(self,model):
        """DOCSTRING
            Initializes View object to allow references to model"""
        self.model = model


    def draw(self, surface):
        surface.blit(self.model.icon, (self.model.x, self.model.y))


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


class Unit():  # TODO Make uninstantiable

    def __init__(self, x, y, team, stats,sprite):  # TODO set to position of the base
        self.position = x, y
        self.team = team
        self.is_selected = False
        self.strength = stats[0]
        self.speed = stats[1]
        self.health = stats[2]
        self.attack = stats[3]
        self.cooldown = stats[4]
        self.sprite = sprite

    def draw():
        pass


# Example specific unit for later use
class Teenie(Unit):
    """ The base unit in the game"""
    def __init__(self, x, y, team):
        Unit.__init__(self, x, y, team, [5,6,10,2,2],sprite)

class Speedie(Unit):
    """ The fast unit in the game"""
    def __init__(self, strength=4, speed = 9, health = 12, attack=1, cooldown=1):
        self.strength = strength
        self.speed = speed
        self.health = health
        self.attack = attack
        self.cooldown = cooldown
        self.sprite = sptire # TODO: put Speedie sprite here

class Heavie(Unit):
    """The strong unit in the game"""

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
