import gameSearch

class FoxAndHounds(gameSearch.Game):
    '''
    Describe your game here.
    Include a reference to the exact rules.
    '''

    emptyState = (  # The setup at the beginning of a full game.
                  '1h.h.h.h',
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
        if state[0][0] == '1':
            return self.get_fox_moves(state)
        else:  # It's the hounds' turn
            return self.get_hounds_moves(state)

    def result(self, state, move):
        board = [[c for c in row]
                 for row in state]

        if state[0][0] == '1':
            r0, c0 = self.get_fox(state)
            r1, c1 = move
            board[r0][c0] = '.'
            board[r1][c1] = 'f'
            board[0][0] == '0'
            new_state = tuple([''.join(row)
                              for row in board])
            return new_state

        else:  # Player is hounds
            hound, r1, c1 = move
            hounds = self.get_hounds(state)
            r0, c0 = hounds[hound]

            board[r0][c0] = '.'
            board[r1][c1] = 'h'
            board[0][0] = '1'
            new_state = tuple([''.join(row)
                               for row in board])
            return new_state

    def utility(self, state, player):
        fox_utility = self.fox_utility(state)
        if player == 'f':
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
        if state[0][0] == '1':
            return 'f'
        else:
            return 'h'

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

    def display(self, state):
        for row in state:
            chars = [c for c in row]
            print('    %s' % ' '.join(chars))


instances = []
# Copy, paste and CHANGE to add successively more complex
# instances here.
# The first instance(s) should be game(s) lost or won.
# Include additional instances one move from the end,
# 2-4 moves from the end, etc.

instances += [FoxAndHounds((
                  '1..f.h.h',
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
                  '1....h.h',
                  '..f.h...',
                  '........',
                  '........',
                  '........',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 1 ply'

instances += [FoxAndHounds((
                  '0....h.h',
                  '..f.h...',
                  '........',
                  '........',
                  '........',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 2 ply'

instances += [FoxAndHounds((
                  '0....h.h',
                  '........',
                  '.h......',
                  'f.......',
                  '.h......',
                  '........',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Hounds win'

instances += [FoxAndHounds((
                  '0....h.h',
                  '..h.....',
                  '........',
                  'f.......',
                  '.h......',
                  '........',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Hounds win in 1 ply'

instances += [FoxAndHounds((
                  '0......h',
                  '........',
                  '........',
                  '........',
                  '........',
                  'h.h.....',
                  '.f......',
                  '..h.....'
                 ))]
instances[-1].label = 'Hounds win in 2 ply'

instances += [FoxAndHounds()]
instances[-1].label = 'Full Game'

# instances += [FoxAndHounds(('XO.','.OX','.OX',))]
# instances[-1].label = 'O wins down center'

# Change to your name
name = 'Fannin, Evan'

games = {}

games['easy'] = {
    'evaluation' : 'table',
    'instances' : instances[0:6],
    'players' : [   # Compare search methods on simple instances.
        gameSearch.MiniMax(),
        gameSearch.AlphaBeta(),
    ]
}

games['hardest'] = {
    'evaluation' : 'table',
    'instances' : [instances[-1]],
    'players' : [   # Only use the best method on hard instances.
        gameSearch.AlphaBeta(6),
    ]
}

# games['fun'] = {
#     'evaluation' : 'play',
#     'instance' : FoxAndHounds(),
#     'players' : [   # uncomment two  Players
#         gameSearch.Query('Evan'),
#         # gameSearch.Random(),            # Add seed in ()'s for a repeatable game
#         # gameSearch.MiniMax(),         # Add horizon in ()'s if != 4
#         gameSearch.AlphaBeta(),       # Add horizon in ()'s if != 4
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
