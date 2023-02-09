import numpy as np
import pygame
import sys
import math
 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7
 
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    if col < 0 or col > 6:
        return False
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
 
board = create_board()
game_over = False
turn = 0

def alphabeta(board, depth, alpha, beta, maximizingPlayer, piece):
    if depth == 0 or winning_move(board, 1) or winning_move(board, 2):
        if winning_move(board, 1):
            return -math.inf
        elif winning_move(board, 2):
            return math.inf
        else:
            return 0
 
    if maximizingPlayer:
        value = -math.inf
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, piece)
                new_score = alphabeta(b_copy, depth-1, alpha, beta, False, piece%2 + 1)
                value = max(value, new_score)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return value
    else:
        value = math.inf
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, piece)
                new_score = alphabeta(b_copy, depth-1, alpha, beta, True, piece%2 + 1)
                value = min(value, new_score)
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return value
 
def get_best_move(board, piece):
    best_col = 0
    best_score = -math.inf
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, piece)
            score = alphabeta(b_copy, 3, -math.inf, math.inf, False, piece%2 + 1)
            if score > best_score:
                best_score = score
                best_col = col
    return best_col
 
while not game_over:
    print_board(board)
    if turn == 0:
        print("Player 1: ")
        col = int(input("Give a col: "))

        while (not is_valid_location(board, col)):
            print("Invalid column! Enter a valid one (0 to 6)")
            col = int(input("Give a col: "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            if winning_move(board, 1):
                print("Congrats! Player 1 won")
                print_board(board)
                game_over = True
        else:
            print("That was an invalid location")
    else:
        print("Player 2: ")
        col = get_best_move(board, 2)

        while (not is_valid_location(board, col)):
            col = get_best_move(board, 2)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if winning_move(board, 2):
                print("Congrats! Player 2 won")
                print_board(board)
                game_over = True
        else:
            print("That was an invalid location")

    turn += 1
    turn = turn % 2




 