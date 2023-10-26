import time
from random import randint

import numpy as np


# TODO: replace with 'struct' whose elements are accessed by x, y
board_size = (12, 18)

characters = np.array(list(' ABCDEFG=#'))
N_types = len(characters)


def shapes(idx, rotation):
    assert rotation in [0, 90, 180, 270]
    shape = np.zeros((7, 4, 4), dtype=int)
    shape[0] = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
    ]
    shape[1] = [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    shape[2] = [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
    shape[3] = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    shape[4] = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    shape[5] = [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0]
    ]
    shape[6] = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    s = shape[idx]
    if rotation == 0:
        return s
    result = np.zeros((4, 4), dtype=int)
    if rotation == 90:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[3 - j, i]
    if rotation == 180:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[3 - i, 3 - j]
    if rotation == 270:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[j, 3 - i]
    return result


board = np.zeros((board_size), dtype=int)
board[:, 0] = N_types - 1
board[:, -1] = N_types - 1
board[-1, :] = N_types - 1


def draw_board(board):
    lines = []
    for line in board:
        lines.append(''.join(characters[line]))
    text = '\n'.join(lines)
    print(text)


def piece_array(idx, pos, rot):
    result = np.zeros(board_size, dtype=int)
    result[pos[1]:pos[1] + 4, pos[0]:pos[0] + 4] = shapes(idx, rot)
    return result


N_ticks_per_step = 20
N_ticks_since_step = 0

position = (4, 0)
rotation = 0

continue_playing = True
while continue_playing:
    piece_index = randint(0, 7)
    print(piece_index)
    time.sleep(0.05)
    N_ticks_since_step += 1
    if N_ticks_since_step % N_ticks_per_step == 0:
        if N_ticks_since_step // N_ticks_per_step == 10:
            N_ticks_since_step = 0
            N_ticks_per_step = max(N_ticks_since_step - 1, 5)
    draw_board(board + piece_array(piece_index, position, 0))
    draw_board(board + piece_array(piece_index, position, 90))
    draw_board(board + piece_array(piece_index, position, 180))
    draw_board(board + piece_array(piece_index, position, 270))
    break
