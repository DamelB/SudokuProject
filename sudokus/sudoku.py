import settings as stg

from sudokus.grid import Grid
from sudokus.cell import Cell
from sudokus.logic import Logic

import string
import pygame as pg


class Sudoku(Grid):
    """
    The sudoku itself class + some extra properties for draw.
    Inherits from grid which is to be drawn.
    """
    def __init__(self, font, surface, file, size=(9, 9)):
        self.font = font  # for drawing numbers in cells
        super().__init__(surface, size[::-1])  # init grid

        self.hlighted = None  # highlighted cell

        if file != "":  # import all the stuff
            self.__import(file)
            return

        # editor
        self.__prepare_cells(size)
        self.name = "New Sudoku"  # TODO
        self.description = "New description"

    def draw(self) -> None:
        super().draw()  # grid

        if self.hlighted:
            self.hlighted.hlight()  # highlight

        for row in self.cells:
            for cell in row:
                cell.draw_number(self.font)  # numbers

        pg.display.flip()

    def mouse_cell(self, pos: tuple) -> None:
        """
        Set highlited cell based on the given mouse position. None if outside.

        :param pos: x,y mouse coordinates
        :return: nothing
        """
        cell_coord = ((pos[1] - stg.pivot[0]) // stg.cell_size,
                      (pos[0] - stg.pivot[1]) // stg.cell_size)

        # had a very nice idea with IndexError try-catch but [-x] index notation issue
        if _out_range(cell_coord[0], self.size[0]) or _out_range(cell_coord[1], self.size[1]):
            self.hlighted = None
            return

        self.hlighted = self.cells[cell_coord[0]][cell_coord[1]]  # new highlited cell

    # input moves of highlight
    def move_left(self) -> None:
        if self.hlighted:
            relative = self.hlighted.relative
            if relative[1] > 0:  # not the most left
                self.hlighted = self.cells[relative[0]][relative[1] - 1]
            else:
                self.hlighted = self.cells[relative[0]][self.size[1] - 1]

    def move_up(self) -> None:
        if self.hlighted:
            relative = self.hlighted.relative
            if relative[0] > 0:  # not the most up
                self.hlighted = self.cells[relative[0] - 1][relative[1]]
            else:
                self.hlighted = self.cells[self.size[0] - 1][relative[1]]

    def move_right(self) -> None:
        if self.hlighted:
            relative = self.hlighted.relative
            if relative[1] < self.size[1] - 1:  # not the most right
                self.hlighted = self.cells[relative[0]][relative[1] + 1]
            else:
                self.hlighted = self.cells[relative[0]][0]

    def move_down(self) -> None:
        if self.hlighted:
            relative = self.hlighted.relative
            if relative[0] < self.size[0] - 1:  # not the most down
                self.hlighted = self.cells[relative[0] + 1][relative[1]]
            else:
                self.hlighted = self.cells[0][relative[1]]

    def change_value(self, val: string) -> None:
        if self.hlighted:  # we have highlighted
            if not self.hlighted.default:  # not default
                self.hlighted.value = val

    def check_completed(self) -> bool:
        # completed when no mistake and full board
        return self.__full() and not self.mistake()

    def __full(self) -> bool:
        # full if no empty cells
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if self.cells[row][col].value == "":  # an empty cell
                    return False
        return True

    def mistake(self) -> bool:
        logic = Logic(self.cells)
        return logic.mistake()

    def __import(self, file) -> None:
        with open(stg.prefix + file + stg.suffix, "r") as file:
            lines = file.readlines()

            self.name = file

            # read size
            size_input = lines[0][:-1].split(",")  # extracting \n
            self.size = (int(size_input[0]), int(size_input[1]))
            super().__init__(self.surface, self.size[::-1])  # recalculate grid

            self.__prepare_cells(self.size)
            # read sudoku lines
            for i, line in enumerate(lines[1:self.size[1] + 1]):
                row_input = line[:-1].split(",")
                for j, val in enumerate(row_input):
                    if val != "":
                        self.cells[i][j].set_default()  # given numbers
                    self.cells[i][j].value = val

    def __prepare_cells(self, size) -> None:
        """
        Prepares the list of cells for both editor and play which adjusts given ones.

        :param size: new size
        :return: nothing
        """
        self.cells = []
        for row in range(size[0]):  # row by row, col by col approach
            row_tmp = []
            for col in range(size[1]):
                coord = (col * stg.cell_size + stg.pivot[0],
                         row * stg.cell_size + stg.pivot[1])  # pre-calculation of coordinates
                row_tmp.append(Cell(self.surface, stg.blue_color, coord, (row, col)))
            self.cells.append(row_tmp)


def _out_range(checked: int, length: int) -> bool:
    return checked < 0 or checked >= length
