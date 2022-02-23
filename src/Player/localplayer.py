import sys
sys.path.insert(1, sys.path[1]+'../Common/')
import player

import render
import pygame

import time
import math
import threading
class LocalPlayer(player.Player):

        
    def __init__(self, name, render=False):
        
        self.name = name
        self.restricted_view = None

        self.wait_for_input = False
        self.pos = None
        self.text = []
        if render:
            t1 = threading.Thread(target=self.render)
            t1.start()

    def set_name(self):
        name = input("name: ")
        self.name = name

    def get_action(self):
        self.message("your turn to move!")
        self.wait_for_input = True

        while not self.pos:
            time.sleep(0.1)
            continue
        
        self_pos = self.restricted_view["position"]
        new_pos = (self_pos[1] + self.pos[1] - 2, self_pos[0] + self.pos[0] - 2)
        self.pos = None
        return new_pos

        # print("my position is " + str(self.restricted_view["position"]))
        # r = int(input("enter new row: "))
        # c = int(input("enter new col: "))
        

    def message(self, *message):
        print(*message)
        self.text += list(message)

        for i in range(len(self.text) - 25):
            self.text.pop(0)


    def update(self, restricted_view):
        self.restricted_view = restricted_view


    def render(self): 
        while True:
            if self.restricted_view:
                break

        pygame.init()
        screen = pygame.display.set_mode([1300, 900])

        running = True
        
        while running:
            if pygame.mouse.get_pressed()[0] and self.wait_for_input:
                try:
                    pos = pygame.mouse.get_pos()
                    pos = [math.floor(pos[1] / 180), math.floor(pos[0] / 180)]

                    self.wait_for_input = False
                    self.pos = pos

                except AttributeError:
                    pass

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill((50, 50, 50))

            render.draw_restricted_level(screen, self.restricted_view)

            render.draw_board(screen, self.text)


            pygame.display.flip()
            time.sleep(0.1)

        pygame.quit()

    
                