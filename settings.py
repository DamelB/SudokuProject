# ALL SETTINGS (USUALLY) REGARDING THE DRAW

# windows - resolution
res = (1450, 1000)
# font installed at the system
font = "Arial"

# the most left top position of the grid
pivot = [50, 50]
# based on 9x9 grid being 900px - FOR 16x16 NEED TO ADJUST
cell_size = 100

# line sizes
thick_size = 6
thin_size = 2
hlight_size = 10
hlight_radius = 5

# colors
black_color = (0, 0, 0)
blue_color = (0, 0, 255)
hlight_color = (0, 153, 255)
error_color = (255, 181, 107)

# common sudokus grid sizes
common_sizes = [(9, 9), (16, 16), (6, 6), (8, 8), (4, 4)]

# checks for mistakes
helper = True

# files
prefix = "files\\"  # might be issue with other OS than Windows
suffix = ".sdk"
