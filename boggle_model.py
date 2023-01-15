from boggle_board_randomizer import randomize_board, LETTERS

PATH_TO_WORD_BANK = 'boggle_dict.txt'
INITIAL_SCORE = 0
SCORE_POW_MULTIPLIER = 2
INITIAL_GAME_BOARD = [['P', 'L', 'A', 'Y'],
                      ['T', 'H', 'I', 'S'],
                      ['W', 'O', 'R', 'D'],
                      ['G', 'A', 'M', 'E'],
                      ]


################### MOVE TO IMPORT OR STATIC METHODS ##################
def generate_words_dict_from_file():
    with open(PATH_TO_WORD_BANK, 'r') as f:
        words_to_set = set(line.strip() for line in f.readlines())
    return words_to_set


def generate_possible_moves_dict(coordinates_list):
    possible_moves_dict = dict()
    left_step = -1
    right_step = 2

    # each coordiante will recieve a key with all possible moves in a list as value
    for coord in coordinates_list:
        possible_moves_dict[coord] = list()

        # check for range of legal moves around the current cell and add it to the dict as a tuple
        for row_delta in range(left_step, right_step):
            for col_delta in range(left_step, right_step):
                res_cell = (coord[0] + row_delta, coord[1] + col_delta)
                # ignore coordinates that aren't in coords_set or equal to checked cell
                if res_cell in coordinates_list and res_cell != coord:
                    # insert into the with coord as key and all possible move in a list as value
                    possible_moves_dict[coord].append(res_cell)

    return possible_moves_dict


def generate_board_coords(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[i]))]


################### MOVE TO IMPORT OR STATIC METHODS ##################
# TODO DELETE THIS

class BoggleBoard:
    """

    """

    def __init__(self):
        self.__board = INITIAL_GAME_BOARD
        self.__board_coords = generate_board_coords(self.__board)
        self.__possible_moves_dict = generate_possible_moves_dict(self.__board_coords)
        self.__words_set = generate_words_dict_from_file()
        self.__current_path = list()
        self.__current_word = str()
        self.__found_words = list()  # of tuples: PATH, WORD
        self.__score = INITIAL_SCORE

    def path_is_valid(self, path):
        # if not path: # current path is empty, and thus valid
        #     return True
        if len(set(path)) != len(path):
            return False
        # iterating through each step in path
        for step in range(len(path) - 1):
            # for each coord, check if the next one is in its possible moves
            if path[step + 1] not in self.__possible_moves_dict[path[step]]:
                return False
        return True

    def undo_last_step(self):  # for undo button
        if self.__current_path:
            popped_coord = self.__current_path.pop()
            self.__current_word = self.__current_word[:-1]
            return popped_coord
        return None  # the path was empty, no word, do nothing

    def clear_current_word(self):  # clear entire current word and path
        self.__current_path = list()
        self.__current_word = str()

    def reset_board(self):  # for reset button, the whole game
        self.__score = INITIAL_SCORE
        self.__found_words = list()
        self.clear_current_word()
        self._reroll_board()
        # something else?

    def _update_found_words(self):  # update list of found words
        # add current path and current word
        # reset them
        self.__found_words.append((self.__current_path[:], self.__current_word))
        self.clear_current_word()

    def get_found_words(self):
        return [path_word_pair[1] for path_word_pair in self.__found_words]

    def _update_current_word(self, char):  # update the currently constructed word
        self.__current_word += char

    def _get_char_from_coord(self, coord):
        return self.__board[coord[0]][coord[1]]

    def update_current_path(self, coord):
        self.__current_path.append(coord)
        new_char = self._get_char_from_coord(coord)
        self._update_current_word(new_char)

    def get_current_word(self):  # get the currently constructed word
        return self.__current_word

    def _update_score(self):  # update score of current game
        self.__score += (len(self.__current_path) ** SCORE_POW_MULTIPLIER)

    def get_score(self):  # get the score of current game
        return self.__score

    def _reroll_board(self):  # re-roll and change to another rand-board
        self.__board = randomize_board(LETTERS)

    def _repeated_word(self):  # if this word with this path was found
        for path_word_pairs in self.__found_words:
            if path_word_pairs[1] == self.__current_word:
                return True
        return False

    def submit_word(self):  # try and submit a word, if it is new and valid, return True, False otherwise
        if self.__current_word in self.__words_set and not self._repeated_word():
            word = self.__current_word
            self._update_score()
            self._update_found_words()
            return word
        return None

    def get_chars_list(self):
        return [char for row in self.__board for char in row]

    def get_board_coords(self):
        return self.__board_coords[:]

    def get_current_path(self):
        return self.__current_path[:]
