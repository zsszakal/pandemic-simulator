import pygame
import random
import math
import sys

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


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.people = []

    def get_neighboring_cells(self, n_rows, n_cols):
        index = self.row * n_cols + self.col
        n = index - n_cols if self.row > 0 else None
        s = index + n_cols if self.row < n_rows - 1 else None
        w = index - 1 if self.col > 0 else None
        e = index + 1 if self.col < n_cols else None
        nw = index - n_cols - 1 if self.row > 0 and self.col > 0 else None
        ne = index - n_cols + 1 if self.row > 0 and self.col < n_cols - 1 else None
        sw = index + n_cols - 1 if self.row < n_rows - 1 and self.col > 0 else None
        se = index + n_cols + 1 if self.row < n_rows - 1 and self.col < n_cols - 1 else None
        return [i for i in [index, n, s, e, w, nw, ne, sw, se] if i]


class Grid:
    def __init__(self, people, h_size=20, v_size=20):
        self.h_size = h_size    # horizontal size
        self.v_size = v_size    # vertical size
        self.n_rows = HEIGHT // v_size
        self.n_cols = WIDTH // h_size
        self.cells = []
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                self.cells.append(Cell(row, col))
        self.store_people(people)

    def store_people(self, people):
        for p in people:
            row = int(p.y / self.v_size)
            col = int(p.x / self.h_size)
            index = row * self.n_cols + col
            self.cells[index].people.append(p)

    def show(self, width=1):
        for c in self.cells:
            x = c.col * self.h_size
            y = c.row * self.v_size
            rect = pygame.Rect(x, y, self.h_size, self.v_size)
            pygame.draw.rect(SCREEN, COLOR_DEFINITIONS["light_grey"], rect, width=width)


class Person:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.dx = 0
        self.dy = 0
        self.state = "healthy"
        self.recovery_counter = 0
        self.immunity_counter = 0

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

    def get_infected(self, value=1000):
        self.state = "infected"
        self.recovery_counter = value

    def recover(self, value=2000):
        self.recovery_counter -= 1
        if self.recovery_counter == 0:
            self.state = "immune"
            self.immunity_counter = value

    def lose_immunity(self):
        self.immunity_counter -= 1
        if self.immunity_counter == 0:
            self.state = "healthy"

    def die(self, probability=0.000001):                # probability initializing parameter = mortality rate.
        if random.uniform(0, 1) < probability:     # randomly choosing a number between 0 and 1 (random.uniform(0, 1) will 0.1% likely to be less than 0.001 (currently set to 0.001 = 0.1%)
            self.state = "dead"


class Pandemic:
    def __init__(self,
                 n_people=500,
                 size=3,
                 speed=0.03,
                 infect_dist=5,
                 recover_time=1000,
                 immune_time=1000,
                 prob_catch=0.1,
                 prob_death=0
                 ):
        self.people = [Person() for i in range(n_people)]
        self.size = size
        self.speed = speed
        self.infect_dist = infect_dist
        self.recover_time = recover_time
        self.immune_time = immune_time
        self.prob_catch = prob_catch
        self.prob_death = prob_death
        self.people[0].get_infected(self.recover_time)
        self.grid = Grid(self.people)

    def update_grid(self):
        self.grid = Grid(self.people)

    def slowly_infect_people(self):
        # infect other people
        for p in self.people:
            if p.state == "infected":
                for other in self.people:
                    if other.state == "healthy":
                        dist = math.sqrt((p.x - other.x) ** 2 + (p.y - other.y) ** 2)
                        if dist < self.infect_dist:
                            other.get_infected()

    def infect_people(self):
        for c in self.grid.cells:
            # move on if nobody is infected in that cell
            states = [p.state for p in c.people]
            if states.count("infected") == 0:
                continue

            # create lists of all/infected/healthy people in the area (in a grid)
            people_in_area = []
            for index in c.get_neighboring_cells(self.grid.n_rows, self.grid.n_cols):
                people_in_area += self.grid.cells[index-1].people
                infected_people = [p for p in people_in_area if p.state == "infected"]
                healthy_people = [p for p in people_in_area if p.state == "healthy"]
                if len(healthy_people) == 0:
                    continue

                # loop through the infected people (and then through the healthy people)
                for i in infected_people:
                    for h in healthy_people:
                        dist = math.sqrt((i.x - h.x) ** 2 + (i.y - h.y) ** 2)
                        if dist < self.infect_dist:
                            if random.uniform(0, 1) < self.prob_catch:
                                h.get_infected(self.recover_time)

    def run(self):
        self.update_grid()
        self.infect_people()

        for p in self.people:
            if p.state == "infected":
                p.die(self.prob_death)
                p.recover(self.immune_time)
            elif p.state == "immune":
                p.lose_immunity()
            p.move(self.speed)
            p.show(self.size)

# create pandemic
def game():

    pandemic = Pandemic()
    # set frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)
    # pygame loop
    animating = True
    pausing = False
    while animating:
        if not pausing:
            # set background color
            SCREEN.fill(COLORS["background"])

            # run pandemic
            pandemic.run()

            # update the screen (and the clock)
            clock.tick()
            clock_string = str(math.floor(clock.get_fps()))
            text = font.render(clock_string, True, COLOR_DEFINITIONS["blue"], COLORS["background"])
            text_box = text.get_rect(topleft=(10, 10))
            SCREEN.blit(text, text_box)
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
                # return key to start with a new pandemic
                if event.key == pygame.K_RETURN:
                    pausing = False
                    pandemic = Pandemic()
                # space bar to (=)un-)pause the animation
                if event.key == pygame.K_SPACE:
                    pausing = not pausing

def main():
    game()
main()