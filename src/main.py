# _*_coding:utf-8_*_
from os import environ

if 'PYGAME_HIDE_SUPPORT_PROMPT' not in environ:
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
del environ

import pygame
from typing import Tuple
from menu import SettingsDisplay
from life_game import GridUniverse


def edit_automanton(settings: SettingsDisplay, grid: GridUniverse, shift_position: Tuple[int, int], mouse_press: bool) -> None:
    if mouse_press and settings.drawing_mode:
        (shift_x, shift_y) = shift_position
        (mousex, mousey) = pygame.mouse.get_pos()
        mousex -= shift_x
        mousey -= shift_y
        if pygame.mouse.get_pressed(0):
            if mousex < grid.width and mousey < grid.height:
                row, column = mousey // grid.block_size, mousex // grid.block_size
                grid.toogle_automaton(row, column, settings.drawing)


def controls(game: bool, settings: SettingsDisplay, grid: GridUniverse, mouse_press: bool) -> Tuple[bool, bool]:
    global FPS

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
            break
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                game = False
                break
            elif e.key == pygame.K_a:
                settings.drawing_mode = not settings.drawing_mode
            elif e.key == pygame.K_s:
                settings.drawing = not settings.drawing
            elif e.key == pygame.K_z:
                if not settings.drawing_mode:
                    settings.drawing_mode = True
                grid.init_automatons()
            elif e.key == pygame.K_x:
                if not settings.drawing_mode:
                    settings.drawing_mode = True
                grid.create_automatons()
            elif e.key == pygame.K_q:
                grid.diminuir_grid()

            elif e.key == pygame.K_w:
                grid.aumentar_grid()

        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = True
        elif e.type == pygame.MOUSEBUTTONUP:
            mouse_press = False

    return game, mouse_press


def main() -> None:

    game = True
    SCREEN_W = 600
    SCREEN_H = 580
    mouse_press = False
    gray_color = (190, 190, 190)
    shift_mouse_position = (0, 100)
    settings_rect = [0, 0, SCREEN_W, 100]

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    icon = pygame.image.load('images/icon32.png')
    pygame.display.set_caption('Conway\'s Game of Life')
    pygame.display.set_icon(icon)

    grid_surface = pygame.Surface((SCREEN_W, 480))
    clock = pygame.time.Clock()
    screen.fill(gray_color)
    grid_surface.fill(gray_color)
    pygame.display.flip()

    settings = SettingsDisplay()
    grid_universe = GridUniverse(SCREEN_W, 480, 10, False)

    while game:

        clock.tick(60)
        pygame.draw.rect(screen, 0x4B0082, settings_rect)
        grid_surface.fill(gray_color)

        game, mouse_press = controls(
            game, settings, grid_universe, mouse_press)

        if game:

            edit_automanton(settings, grid_universe,
                            shift_mouse_position, mouse_press)
            if not settings.drawing_mode:
                grid_universe.update_automatons()

            grid_universe.draw_automatons(grid_surface)
            settings.draw(screen, grid_universe)

            screen.blit(grid_surface, shift_mouse_position)
            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
