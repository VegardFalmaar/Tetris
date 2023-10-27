import time
from random import randint
from collections import namedtuple

import numpy as np
import keyboard     # type: ignore


def shapes(idx: int, rot: int):
    assert rot in [0, 1, 2, 3]
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
    if rot == 0:
        return s.copy()
    result = np.zeros((4, 4), dtype=int)
    if rot == 1:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[3 - j, i]
    if rot == 2:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[3 - i, 3 - j]
    if rot == 3:
        for i in range(4):
            for j in range(4):
                result[i, j] = s[j, 3 - i]
    return result.copy()


def draw_board(b, clear_screen=False):
    lines = []
    for line in b:
        lines.append(''.join(characters[line]))
    text = '\n'.join(lines)
    if clear_screen:
        print('\b'*len(text))
    print(text)


def piece_array(idx: int, x: int, y: int, rot: int):
    result = np.zeros(board_size, dtype=int)
    result[y:y + 4, x:x + 4] = shapes(idx, rot) * (idx + 1)
    return result


def piece_fits(b: np.ndarray, idx: int, x: int, y: int, rot: int):
    if not 0 <= x < board_size.x - 3:
        return False
    if not 0 <= y < board_size.y - 3:
        return False
    piece = piece_array(idx, x, y, rot)
    return not np.any((piece != 0) & (b != 0))


Size = namedtuple('Size', 'y x')
board_size = Size(18, 16)
characters = np.array(list(' ABCDEFG=#'))


def main():
    N_types = len(characters)

    board = np.zeros(board_size, dtype=int)
    board[:, 0] = N_types - 1
    board[:, -1] = N_types - 1
    board[-1, :] = N_types - 1


    N_ticks_per_step = 15
    N_ticks_since_step = 0

    pos_x, pos_y = 4, 0
    piece_index = randint(0, 6)
    rotation = 0
    key_pressed = False
    draw_board(board)

    while True:
        time.sleep(0.1)
        draw_board(board + piece_array(piece_index, pos_x, pos_y, rotation), clear_screen=True)

        if keyboard.is_pressed('left') and not key_pressed:
            key_pressed = True
            if piece_fits(board, piece_index, pos_x - 1, pos_y, rotation):
                pos_x -= 1
        if keyboard.is_pressed('right') and not key_pressed:
            key_pressed = True
            if piece_fits(board, piece_index, pos_x + 1, pos_y, rotation):
                pos_x += 1
        if keyboard.is_pressed('up') and not key_pressed:
            key_pressed = True
            if piece_fits(board, piece_index, pos_x, pos_y, (rotation + 1) % 4):
                rotation = (rotation + 1) % 4
        if keyboard.is_pressed('down') and not key_pressed:
            key_pressed = True
            if piece_fits(board, piece_index, pos_x, pos_y + 1, rotation):
                pos_y += 1
        key_pressed = False

        N_ticks_since_step += 1
        if N_ticks_since_step % N_ticks_per_step == 0:
            pos_y += 1
            mask = np.any(board == N_types - 2, axis=1)
            for i, e in enumerate(mask):
                if e:
                    board[1:i + 1] = board[:i]
            if N_ticks_since_step // N_ticks_per_step == 10:
                N_ticks_since_step = 0
                N_ticks_per_step = max(N_ticks_per_step - 1, 5)

        if not piece_fits(board, piece_index, pos_x, pos_y, rotation):
            board += piece_array(piece_index, pos_x, pos_y - 1, rotation)
            mask = np.all(board != 0, axis=1)
            mask[-1] = False
            board[mask, 1:-1] = N_types - 2
            pos_x, pos_y = 4, 0
            piece_index = randint(0, 6)
            if not piece_fits(board, piece_index, pos_x, pos_y, rotation):
                print('Game over')
                break


if __name__ == '__main__':
    main()
