from copy import deepcopy
from trie import PrefixTree
import sys

def build_lexicon():
    print("Building Lexicon...")
    trie = PrefixTree()
    path = '../resources/words_long.txt'  # might need to change
    with open(path) as f:
        for i, l in enumerate(f):
            pass
    file_length = i + 1
    toolbar_width = 20
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))
    with open(path, 'r') as file:
        interval = file_length // toolbar_width
        counter = 1
        for line in file:
            if counter % interval == 0:
                sys.stdout.write("-")
                sys.stdout.flush()
            line = line.lower()
            line = line[:-1]  # remove newline character from each line
            trie.add(line)
            counter += 1
    sys.stdout.write("\n")
    return trie

def find_all_words(lexicon, letter_list, word=[], valid_words=[], first_time=False):
    if first_time:
        sys.stdout.write("[%s]" % (" " * len(letter_list)))
        sys.stdout.flush()
        sys.stdout.write("\b" * (len(letter_list)+1))
    for letter in letter_list:
        word.append(letter)
        if lexicon.is_valid_word("".join(word)):
            if "".join(word) not in valid_words:
                valid_words.append("".join(word))
        if lexicon.is_valid_prefix("".join(word)):
            newlist = deepcopy(letter_list)
            newlist.remove(letter)
            valid_words = find_all_words(lexicon, newlist, word, valid_words)
        word.pop()
        if first_time:
            sys.stdout.write("-")
            sys.stdout.flush()
    valid_words.sort(key=len, reverse=True)
    if first_time:
        print("\n")
    return valid_words


def find_all_words_force_positions(lexicon, letter_list, forced, min_length, max_length, word=[], valid_words=None):
    if not valid_words:
        valid_words = list()
    for letter in letter_list:
        flag = True
        if len(word) not in forced:
            word.append(letter)
        else:
            word.append(forced[len(word)])
            flag = False
        if lexicon.is_valid_word("".join(word)):
            if "".join(word) not in valid_words:
                if len(word) >= min_length and len(word) <= max_length:
                    valid_words.append("".join(word))
        if lexicon.is_valid_prefix("".join(word)):
            newlist = deepcopy(letter_list)
            if flag:
                newlist.remove(letter)
            valid_words = find_all_words_force_positions(
                lexicon, newlist, forced, min_length, max_length, word, valid_words)
        word.pop()
    valid_words.sort(key=len, reverse=True)
    return valid_words


def build_longest_word(lexicon, letter_list, word=[], longest_word=[]):
    for letter in letter_list:
        word.append(letter)
        if lexicon.is_valid_word("".join(word)):
            if len(word) > len(longest_word):
                longest_word = deepcopy(word)
        if lexicon.is_valid_prefix("".join(word)):
            newlist = deepcopy(letter_list)
            newlist.remove(letter)
            longest_word = build_longest_word(
                lexicon, newlist, word, longest_word)
        word.pop()
    return longest_word


def print_grid(grid):
    for x in grid:
        string = ""
        for y in x:
            string += y + " "
        print(string)
    print("\n")


def trim_grid(grid):
    rows = len(grid)
    grid = deepcopy(grid)
    for x in range(1, rows + 1):
        flag = True
        for col in grid[rows - x]:
            if col != "_":
                flag = False
                break
        if flag:
            del grid[rows - x]

    rez = [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]
    rows = len(rez)
    for x in range(1, rows + 1):
        flag = True
        for col in rez[rows - x]:
            if col != "_":
                flag = False
                break
        if flag:
            del rez[rows - x]
    g = [[rez[j][i] for j in range(len(rez))] for i in range(len(rez[0]))]
    for x in range(0, len(g)):
        for y in range(0, len(g[x])):
            if g[x][y] == "_":
                g[x][y] = " "
    return g
