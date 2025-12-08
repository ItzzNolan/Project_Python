"""corriger la partie qu’Inès a faite"""

import pygame
import sys

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Battle Run")

        self.clock = pygame.time.Clock()
        self.running = False
        self.paused = False

    def game_loop(self):
        self.running = True

        while self.running:
            dt = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Quit requested by user.")
                        self.running = False

                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        print("Pause toggled:", self.paused)

            if not self.paused:
                self.update(dt)
                self.render()

        pygame.quit()

    def update(self, dt):
        pass

    def render(self):
        self.screen.fill((30, 30, 30))
        pygame.display.flip()
