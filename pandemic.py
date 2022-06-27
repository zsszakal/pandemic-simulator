import pygame
import random

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

class Person:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.dx = 0
        self.dy = 0
        self.state = "healthy"

    def show(self, size=10):
        pygame.draw.circle(SCREEN, COLORS[self.state], (self.x, self.y), size)

    def move(self, speed=0.01):
        # adjust position vector
        self.x += self.dx
        self.y += self.dy
        # avoid going out of bounds
        if self.x >= WIDTH:
            self.x = WIDTH - 1
            self.dx *= - 1
        if self.y >= HEIGHT:
            self.y = HEIGHT - 1
            self.dy *= - 1
        if self.x <= 0:
            self.x = 1
            self.dx *= -1
        if self.y <= 0:
            self.y = 1
            self.dy *= -1

        # adjust velocity vector
        self.dx += random.uniform(-speed, speed)
        self.dy += random.uniform(-speed, speed)


people = [Person () for i in range(10)]

# pygame loop
animating = True
while animating:
    # set background color
    SCREEN.fill(COLORS["background"])
    # pygame draws things to the screen
    for p in people:
        p.move()
        p.show()
    # update the screen
    pygame.display.flip()


    # track user interaction
    for event in pygame.event.get():
        # user closes the pygame window
        if event.type == pygame.QUIT:
            animating = False

        # user presses keys on keyboard
        if event.type == pygame.KEYDOWN:
            # escape key to close the animation
            if event.key == pygame.K_ESCAPE:
                animating = False
