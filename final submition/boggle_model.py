#################################################################
# FILE : boggle_model.py
# WRITERS : Arie Levental , Arie_Levental , 319142055
#           Adir Barak , adir.barak, 207009739
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: This program runs the game of Boggle
# STUDENTS WE DISCUSSED THE EXERCISE WITH: No-one
# WEB PAGES WE USED: Too many to count.
#################################################################
from boggle_board_randomizer import randomize_board, LETTERS

PATH_TO_WORD_BANK = 'boggle_dict.txt'
INITIAL_SCORE = 0
SCORE_POW_MULTIPLIER = 2
INITIAL_GAME_BOARD = [['M', 'A', 'D', 'E'],
                      ['~', 'B', 'Y', '~'],
                      ['A', 'R', 'I', 'E'],
                      ['A', 'D', 'I', 'R'],
                      ]


################### MOVE TO IMPORT OR STATIC METHODS ##################
def generate_words_set_from_file():
    """
    Generates a set of words from a file containing a list of words, one word per line.
    The file path is specified by the global variable PATH_TO_WORD_BANK.

    :return: A set of words read from the specified file.
    """
    with open(PATH_TO_WORD_BANK, 'r') as f:
        words_to_set = set(line.strip() for line in f.readlines())
    return words_to_set


def generate_possible_moves_dict(coordinates_list):
    """
    Returns a dictionary of all possible next moves for each coordinate on the board.

    :param coordinates_list: A list of all the coordinates on the board.
    :return: A dictionary of Tuple[int, int]: List[Tuple[int, int]] format,
             where the key is a coordinate and the value is a list of possible next moves from that coordinate.
    """
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
    """
    Given a Boggle board represented as a 2D list, this function returns a list of tuples representing the
    coordinates of all cells on the board. Each tuple (x, y) represents the coordinates of a cell on the board,
    where x is the row number and y is the column number.

    :param board: 2D list representing the Boggle board
    :return: List of tuples, each tuple representing the coordinates of a cell on the board
    """
    return [(i, j) for i in range(len(board)) for j in range(len(board[i]))]


class BoggleBoard:
    """
    A class that represents a Boggle board game. It contains the board, a set of valid words,
    a list of found words, a current word, a current path and a score.
    It also contains methods for handling user input, updating the board and score, and validating words.
    """

    def __init__(self):
        """
        Initializes the Boggle board with an initial game board, coordinates of the board,
        possible moves from each coordinate, a set of valid words from a file, an empty current path,
        an empty current word, an empty list of found words, and an initial score.
        """
        self.__board = INITIAL_GAME_BOARD
        self.__board_coords = generate_board_coords(self.__board)
        self.__possible_moves_dict = generate_possible_moves_dict(self.__board_coords)
        self.__words_set = generate_words_set_from_file()
        self.__current_path = list()
        self.__current_word = str()
        self.__found_words = list()  # of tuples: PATH, WORD
        self.__score = INITIAL_SCORE

    def path_is_valid(self, path):
        """
        Given a path, checks if it is a valid path on the board.
        A path is considered valid if it contains unique coordinates and each next coordinate in the path
        is a valid move from the previous coordinate.

        :param path: A list of coordinates representing a path on the board
        :return: A boolean indicating if the path is valid
        """
        if len(set(path)) != len(path):
            return False
        # iterating through each step in path
        for step in range(len(path) - 1):
            # for each coord, check if the next one is in its possible moves
            if path[step + 1] not in self.__possible_moves_dict[path[step]]:
                return False
        return True

    def undo_last_step(self):
        """
        Removes the last coordinate from the current path and removes the last character from the current word.

        :return: The coordinate that was removed from the current path or None if the path was already empty
        """
        if self.__current_path:
            popped_coord = self.__current_path.pop()
            self.__current_word = self.__current_word[:-1]
            return popped_coord
        return None  # the path was empty, no word, do nothing

    def clear_current_word(self):
        """
        Clears the current path and current word.
        """
        self.__current_path = list()
        self.__current_word = str()

    def reset_board(self):
        """
        Resets the board, score, found words, and current word.
        """
        self.__score = INITIAL_SCORE
        self.__found_words = list()
        self.clear_current_word()
        self._reroll_board()
        # something else?

    def _update_found_words(self):
        """
        This function updates the found words list by appending the current word and path to it.
        It also resets the current word and path.
        """
        # add current path and current word
        # reset them
        self.__found_words.append((self.__current_path[:], self.__current_word))
        self.clear_current_word()

    def get_found_words(self):
        """
        This function returns a list of all the found words.
        """
        return [path_word_pair[1] for path_word_pair in self.__found_words]

    def _update_current_word(self, char):
        """
        This function updates the current word by appending a new character to it.
        :param char: The character to be added to the current word.
        """
        self.__current_word += char

    def _get_char_from_coord(self, coord):
        """
        This function returns the character at the given coordinates on the board.
        :param coord: Tuple containing the row and column coordinates of the character on the board.
        """
        return self.__board[coord[0]][coord[1]]

    def update_current_path(self, coord):
        """
        This function updates the current path by appending a new coordinate to it and adds the corresponding
        character to the current word.
        :param coord: Tuple containing the row and column coordinates of the next cell
        in the path.
        """
        self.__current_path.append(coord)
        new_char = self._get_char_from_coord(coord)
        self._update_current_word(new_char)

    def get_current_word(self):
        """
        This function returns the current word being formed.
        """
        return self.__current_word

    def _update_score(self):
        """
        This function updates the score by adding the length of the current path to the score.
        """
        self.__score += (len(self.__current_path) ** SCORE_POW_MULTIPLIER)

    def get_score(self):
        """
        This function returns the current score.
        """
        return self.__score

    def _reroll_board(self):
        """
        This function re-rolls the board by generating a new random board.
        """
        self.__board = randomize_board(LETTERS)

    def _repeated_word(self):
        """
        This function checks if the current word has already been found.
        """
        for path_word_pairs in self.__found_words:
            if path_word_pairs[1] == self.__current_word:
                return True
        return False

    def submit_word(self):
        """
        This function submits the current word if it is valid.
        It updates the score, found words list and resets the current word and path.
        :return: The word that is submitted or None if the word is invalid.
        """
        if self.__current_word in self.__words_set and not self._repeated_word():
            word = self.__current_word
            self._update_score()
            self._update_found_words()
            return word
        return None

    def get_chars_list(self):
        """
        This function returns a list of all characters in the current game board.
        :return: List of characters in the current game board
        """
        return [char for row in self.__board for char in row]

    def get_board_coords(self):
        """
        This function returns a list of tuples representing the coordinates of all cells on the game board.
        :return: List of tuples representing coordinates of all cells on the game board
        """
        return self.__board_coords[:]

    def get_current_path(self):
        """
        This function returns a list of tuples representing the coordinates of the cells that are currently selected.
        :return: List of tuples representing coordinates of the cells that are currently selected
        """
        return self.__current_path[:]
