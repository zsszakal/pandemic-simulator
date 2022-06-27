import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

COLOR_DEFINITIONS = {
    "grey": (35, 35, 40),
    "light_grey": (70, 70, 90),
    "white": (255, 248, 240),
    "red": (239, 71, 111),
    "blue": (17, 138, 178)
}

COLORS = {
    "background": COLOR_DEFINITIONS["grey"],
    "healthy": COLOR_DEFINITIONS["white"],
    "infected": COLOR_DEFINITIONS["red"],
    "immune": COLOR_DEFINITIONS["blue"],
    "dead": COLOR_DEFINITIONS["grey"]
}

# pygame loop
animating = True
while animating:
    # pygame draws things to the screen

    # set background color
    SCREEN.fill(COLORS["background"])
    # update the screen
    pygame.display.flip()


    # track user interaction
    for event in pygame.event.get():
        # user closes the pygame window
        if event.type == pygame.QUIT:
            animating = False