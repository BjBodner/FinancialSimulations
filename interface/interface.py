import pygame
import pygame_menu


def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

if __name__ == "__main__":

    pygame.init()
    surface = pygame.display.set_mode((600, 400))



    menu = pygame_menu.Menu(300, 400, 'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)

    menu.add_text_input('Name :', default='John Doe')
    menu.add_text_input('mean :', default=0)
    menu.add_text_input('std :', default=1)
    menu.add_text_input('num_samples :', default=100)
    menu.add_text_input('num_bins :', default=100)
    # menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add_button('plot', start_the_game)
    menu.add_button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)
