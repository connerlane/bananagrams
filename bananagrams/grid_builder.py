from time import time
from helpers import find_all_words, print_grid, trim_grid, find_all_words_force_positions, build_lexicon
from copy import deepcopy
import re
from random import shuffle


def solution_found(grid):
    print("Solution Found!\n")
    grid = trim_grid(grid)
    print_grid(grid)
    exit()



def _build_down(lexicon, grid, grid_len, letter_list, best_grid, best_grid_len, anchor_x, anchor_y):
    true_anchor_x = anchor_x
    for z in range(0, len(letter_list)):
        anchor_x = true_anchor_x - z
        restricted = dict()
        max_length = 0
        i = 0
        if grid[anchor_x - 1][anchor_y] == "_":
            while i < len(letter_list) + len(restricted):
                if i == z:
                    restricted[i] = grid[anchor_x + i][anchor_y]
                    i += 1
                    continue
                elif grid[anchor_x + i][anchor_y] != '_':
                    if grid[anchor_x + i + 1][anchor_y] == "_":
                        restricted[i] = grid[anchor_x + i][anchor_y]
                    else:
                        max_length -= 1
                        break

                elif grid[anchor_x + i][anchor_y - 1] != "_" or grid[anchor_x + i][anchor_y + 1] != "_":
                    break
                max_length += 1
                i += 1
            words = [list(i) for i in find_all_words_force_positions(
                lexicon, letter_list, restricted, z + 1, max_length + len(restricted))]
            for word in words:
                new_grid_len = grid_len
                grid_copy = deepcopy(grid)
                letters_copy = deepcopy(letter_list)
                for q in range(0, len(word)):
                    grid_copy[anchor_x + q][anchor_y] = word[q]
                    if q not in restricted:
                        letters_copy.remove(str(word[q]))
                num_tiles_used = len(letter_list) - len(letters_copy)
                if num_tiles_used > 0:
                    new_grid_len += num_tiles_used
                    # print(letters_copy)
                    # print(new_grid_len)
                    print_grid(grid_copy)
                    return _build(lexicon, grid_copy, new_grid_len, letters_copy, best_grid, best_grid_len)
    return best_grid


def _build_sideways(lexicon, grid, grid_len, letter_list, best_grid, best_grid_len, anchor_x, anchor_y):
    true_anchor_y = anchor_y
    for z in range(0, len(letter_list)):
        anchor_y = true_anchor_y - z
        restricted = dict()
        max_length = 0
        i = 0
        if grid[anchor_x][anchor_y - 1] == "_":
            while i < len(letter_list) + len(restricted):

                if i == z:
                    restricted[i] = grid[anchor_x][anchor_y + i]
                    i += 1
                    continue
                elif grid[anchor_x][anchor_y + i] != '_':
                    if grid[anchor_x][anchor_y + i + 1] == "_":
                        restricted[i] = grid[anchor_x][anchor_y + i]
                    else:
                        max_length -= 1
                        break

                elif grid[anchor_x - 1][anchor_y + i] != "_" or grid[anchor_x + 1][anchor_y + i] != "_":
                    break
                max_length += 1
                i += 1
            words = [list(i) for i in find_all_words_force_positions(
                lexicon, letter_list, restricted, z + 1, max_length + len(restricted))]
            for word in words:
                new_grid_len = grid_len
                grid_copy = deepcopy(grid)
                letters_copy = deepcopy(letter_list)
                for q in range(0, len(word)):
                    grid_copy[anchor_x][anchor_y + q] = word[q]
                    if q not in restricted:
                        letters_copy.remove(str(word[q]))
                num_tiles_used = len(letter_list) - len(letters_copy)
                if num_tiles_used > 0:
                    new_grid_len += num_tiles_used
                    # print(letters_copy)
                    # print(new_grid_len)
                    print_grid(grid_copy)
                    return _build(lexicon, grid_copy, new_grid_len, letters_copy, best_grid, best_grid_len)
    return best_grid


def _build(lexicon, grid, grid_len, letter_list, best_grid, best_grid_len):
    if grid_len > best_grid_len[0]:
        best_grid = deepcopy(grid)
        best_grid_len[0] = grid_len
        if len(letter_list) == 0:
            solution_found(grid)

    for x in range(0, len(grid)):
        for y in range(0, len(grid)):
            if grid[x][y] != "_":
                best_grid_down = []
                best_grid_sideways = []
                if grid[x - 1][y] == "_" and grid[x + 1][y] == "_":
                    best_grid = _build_down(
                        lexicon, grid, grid_len, letter_list, best_grid, best_grid_len, x, y)
                    if len(letter_list) == 0:
                        return best_grid
                if grid[x][y - 1] == "_" and grid[x][y + 1] == "_":
                    best_grid = _build_sideways(
                        lexicon, grid, grid_len, letter_list, best_grid, best_grid_len, x, y)
                    if len(letter_list) == 0:
                        return best_grid

    return best_grid


def build_grid(lexicon, letter_list):
    print("\nFinding all possible starting configurations... \nThis could take a minute...\n")
    shuffle(letter_list)
    start_words = find_all_words(lexicon, letter_list, first_time=True)
    if not start_words:
        print("No words can be made with these tiles at all :(")
        return
    grid = []
    best_grid_len = [0]
    for x in range(0, len(letter_list) * 2 + 1):  # make empty board that is plenty large
        # not sure why i have to make the board this big, but it keeps going out of bounds
        new = ["_"] * (len(letter_list) * 2 + 1)
        grid.append(new)
    best_grid = deepcopy(grid)
    
    for start_word in start_words:
        start_row = start_column = len(letter_list)
        g2 = deepcopy(grid)
        word_array = list(start_word)
        l2 = deepcopy(letter_list)
        grid_len = 0
        for letter in word_array:
            g2[start_row][start_column] = letter
            l2.remove(letter)
            start_column += 1
            grid_len += 1
        best_grid = _build(lexicon, g2, grid_len, l2, best_grid, best_grid_len)
    # print(best_grid_len[0])
    best_grid = trim_grid(best_grid)
    print("\nNot all tiles could be used.")
    print("Here is a solution that uses {} of the {} tiles... \n".format(
        best_grid_len[0], len(letter_list)))
    print_grid(best_grid)


if __name__ == "__main__":
    start = time()
    lexicon = build_lexicon()
    print("")
    # letters = ['a', 'm', 'd', 'o', 'd', 'x', 'z', 't', 'z', 'q']
    # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    string = str(input(
        "Enter in your list of characters as one word without spaces: ")).strip().lower()  # might have to change for 2.7
    prog = re.compile("^[A-Za-z]+$")
    result = prog.match(string)
    if result:
        letters = list(string)
        build_grid(lexicon, letters)
    else:
        print("Invalid input. Only english letters are accepted")
