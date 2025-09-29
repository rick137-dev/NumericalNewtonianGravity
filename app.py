from StarSystem import StarSystem
from Solver import SystemSolver
from Star import Star
import pygame


def startApp():
    print("App opened")
    pygame.init()
    dt =0
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    game_time_limit = 2000

    while running and dt < game_time_limit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(60)
        print("")

    pygame.quit()
