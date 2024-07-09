import settings as stg

import string
import pygame as pg


class Window:
    """
    Menu and game inherit from this, some other window properties could get added.
    """
    def __init__(self, surface):
        self.surface = surface


class Button:
    """
    A single button class.
    """
    def __init__(self, surface, font, label: string, pivot: tuple, size: tuple):
        self.surface = surface
        self.font = font

        self.rect = (*pivot, *size)
        self.pivot = pivot
        self.size = size

        text_pos = (size[0] / 2 + pivot[0], size[1] / 2 + pivot[1])
        self.text = self.font.render(label, True, stg.black_color)
        self.text_rect = self.text.get_rect(center=text_pos)

    def pressed(self, pos: tuple) -> bool:
        """
        Check if the button was pressed

        :param pos: x,y position of a click
        :return: true if within button frame
        """
        cond0 = pos[0] > self.pivot[0] and pos[0] < self.pivot[0] + self.size[0]
        cond1 = pos[1] > self.pivot[1] and pos[1] < self.pivot[1] + self.size[1]
        return cond0 and cond1

    def draw(self) -> None:
        """
        Draw the button.

        :return: nothing
        """
        rect = pg.Rect(*self.pivot, *self.size)
        pg.draw.rect(self.surface, stg.black_color, rect, 15, 10)
        self.surface.blit(self.text, self.text_rect)


def print_message(surface, label) -> None:
    """
    A message overwriting the whole surface.

    :param surface: pygame surface instance
    :param label: text to be printed
    :return: nothing
    """
    surface.fill((255, 255, 255))  # background
    font = pg.font.SysFont(stg.font, 150)
    text = font.render(label, False, stg.black_color)
    surface.blit(text, (175, 300))
    pg.display.flip()
