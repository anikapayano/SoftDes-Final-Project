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
        self.screen.blit(self.screen_sprite, (0, 0))
        pygame.display.update()

        # Initialize MVC classes

        self.model = mvc.Model(self.screen_size)


        self.model.set_up(2)

        self.view = mvc.View(self.model, self.screen, self.screen_sprite)

        self.control = mvc.Controller(self.model)

        self.running = True
        self.tick = 0 # Initializes world tick clock


    def run(self):

        # Eventually add pre-game setup stuff somewhere here
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
            # User Input May Eventually go here
            # AI Input WILL Go here
            self.view.draw_all()
            pygame.display.update()

            self.control.update_base(self.tick)



if __name__ == "__main__":
    game = CaptureGame()
    game.run()
    unittest.main()
