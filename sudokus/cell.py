import settings as stg

import pygame as pg


class Cell:
    def __init__(self, surface, color, coords: tuple, relative: tuple):
        self.surface = surface

        self.color = color
        self.value = ""

        self.coord_piv = coords
        self.coord_num = (stg.cell_size / 2 + coords[0], stg.cell_size / 2 + coords[1])

        self.relative = relative
        self.default = False

    def draw_number(self, font) -> None:
        number = font.render(self.value, False, self.color)
        num_rect = number.get_rect(center=self.coord_num)
        self.surface.blit(number, num_rect)

    def hlight(self) -> None:
        hlight_rect = pg.Rect(*self.coord_piv, stg.cell_size, stg.cell_size)
        pg.draw.rect(self.surface, stg.hlight_color, hlight_rect, stg.hlight_size, stg.hlight_radius)

    def error(self) -> None:
        error_rect = pg.Rect(*self.coord_piv, stg.cell_size, stg.cell_size)
        pg.draw.rect(self.surface, stg.error_color, error_rect)

    # for imported sudoku
    def set_default(self) -> None:
        self.default = True
        self.color = stg.black_color
