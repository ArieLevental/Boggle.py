#################################################################
# FILE : ex11_utils.py
# WRITERS : Arie Levental , Arie_Levental , 319142055
#           Adir Barak , adir.barak, 207009739
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: This program runs the game of Boggle
# STUDENTS WE DISCUSSED THE EXERCISE WITH: No-one
# WEB PAGES WE USED: Too many to count.
#################################################################
from typing import List, Tuple, Iterable, Optional, Callable, Dict
import time

Board = List[List[str]]
Path = List[Tuple[int, int]]


def timeit(f: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = f(*args, **kwargs)
        end_time = time.time()
        print(f'Execution Time: {end_time - start_time}')
        return return_value

    return wrapper


#############################################################
#                                                           #
#                     main-functions                        #
#                                                           #
#############################################################

def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    Check if a given path on the board is valid. A path is considered valid if:
    1. the path does not contain any duplicated coordinates.
    2. all the coordinates on the path are on the board.
    3. all the moves between coordinates on the path are valid.
    4. the word formed by the letters on the path is in the given words.

    :param board: A 2D list representing the board of the game.
    :param path: A list of coordinates (tuples) representing a path on the board.
    :param words: An iterable collection of words to check the path against.
    :return: The valid word on the path if the path is valid, None otherwise.
    """
    # check 1 (in doc-str)
    if len(set(path)) != len(path):
        return

    # Init needed data
    available_coords, possible_moves_dict = init_partial_data(board)

    # check 3 (in doc-str)
    for step in path:
        if step not in available_coords:
            return
    for step in range(len(path) - 1):
        if path[step + 1] not in possible_moves_dict[path[step]]:
            return

    # gets the word on current path
    word = get_word_from_path(board, path)

    # check 4 (in doc-str)
    if word not in words:
        return

    # if passed all checks
    return word


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all valid paths of length n on the board.
    A path is considered valid if:
    1. the path does not contain any duplicated coordinates.
    2. all the coordinates on the path are on the board.
    3. all the moves between coordinates on the path are valid.
    4. the word formed by the letters on the path is in the given words.

    :param n: The length of the paths to find.
    :param board: A 2D list representing the board of the game.
    :param words: An iterable collection of words to check the paths against.
    :return: A list of valid paths of length n on the board.
    """
    # Init needed data
    available_coords, possible_moves_dict, words, prefix_set = init_data(board, words)
    all_found = list()
    
    # calling to the helper function for each and every coord in board
    for coord in available_coords[:]:
        # remove the current coord to avoid counting it as a possible move
        available_coords.remove(coord)
        find_length_n_paths_helper(board, n, coord, available_coords, [coord], all_found,
                                   possible_moves_dict, words, prefix_set)
        # return the coord to preserve the data integrity
        available_coords.append(coord)

    return all_found


def find_length_n_paths_helper(board, n, coord, available_coords, cur_path, all_found,
                               possible_moves_dict, word_set, prefix_set):
    """
    A helper function for find_length_n_paths that recursively finds all valid paths of length n
    on the board starting from a given coordinate.

    :param board: A 2D list representing the board of the game.
    :param n: The length of the paths to find.
    :param coord: The starting coordinate for the path.
    :param available_coords: A set of coordinates that can be used in the path.
    :param cur_path: The current path being built.
    :param all_found: A list to store all valid paths found.
    :param possible_moves_dict: A dictionary containing all possible moves for each coordinate.
    :param word_set: The set of words to check the paths against.
    :param prefix_set: A set containing all the possible word prefixes
    """
    # get word from path
    word = get_word_from_path(board, cur_path)

    # check that current state of word is even possible
    if word not in prefix_set:
        return

    # BASE CASE found valid path with the n length
    if len(cur_path) == n and word in word_set:
        all_found.append(cur_path[:])
        return

    # else, check the next available moves recursivly
    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            # if the move's destination is unavailable, continue
            continue
        # add move to the path, and remove it from the available destinations list
        cur_path.append(move)
        available_coords.remove(move)
        find_length_n_paths_helper(board, n, move, available_coords, cur_path, all_found,
                                   possible_moves_dict, word_set, prefix_set)
        # revert the changes - remove move from path, and red-add it to the available destinations list
        cur_path.pop()
        available_coords.append(move)
    return


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all valid paths of length n that form words in the given words list.
    A path is considered valid if:
    1. the path does not contain any duplicated coordinates.
    2. all the coordinates on the path are on the board.
    3. all the moves between coordinates on the path are valid.
    4. the word formed by the letters on the path has a length of n.
    5. the word formed by the letters on the path is in the given words.

    :param n: The length of the words to find.
    :param board: A 2D list representing the board of the game.
    :param words: An iterable collection of words to check the paths against.
    :return: A list of valid paths of length n that form words in the given words list.
    """
    # Init needed data
    available_coords, possible_moves_dict, words, prefix_set = init_data(board, words)
    all_found = list()

    # calling to the helper function for each and every coord in board
    for coord in available_coords[:]:
        # remove the current coord to avoid counting it as a possible move
        available_coords.remove(coord)
        find_length_n_words_helper(board, n, coord, available_coords, [coord], all_found,
                                   possible_moves_dict, words, prefix_set)
        # return the coord to preserve the data integrity
        available_coords.append(coord)

    return all_found


def find_length_n_words_helper(board, n, coord, available_coords, cur_path, all_found,
                               possible_moves_dict, word_set, prefix_set):
    """
    A helper function for find_length_n_words that recursively finds all valid paths of length n
    that form words in the given words list starting from a given coordinate.

    :param board: A 2D list representing the board of the game.
    :param n: The length of the words to find.
    :param coord: The starting coordinate for the path.
    :param available_coords: A set of coordinates that can be used in the path.
    :param cur_path: The current path being built.
    :param all_found: A list to store all valid paths found.
    :param possible_moves_dict: A dictionary containing all possible moves for each coordinate.
    :param word_set: The set of words to check the paths against.
    :param prefix_set: A set containing all the possible word prefixes
    """
    # get word from path
    word = get_word_from_path(board, cur_path)

    # check that current state of word is even possible
    if word not in prefix_set:
        return

    # BASE CASE found valid word in length n
    if len(word) == n and word in word_set:
        all_found.append(cur_path[:])
        return

    # else, check the next available moves recursivly
    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            # if the move's destination is unavailable, continue
            continue
        # add move to the path, and remove it from the available destinations list
        cur_path.append(move)
        available_coords.remove(move)
        find_length_n_words_helper(board, n, move, available_coords, cur_path, all_found,
                                   possible_moves_dict, word_set, prefix_set)
        # revert the changes - remove move from path, and red-add it to the available destinations list
        cur_path.pop()
        available_coords.append(move)

    return


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Find all valid paths on the board with unique words and return them.
    A path is considered valid if:
    1. the path does not contain any duplicated coordinates.
    2. all the coordinates on the path are on the board.
    3. all the moves between coordinates on the path are valid.
    4. the word formed by the letters on the path is in the given words.

    :param board: A 2D list representing the board of the game.
    :param words: An iterable collection of words to check the paths against.
    :return: A list of valid paths on the board with unique words, each with highest scoring
    """
    # Init needed data
    available_coords, possible_moves_dict, words, prefix_set = init_data(board, words)
    all_found = list()
    words_found = list()
    range_of_possible_path_lens = range(16, 0, -1)

    # iterating through each possible path lengths
    for n in range_of_possible_path_lens:
        # calling to the helper function for each and every coord in board
        for coord in available_coords[:]:
            # remove the current coord to avoid counting it as a possible move
            available_coords.remove(coord)
            max_score_helper(board, n, coord, available_coords, [coord], all_found, words_found,
                             possible_moves_dict, words, prefix_set)
            # return the coord to preserve the data integrity
            available_coords.append(coord)
            
    return all_found


def max_score_helper(board, n, coord, available_coords, cur_path, all_found, words_found,
                     possible_moves_dict, word_set, prefix_set):
    """
    A helper function for max_score_paths that recursively finds all valid paths on the board with unique words starting from a given coordinate.

    :param board: A 2D list representing the board of the game.
    :param n: The length of the paths to find.
    :param coord: The starting coordinate for the path.
    :param available_coords: A set of coordinates that can be used in the path.
    :param cur_path: The current path being built.
    :param all_found: A list to store all valid paths found.
    :param words_found: A list of unique words that have been found so far.
    :param possible_moves_dict: A dictionary containing all possible moves for each coordinate.
    :param word_set: The set of words to check the paths against.
    :param prefix_set: A set containing all the possible word prefixes
    """
    # get word from path
    word = get_word_from_path(board, cur_path)

    # check that current state of word is even possible
    if word not in prefix_set:
        return

    # BASE CASE found valid word, with the highest score, and with the right path length
    if len(cur_path) == n and word in word_set and word not in words_found:
        all_found.append(cur_path[:])
        return words_found.append(word)

    # else, check the next available moves recursivly
    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            # if the move's destination is unavailable, continue
            continue
        # add move to the path, and remove it from the available destinations list
        cur_path.append(move)
        available_coords.remove(move)
        max_score_helper(board, n, move, available_coords, cur_path, all_found, words_found,
                         possible_moves_dict, word_set, prefix_set)
        # revert the changes - remove move from path, and re-add it to the available destinations list
        cur_path.pop()
        available_coords.append(move)
    return


#############################################################
#                                                           #
#                      sub-functions                        #
#                                                           #
#############################################################

def init_data(board: Board, words: Iterable[str]) -> Tuple[List[Tuple[int, int]],
                                                           Dict[Tuple[int, int], List[Tuple[int, int]]], set, set]:
    """
    Initializes and returns data required for the game of Boggle.
    The function returns a tuple containing the following elements:
    1. available_coords: a list of all coordinates of cells on the Boggle board represented as tuple (x, y).
    2. possible_moves_dict: a dictionary of all possible next moves for each coordinate on the board.
    3. words: a set of all words to be searched for on the board
    4. words_prefix: a set of all prefixes of words in the words set

    :param board: 2D list representing the Boggle board
    :param words: Iterable set of words to be searched for on the board
    :return: Tuple of data required for the game of Boggle
    """
    available_coords, possible_moves_dict = init_partial_data(board)
    words = set(words)
    words_prefix = words_prefix_set(words)
    return available_coords, possible_moves_dict, words, words_prefix


def init_partial_data(board: Board):
    """
    Initialize the partial data that is used in multiple functions in the program.
    This includes all the coordinates on the board and the possible moves from each coordinate.

    :param board: 2D list representing the Boggle board
    :return: Tuple of a list and dict, one containing all the coordinates on the board,
    and the other containing the possible moves from each coordinate.
    """
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)
    return available_coords, possible_moves_dict


def board_coordinates(board: Board) -> List[Tuple[int, int]]:
    """
    Returns a list of all coordinates of cells on the Boggle board represented as tuple (x, y).
    The cells are represented as rows, columns of a 2D list and the indexes represent the coordinates of the cell.

    :param board: 2D list representing the Boggle board
    :return: List of tuples, each tuple representing the coordinates of a cell
    """
    return [(i, j) for i in range(len(board)) for j in range(len(board[i]))]


def possible_moves(coordinates_list: List[Tuple[int, int]]) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """
    Returns a dictionary of all possible next moves for each coordinate on the board.

    :param coordinates_list: A list of all the coordinates on the board.
    :return: A dictionary of Tuple[int, int]: List[Tuple[int, int]] format,
             where the key is a coordinate and the value is a list of possible next moves from that coordinate.
    """
    # init needed data
    possible_dict = dict()
    left_step = -1
    right_step = 2

    # each coordiante will recieve a key with all possible moves in a list as value
    for coord in coordinates_list:
        possible_dict[coord] = list()

        # check for range of legal moves around the current cell and add it to the dict as a tuple
        for row_delta in range(left_step, right_step):
            for col_delta in range(left_step, right_step):
                res_cell = (coord[0] + row_delta, coord[1] + col_delta)
                # ignore coordinates that aren't in coords_set or equal to checked cell
                if res_cell in coordinates_list and res_cell != coord:
                    # insert into the with coord as key and all possible move in a list as value
                    possible_dict[coord].append(res_cell)

    return possible_dict


def words_prefix_set(words_set: Iterable[str]) -> set:
    """
    Returns a set of all prefixes of words in the input set.

    :param words_set: Iterable set of words
    :return: set of all prefixes of words in the input set
    """
    res_set = set()

    for word in words_set:
        for i in range(len(word)):
            res_set.add(word[:i + 1])
    return res_set


def get_word_from_path(board: Board, path: Path) -> str:
    """
    Returns the word that corresponds to the path of coordinates on the board

    :param board: 2D list representing the Boggle board
    :param path: List of tuples where each tuple represents the coordinates of a cell that holds a letter/letters
    :return: string representation of the word based on a board
    """
    return "".join(board[x][y] for x, y in path)
