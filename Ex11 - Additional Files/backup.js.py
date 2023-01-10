from typing import List, Tuple, Iterable, Optional, Set
import time
from pprint import pprint
from boggle_board_randomizer import randomize_board as random_board, LETTERS
import copy

Board = List[List[str]]
Path = List[Tuple[int, int]]

CUTOFF_SIZE = 6
SHORT_WORDS = "short_words"


def timeit(f):
    def func(*args, **kwargs):
        s = time.time()
        a = f(*args, **kwargs)
        e = time.time()
        print(e - s)
        return a

    return func


def board_coordinates(board):
    """
    generates a set of all the coordinates on the board
    returns a set of tuples
    """
    cells_coords_set = list()
    for i in range(len(board)):
        for j in range(len(board[i])):
            cells_coords_set.append((i, j))
    return cells_coords_set


# print(board_coordinates(random_board(LETTERS)))


def possible_moves(coords_lst: List):
    """
    generates a dictionary of all generally possible moves from each coord in
    board
    :param: full coordinates set with all coordinates in board
    :return: returns dictionary of Tuple: List[Tuple] format
    """
    possible_dict = dict()
    # each coordiante will recieve a key with all possible move in a list as value
    for coordinate in coords_lst:
        possible_dict[coordinate] = list()
        # check for viable range around the current cell
        for row_delta in range(-1, 2):
            for col_delta in range(-1, 2):
                res_cell = (coordinate[0] + row_delta, coordinate[1] + col_delta)
                # ignore coordinate that isn't in coords_set or equal to checked cell
                if res_cell in coords_lst and res_cell != coordinate:
                    # insert into the with coord as key and all possible move in a list as value
                    possible_dict[coordinate].append(res_cell)

    return possible_dict


def get_word_from_path(board, path):
    """

    :param board:
    :param path:
    :return:
    """
    result_word = ""
    for coord in path:
        # TODO add constans in all ints appearing out of nowwhere in functions
        result_word += board[coord[0]][coord[1]]
    return result_word


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    :param board:
    :param path:
    :param words:
    :return:
    """
    # if one of the coords is duplicated, return None
    if len(set(path)) != len(path):
        return

    # initialise coords_set and possible_moves_dict
    coords_set = board_coordinates(board)
    possible_moves_dict = possible_moves(coords_set)
    for index in range(len(path)):
        # if one of the coords is not on the board, return None
        if path[index] not in coords_set:
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
    :param n:
    :param board:
    :param words:
    :return:
    """
    available_coords = board_coordinates(board)
    possible_moves_dict = possible_moves(available_coords)

    final_list = []
    for coord in available_coords[:]:
        available_coords.remove(coord)
        final_list.extend(find_length_n_paths_helper(n, board, words, possible_moves_dict,
                                                     coord, available_coords, [coord], list()))
        available_coords.append(coord)
    for lstlst in final_list:
        print(get_word_from_path(board, lstlst))
    return final_list


def find_length_n_paths_helper(n, board, words, possible_moves_dict, coord, available_coords: List, cur_path: Path,
                               all_paths: List[Path]) -> Optional[List[Path]]:
    if len(cur_path) == n:
        if get_word_from_path(board, cur_path) in words:
            all_paths.append(cur_path[:])
        return

    for move in possible_moves_dict[coord]:
        if move not in available_coords[:]:
            continue
        else:
            copied_coords = copy.deepcopy(available_coords)
            copied_coords.remove(move)
            cur_path.append(move)
            find_length_n_paths_helper(n, board, words, possible_moves_dict, move, available_coords, cur_path,
                                       all_paths)
            # available_coords.append(move)
            # always path to remove is always the last element so pop() is O(1) and more efficent
            cur_path.pop()
    return all_paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass


def valid_words_for_game():
    with open('boggle_dict.txt', 'r') as f:
        words_set = set(line.strip() for line in f.readlines())
    return words_set


# def valid_words_for_game():
#     words_dict = {SHORT_WORDS: set()}
#
#     with open('boggle_dict.txt', 'r') as f:
#         for line in f.readlines():
#             line_s = line.strip()
#             if len(line_s) < CUTOFF_SIZE:
#                 words_dict[SHORT_WORDS].add(line_s)
#                 continue
#             line_sliced = line_s[:CUTOFF_SIZE]
#             if line_sliced in words_dict:
#                 words_dict[line_sliced].add(line_s)
#             else:
#                 words_dict[line_sliced] = set()
#                 words_dict[line_sliced].add(line_s)
#
#     return words_dict
#
# print(valid_words_for_game()[SHORT_WORDS])
# print(valid_words_for_game())

# print(valid_words_for_game())
# print(valid_words_for_game()['three_letter_words'])

# print(random_board(boggle_board_randomizer.LETTERS))
# for word in valid_words_for_game():
#     if len(word) == 12:
#         print(word)

boardd = [['A', 'B', 'C', 'D'],
          ['P', 'O', 'N', 'E'],
          ['K', 'L', 'M', 'F'],
          ['J', 'I', 'H', 'G']]
rand = random_board(LETTERS)
pprint(rand)
# print(valid_words_for_game()["ABCD"])
# print(find_length_n_paths(16, random_board(), valid_words_for_game()))
print(find_length_n_paths(6, rand, valid_words_for_game()))

# regular check
# word = get_word_from_path(board, cur_path)
# if n < 4:
#     # TODO "SHORT WORDS"
#     if word in words['three_letter_words']:
#         all_paths.append(cur_path)
# else:
#     word_start = word[:4]
#     if word_start in words and word in words[word_start]:
#         all_paths.append(cur_path)
#     return all_paths
#
# for move in possible_moves_dict[coord]:
#     if move not in available_coords:
#         continue
#     available_coords.remove(move)
#     cur_path.append(move)
#     find_length_n_paths_helper(n, board, words, possible_moves_dict, move, available_coords, cur_path, all_paths)
#     available_coords.add(move)
#     # always path to remove is always the last element so pop() is O(1) and more efficent
#     cur_path.pop()
# return all_paths


### TEST BOARD COORDS AND POSSIBLE MOVES###
# test_board = [['0' for i in range(4)] for j in range(4)]
# print(test_board)
# coords = board_coordinates(test_board)
# print(coords)
# moves = possible_moves(coords)
# print(moves)
# print(moves[(1,1)])
# assert len(possible_moves(board[3][3]) == 3
#####

# TESTS
# test_board = [[f'{i + j}' for i in range(4)] for j in range(4)]
# pprint(test_board)
# invalid_path_1 = [(0, 0), (0, 0), (5, 0)]
# invalid_path_2 = [(-1, 0), (0, 0), (0, 2)]
# print(get_word_from_path(test_board, [(1, 1), (2, 1), (3, 1)]))
# print(is_valid_path(test_board, invalid_path_1, []))
# print(is_valid_path(test_board, invalid_path_2, []))
