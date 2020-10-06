import gameSearch

class FoxAndHounds(gameSearch.Game):
    '''
    Describe your game here.
    Include a reference to the exact rules.
    '''

    fox_turn = False  # Fox moves first, this is flipped at the start of actions

    emptyState = (  # The setup at the beginning of a full game.
                  '.h.h.h.h',
                  '........',
                  '........',
                  '........',
                  '........',
                  '........',
                  '........',
                  'f.......'
                 )

    def __init__(self, initial=None):
        if initial == None:
            self.initial = self.emptyState
        else:
            self.initial = initial

    def actions(self, state):
        self.fox_turn = not self.fox_turn

        if self.fox_turn:
            return self.get_fox_moves(state)
        else:  # It's the hounds' turn
            return self.get_hounds_moves(state)

    def result(self, state, move):
        board = [[c for c in row]
                 for row in state]
        player = self.to_move

        if player:
            r0, c0 = self.get_fox(state)
            r1, c1 = move
            board[r0][c0] = '.'
            board[r1][c1] = 'f'
            new_state = tuple([''.join(row)
                              for row in board])
            return new_state

        else:  # Player is hounds
            hound, r1, c1 = move
            hounds = self.get_hounds(state)
            r0, c0 = hounds[hound]

            board[r0][c0] = '.'
            board[r1][c1] = 'h'
            new_state = tuple([''.join(row)
                               for row in board])
            return new_state

    def utility(self, state, player):
        fox_utility = self.fox_utility(state)
        if player:
            return fox_utility
        else:
            return -fox_utility

    def fox_utility(self, state):
        if self.fox_wins(state):
            return 1
        if self.hounds_win(state):
            return -1
        return 0

    def terminal_test(self, state):
        fox_wins = self.fox_wins(state)
        hounds_win = self.hounds_win(state)

        if fox_wins or hounds_win:
            return True

        return False

    def to_move(self, state):
        return self.fox_turn

    def get_fox(self, state):
        for r in range(8):
            for c in range(8):
                cell = state[r][c]
                if cell == 'f':
                    return r, c
        return 'error'

    def get_fox_moves(self, state):
        moves = []
        r, c = self.get_fox(state)

        # Four possible moves: two diagonally above, two diagonally below

        # Check row above
        if r - 1 >= 0:

            # Check above left
            if c - 1 >= 0:
                if state[r - 1][c - 1] == '.':
                    moves.append((r - 1, c - 1))

            # Check above right
            if c + 1 <= 7:
                if state[r - 1][c + 1] == '.':
                    moves.append((r - 1, c + 1))

        # Check row below
        if r + 1 <= 7:

            # Check below left
            if c - 1 >= 0:
                if state[r + 1][c - 1] == '.':
                    moves.append((r + 1, c - 1))

            # Check below right
            if c + 1 <= 7:
                if state[r + 1][c + 1] == '.':
                    moves.append((r + 1, c + 1))

        return moves

    def fox_wins(self, state):
        r, c = self.get_fox(state)

        if r == 0:
            if c == 1 or c == 3 or c == 5 or c == 7:
                return True

        return False

    def get_hounds(self, state):
        count = 0
        hounds = []
        for r in range(8):
            for c in range(8):
                cell = state[r][c]
                if cell == 'h':
                    hounds.append((r, c))
                    count += 1
                    if count == 4:
                        return hounds
        return 'error'

    def get_hounds_moves(self, state):
        moves = []
        hounds = self.get_hounds(state)

        for hound in range(4):
            r, c = hounds[hound]

            # Check row below
            if r + 1 <= 7:

                # Check below left
                if c - 1 >= 0:
                    if state[r + 1][c - 1] == '.':
                        moves.append((hound, r + 1, c - 1))

                # Check below right
                if c + 1 <= 7:
                    if state[r + 1][c + 1] == '.':
                        moves.append((hound, r + 1, c + 1))

        return moves

    def hounds_win(self, state):
        fox_moves = self.get_fox_moves(state)

        if len(fox_moves) == 0:
            return True

        return False


instances = []
# Copy, paste and CHANGE to add successively more complex
# instances here.
# The first instance(s) should be game(s) lost or won.
# Include additional instances one move from the end,
# 2-4 moves from the end, etc.

instances += [FoxAndHounds((
                  '...f.h.h',
                  '....h...',
                  '........',
                  '........',
                  '........',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins'

instances += [FoxAndHounds((
                  '.....h.h',
                  '..f.h...',
                  '........',
                  '........',
                  '........',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 1 ply'

# instances += [FoxAndHounds(('XO.','.OX','.OX',))]
# instances[-1].label = 'O wins down center'

# Change to your name
name = 'Fannin, Evan'

games = {}

games['easy'] = {
    'evaluation' : 'table',
    'instances' : instances[0:2],
    'players' : [   # Compare search methods on simple instances.
        gameSearch.MiniMax(),
        gameSearch.AlphaBeta(),
    ]
}

# games['hardest'] = {
#     'evaluation' : 'table',
#     'instances' : [],
#     'players' : [   # Only use the best method on hard instances.
#         gameSearch.AlphaBeta(6),
#     ]
# }

# games['fun'] = {
#     'evaluation' : 'play',
#     'instance' : RenameThisGame(),
#     'players' : [   # uncomment two  Players
#         gameSearch.Query('Aaron'),
#         gameSearch.Random(),            # Add seed in ()'s for a repeatable game
#         # gameSearch.MiniMax(),         # Add horizon in ()'s if != 4
#         # gameSearch.AlphaBeta(),       # Add horizon in ()'s if != 4
#         # gameSearch.Query('Aamy'),
#     ]
# }

###################################################

# Modules in the examples folder
# Import them for testing only.
#
# from examples import aimaTTT
# name = aimaTTT.name
# games = aimaTTT.games
#
# from examples import tictactoe
# name = tictactoe.name
# games = tictactoe.games
