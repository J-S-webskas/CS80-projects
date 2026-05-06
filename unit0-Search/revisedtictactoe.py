"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    # Board is a 3x3 list
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
       return "the game is already over"

    count = sum(1 for row in board for cell in row if cell != EMPTY)
    return X if count % 2 == 0 else O
    
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return "the game is already over"

    # Possible action == square without X or O == EMPTY
    possible = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible.add((i, j)) 
    return possible

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    i = action[0]
    j = action[1]
    # Out of bounds
    if i < 0 or j < 0:
        raise ValueError
    # Taken move
    if board[i][j] != EMPTY:
        raise ValueError
    # Call player to determine whether X or O gets implemented
    turn = player(board)
    new_board[i][j] = turn
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
        
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
                return board[0][col]
        
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for row, column, diagonal wins for individual player
    if winner(board) == X or winner(board) == O:
        return True
    # Check for ties
    n = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
            else:
                n += 1
    if n == 9:
        return True
    # On going game
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

# Using a key function
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    best_value = 0
    best_action = None
    if player(board) == X:
        best_value, best_action = MAX_VALUE(board)
    if player(board) == O:
        best_value, best_action = MIN_VALUE(board)
    
    return best_action

def MAX_VALUE(board):
    if terminal(board):
        return utility(board), None
    
    best_move = None
    v = -math.inf
    for action in actions(board):
        min_val = MIN_VALUE(result(board, action))[0]
        if min_val > v:
            v = min_val
            best_move = action
    return v, best_move

def MIN_VALUE(board):
    if terminal(board):
        return utility(board), None
    
    best_move = None
    v = +math.inf
    for action in actions(board):
        max_val = MAX_VALUE(result(board, action))[0]
        if max_val < v:
            v = max_val
            best_move = v
    return v, best_move