import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    board = []
    for _ in range(3):
        row = [EMPTY] * 3  # Initialize each row with EMPTY cells
        board.append(row)
    return board


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)

    # Determine which player's turn it is based on the counts
    if num_X == num_O:
        return X  # It's player 'X''s turn
    else:
        return O  # It's player 'O''s turn


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    current_player = player(board)
    new_board = [row.copy() for row in board]
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O

    # Check columns
    for j in range(3):
        if [board[i][j] for i in range(3)].count(X) == 3:
            return X
        elif [board[i][j] for i in range(3)].count(O) == 3:
            return O

    # Check diagonals
    if all(board[i][i] == X for i in range(3)) or all(board[i][i] == O for i in range(3)):
        return X if board[1][1] == X else O

    if all(board[i][2 - i] == X for i in range(3)) or all(board[i][2 - i] == O for i in range(3)):
        return X if board[1][1] == X else O

    return None  # No winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player using the minimax algorithm.
    """
    def max_value(board):
        if terminal(board):
            return utility(board)

        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)

        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    if player(board) == X:
        return max(actions(board), key=lambda x: min_value(result(board, x)))
    else:
        return min(actions(board), key=lambda x: max_value(result(board, x)))
