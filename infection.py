# -*- coding: utf-8 -*-
"""
撰寫infection遊戲的規則。
基本定義:
棋盤用一個二維陣列表示，由0、1、2組成，
0: 空格、1:黑棋、2:白棋
如: [[0,1,2,1],
    [0,1,2,0],
    [1,2,0,2]]
最左上角的座標為(0,0)，座標以(row, col)表示。
棋步為元組以(jr,jc, r,c)表示
"""

def breed(turn, board):
    """
    (繁殖棋步)
    turn: 1或2，表示現在換誰走
    board: 棋盤狀態
    """
    n, m = len(board), len(board[0])
    direc = [(1,0),(-1,0),(0,1),(0,-1)]
    in_board = lambda r, c: 0<=r<n and 0<=c<m
    moves = []
    for r in range(n):
        for c in range(m):
            if board[r][c]==0:
                for dr, dc in direc:
                    tr, tc = r+dr, c+dc
                    if in_board(tr,tc) and board[tr][tc]==turn:
                        moves.append((-1,-1,r,c))
                        break
    return moves

def jump(turn, board):
    """
    (跳躍棋步)
    turn: 1或2，表示現在換誰走
    board: 棋盤狀態
    """
    n, m = len(board), len(board[0])
    direc = [(2,0),(-2,0),(0,2),(0,-2),(1,1),(1,-1),(-1,1),(-1,-1)]
    in_board = lambda r, c: 0<=r<n and 0<=c<m
    moves = []
    for r in range(n):
        for c in range(m):
            if board[r][c]==turn:
                for dr, dc in direc:
                    tr, tc = r+dr, c+dc
                    if in_board(tr,tc) and board[tr][tc]==0:
                        moves.append((r,c,tr,tc))
    return moves

def valid_move(turn, board):
    """
    (合法棋步)
    turn: 1或2，表示現在換誰走
    board: 棋盤狀態
    """
    return breed(turn, board)+jump(turn, board)

def is_valid(turn, board, move):
    """
    判斷是否為合法棋步
    """
    return move in valid_move(turn, board)

def action(turn, board, move):
    n, m = len(board), len(board[0])
    jr, jc, r,c = move
    in_board = lambda r, c: 0<=r<n and 0<=c<m
    direc = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    if (jr,jc)!=(-1,-1):
        board[jr][jc] = 0
    board[r][c] = turn
    
    for dr, dc in direc:
        tr, tc = r+dr, c+dc
        if in_board(tr,tc) and board[tr][tc]==3-turn:
            board[tr][tc] = turn

if __name__=='__main__':
    board = [[0,1,2,1],
            [0,1,2,0],
            [1,2,0,2]]
    turn = 1
    print(valid_move(turn, board))
    move = (2, 0, 2, 2)
    action(turn, board, move)
    print(board)