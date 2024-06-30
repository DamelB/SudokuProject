import settings as stg

import string
import pygame as pg


# really unsure what else this class should do atm but there has to be something within pygame :D
class Window:
    def __init__(self, surface):
        self.surface = surface


class Button:
    def __init__(self, surface, font, label: string, pivot: tuple, size: tuple):
        self.surface = surface
        self.font = font

        self.rect = (*pivot, *size)
        self.pivot = pivot
        self.size = size

        text_pos = (size[0] / 2 + pivot[0], size[1] / 2 + pivot[1])
        self.text = self.font.render(label, True, stg.black_color)
        self.text_rect = self.text.get_rect(center=text_pos)

    # based on the position return if within the range
    def pressed(self, pos: tuple) -> bool:
        cond0 = pos[0] > self.pivot[0] and pos[0] < self.pivot[0] + self.size[0]
        cond1 = pos[1] > self.pivot[1] and pos[1] < self.pivot[1] + self.size[1]
        return cond0 and cond1

    def draw(self) -> None:
        rect = pg.Rect(*self.pivot, *self.size)
        pg.draw.rect(self.surface, stg.black_color, rect, 15, 10)
        self.surface.blit(self.text, self.text_rect)


# a message overwriting the whole surface
def print_message(surface, label) -> None:
    surface.fill((255, 255, 255))  # background
    font = pg.font.SysFont(stg.font, 150)
    text = font.render(label, False, stg.black_color)
    surface.blit(text, (175, 300))
    pg.display.flip()
