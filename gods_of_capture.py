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
        self.screen_size = [920,460] # [1840, 920]  # size of screen
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen_sprite = pygame
        # Add background sprite

        # Initialize MVC classes
        self.model = Model(self.screen_size)
        self.view = View(self.model)
        self.control = Controller(self.model)

        self.running = True
        self.tick = 0

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

            self.control.update_base(self.tick)

            self.tick += 1


class Model(object):
    """DOCSTRING:
        Provides model of the current game state that is changed by the
        Controller and shown by the Viewer; holds lists of all entities on the
        field"""

    def __init__(self, screen_size):
        '''DOCSTRING
        Initializes Model for initial game stages
        '''
        self.tick = 0
        # Lists of objects
        self.unit_list = []
        self.wall_list = []
        self.flag_list = []
        self.base_list = []
        self.screen_size = screen_size # Need this to place obj rel. to screen

        base_width = 50
        base_height = 50

        # Sets up initial team positions
        self.base_list.append(Base(base_width/2, base_height/2, 1))
        self.base_list.append(Base(screen_size[0]-base_width/2, screen_size[1]-base_height/2, 2))


class View(object):
    """Makes the draw methods for all of the classes with"""

    def __init__(self,model):
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

    def generate_new_unit(self, time, unit_type):
        #for each team, if time = 5s
            #new_unit = Unit(x,y,team) => x, y would be set for each team
            #new_unit.draw(x,y)
            #team_base.unit_generation()
        pass

    def update_base(self, tick):
        # Tells base class to update their personal timecounters
        for base in self.model.base_list:
            unit = base.update(tick, 0)
        if unit == False:
            pass
        else:
            self.model.unit_list.append(unit)
        print(self.model.unit_list)
        


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
        self.rect = pygame.Rect(self.position[0],self.position[1],45,45) # Makes collision rect for unit given pos and size

    def move(self):
        # TODO make unit move in force direction by speed stuff
        pass

    def attack(self, unit):
        # TODO make unit attack other unit
        pass

# Example specific unit for later use
class Teenie(Unit):
    """ The base unit in the game"""
    def __init__(self, x, y, team):
        Unit.__init__(self, x, y, team, [5,6,10,2,2], 'sprite')

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
    def __init__(self, x, y, team):
        # TODO: Initialize attributes like position, type of unit selected
        self.position = x, y #pixel position 
        self.cycle_count = 0 #initial cycle count
        if team == 1:
            self.color = 'red' 
        elif team == 2:
            self.color = 'blue'

        #self.unit_type = unit_type #this is just a placeholder, I imagine that
            # we'd pass this into a fxn or something like that rather than have it
            # be an attribute
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
        new_unit = Teenie(self.position[0], self.position[1], self.color)
        return(new_unit)

        #if self.cycle_count == self.current_unit_cycle:




    # TODO more methods here!


# The Big Cheese, the main loop!
if __name__ == "__main__":
    game = CaptureGame()
    game.run()
