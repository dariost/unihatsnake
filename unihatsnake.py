#!/usr/bin/env python3
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright 2017 - Dario Ostuni <dario.ostuni@gmail.com>
#

import unicornhat as unicorn
import curses
from time import sleep
from random import randrange
from sys import exit, argv

LED_BRIGHTNESS = 0.5
COLOR_SNAKE_BODY = (0, 255, 0)
COLOR_SNAKE_HEAD = (255, 255, 0)
COLOR_APPLE = (255, 0, 0)
if len(argv) <= 1:
    VELOCITY_SNAKE = 5.0
else:
    try:
        VELOCITY_SNAKE = float(argv[-1])
    except:
        VELOCITY_SNAKE = 5.0
ROTATION = 0

def main(stdscr):
    global snake
    stdscr.nodelay(1)
    unicorn.set_layout(unicorn.HAT)
    unicorn.rotation(ROTATION)
    unicorn.brightness(LED_BRIGHTNESS)
    width, height = unicorn.get_shape()
    assert width == 8 and height == 8
    end_game = False
    won = False
    free_cells = [(i, j) for i in range(8) for j in range(8)]
    free_cells.remove((0, 0))
    free_cells.remove((1, 0))
    snake = [(1, 0), (0, 0)]
    apple = free_cells[randrange(len(free_cells))]
    direction = (1, 0)
    def print_snake():
        global snake
        unicorn.clear()
        unicorn.set_pixel(snake[0][0], snake[0][1], COLOR_SNAKE_HEAD[0], COLOR_SNAKE_HEAD[1], COLOR_SNAKE_HEAD[2])
        for i in range(1, len(snake)):
            unicorn.set_pixel(snake[i][0], snake[i][1], COLOR_SNAKE_BODY[0], COLOR_SNAKE_BODY[1], COLOR_SNAKE_BODY[2])
        unicorn.set_pixel(apple[0], apple[1], COLOR_APPLE[0], COLOR_APPLE[1], COLOR_APPLE[2])
        unicorn.show()
    def print_all(color):
        unicorn.clear()
        for i in range(8):
            for j in range(8):
                unicorn.set_pixel(i, j, color[0], color[1], color[2])
        unicorn.show()
    print_snake()
    sleep(2.5)
    while True:
        if end_game:
            sleep(2.5)
            exit(0)
        else:
            print_snake()
            sleep(1.0 / VELOCITY_SNAKE)
            code = -1
            while True:
                code_tmp = stdscr.getch()
                if code_tmp != -1:
                    code = code_tmp
                else:
                    break
            if code == 260:
                if direction != (1, 0):
                    direction = (-1, 0)
            elif code == 258:
                if direction != (0, -1):
                    direction = (0, 1)
            elif code == 261:
                if direction != (-1, 0):
                    direction = (1, 0)
            elif code == 259:
                if direction != (0, 1):
                    direction = (0, -1)
            next_cell = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            if next_cell[0] < 0 or next_cell[0] >= 8 or next_cell[1] < 0 or next_cell[1] >= 8:
                end_game = True
                print_all((255, 0, 0))
                continue
            if next_cell in snake:
                end_game = True
                print_all((255, 0, 0))
                continue
            free_cells.remove(next_cell)
            if len(free_cells) == 0:
                end_game = True
                print_all((0, 255, 0))
                continue
            if next_cell == apple:
                apple = free_cells[randrange(len(free_cells))]
            else:
                free_cells.append(snake.pop())
            snake.insert(0, next_cell)

if __name__ == "__main__":
    curses.wrapper(main)
