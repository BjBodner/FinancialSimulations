import pygame
import pygame_menu


def set_difficulty(value, difficulty):
    print(f"value = {value}, difficulty = {difficulty}")


def process_name(value):
    print(value)


def start_the_game():
    print("rock and roll")


if __name__ == "__main__":
    pygame.init()
    surface = pygame.display.set_mode((600, 400))

    menu = pygame_menu.Menu(300, 400, "Welcome", theme=pygame_menu.themes.THEME_BLUE)

    # add all widgets
    menu.add_text_input("name :", default="John Doe", onreturn=process_name)
    menu.add_text_input("price :", default="0", onreturn=process_name, valid_chars=["0", "1"])

    menu.add_selector("difficulty :", [("hard", 1), ("easy", 2)], onchange=set_difficulty)
    # menu.add_color_input("select color", "rgb", "1")
    menu.add_image("interface/ball.jpg", scale=(0.1, 0.1))
    menu.add_vertical_margin(40)
    menu.add_label("press below to enter or quit")
    menu.add_button("play", start_the_game)
    menu.add_button("quit", pygame_menu.events.PYGAME_QUIT)


    menu.mainloop(surface)
