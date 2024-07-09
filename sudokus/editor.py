import settings as stg
from sudokus.sudoku import Sudoku

import string


class Editor(Sudoku):
    """
    Special case of sudoku - has extra only export function,
    couldn't do the loop it's an ongoing while.
    """
    def __init__(self, font, surface, size=(9, 9)):
        super().__init__(font, surface, "", size)

    def export(self):
        filepath = stg.prefix + self.name + stg.suffix
        with open(filepath, "w") as file:
            file.write(str(self.size[0]) + "," + str(self.size[1]) + "\n")
            file.write(self.__export_cells())
            file.write(self.description)

    def set_name(self, name: string) -> None:
        self.name = name

    def set_description(self, description: string) -> None:
        self.description = description

    def __export_cells(self) -> string:
        exported = ""
        for row in self.cells:
            row_export = ""
            for i, cell in enumerate(row):
                row_export += cell.value + "," if i != self.size[1] - 1 else cell.value
            exported += row_export + "\n"
        return exported
