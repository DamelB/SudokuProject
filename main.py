import settings as stg

from windows.game import Game
from windows.menu import Menu
from windows.window import print_message

import pygame as pg
import glob
import string


def main():
    """
    Main initiates pygame requirements and cycles through states.

    States: 0 - menu, 1 - play from file, 2 - editor
    Once **X** quit button was called the returned state should be -1.

    :return: nothing
    """
    surface = pg.display.set_mode(stg.res)  # surface of window
    pg.display.set_caption("Sudoku game")
    pg.font.init()

    state = 0
    while state >= 0:
        if state == 0:
            state = Menu(surface).pick_option()
        elif state == 1:
            print_message(surface, "CHECK CONSOLE")
            file = _get_file_from_input(glob.glob("files/*.sdk"))
            state = Game(surface, False, file).loop() if file else 0
        elif state == 2:
            state = Game(surface, True).loop()


def _get_file_from_input(filepaths: list) -> string:
    """
    Lets user pick from all given files a particular one in the console.

    :param filepaths: list of all filepaths
    :return: selected filename
    """
    files = [file[len(stg.prefix):-len(stg.suffix)] for file in filepaths]  # remove prefix and ".sdk"

    # table of prints
    print("SUDOKU:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")

    invalid_number = True
    while invalid_number:  # wait for a valid in range number
        i = input("Choose number of a sudoku you want to play: ")
        try:
            i = int(i) - 1  # shift back
        except ValueError:
            print("Not a number. Try again.")
            continue

        if i < 0 or i >= len(files):
            print("Number out of range. Try again.")
            continue
        return files[i]


if __name__ == "__main__":
    main()
