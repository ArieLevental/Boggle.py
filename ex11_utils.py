from typing import List, Tuple, Iterable, Optional, Callable, Dict
from boggle_board_randomizer import randomize_board as random_board, LETTERS
import time

Board = List[List[str]]
Path = List[Tuple[int, int]]

WORDS_PREFIX = 6
SHORT_WORDS = "short_words"


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
    Given a board, a path and a set of valid words, this function checks whether the path is a valid path on the board,
    and that the word formed by the path is valid, if both conditions are met it will return the word formed by the path
    ,otherwise it returns None.

    :param board: 2D list representing the Boggle board.
    :param path: list of tuples representing a sequence of coordinates on the board.
    :param words: An iterable of strings representing the valid words for the game.
    :return: The word formed by the path if the path is valid and the word is valid, Otherwise None.
    """
    # if one of the coords is duplicated, return None
    if len(set(path)) != len(path):
        return

    # initialize coords_set and possible_moves_dict
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)

    # iterating through each step in path
    for step in range(len(path) - 1):  # TODO minus 1 right?
        # if one of the coords is not on the board, return None
        if path[step] not in available_coords:
            return
        # for each coord, check if the next one is in its possible moves
        if path[step + 1] not in possible_moves_dict[path[step]]:
            return
    # gets the word on path
    word = get_word_from_path(board, path)
    # checks for a valid word
    if word not in words:
        return

    return word


# @timeit
def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    :param n: length of wanted path to be returned if path is a viable word
    :param board: a board of Boggle
    :param words: an iterable of words to be considered legal for this game
    :return: a list of paths with the length of n for legal words
    """
    return find_length_parent(n, board, words, find_length_n_paths_helper)


def find_length_n_paths_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                               all_paths: List[Path]) -> None:
    """
    Given the current state of the game, this function checks for all possible paths of length `n` starting from
    coordinate `coord` that are valid words and appends them to `all_paths`.
    It explores the possibilities by recursively calling itself on each possible next move on the board.

    :param n: the desired length of the path
    :param board: a 2D list representing the Boggle board
    :param words: an iterable of words to be considered legal for this game
    :param possible_moves_dict: a dictionary of all possible next moves for each coordinate on the board
    :param coord: the current coordinate that the function is exploring
    :param available_coords: a list of all the coordinates on the board that haven't been used in the current path
    :param cur_path: the current path that is being explored
    :param all_paths: a list of paths with the length of n for legal words
    :return: None
    """
    # if the len is at threshold, check if the word is in the dict
    if len(cur_path) == WORDS_PREFIX:
        if get_word_from_path(board, cur_path) not in words:
            return  # the word is not a key, no word resulting from it exists
    # if we reached length of n for sub-threshold lengths, check the dedicated word bank
    if len(cur_path) < WORDS_PREFIX and len(cur_path) == n:
        if get_word_from_path(board, cur_path) in words[SHORT_WORDS]:
            return all_paths.append(cur_path[:])
    if len(cur_path) >= WORDS_PREFIX:
        # if we are over the threshold length, we compare the prefix of the word
        word_start = get_word_from_path(board, cur_path)[:WORDS_PREFIX]
        # if the word's prefix is not found in the dict, it won't result in a valid word
        if word_start not in words:
            return
        # if we also reached the length of n, check if the word exists in the relevant word bank
        if len(cur_path) == n:
            if get_word_from_path(board, cur_path) in words[word_start]:
                return all_paths.append(cur_path[:])
            return  # the word is not a valid n-length word
    # continue constructing the current path:
    return recursive_search_loop(n, board, words, possible_moves_dict, coord, available_coords, cur_path, all_paths,
                                 find_length_n_paths_helper)


# @timeit
def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    :param n: length of wanted path to be returned if path is a viable word
    :param board: a board of Boggle
    :param words: an iterable of words to be considered legal for this game
    :return: a list of paths with the which contains words with the length of n
    """
    # Loading data
    return find_length_parent(n, board, words, find_length_n_words_helper)


def find_length_n_words_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                               all_paths: List[Path]) -> None:
    """
    Given the board, words, possible moves and the current path, this function recursively check possible path with n length
    and if the word formed by the path is in the words, and it's not already added to all_paths.

    :param n: length of wanted path to be returned if path is a viable word
    :param board: a board of Boggle
    :param words: dict containing possible words separated by prefix, and short words
    :param possible_moves_dict: a dict of all possible moves on the board
    :param coord: current position on the board
    :param available_coords: coordinates that are still available to move to
    :param cur_path: current path that is being built
    :param all_paths: list that contains all the legal paths
    :return: None
    """
    current_word = get_word_from_path(board, cur_path)
    # if the len is at threshold, check if the word is in the dict
    if len(current_word) == WORDS_PREFIX:
        if current_word not in words:
            return  # the word is not a key, no word resulting from it exists
    # if we reached length of n for sub-threshold lengths, check the dedicated word bank
    if len(current_word) < WORDS_PREFIX and len(current_word) == n:
        if current_word in words[SHORT_WORDS]:
            all_paths.append(cur_path[:])
            return
    if len(cur_path) >= WORDS_PREFIX:
        # if we are over the threshold length, we compare the prefix of the word

        word_start = get_word_from_path(board, cur_path)[:WORDS_PREFIX]
        # if the word's prefix is not found in the dict, it won't result in a valid word
        if word_start not in words:
            return
        # if we also reached the length of n, check if the word exists in the relevant word bank
        if len(get_word_from_path(board, cur_path)) == n:
            if get_word_from_path(board, cur_path) in words[word_start]:
                return all_paths.append(cur_path[:])
            return  # the word is not a valid n-length word
    # continue constructing the current path:
    return recursive_search_loop(n, board, words, possible_moves_dict, coord, available_coords, cur_path, all_paths,
                                 find_length_n_words_helper)


# @timeit
def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    Given a board and a set of valid words, this function finds all legal paths on the board that forms valid words,
    where the length of the path is the maximum possible. The function returns a dictionary, where the key is the valid word
    formed by the path, and the value is the path itself represented as a list of tuples.

    :param board: 2D list representing the Boggle board.
    :param words: An iterable of strings representing the valid words for the game.
    :return: A dictionary of string : list of tuples.
    """
    available_coords, possible_moves_dict, words = init_data(board, words)
    # List of legal paths with length of n to be returned
    # checking for possible paths for each board coordinate as a starting point
    final_dict = dict()
    for n in range(16, 0, -1):
        for coord in available_coords[:]:
            search_loop(n, board, words, possible_moves_dict, coord, available_coords, final_dict,
                        max_score_paths_helper)
    return list(final_dict.values())


def max_score_paths_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                           final_dict: Dict[str, Path]) -> None:
    """
    This function will search for all paths of length n on the board, starting from given coord and using
    possible_moves_dict to navigate.
    If a path is a valid word, it will be added to the final_dict.
    If a path is of length n and not a valid word, it will be ignored.
    If a path is longer than n and not a valid word, the search will be stopped for that path.
    This function will be called recursively and will return None

    :return: None, the final_dict will be updated within the function.
    """
    # if the len is at threshold, check if the word is in the dict
    current_word = get_word_from_path(board, cur_path)
    if len(current_word) == WORDS_PREFIX:
        if current_word not in words:
            return  # the word is not a key, no word resulting from it exists
    # if we reached length of n for sub-threshold lengths, check the dedicated word bank
    if len(current_word) < WORDS_PREFIX and len(current_word) == n:
        # if current word is already in dict, we have a better score path and no need for further actions
        if current_word in final_dict:
            return
        if current_word in words[SHORT_WORDS]:
            final_dict[current_word] = cur_path[:]
            return  # the word is a valid sub-threshold word
    if len(current_word) >= WORDS_PREFIX:
        # print(cur_path)
        current_word = get_word_from_path(board, cur_path)
        word_start = current_word[:WORDS_PREFIX]
        # if the word's prefix is not found in the dict, it won't result in a valid word
        if word_start not in words:
            return
        # if we also reached the length of n, check if the word exists in the relevant word bank
        if len(current_word) == n:
            # if current word is already in dict, we have a better score path and no need for further actions
            if current_word in final_dict:
                return
            word_start = current_word[:WORDS_PREFIX]
            if current_word in words[word_start]:
                final_dict[current_word] = cur_path[:]
                return
            return  # the word is not a valid n-length word
    # continue constructing the current path:
    return recursive_search_loop(n, board, words, possible_moves_dict, coord, available_coords, cur_path, final_dict,
                                 max_score_paths_helper)

#############################################################
#                                                           #
#                     data functions                        #
#                                                           #
#############################################################

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


def get_word_from_path(board: Board, path: Path) -> str:
    """
    Returns the word that corresponds to the path of coordinates on the board

    :param board: 2D list representing the Boggle board
    :param path: List of tuples where each tuple represents the coordinates of a cell that composes the word
    :return: string representation of the word
    """
    return "".join(board[x][y] for x, y in path)


def valid_words_for_game(words_iterable):
    """
    This function creates a special dict from given bank of words.
    The dict keys are prefix of given words, with a constant length.
    Each key will have a set of words that start with the same prefix as value.
    There's a special key:value pair for words that are shorter than prefix length constant.
    This order will come handy while trying to shorten recursive functions runtime.

    :arg words_iterable: a word iterable which containts a bank of words for this game
    :return dict of words, sorted by specific word's prefix, with a special key for short words
    """
    words_dict = {SHORT_WORDS: set()}

    # Opening the words text file and getting the game words
    for word in words_iterable:
        # If current word is shorter than prefix constant, add to short words set
        if len(word) < WORDS_PREFIX:
            words_dict[SHORT_WORDS].add(word)
            continue

        # If current word is equal or longer than prefix:
        word_prefix = word[:WORDS_PREFIX]
        # If prefix key is already existed, add word to word's prefix values
        if word_prefix in words_dict:
            words_dict[word_prefix].add(word)
        # If prefix key doesn't exist, create the word's prefix key and add the word as value as well
        else:
            words_dict[word_prefix] = set()
            words_dict[word_prefix].add(word)
    return words_dict


#############################################################
#                                                           #
#             recursive functions builder                   #
#                                                           #
#############################################################

def init_data(board: Board, words: Iterable[str]):
    """
    This function Initializes the data needed for find_length_n_paths_helper, max_score_paths_helper and max_score_paths functions.
    :param board: 2D list representing the Boggle board
    :param words: an iterable of words to be considered legal for this game
    :return: a tuple of
              1. list of all the coordinates on the board.
              2. dictionary of Tuple[int, int]: List[Tuple[int, int]] format,
                 where the key is a coordinate and the value is a list of possible next moves from that coordinate.
              3. dict of words, sorted by specific word's prefix, with a special key for short words
    """
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)
    words = valid_words_for_game(words)
    return available_coords, possible_moves_dict, words


def search_loop(n: int, board: Board, words: Iterable[str], possible_moves_dict, coord: Tuple[int, int],
                available_coords, final_res, helper_func):
    """
    This function serves as a loop for the search functions, it removes the current coord from available_coords and calls the helper_func
    then adds the coord back to available_coords.
    """
    available_coords.remove(coord)
    helper_func(n, board, words, possible_moves_dict, coord,
                available_coords, [coord], final_res)
    available_coords.append(coord)
    return final_res


def find_length_parent(n: int, board: Board, words: Iterable[str], helper_func) -> List[Path]:
    """
    This function finds all legal paths of length n on a Boggle board by calling a helper function
    for each starting coordinate on the board.
    """
    available_coords, possible_moves_dict, words = init_data(board, words)

    # List of legal paths with length of n to be returned
    paths = []
    # checking for possible paths for each board coordinate as a starting point
    for coord in available_coords[:]:
        search_loop(n, board, words, possible_moves_dict, coord, available_coords, paths, helper_func)
    return paths


def recursive_search_loop(n, board, words, possible_moves_dict, coord, available_coords, cur_path, final_res,
                          recursive_func):
    """
    This function is a helper function that is being used by other functions that performs recursive search.
    It looks for legal moves for the given coord and performs the recursive search accordingly.
    And adding the found paths to final_res data structure if the path is legal.
    """
    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            continue
        else:
            available_coords.remove(move)
            cur_path.append(move)
            recursive_func(n, board, words, possible_moves_dict, move, available_coords, cur_path, final_res)
            available_coords.append(move)
            # always path to remove is always the last element so pop() is O(1) and more efficent
            cur_path.pop()
    return final_res


# TODO: REMOVE, ONLY FOR TESTING
def valid_words_for_game_set():
    with open('boggle_dict.txt', 'r') as f:
        words_to_set = set(line.strip() for line in f.readlines())
    return words_to_set


# TESTING ZONE

# BOARDS
# board_AAA = [['A', 'A', 'A', 'A'],
#              ['A', 'A', 'A', 'A'],
#              ['A', 'A', 'A', 'A'],
#              ['A', 'A', 'A', 'A']]
# board_ABC = [['A', 'B', 'C', 'D'],
#              ['P', 'O', 'N', 'E'],
#              ['K', 'L', 'M', 'F'],
#              ['J', 'I', 'H', 'G']]
# board_regular = [['L', 'E', 'T', 'Y'],
#                  ['D', 'E', 'QU', 'N'],
#                  ['W', 'P', 'T', 'E'],
#                  ['A', 'B', 'L', 'P']]
# board_fucked = [['L', 'E', 'T', 'Y'],
#                 ['D', 'Z', 'QU', 'N'],
#                 ['W', 'P', 'T', 'X'],
#                 ['T', 'B', 'L', 'P']]
# board_DOUBLE = [['A', 'B', 'C', 'D'],
#                 ['P', 'OU', 'N', 'IE'],
#                 ['K', 'L', 'M', 'F'],
#                 ['J', 'AE', 'TH', 'AE']]
# board_6on6 = [['A', 'E', 'A', 'N', 'E', 'G'],
#               ['A', 'H', 'S', 'P', 'C', 'O'],
#               ['A', 'S', 'P', 'F', 'F', 'K'],
#               ['O', 'B', 'J', 'O', 'A', 'B'],
#               ['I', 'O', 'T', 'M', 'U', 'C'],
#               ['R', 'Y', 'V', 'D', 'E', 'L']]

# board_random = random_board(LETTERS)
# words_set = valid_words_for_game_set()
# TEST BOARD
# test_board = board_random
# test_words = words_set
failed_board = [['E', 'M', 'AB', 'O'],
                ['IN', 'ON', 'AN', 'M'],
                ['ST', 'R', 'U', 'TH'],
                ['Y', 'ST', 'R', 'W']]

# ADD SPECIFIC WORDS
# test_words["ABCDEF"] = {"ABCDEFGHIJKLMNOP"}  # PREFIX 6 n = 16
# test_words["AAAAAA"] = {"AAAAAAAAAAAAAAAA", "AAAAAAAAAAAAAA", "AAAAAAAAAAAA",
#                         "AAAAAAAAAA", "AAAAAAAA", "AAAA", "AA", "A"}  # PREFIX 6 n = 16, 14, 12, 10, 8, 4, 2, 1
# test_words["FJSSNEG"] = {"FJSSNEGCFOUL"}  # PREFIX 7, n = 12

# PRINTING AREA

# pprint(test_board)

# results = find_length_n_paths(6, test_board, test_words)
# results = find_length_n_words(5, test_board, test_words)
# results = max_score_paths(failed_board, test_words)
#
# print(len(results))
# print(results)

# PRINT PATHS FOUND
# print(results)

# CHECK FOR DUPLICATES
# for index, result in enumerate(results):
#     for res in results[index + 1:]:
#         if res == result:
#             print(f"OH BOY! {res} have a duplicate")

# PRINT WORDS FOUND
# print("************* Words found: *************")
# for res in results:
#     print(get_word_from_path(test_board, res), res)

# PRINT WORDS FROM WORDS BANK WITH SPECIFIC LENGTH
# with open('boggle_dict.txt', 'r') as f:
#     words_set = set(line.strip() for line in f.readlines())
#     for word in words_set:
#         if len(word) == 16:
#             print(word)
