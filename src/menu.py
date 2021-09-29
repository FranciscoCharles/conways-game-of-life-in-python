# _*_coding:utf-8_*_
from os import environ

if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
del environ

import PIL
import pygame
from PIL import Image
from pygame import Surface
from life_game import GridUniverse
from typing import Tuple, List, Optional, Union

Color = Union[int, Tuple[int, int, int]]


def draw_image_in_rect(destiny: Surface, image: Surface, pos: Tuple[int, int], rect: List[int], color: Color, border_color: int):
    [x, y, width, height, border_size] = rect
    pygame.draw.rect(destiny, color, [x, y, width, height], 0)
    pygame.draw.rect(destiny, border_color, [
                     x + border_size, y + border_size, width - 2 * border_size, height - 2 * border_size], 0)
    destiny.blit(image, pos)


def pillImageResize(filename: str, size: Optional[Tuple[int, int]] = (60, 60)) -> Surface:

    image = Image.open(filename)
    image = image.resize(size, PIL.Image.ANTIALIAS)
    image = pygame.image.fromstring(image.tobytes(),
                                    image.size, image.mode)
    return image


class SettingsDisplay:

    def __init__(self, drawing_mode: Optional[bool] = True, x: Optional[int] = 0, y: Optional[int] = 0) -> None:
        self.image_dict = {False: pygame.image.load('images/play.png').convert_alpha(),
                           True: pygame.image.load('images/pause.png').convert_alpha()}
        self.icones = {False: pillImageResize('images/eraser.png').convert_alpha(),
                       True: pillImageResize('images/pencil.png').convert_alpha()}
        self.x = x
        self.y = y
        self.drawing = True
        self.drawing_mode = drawing_mode
        self.font = pygame.font.SysFont('Verdana', 20)
        self.font.set_bold(True)

    def draw(self, destiny: Surface, grid: GridUniverse) -> None:

        image = self.image_dict[self.drawing_mode]
        draw_image_in_rect(destiny, image, (30, 28), [
                           16, 18, 64, 64, 2], (0), (140, 140, 140))
        icone = self.icones[self.drawing]

        draw_image_in_rect(destiny, icone, (108, 20), [
                           106, 18, 64, 64, 2], (0), (120, 120, 120))

        text = self.font.render(
            f"population : {grid.population_size}", True, (255, 255, 255))
        destiny.blit(text, (200, 5))

        text = self.font.render(
            f"generation : {grid.geration}", True, (255, 255, 255))
        destiny.blit(text, (197, 37))

        text = self.font.render(
            f"block size : {grid.block_size}", True, (255, 255, 255))
        destiny.blit(text, (207, 70))
