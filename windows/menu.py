import settings as stg
from windows.window import Window, Button

import pygame as pg


class Menu(Window):
    """
    Class handling the main menu screen. Just a title and buttons atm.
    """
    def __init__(self, surface):
        super().__init__(surface)
        self.font = pg.font.SysFont(stg.font, 100, True)

        self.title = self.font.render("SUDOKU MENU", False, stg.black_color)

        # TODO need to center eventually somehow
        self.buttons = []
        self.buttons.append(Button(self.surface, self.font, "Load sudoku", (310, 350), (700, 200)))
        self.buttons.append(Button(self.surface, self.font, "Editor", (400, 580), (500, 200)))

    def pick_option(self) -> int:
        """
        Menu loop.

        :return: next state
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return -1
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0]:
                        pos = pg.mouse.get_pos()
                        if self.buttons[0].pressed(pos):  # load sudoku
                            return 1
                        elif self.buttons[1].pressed(pos):  # editor
                            return 2

            self.surface.fill((255, 255, 255))
            self.surface.blit(self.title, (300, 50))
            for button in self.buttons:
                button.draw()
            pg.display.flip()
