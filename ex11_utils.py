from typing import List, Tuple, Iterable, Optional, Callable, Dict
from boggle_board_randomizer import randomize_board as random_board, LETTERS
from pprint import pprint
import time

Board = List[List[str]]
Path = List[Tuple[int, int]]

WORDS_PREFIX = 6
SHORT_WORDS = "short_words"


# TODO LIST:
#   - use of constants
#   - breaking functions into small pieces
#   - type hints and doco (chatGPT)

def timeit(f: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = f(*args, **kwargs)
        end_time = time.time()
        print(f'Execution Time: {end_time - start_time}')
        return return_value

    return wrapper


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
    # each coordiante will recieve a key with all possible moves in a list as value
    for coord in coordinates_list:
        possible_dict[coord] = list()
        # check for range of legal moves around the current cell and add it to the dict as a tuple
        for row_delta in range(-1, 2):
            for col_delta in range(-1, 2):
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

    # initialise coords_set and possible_moves_dict
    coords_list = board_coordinates(board)
    possible_moves_dict = possible_moves(coords_list)
    for index in range(len(path)):
        # if one of the coords is not on the board, return None
        if path[index] not in coords_list:
            return
        # for each coord, check if the next one is in its possible moves
        if path[index + 1] not in possible_moves_dict[path[index]]:
            return
    #
    word = get_word_from_path(board, path)
    # if the word is not a valid word, return None
    if word not in words:
        return
    # all well, return the word that was described by the path
    return word


@timeit
def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    :param n: length of wanted path to be returned if path is a viable word
    :param board: a board of Boggle
    :param words: an iterable of words to be considered legal for this game
    :return: a list of paths with the length of n for legal words
    """
    # Loading data
    # TODO: EDIT NAMES
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)
    words = valid_words_for_game(words)

    # List of legal paths with length of n to be returned
    paths = []
    # checking for possible paths for each board coordinate as a starting point
    for coord in available_coords[:]:
        available_coords.remove(coord)
        paths.extend(find_length_n_paths_helper(n, board, words, possible_moves_dict, coord, available_coords,
                                                [coord], list()))
        available_coords.append(coord)

    return paths


def find_length_n_paths_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                               all_paths: List[Path]) -> Optional[List[Path]]:
    if len(cur_path) == WORDS_PREFIX:
        if get_word_from_path(board, cur_path) not in words:
            return
    if len(cur_path) < WORDS_PREFIX and len(cur_path) == n:
        if get_word_from_path(board, cur_path) in words[SHORT_WORDS]:
            all_paths.append(cur_path[:])
            return
    if len(cur_path) >= WORDS_PREFIX:
        # print(cur_path)
        word_start = get_word_from_path(board, cur_path)[:WORDS_PREFIX]
        if len(cur_path) == n:
            if get_word_from_path(board, cur_path) in words[word_start]:
                all_paths.append(cur_path[:])
                return
            return
        else:
            if word_start not in words:
                return

    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            continue
        else:
            available_coords.remove(move)
            cur_path.append(move)
            find_length_n_paths_helper(n, board, words, possible_moves_dict, move, available_coords, cur_path,
                                       all_paths)
            available_coords.append(move)
            # always path to remove is always the last element so pop() is O(1) and more efficent
            cur_path.pop()
    return all_paths


@timeit
def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """

    :param n:
    :param board:
    :param words:
    :return:
    """
    # Loading data
    # TODO: EDIT NAMES
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)
    words = valid_words_for_game(words)

    # List of legal paths with length of n to be returned
    paths = []
    # checking for possible paths for each board coordinate as a starting point
    for coord in available_coords[:]:
        available_coords.remove(coord)
        paths.extend(find_length_n_words_helper(n, board, words, possible_moves_dict, coord, available_coords,
                                                [coord], list()))
        available_coords.append(coord)

    # TODO: Remove
    # for lstlst in final_list:
    #     print(get_word_from_path(board, lstlst))
    return paths


def find_length_n_words_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                               all_paths: List[Path]) -> Optional[List[Path]]:
    current_word = get_word_from_path(board, cur_path)
    # print(current_word)
    if len(current_word) == WORDS_PREFIX:
        if current_word not in words:
            return
    if len(current_word) < WORDS_PREFIX and len(current_word) == n:
        if current_word in words[SHORT_WORDS]:
            all_paths.append(cur_path[:])
            return
    if len(current_word) >= WORDS_PREFIX:
        # print(cur_path)
        word_start = current_word[:WORDS_PREFIX]
        if len(current_word) == n:
            if current_word in words[word_start]:
                all_paths.append(cur_path[:])
                return
            return
        else:
            if word_start not in words:
                return

    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            continue
        else:
            available_coords.remove(move)
            cur_path.append(move)
            find_length_n_words_helper(n, board, words, possible_moves_dict, move, available_coords, cur_path,
                                       all_paths)
            available_coords.append(move)
            # always path to remove is always the last element so pop() is O(1) and more efficent
            cur_path.pop()
    return all_paths


@timeit
def max_score_paths(board: Board, words: Iterable[str]) -> Dict[str, Path]:
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)
    words = valid_words_for_game(words)
    # List of legal paths with length of n to be returned
    # checking for possible paths for each board coordinate as a starting point
    final_dict = dict()
    available_coords_copy = available_coords[:]
    for n in range(16, 0, -1):
        for coord in available_coords_copy:
            available_coords.remove(coord)
            max_score_paths_helper(n, board, words, possible_moves_dict, coord, available_coords, [coord], final_dict)
            available_coords.append(coord)
    return final_dict


def max_score_paths_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                           final_dict: Dict[str, Path]) -> Optional[Dict[str, Path]]:
    if len(cur_path) == WORDS_PREFIX:
        if get_word_from_path(board, cur_path) not in words:
            return
    if len(cur_path) < WORDS_PREFIX and len(cur_path) == n:
        current_word = get_word_from_path(board, cur_path)
        # if current word is already in dict, we have a better score path and no need for further actions
        if current_word in final_dict:
            return
        if current_word in words[SHORT_WORDS]:
            final_dict[current_word] = cur_path[:]
            return
    if len(cur_path) >= WORDS_PREFIX:
        # print(cur_path)
        current_word = get_word_from_path(board, cur_path)
        if len(cur_path) == n:
            if current_word in final_dict:
                return
            word_start = current_word[:WORDS_PREFIX]
            if current_word in words[word_start]:
                final_dict[current_word] = cur_path[:]
                return
            return
        else:
            word_start = current_word[:WORDS_PREFIX]
            if word_start not in words:
                return

    for move in possible_moves_dict[coord]:
        if move not in available_coords:
            continue
        else:
            available_coords.remove(move)
            cur_path.append(move)
            max_score_paths_helper(n, board, words, possible_moves_dict, move, available_coords, cur_path, final_dict)
            available_coords.append(move)
            # always path to remove is always the last element so pop() is O(1) and more efficent
            cur_path.pop()
    return final_dict


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


# GET WORDS FROM GIVEN PATH - BACKUP FUNCTION
# def valid_words_for_game(path_to_words_text_file):
#     """
#     This function creates a special dict from given bank of words.
#     The dict keys are prefix of given words, with a constant length.
#     Each key will have a set of words that start with the same prefix as value.
#     There's a special key:value pair for words that are shorter than prefix length constant.
#     This order will come handy while trying to shorten recursive functions runtime.
#
#     :arg path_to_words_text_file: path to a text file which containts a bank of words for this game
#     :return dict of words, sorted by specific word's prefix, with a special key for short words
#     """
#
#     words_dict = {SHORT_WORDS: set()}
#
#     # Opening the words text file and getting the game words
#     with open(path_to_words_text_file, 'r') as f:
#         for possible_word in f.readlines():
#             word = possible_word.strip()
#
#             # If current word is shorter than prefix constant, add to short words set
#             if len(word) < WORDS_PREFIX:
#                 words_dict[SHORT_WORDS].add(word)
#                 continue
#
#             # If current word is equal or longer than prefix:
#             word_prefix = word[:WORDS_PREFIX]
#             # If prefix key is already existed, add word to word's prefix values
#             if word_prefix in words_dict:
#                 words_dict[word_prefix].add(word)
#             # If prefix key isn't existed, create the word's prefix key and add the word as value as well
#             else:
#                 words_dict[word_prefix] = set()
#                 words_dict[word_prefix].add(word)
#
#     return words_dict

def valid_words_for_game_set():
    with open('boggle_dict.txt', 'r') as f:
        words_to_set = set(line.strip() for line in f.readlines())
    return words_to_set


# TESTING ZONE

# BOARDS
board_AAA = [['A', 'A', 'A', 'A'],
             ['A', 'A', 'A', 'A'],
             ['A', 'A', 'A', 'A'],
             ['A', 'A', 'A', 'A']]
board_ABC = [['A', 'B', 'C', 'D'],
             ['P', 'O', 'N', 'E'],
             ['K', 'L', 'M', 'F'],
             ['J', 'I', 'H', 'G']]
board_regular = [['L', 'E', 'T', 'Y'],
                 ['D', 'E', 'QU', 'N'],
                 ['W', 'P', 'T', 'E'],
                 ['A', 'B', 'L', 'P']]
board_fucked = [['L', 'E', 'T', 'Y'],
                ['D', 'Z', 'QU', 'N'],
                ['W', 'P', 'T', 'X'],
                ['T', 'B', 'L', 'P']]
board_DOUBLE = [['A', 'B', 'C', 'D'],
                ['P', 'OU', 'N', 'IE'],
                ['K', 'L', 'M', 'F'],
                ['J', 'AE', 'TH', 'AE']]
board_6on6 = [['A', 'E', 'A', 'N', 'E', 'G'],
              ['A', 'H', 'S', 'P', 'C', 'O'],
              ['A', 'S', 'P', 'F', 'F', 'K'],
              ['O', 'B', 'J', 'O', 'A', 'B'],
              ['I', 'O', 'T', 'M', 'U', 'C'],
              ['R', 'Y', 'V', 'D', 'E', 'L']]
board_random = random_board(LETTERS)
words_set = valid_words_for_game_set()
# TEST BOARD
test_board = board_random
test_words = words_set

# ADD SPECIFIC WORDS
# test_words["ABCDEF"] = {"ABCDEFGHIJKLMNOP"}  # PREFIX 6 n = 16
# test_words["AAAAAA"] = {"AAAAAAAAAAAAAAAA", "AAAAAAAAAAAAAA", "AAAAAAAAAAAA",
#                         "AAAAAAAAAA", "AAAAAAAA", "AAAA", "AA", "A"}  # PREFIX 6 n = 16, 14, 12, 10, 8, 4, 2, 1
# test_words["FJSSNEG"] = {"FJSSNEGCFOUL"}  # PREFIX 7, n = 12

# PRINTING AREA

pprint(test_board)

# results = find_length_n_paths(16, test_board, test_words)
# results = find_length_n_words(4, test_board, test_words)
results = max_score_paths(test_board, test_words)

print(len(results))
print(results)

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

# SET OF WORDS INSTEAD OF DICT
