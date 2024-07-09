import settings as stg
from windows.window import Window, Button
from sudokus.editor import Editor
from sudokus.sudoku import Sudoku

import pygame as pg

# fixed keyboard values
NUM_KEYS = (pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9)
NUMPAD_KEYS = (pg.K_KP0, pg.K_KP1, pg.K_KP2, pg.K_KP3, pg.K_KP4, pg.K_KP5, pg.K_KP6, pg.K_KP7, pg.K_KP8, pg.K_KP9)


class Game(Window):
    """
    Sudoku game class. Can be editor or playable based.
    """
    def __init__(self, surface, editor: bool, file=""):
        super().__init__(surface)
        self.font = pg.font.SysFont(stg.font, stg.cell_size * 3 // 4, True)

        self.editor = editor
        self.QUIT_EDITOR = False

        # TODO numpad
        self.buttons = [Button(self.surface, self.font, "Menu", (980, 100), (400, 200))]
        if self.editor:
            size = _choose_size(self.surface, self.font)  # pre-screen
            if size == (-1, -1):  # quit button was pressed
                self.QUIT_EDITOR = True
                return
            self.sudoku = Editor(self.font, self.surface, size)
            self.buttons.append(Button(self.surface, self.font, "Export", (980, 350), (400, 200)))
        else:
            self.sudoku = Sudoku(self.font, surface, file)

        self.last_keys = pg.key.get_pressed()  # just to define

    def loop(self) -> int:
        """
        Main sudoku game loop.

        :return: next state
        """
        if self.QUIT_EDITOR:
            return -1

        solved_button = False
        while True:
            for event in pg.event.get():
                # user clicked the X to close the windows
                if event.type == pg.QUIT:
                    return -1
                # mouse click
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed()[0]:
                        pos = pg.mouse.get_pos()
                        self.sudoku.mouse_cell(pos)  # check cell
                        if self.buttons[0].pressed(pos):  # back to menu
                            return 0
                        if self.editor:  # check export button
                            if self.buttons[-1].pressed(pos):
                                self.sudoku.export()
                                return 0

            # all keys
            self.__check_keys()

            # draw the sudoku
            self.surface.fill((255, 255, 255))  # background
            if stg.helper:  # helper highlighting mistakes
                self.sudoku.mistake()
            for button in self.buttons:
                button.draw()
            self.sudoku.draw()  # grid with numbers

            # if completed and correctly - draw win state
            if not self.editor and not solved_button:
                if self.sudoku.check_completed():
                    # add win button
                    self.buttons.append(Button(self.surface, self.font, "Solved, cg!", (940, 350), (500, 200)))
                    solved_button = True  # already printed msg

    def __check_keys(self) -> None:
        """
        Handles keyboard input.

        :return: nothing
        """
        self.new_keys = pg.key.get_pressed()
        if self.__key_cond(pg.K_LEFT):
            self.sudoku.move_left()
        if self.__key_cond(pg.K_UP):
            self.sudoku.move_up()
        if self.__key_cond(pg.K_RIGHT):
            self.sudoku.move_right()
        if self.__key_cond(pg.K_DOWN):
            self.sudoku.move_down()

        # numbers
        for i, key in enumerate(NUM_KEYS):
            if self.__key_cond(key):
                self.sudoku.change_value(str(i))
        # numpad
        for i, key in enumerate(NUMPAD_KEYS):
            if self.__key_cond(key):
                self.sudoku.change_value(str(i))

        # need to delete the value
        if self.__key_cond(pg.K_BACKSPACE) or self.__key_cond(pg.K_DELETE):
            self.sudoku.change_value("")

        self.last_keys = self.new_keys

    def __key_cond(self, key) -> bool:
        """
        New key state vs old key state.

        :param key: particular key macro
        :return: true if not same
        """
        return self.new_keys[key] and not self.last_keys[key]


def _choose_size(surface, font) -> tuple:
    """
    A window that lets user choose from sizes of sudoku they want to make.

    :param surface: pygame surface
    :param font: pygame font
    :return: size of sudoku, (-1, -1) if QUIT was called
    """
    buttons = [Button(surface, font, "9x9", (200, 200), (250, 150)),
               Button(surface, font, "6x6", (600, 200), (250, 150)),
               Button(surface, font, "16x16", (1000, 200), (250, 150)),
               Button(surface, font, "8x8", (400, 400), (250, 150)),
               Button(surface, font, "4x4", (800, 400), (250, 150))]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return -1, -1
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    if buttons[0].pressed(pos):
                        return 9, 9
                    elif buttons[1].pressed(pos):
                        return 6, 6
                    elif buttons[2].pressed(pos):
                        return 16, 16
                    elif buttons[3].pressed(pos):
                        return 8, 8
                    elif buttons[4].pressed(pos):
                        return 4, 4

            surface.fill((255, 255, 255))  # background
            for button in buttons:
                button.draw()
            pg.display.flip()
