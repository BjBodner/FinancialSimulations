"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - SIMPLE
Super simple example of pygame-menu usage, featuring a selector and a button.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import pygame_menu
# from pygame_menu.examples import create_example_window
import pygame
from typing import Tuple, Any

# surface = create_example_window('Example - Simple', (600, 400))


# noinspection PyTypeChecker
def create_example_window(
        title: str,
        window_size: Tuple[int, int],
        pygame_menu_icon: bool = True,
        init_pygame: bool = True,
        center_window: bool = True,
        **kwargs
) -> 'pygame.Surface':
    """
    Set pygame window.
    :param title: Window title
    :param window_size: Window size
    :param pygame_menu_icon: Use pygame menu icon
    :param init_pygame: Init pygame
    :param center_window: Center the window
    :param kwargs: Optional keyword arguments received by display set mode
    :return: Pygame surface from created display
    """
    assert len(title) > 0, 'title cannot be empty'
    assert len(window_size) == 2, 'window size shape must be (width, height)'
    assert isinstance(window_size[0], int), 'width must be an integer'
    assert isinstance(window_size[1], int), 'height must be an integer'

    from pygame_menu.baseimage import IMAGE_EXAMPLE_PYGAME_MENU, BaseImage
    import os

    if init_pygame:
        pygame.init()
    if center_window:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    try:
        surface = pygame.display.set_mode(window_size, **kwargs)
    except TypeError:
        surface = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)

    if pygame_menu_icon:
        # noinspection PyBroadException
        try:
            if _PYGAME_ICON[0] is not None:
                pygame.display.set_icon(_PYGAME_ICON[0])
            else:
                icon = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU).get_surface(new=False)
                pygame.display.set_icon(icon)
                _PYGAME_ICON[0] = icon
        except BaseException:  # lgtm [py/catch-base-exception]
            pass

    return surface

def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.

    :return: None
    """
    print('Set difficulty to {} ({})'.format(selected[0], value))


def start_the_game() -> None:
    """
    Function that starts a game. This is raised by the menu button,
    here menu can be disabled, etc.

    :return: None
    """
    global user_name
    print('{0}, Do the job here!'.format(user_name.get_value()))



surface = create_example_window('Example - Simple', (600, 400))


menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)

user_name = menu.add_text_input('Name: ', default='John Doe', maxchar=10)
menu.add_selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)