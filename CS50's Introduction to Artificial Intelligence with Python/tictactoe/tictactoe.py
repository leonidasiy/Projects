"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0
    for row in board:
        count_X += row.count(X)
        count_O += row.count(O)
    if count_X == count_O:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception(str(action), 'is not a valid action.')
    new_board = deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][1] == board[i][0] == board[i][2] != EMPTY:
            return board[i][1]
    for i in range(len(board[0])):
        if board[1][i] == board[0][i] == board[2][i] != EMPTY:
            return board[1][i]
    if board[1][1] == board[0][0] == board[2][2] != EMPTY or board[1][1] == board[0][2] == board[2][0] != EMPTY:
        return board[1][1]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or not actions(board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    action_values = {}
    if player(board) == X:
        for action in actions(board):
            action_values[action] = minimizing(result(board, action))
        return sorted(action_values, key=lambda action: action_values[action])[-1]
    elif player(board) == O:
        for action in actions(board):
            action_values[action] = maximizing(result(board, action))
        return sorted(action_values, key=lambda action: action_values[action])[0]
    

#Helper Functions

def maximizing(board):
    value = -999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        value = max(value, minimizing(result(board, action)))
    return value 


def minimizing(board):
    value = 999
    if terminal(board):
        return utility(board)
    for action in actions(board):
        value = min(value, maximizing(result(board, action)))
    return value
