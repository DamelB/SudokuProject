import settings as stg
from sudokus.cell import Cell


class Logic:
    """
    A logic class checking current state of a list of cells.
    """
    def __init__(self, cells: list[list[Cell]]):
        self.cells = cells
        self.size = (len(cells), len(cells[0]))

    def mistake(self):
        """
        Checks all possible mistakes within the sudoku.
        :return: nothing
        """
        mistake = False
        for row in range(self.size[0]):
            if self.__mistake_row(row):
                mistake = True

        for col in range(self.size[1]):
            if self.__mistake_col(col):
                mistake = True

        if self.size in stg.common_sizes:
            if self.size == (9, 9):
                if self.__mistake_3x3s():
                    mistake = True
            # TODO other sizes
        return mistake

    def __mistake_row(self, row: int) -> bool:
        # counter for each 0-9 in the row
        # e.g. cnt[3] will have all 3s in it as a list
        cnt = _get_counter()

        for col in range(self.size[1]):
            curr_val = self.cells[row][col].value
            if curr_val == "":  # skipping empty cells
                continue
            curr_val = int(curr_val)
            cnt[curr_val].append(self.cells[row][col])

        return _check_cnt_duplicity(cnt)

    def __mistake_col(self, col: int) -> bool:
        cnt = _get_counter()

        for row in range(self.size[1]):
            curr_val = self.cells[row][col].value
            if curr_val == "":
                continue
            curr_val = int(curr_val)
            cnt[curr_val].append(self.cells[row][col])

        return _check_cnt_duplicity(cnt)

    def __mistake_3x3s(self) -> bool:
        mistake = False

        for i in range(3):  # relative row
            for j in range(3):  # relative col
                box = []
                for k in range(3):  # move row in relative
                    box.append(self.cells[i * 3 + k][j * 3])
                    box.append(self.cells[i * 3 + k][j * 3 + 1])
                    box.append(self.cells[i * 3 + k][j * 3 + 2])

                cnt = _get_counter()
                for cell in box:
                    if cell.value == "":
                        continue
                    curr_val = int(cell.value)
                    cnt[curr_val].append(cell)

                if _check_cnt_duplicity(cnt):
                    mistake = True

        return mistake


def _get_counter() -> list[list[Cell]]:
    cnt = []
    for i in range(10):
        cnt.append([])

    return cnt


def _give_error(cells: list[Cell]) -> None:
    # call error on top of the cells in the list
    for cell in cells:
        cell.error()


def _check_cnt_duplicity(cnt: list[list[Cell]]) -> bool:
    duplicity = False
    for i in range(10):
        if len(cnt[i]) > 1:  # at least 2
            duplicity = True
            _give_error(cnt[i])

    return duplicity
