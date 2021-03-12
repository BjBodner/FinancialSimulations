import pygame
from menus import MainMenu, SURFACE_SIZE


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode(SURFACE_SIZE)
    MainMenu(surface, number=1).run(surface)