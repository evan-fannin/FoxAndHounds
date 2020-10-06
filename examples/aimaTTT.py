from collections import namedtuple
import gameSearch

GameState = namedtuple('GameState', 'to_move, utility, board, moves')

class TicTacToe(gameSearch.Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3, initial=None):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        if not initial:
            self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)
        else:
            self.initial = initial

    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        return state.to_move

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        "If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        "Return true if there is a line through move on board for player."
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

ttts = []

gs = GameState(to_move='O', utility=1,
               board={(0,0):'X',(0,1):'X',(0,2):'X',
                      (1,0):'O',(1,1):'O',},
               moves=[(1,2),(2,0),(2,1),(2,2),])
ttts += [TicTacToe(3, 3, 3, gs)]
ttts[-1].label = 'X wins across top'

gs = GameState(to_move='X', utility=0,
               board={(0,0):'X',(0,1):'X',(0,2):'O',
                      (1,0):'O',(1,1):'X',
                                          (2,2):'O',},
               moves=[(1,2),(2,0),(2,1),])
ttts += [TicTacToe(3, 3, 3, gs)]
ttts[-1].label = 'One Ply From Win'

gs = GameState(to_move='O', utility=0,
               board={(0,0):'X',(0,1):'X',(0,2):'O',
                      (1,0):'O',(1,1):'X',},
               moves=[(1,2),(2,0),(2,1),(2,2),])
ttts += [TicTacToe(3, 3, 3, gs)]
ttts[-1].label = 'Two Plys From Loss'

gs = GameState(to_move='X', utility=0,
               board={(0,0):'X',(0,1):'X',(0,2):'O',
                      (1,0):'O',},
               moves=[(1,1),(1,2),(2,0),(2,1),(2,2),])
ttts += [TicTacToe(3, 3, 3, gs)]
ttts[-1].label = 'Three Plys From Win'

name = 'Norvig, Peter'

games = {}

games['easy'] = {
    'evaluation' : 'table',
    'instances' : [
        ttts[0],
        ttts[1],
    ],
    'players' : [   # Compare search methods on simple instances.
        gameSearch.MiniMax(),
        gameSearch.AlphaBeta(),
    ],
}

games['hardest'] = {
    'evaluation' : 'table',
    'instances' : [
        ttts[-2],
        ttts[-1],
    ],
    'players' : [
        # Only use the best method on hard instances.
        gameSearch.AlphaBeta(9),
    ],
}

games['fun'] = {
    'evaluation' : 'play',
    'instance' : TicTacToe(),
    'players' : [
        gameSearch.Query('Peter'),
        gameSearch.AlphaBeta(9),
    ],
}