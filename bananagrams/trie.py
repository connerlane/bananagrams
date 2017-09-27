class Node:

    def __init__(self, character, end_of_word=False):
        self.character = character
        self.end_of_word = False
        self.children = dict()

    def add_child(self, child):
        self.children[child] = None

    def __hash__(self):
        return hash((self.character))


class PrefixTree:
    def __init__(self):
        self.tree = Node("", None)  # top level string is empty

    def add(self, word):
        word_list = list(word)
        level = self.tree
        x = 0
        while x < len(word_list):
            if word_list[x] not in level.children:
                for i in range(x, len(word_list)):
                    level.children[word_list[i]] = Node(word_list[i], level)
                    level = level.children[word_list[i]]
                level.end_of_word = True
                return
            level = level.children[word_list[x]]
            x += 1
        level_pointer = level
        level_pointer.end_of_word = True

    def is_valid_prefix(self, prefix):
        if prefix == "":
            return True
        word_list = list(prefix)
        level = self.tree
        x = 0
        while x < len(word_list):
            if word_list[x] not in level.children:
                return False
            level = level.children[word_list[x]]
            x += 1
        level_pointer = level
        return True

    def is_valid_word(self, word):
        word_list = list(word)
        level = self.tree
        x = 0
        while x < len(word_list):
            if word_list[x] not in level.children:
                return False
            level = level.children[word_list[x]]
            x += 1
        level_pointer = level
        if level_pointer.end_of_word == True:
            return True
        return False
