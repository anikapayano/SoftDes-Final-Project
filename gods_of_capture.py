"""
This is a capture the flag game made to perform evolutionary algorithms on an
AI.
@authors Colvin Chapman, Sophia Nielsen, Connor Novak,
         Emily Lepert, Anika Payano
         """
import pygame


class CaptureGame(object):
    """Class that defines a game of capture the flag.
       Creates instancese of other important classes,
       Uses Model View Controller Architecture"""
    def __init__(self):
        pygame.init()                   # initialize pygame

        # Initializes screen and places background on it
        self.screen_size = [1840, 920]  # size of screen
        self.screen_sprite = pygame.image.load("sprites/background.png")
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.blit(self.screen_sprite, (0,0))
        pygame.display.update()

        # Initialize MVC classes
        self.model = Model(self.screen_size)

        self.view = View(self.model, self.screen, self.screen_sprite)

        self.control = Controller(self.model)

        self.running = True
        self.game_clock = 0 # Initializes world tick clock


    def run(self):

        # Eventually add pre-game setup stuff somewhere here

        while self.running:
            """runs the game loop"""
            self.game_clock += 1 # Increments world tick clock
            # TODO Check wincase (Controller)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # quits
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    check_pos = pygame.mouse.get_pos()
                    self.control.click_object(check_pos)
                elif event.type == pygame.MOUSEMOTION:
                    new_pos = (event.pos[0], event.pos[1])
                    self.control.move_object(new_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    new_pos = pygame.mouse.get_pos()
                    self.control.place_object(new_pos)



            # User Input May Eventually go here
            # AI Input WILL Go here
            self.view.draw_all()
            pygame.display.update()

            #self.control.update_base(self.game_clock)


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

        # Sets up initial team positions
        self.base_list.append(Base((25,25),1))
        self.flag_list.append(Flag((200,200),2))


class View(object):
    """DOCSTRING
        Class for viewing a model. Contains methods to draw single object and
        to draw all objects
        """

    def __init__(self,model,screen, sprite):
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

    def generate_new_unit(time, unit_type):
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
        


class Unit(object):  # TODO Make uninstantiable

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


class Flag(object):
    """ The flag class for the game"""
    def __init__(self, position, team):
        # TODO: Initialize attributes like position, color
        self.position = x , y = position #should define the position based off of mouse position
        self.team = team #One basic color for each side of team
        self.sprite = pygame.image.load("sprites/team"+str(team)+"flag.png")
        self.oldsprite = self.sprite
        self.is_selected = False
        self.rect = pygame.Rect(self.position[0], self.position[1], 40, 60)
        self.pickedup = False # Bool for flag picked up
        # has to be removeable
        pass

    def select(self):
        if self.is_selected == False:
            self.is_selected = True
            self.sprite = pygame.image.load("sprites/yellowflag.png")
        else:
            self.is_selected = False
            self.sprite = self.oldsprite

    def move(self,mouse_pos):
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
        if self.team == 1:
            self.color = 'red' 
        elif self.team == 2:
            self.color = 'blue'

        #self.unit_type = unit_type #this is just a placeholder, I imagine that
            # we'd pass this into a fxn or something like that rather than have it
            # be an attribute
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
        new_unit = Teenie(self.position[0]+20, self.position[1]+20, self.color)
        return(new_unit)

        #if self.cycle_count == self.current_unit_cycle:




    # TODO more methods here!


# The Big Cheese, the main loop!
if __name__ == "__main__":
    game = CaptureGame()
    game.run()
