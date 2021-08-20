import os
import sys
import time
import getopt
import numpy as np
from queue import PriorityQueue, Queue
'''
The basic operation could be determined by counted the number of time for node in reversed(path) 
is iterated through. Thus basic operation would be counted as being the printing of the position 
str((in_r, in_c)) which is called the number of tile moves that occur.
'''

class BoardNode:
    def __init__(self, brd, level, parent=None):
        self.__brd = brd
        self.__level = level
        self.__parent = parent

    def __hash__(self):
        return hash(str(self.__brd))

    def get_board(self):
        return self.__brd

    def get_level(self):
        return self.__level

    def get_parent(self):
        return self.__parent


def solve_bfs(init_brd, goal_brd, max_iter=10000):
    q_max = 10000
    x_axis = [1, 0, -1, 0]
    y_axis = [0, 1, 0, -1]
    goal_brd_list = goal_brd.flatten().tolist()

    path = []
    summary = ""
    level = 0
    visited_nodes = set()

    nodes = Queue(q_max)
    init_node = BoardNode(init_brd.flatten().tolist(), level)
    nodes.put(init_node)

    start_time = time.process_time()
    iter_count = 0
    while nodes.qsize() and iter_count <= max_iter:
        iter_count += 1

        cur_node = nodes.get()
        cur_brd = cur_node.get_board()

        if str(cur_brd) in visited_nodes:
            continue
        visited_nodes.add(str(cur_brd))

        if cur_brd == goal_brd_list:
            elapsed_time = time.process_time() - start_time
            summary = str("BFS took " + str(cur_node.get_level()) + " tile moves and about " +
                      str(int((np.round(elapsed_time, 4)) * 1000)) + " msecs.")
            while cur_node.get_parent():
                path.append(cur_node)
                cur_node = cur_node.get_parent()
            break

        empty_tile = cur_brd.index(0)
        i, j = empty_tile // goal_brd.shape[0], empty_tile % goal_brd.shape[0]

        cur_brd = np.array(cur_brd).reshape(goal_brd.shape[0], goal_brd.shape[0])
        for x, y in zip(x_axis, y_axis):
            new_state = np.array(cur_brd)
            if i + x >= 0 and i + x < goal_brd.shape[0] and j + y >= 0 and j + y < goal_brd.shape[0]:
                new_state[i, j], new_state[i + x, j + y] = new_state[i + x, j + y], new_state[i, j]
                board_node = BoardNode(new_state.flatten().tolist(), cur_node.get_level() + 1, cur_node)
                if str(board_node.get_board()) not in visited_nodes:
                    nodes.put(board_node)

    if iter_count > max_iter:
        print('This board is not solvable')
    return path, summary


# print board
def print_board(board):
    build_board = ""
    n = board.shape[0]
    for r in range(n):
        build_board += "["
        if n > 3 and board[r, 0] <= 9:
            build_board += " "
        for c in range(n):
            if c:
                build_board += " " if board[r, c] > 9 else "  "
            if board[r, c] == 0:
                build_board += str('X')
            else:
                build_board += str(board[r, c])
        build_board += "]\n"
    print(build_board)


# Breadth first search
def bread_first_search(input_brd, goal_brd):
    path, summary = solve_bfs(input_brd, goal_brd)

    if len(path):
        print('INPUT BOARD')
        print_board(input_brd)

        n = goal_brd.shape[0]
        in_idx = input_brd.flatten().tolist().index(0)
        in_r, in_c = in_idx // n, in_idx % n

        for node in reversed(path):
            cur_idx = node.get_board().index(0)
            cur_r, cur_c = cur_idx // n, cur_idx % n

            new_r, new_c = cur_r - in_r, cur_c - in_c
            if new_c == 0 and new_r == -1:
                print('Moved UP    from ' + str((in_r, in_c)) + ' --> ' + str((cur_r, cur_c)))
            elif new_c == 0 and new_r == 1:
                print('Moved DOWN  from ' + str((in_r, in_c)) + ' --> ' + str((cur_r, cur_c)))
            elif new_r == 0 and new_c == 1:
                print('Moved RIGHT from ' + str((in_r, in_c)) + ' --> ' + str((cur_r, cur_c)))
            else:
                print('Moved LEFT  from ' + str((in_r, in_c)) + ' --> ' + str((cur_r, cur_c)))
            in_r, in_c = cur_r, cur_c

        print('\nFINAL BOARD')
        brd = np.array(path[0].get_board()).reshape(n, n)
        print_board(brd)
        print(summary)
        print("****************************************")


# Get inversion count
def get_inversion_count(arr):
    inv_count = 0
    n = len(arr)
    arr = arr.flatten()
    for i in range(n * n - 1):
        for j in range(i + 1, n * n):
            # count pairs(i, j) such that i appears before j, but i > j.
            if arr[j] and arr[i] and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


# find Position of blank from bottom
def find_x_position(input_brd):
    n = len(input_brd)
    # start from bottom-right corner of matrix
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if input_brd[i][j] == 0:
                return n - i


# This function returns true if given instance of N * N puzzle is solvable
def is_solvable(input_brd):
    # Count inversions in the given puzzle
    n = len(input_brd)
    inv_count = get_inversion_count(input_brd)

    # If grid is odd, return true if inversion count is even.
    if n & 1:  # grid is odd
        return not (inv_count & 1)
    else:  # grid is even
        pos = find_x_position(input_brd)
        if pos & 1:
            return not (inv_count & 1)
        else:
            return inv_count & 1


# Read tile board from the input file
def read_tile_puzzle(filename):
    with open(filename, 'r') as file:
        board = []
        for line in file:
            line = line.split()
            for i in range(0, len(line)):
                if line[i] == 'X':
                    line[i] = 0
                else:
                    line[i] = int(line[i])

            board.append(line)
    return board


# Main
def main(argv):
    # Check puzzles folder in the source directory
    if not os.path.exists('puzzles'):
        print('puzzles folder containing tile puzzles does not exit')
        exit(1)

    # Files in the puzzles folder
    folder_list = os.listdir('puzzles')
    if len(folder_list) == 0:
        print('Empty folder')
        exit(1)

    # User selection
    print('Choose the following tile files or exit')
    puzzles_list = []
    for folder in folder_list:
        file_list = os.listdir(os.path.join('puzzles', folder))
        if len(file_list) != 0:
            for file in file_list:
                file = os.path.join(folder, file)
                puzzles_list.append(file)

    # Loop through user input to solve the puzzle
    while True:
        index = 1
        print("\n**********TILE PUZZLE**********")
        print("Available puzzle files:")
        for file in puzzles_list:
            print("%2d. %s" % (index, file))
            index = index + 1

        file_index = int(input("\nEnter file name index or -1 to exit: "))
        if file_index < 0:
            exit(1)

        if file_index <= 0 or file_index > len(puzzles_list):
            print("Invalid selection, try again")
            continue

        file_index = file_index - 1  # file index 0-n
        print("Chosen tile file is %s\n" % puzzles_list[file_index])
        file_name = os.path.join('puzzles', puzzles_list[file_index])
        input_brd = read_tile_puzzle(file_name)

        # Make final goal board
        n = len(input_brd)  # Board size n x n
        error = False
        goal_brd = []
        for i in range(1, n * n, n):
            if n == 2:
                row = [i, i + 1]
            elif n == 3:
                row = [i, i + 1, i + 2]
            elif n == 4:
                row = [i, i + 1, i + 2, i + 3]
            else:
                print("Unsupported input array size")
                error = True
                break
            goal_brd.append(row)

        if error:
            continue

        goal_brd[n - 1][n - 1] = 0
        goal_brd = np.array(goal_brd).reshape(n, n)
        input_brd = np.array(input_brd).reshape(n, n)

        if is_solvable(input_brd):
            bread_first_search(input_brd, goal_brd)
        else:
            print("puzzle unsolvable")


if __name__ == "__main__":
    main(sys.argv[1:])
