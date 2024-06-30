import settings as stg

from windows.game import Game
from windows.menu import Menu
from windows.window import print_message

import pygame as pg
import glob
import string

def main():
    surface = pg.display.set_mode(stg.res) # surface of window
    pg.display.set_caption("Sudoku game")
    pg.font.init()

    state = 0
    while state >= 0:
        if state == 0: # menu
            state = Menu(surface).pick_option()
        elif state == 1: # play from file
            print_message(surface, "CHECK CONSOLE")
            file = _get_file_from_input(glob.glob("files/*.sdk"))
            state = Game(surface,False, file).loop() if file else 0
        elif state == 2: # creating a new sudokus
            state = Game(surface, True).loop()

# take all files and take their name as sudoku name + let user choose one
def _get_file_from_input(filepaths: list) -> string:
    files = [file[len(stg.prefix):-len(stg.suffix)] for file in filepaths]  # remove prefix and ".sdk"

    # table of prints
    print("SUDOKUS:")
    for id, file in enumerate(files):
        print(f"{id + 1}. {file}")

    invalid_number = True
    while invalid_number:  # wait for a valid in range numnber
        id = input("Choose number of a sudoku you want to play: ")
        try:
            id = int(id) - 1  # shift back
        except ValueError:
            print("Not a number. Try again.")
            continue

        if id < 0 or id >= len(files):
            print("Number out of range. Try again.")
            continue
        return files[id]

if __name__ == "__main__":
    main()