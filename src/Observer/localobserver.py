import sys
sys.path.insert(0, sys.path[0]+'../Common/')
import observer
import pygame
import render
class LocalObserver(observer.Observer):

    def __init__(self):
        self.state = None
    
    def update(self, state):
        self.state = state

    def render(self):
        while True:
            if self.state:
                break

        pygame.init()
        screen = pygame.display.set_mode([900, 900])

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((50, 50, 50))
    
            render.draw_level(screen, self.state)
            render.draw_character(screen, str(self.state))

            pygame.display.flip()

        pygame.quit()

   