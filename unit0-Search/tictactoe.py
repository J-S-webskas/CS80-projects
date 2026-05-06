"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None
"""
Feedback from Benjamin Basseri:

player: the only thing you really need to know is the parity of the number of markers
winner: an ongoing game (no winner, open space available) will already be detected in the loop, so this logic could be cleaned up a bit
minimax: using a key function can simplify this a bit
MAX_VALUE: only constant values should be all caps. Functions should follow snake_case

Other functions: looks good!
"""


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
    
    x = 0
    o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            if board[i][j] == O:
                o += 1
    
    # if board is empty, it is x's turn
    if x == o == 0:  # Initial
        return X
    if x == o:
        return X
    else:
        return O
    
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
    # Identify possible consecutive 3s in a row
    for i in range(0, 3):  
        if board[i][0] == board[i][1] == board[i][2] == X:
            return X
        if board[i][0] == board[i][1] == board[i][2] == O:  # 3 consecutive o
            return O
    
    # Identify possible consecutive 3s in a column
    for i in range(0, 3):
        if board[0][i] == board[1][i] == board[2][i] == X:
            return X
        if board[0][i] == board[1][i] == board[2][i] == O:  # 3 consecutive o
            return O
        
    # Identify possible consecutive 3s in a diagonal line
    # Case 1: Top right to bottom left
    if board[2][0] == board[1][1] == board[0][2] != EMPTY: 
        if board[2][0] == X:
            return X
        if board[2][0] == O:
            return O
    
    # Case 2: Top left to bottom right
    if board[0][0] == board[1][1] == board[2][2] !=EMPTY:
        if board[0][0] == X:
            return X
        if board[0][0] == O:
            return O
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