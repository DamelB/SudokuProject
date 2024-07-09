import settings as stg

import pygame as pg


class Grid:
    """
    Class of all grid lines and drawing on top of them.
    """
    def __init__(self, surface, size):
        self.surface = surface
        self.size = size
        self.__calc_pts()  # prepares a list of grid points

    def draw(self):
        self.__draw_thin()
        self.__draw_thick()

    def __draw_thin(self) -> None:
        for pt in self.row_pts[1:self.size[0]]:
            self.__draw_line(True, pt)

        for pt in self.col_pts[1:self.size[1]]:
            self.__draw_line(True, pt)

    def __draw_thick(self) -> None:
        # rectangle around the grid
        rect_pivot = (coord - stg.thick_size for coord in stg.pivot)  # shift by the line size
        rect_size = (size*stg.cell_size + 2*stg.thick_size for size in self.size[::-1])  # grid + 2 lines
        big_rect = pg.Rect(*rect_pivot, *rect_size)
        pg.draw.rect(self.surface, stg.black_color, big_rect, stg.thick_size)

        # lines in common cases, not sure how to handle other
        if self.size in stg.common_sizes:
            if self.size == (9, 9):
                self.__draw_thick_9x9()
            elif self.size == (16, 16):
                self.__draw_thick_16x16()
            else:
                self.__draw_thick_other()

    def __draw_thick_9x9(self) -> None:
        for i in range(3, 7, 3):
            self.__draw_line(False, self.row_pts[i])
            self.__draw_line(False, self.col_pts[i])

    def __draw_thick_16x16(self) -> None:
        for i in range(4, 13, 4):
            self.__draw_line(False, self.row_pts[i])
            self.__draw_line(False, self.col_pts[i])

    # 4x4, 6x6, 8x8 - based on ones I have seen
    def __draw_thick_other(self) -> None:
        self.__draw_line(False, self.col_pts[self.size[1] // 2])  # middle
        for i in range(2, self.size[0], 2):
            self.__draw_line(False, self.row_pts[i])

    def __draw_line(self, thin: bool, pt: list) -> None:
        if thin:
            pg.draw.line(self.surface, stg.black_color, *pt, stg.thin_size)
        else:
            pg.draw.line(self.surface, stg.black_color, *pt, stg.thick_size)

    def __calc_pts(self) -> None:
        """
        Pre-calculation of all points the lines are on - from A to B.
        :return:
        """
        # horizontal
        self.row_pts = []
        x_end = stg.pivot[0] + stg.cell_size * self.size[1]
        for y in range(0, self.size[0] + 1):
            line = []
            y_pos = y * stg.cell_size + stg.pivot[1]
            line.append((stg.pivot[0], y_pos))
            line.append((x_end, y_pos))
            self.row_pts.append(line)

        # vertical lines points
        self.col_pts = []
        y_end = stg.pivot[1] + stg.cell_size * self.size[0]  # end y point - yPivot + yEnd
        for x in range(0, self.size[1] + 1):  # +1 to the size cause there is one extra line
            line = []
            x_pos = x * stg.cell_size + stg.pivot[0]  # fixed position for vertical, just shift + xPivot
            line.append((x_pos, stg.pivot[1]))  # starting point
            line.append((x_pos, y_end))  # ending point
            self.col_pts.append(line)
