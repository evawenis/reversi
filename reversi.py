#!/usr/bin/env python3

import argparse

hori = 8
vert = 8

def print_board(board):
    for i in range(hori):
        print("+---" * vert, end='')
        print('+')
        for j in range(vert):
            leng = len(board[i][j])
            print(f"|{'' if leng == 3 else ' '}{board[i][j]}{' ' if leng == 1 else ''}", end='')
        print('|')
    print("+---" * vert, end='')
    print('+')

def clear_board(board):
    for i in range(hori):
        for j in range(vert):
            if board[i][j] not in 'ox ':
                board[i][j] = ' '

def dig(board, x, y, xw, yw, p, end):
    if x < 0 or x >= hori or y < 0 or y >= vert:
        return -1, -1
    if board[x][y] == p:
        return dig(board, x + xw, y + yw, xw, yw, p, end)
    if board[x][y] == end:
        return x, y
    return -1, -1

xaxis = [-1, -1, 0, 1, 1, 1, 0, -1]
yaxis = [0, 1, 1, 1, 0, -1, -1, -1]

def gen_board(board, p, position):
    oth = 'x' if p == 'o' else 'o'
    counter = 1
    for i in range(hori):
        for j in range(vert):
            if board[i][j] != p:
                continue
            for k in range(len(xaxis)):
                nx = i + xaxis[k]
                ny = j + yaxis[k]
                if nx < 0 or nx >= hori or ny < 0 or ny >= vert:
                    continue
                if board[nx][ny] != oth:
                    continue
                x, y = dig(board, nx, ny, xaxis[k], yaxis[k], oth, ' ')
                if x == -1 or y == -1:
                    continue
                position.append((x, y))
                board[x][y] = str(counter)
                counter += 1

def put(board, p, pos):
    oth = 'x' if p == 'o' else 'o'
    board[pos[0]][pos[1]] = p
    for i in range(len(xaxis)):
        nx = pos[0] + xaxis[i]
        ny = pos[1] + yaxis[i]
        if nx < 0 or nx >= hori or ny < 0 or ny >= vert:
            continue
        if board[nx][ny] != oth:
            continue
        x, y = dig(board, nx, ny, xaxis[i], yaxis[i], oth, p)
        if x == -1 or y == -1:
            continue
        while nx != x or ny != y:
            board[nx][ny] = p
            nx += xaxis[i]
            ny += yaxis[i]

def result(board):
    res = [0, 0]
    for i in board:
        for j in i:
            if j == 'o':
                res[0] += 1
            elif j == 'x':
                res[1] += 1

    print(f"o: {res[0]}, x: {res[1]}")
    if res[0] > res[1]:
        print("o won !!!")
    elif res[1] > res[0]:
        print("x won !!!")
    else:
        print("draw")

def posint(num):
    try:
        num = int(num)
        if num < 0:
            raise argparse.ArgumentTypeError(f"Error: {num} should be positive integer")
        return num
    except:
        raise argparse.ArgumentTypeError(f"Error: {num} should be positive integer")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-w', '--width', help='width of board', type=posint)
    p.add_argument('-v', '--vertical-height', help='height of board', type=posint)
    args = p.parse_args()
    global vert, hori
    if args.vertical_height:
        vert = int(args.vertical_height)
    if args.width is not None:
        hori = int(args.width)
    board = [[' '] * vert for _ in range(hori)]

    board[hori // 2 - 1][vert // 2 - 1] = board[hori // 2][vert // 2] = 'o'
    board[hori // 2 - 1][vert // 2] = board[hori // 2][vert // 2 - 1] = 'x'

    turn = 1
    offset = 0

    while turn <= hori * vert - 4:
        p = 'o' if (turn + offset) % 2 else 'x'
        position = []
        gen_board(board, p, position)
        if len(position) == 0:
            offset += 1
            message = f"{p} cannot put any position, so skip"
            p = 'o' if (turn + offset) % 2 else 'x'
            position = []
            gen_board(board, p, position)
            if len(position) == 0:
                break
            print(message)
        print(f"Turn {turn}: {p}")
        print_board(board)
        clear_board(board)
        pos = input("number?\n> ")
        try:
            pos = int(pos) - 1
            if pos >= len(position):
                print("Error: please input valid numbers")
                continue
        except:
            continue
        put(board, p, position[pos])
        turn += 1

    print_board(board)
    result(board)

if __name__ == '__main__':
    main()
