#!/usr/bin/env python
# coding: utf8

from minesweepingpath import MineSweepingPath
import pygame
import RPi.GPIO as GPIO


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(7, GPIO.IN, GPIO.PUD_DOWN)

def generate_paths(current_path):
    paths = []
    if len(current_path.path) == 5:
        paths.append(current_path)
        print(current_path)
        return paths
    paths = []
    x_curr, y_curr = current_path.path[-1]
    for x in range(0, 4):
        for y in range(0, 4):
            if x == x_curr and y == y_curr or (x, y) in current_path.path:
                continue
            newpath = MineSweepingPath()
            newpath.path = current_path.path.copy()
            newpath.totalDifficulty = current_path.totalDifficulty
            newpath.difficulties = current_path.difficulties.copy()
            newpath.add_step((x, y))
            paths.extend(generate_paths(newpath))

    return paths


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 50
HEIGHT = 50

# This sets the margin between each cell
MARGIN = 5


def main():
    gpio_setup()

    pygame.init()
    (width, height) = (600, 400)
    screen = pygame.display.set_mode((width, height))
    pygame.display.flip()
    running = True
    pygame.display.set_caption('Piwars Mine Sweeper')
    background_colour = (255, 255, 255)
    screen.fill(background_colour)
    pygame.display.flip()
    grid = []
    path = MineSweepingPath()
    number_of_step = 0
    font = pygame.font.Font('font/dosis.ttf', 16)

    for row in range(4):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(4):
            grid[row].append(0)  # Append a cell
    x, y = path.path[number_of_step]
    grid[x][y] = 1
    # create a new Surface
    grid_surface = pygame.Surface((500, 300))

    # change its background color
    grid_surface.fill((55, 200, 255))

    # blit myNewSurface onto the main screen at the position (0, 0)
    screen.blit(grid_surface, (50, 50))

    grid_position = (50, 50)
    log_position = (400, 200)
    button_pressed = False
    while running:

        next_block=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                next_block=True
        if button_pressed and GPIO.input(7)==GPIO.LOW:
            next_block=True
        if not button_pressed and GPIO.input(7)==GPIO.HIGH:
            button_pressed=True
        if next_block or GPIO.input(7):
            print("next block!")
            x, y = path.next_step()
            reset_grid(grid)
            grid[x][y] = 1
        # Draw the grid
        refresh_grid(grid, grid_surface, screen, grid_position)
        print_log(path, font, screen, log_position)
        pygame.display.flip()
    pygame.quit()





def reset_grid(grid):
    for x in range(4):
        for y in range(4):
            grid[x][y] = 0


def print_log(path, font, log_screen, log_position):
    if (len(path.difficulties) > 0):
        log = "DIFFICULTY: " + str(path.difficulties[-1]) + "\n" + " ORIENTATION: " + \
              str(round(path.current_orientation, 2)) + " \n"
    else:
        log = "DIFFICULTY: n/a \n" + " ORIENTATION: " + str(path.current_orientation) + " \n"
    log += "BUDGET: " + str(round(path.difficulty_budget,2))
    blit_text(log_screen, log, log_position, font)


def refresh_grid(grid, grid_surface, screen, grid_position):
    rect = screen.get_rect()
    for row in range(4):
        for column in range(4):
            color = WHITE
            if grid[row][column] == 1:
                color = RED
            pygame.draw.rect(grid_surface,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN + 20,
                              (MARGIN + HEIGHT) * row + MARGIN + 20,
                              WIDTH,
                              HEIGHT])
            screen.blit(grid_surface, grid_position)


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


if __name__ == '__main__':
    # path = MineSweepingPath()
    # path.path = [(0, 0)]
    # path.add_step((0, 1))
    # path.add_step((1, 1))
    # path.add_step((0, 0))
    # path.add_step((0, 1))
    # path.add_step((3, 3))
    # path.add_step((0, 0))
    # print(path)
    # main()
    main()
