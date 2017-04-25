"""
This is a capture the flag game made to perform evolutionary algorithms on an
AI.
@authors Colvin Chapman, Sophia Nielsen, Connor Novak,
         Emily Lepert, Anika Payano
         """
import pygame
import unittest
import math
import objects as obj
import mvc
import ai_rule
from objects import TestUnit


class CaptureGame(object):
    """ DOCSTRING:
        Class that defines a game of capture the flag.
        Creates instancese of other important classes,
        Uses Model View Controller Architecture
        """
    def __init__(self):
        pygame.init()                   # initialize pygame

        # Initializes screen and places background on it
        self.screen_size = [1840, 920]  # size of screen
        self.screen_sprite = pygame.image.load("sprites/background.png")
        self.screen = pygame.display.set_mode(self.screen_size)
        self.screen.blit(self.screen_sprite, (0, 0))
        pygame.display.update()

        # Initialize MVC classes

        self.model = mvc.Model(self.screen_size)


        self.model.set_up(1)

        self.view = mvc.View(self.model, self.screen, self.screen_sprite)

        self.control = mvc.Controller(self.model)

        # Creates ai; passes in first info about board
        self.ai1 = ai_rule.AIRule(1,[1,0.1,1,1,1])
        self.ai1.update(self.model.unit_list,self.model.flag_list,self.model.base_list)
        self.ai2 = ai_rule.AIRule(2,[0.1,1,1,1,1])
        self.ai2.update(self.model.unit_list,self.model.flag_list,self.model.base_list)

        self.running = True
        self.tick = 0 # Initializes world tick clock



    def run(self):
        """ DOCSTRING:
            implements game loop, win case, and transitions between them
            """
        while self.running:
            """runs the game loop"""
            self.tick += 1 # Increments world tick clock
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

                # Key controls for selecting units to generate at bases
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.control.update_unit_type('1')
                    elif event.key == pygame.K_2:
                        self.control.update_unit_type('2')
                    elif event.key == pygame.K_3:
                        self.control.update_unit_type('3')
                    elif event.key == pygame.K_q:
                        self.control.update_unit_type('q')
                    elif event.key == pygame.K_w:
                        self.control.update_unit_type('w')
                    elif event.key == pygame.K_e:
                        self.control.update_unit_type('e')

            self.control.drive_unit(event) # Allows arrow key control of 1 unit

            # Tells ais to give units direction commands
            self.ai1.unit_command()
            self.ai2.unit_command()

            # Updates display
            self.view.draw_all()
            pygame.display.update()

            # Tells ais to update unit choices at bases if bases have made units
            infolist = self.control.updates(self.tick)
            if infolist[0][0] == 1:
                if infolist[0][1] == True: self.control.update_unit_type(self.ai1.base_command())
                if infolist[1][1] == True: self.control.update_unit_type(self.ai2.base_command())
            elif infolist[0][0] == 2:
                if infolist[0][1] == True: self.control.update_unit_type(self.ai2.base_command())
                if infolist[1][1] == True: self.control.update_unit_type(self.ai1.base_command())

            # Updates info that ais "know"
            self.ai1.update(self.model.unit_list,self.model.flag_list,self.model.base_list)
            self.ai2.update(self.model.unit_list,self.model.flag_list,self.model.base_list)

            if self.control.check_win() is True:
                self.running = False
                self.winning = True

        while self.winning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # quits
                    self.winning = False


if __name__ == "__main__":
    game = CaptureGame()
    game.run()

    #TestUnit().run_tests()
