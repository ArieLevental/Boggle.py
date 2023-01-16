from boggle_board_randomizer import randomize_board
import pprint
import time

PATH = "boggle_dict.txt"


def timeit(f):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        return_value = f(*args, **kwargs)
        end_time = time.time()
        print(f'Execution Time: {end_time - start_time}')
        return return_value

    return wrapper


# @timeit
def words_file_to_set():
    with open(PATH, 'r') as f:
        words_to_set = set(line.strip() for line in f.readlines())
    return words_to_set


@timeit
def get_words_prefix_set(words):
    # words_to_set = set(words)
    words_prefix_set = dict()
    for word in words:
        for i in range(1, len(word)):
            part_wrd = word[:i+1]
            if part_wrd not in words_prefix_set:
                words_prefix_set[part_wrd] = None
    return words_prefix_set


# print(words_file_to_set())
# print(get_words_prefix_set())
# game_words = words_file_to_set
words_set = words_file_to_set()
prefix = get_words_prefix_set(words_set)

# for word in prefix:
#     if len(word) == 1:
#         print(word, end=" ")

@timeit
def bs():
    with open(PATH) as f:
        set_test2 = set()
        set_test = set()
        # lines = [line for line in f]
        for line in f:
            # print(len(line))
            line.strip()
            set_test2.add(line)
            for i in range(len(line)):
                set_test.add(line[:i+1])
    return set_test, set_test2

# bs()
# print(bs())

# print("ABOMINABLENESS" in prefix)
