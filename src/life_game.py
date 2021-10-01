# _*_coding:utf-8_*_
from __future__ import annotations
from os import environ

if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
del environ

import pygame
import numpy as np
from random import choice
from pygame import Surface
from typing import Optional
from math import floor


class Automaton:
    def __init__(self, type: str, alive: bool) -> None:
        self.alive = alive
        self.type = type
        self.must_die = False

    def copy(self) -> Automaton:
        return Automaton(self.type, self.alive)

    def update(self) -> None:
        if self.must_die:
            self.alive = False
            self.must_die = False
        else:
            self.alive = True

    def draw(self, destiny: Surface, x: int, y: int, size: Optional[int] = 10):
        if self.alive:
            pygame.draw.rect(destiny, (100, 0, 0), (x, y, size, size))


class GridUniverse:

    def __init__(self, max_width: int, max_height: int, size: Optional[int] = 10, ignore_edge: Optional[bool] = True) -> None:
        self.geration = 0
        self.population_size = 0
        self.automatons_list = []

        self.block_size = size
        self.max_width = max_width
        self.max_height = max_height
        self.ignore_edge = ignore_edge
        self.grid_shift_position = (0, 0)
        self.change_block_size(size, max_width, max_height)
        self.position_neighbors = np.array(
            [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]], dtype=int)

    def init_automatons(self) -> None:
        self.geration = 0
        self.population_size = 0
        self.automatons_list.clear()
        for _ in range(self.rows):
            self.automatons_list.append(
                [Automaton('child', False) for _ in range(self.columns)])

    def increase_grid(self):
        if self.block_size < 60:
            self.change_block_size(self.block_size + 2)

    def decrease_grid(self):
        if self.block_size > 10:
            self.change_block_size(self.block_size - 2)

    def change_block_size(self, size: int, width: Optional[int] = None, height: Optional[int] = None) -> None:
        if width is None:
            width = self.max_width
        if height is None:
            height = self.max_height
        (rows, columns) = (int(floor(height / size)), int(floor(width / size)))
        self.rows = rows
        self.columns = columns
        self.height = size * rows
        self.width = size * columns
        self.block_size = size
        self.center_grid()
        self.init_automatons()

    def create_automatons(self) -> None:
        self.geration = 0
        self.population_size = 0
        self.automatons_list.clear()
        for i in range(self.rows):
            self.automatons_list.append([])
            for j in range(self.columns):
                self.automatons_list[i].append(
                    Automaton(choice(['child', 'adult']), choice([False, True])))

    def update_automatons(self) -> None:
        for i in range(self.rows):
            for j in range(self.columns):
                count = 0
                automaton = self.automatons_list[i][j]
                for x, y in self.position_neighbors + [i, j]:
                    if self.ignore_edge:
                        if self.automatons_list[x % self.rows][y % self.columns].alive:
                            count += 1
                    else:
                        if -1 < x < self.rows and -1 < y < self.columns and self.automatons_list[x][y].alive:
                            count += 1
                if count == 3 and (not automaton.alive):
                    automaton.must_die = False
                    automaton.type = 'child'
                elif (count < 2 or count > 3) and automaton.alive:
                    automaton.must_die = True
                    automaton.type = 'adult'
                elif (1 < count < 4) and automaton.alive:
                    automaton.must_die = False
                    automaton.type = 'adult'
                else:
                    automaton.must_die = True
        self.population_size = 0
        self.geration += 1
        for rows in self.automatons_list:
            for automaton in rows:
                automaton.update()
                if automaton.alive:
                    self.population_size += 1

    def center_grid(self):
        self.grid_shift_position = (
            (self.max_width - self.width) // 2, (self.max_height - self.height) // 2)

    def toogle_automaton(self, row: int, column: int, alive: bool) -> None:
        automaton = self.automatons_list[row][column]
        if alive and not automaton.alive:
            self.population_size += 1
        elif not alive and automaton.alive:
            self.population_size -= 1
        automaton.alive = alive
        automaton.must_die = not alive
        automaton.type = 'adult'

    def draw_automatons(self, destiny: Surface) -> None:
        (shift_x, shift_y) = self.grid_shift_position
        if self.height != self.max_height or self.width != self.max_width:
            destiny.fill((0x4B0082))

        pygame.draw.rect(destiny, (190, 190, 190), [
                         shift_x, shift_y, self.width, self.height])

        for i in range(self.rows):
            for j in range(self.columns):
                self.automatons_list[i][j].draw(
                    destiny, shift_x + j * self.block_size, shift_y + i * self.block_size, self.block_size)

                pygame.draw.line(destiny, (0), (shift_x + j * self.block_size, shift_y),
                                 (shift_x + j * self.block_size, shift_y + self.rows * self.block_size), 2)
            pygame.draw.line(destiny, (0), (shift_x, shift_y + i * self.block_size),
                             (shift_x + self.columns * self.block_size, shift_y + i * self.block_size), 2)
        pygame.draw.line(destiny, (0), (shift_x + self.width, shift_y),
                         (shift_x + self.width, shift_y + self.height), 2)
        pygame.draw.line(destiny, (0), (shift_x, shift_y + self.height),
                         (shift_x + self.width, shift_y + self.height), 2)
