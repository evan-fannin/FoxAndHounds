import gameSearch
import networkx as nx

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
            # choose_start = input('Choose a starting point? ("yes" / "no"):  ')
            choose_start = 'no'
            if choose_start == 'yes':
                initial = input('''Enter initial game board as a string tuple.\nIt\'s your fault if you enter it wrong and the game messes up. We only take so much responsibility.
                Here\'s an example:
                (
                '0......h',
                '........',
                '..h.....',
                '....h...',
                '........',
                '..h.....',
                '.......f',
                '........',
                )
                :''')

                self.initial = initial
            else:
                # print('You either typed "no" or gibberish.\n'
                #       'Here we go from the start!')
                self.initial = self.emptyState


    def actions(self, state):
        if state[0][0] == '1':
            fox_moves = self.get_fox_moves(state)
            return fox_moves
            # return self.get_fox_moves(state)
        else:  # It's the hounds' turn
            hounds_moves = self.get_hounds_moves(state)
            return hounds_moves
            # return self.get_hounds_moves(state)

    def result(self, state, move):
        board = [[c for c in row]
                 for row in state]

        if state[0][0] == '1':
            r0, c0 = self.get_fox(state)
            r1, c1 = move
            board[r0][c0] = '.'
            board[r1][c1] = 'f'
            board[0][0] = '0'
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
        total_utility = 0
        distance_from_goal_utility = 7 - self.distance_from_goal_utility(state)
        number_of_moves_utility = 10 * (4 - self.number_of_moves_utility(state))
        winning_utility = self.winning_utility(state)
        total_distance = self.distance_from_fox_utility(state)

        if player == 'f':
            total_utility += max(0, distance_from_goal_utility)
            total_utility -= number_of_moves_utility
            total_utility += winning_utility
            return total_utility

        else:
            total_utility -= 5 * max(0, distance_from_goal_utility)
            # total_utility += 10 * (4 * number_of_moves_utility)
            total_utility -= 100 * winning_utility
            return total_utility

    def winning_utility(self, state):
        if self.fox_wins(state):
            return 100
        if self.hounds_win(state):
            return -100
        return 0

    def distance_from_goal_utility(self, state):
        r, c = self.get_fox(state)
        distances = []
        distances.append(self.get_distance(r, c, 0, 1))
        distances.append(self.get_distance(r, c, 0, 3))
        distances.append(self.get_distance(r, c, 0, 5))
        distances.append(self.get_distance(r, c, 0, 7))
        return min(distances)

    def distance_from_fox_utility(self, state):
        r, c = self.get_fox(state)
        hounds = self.get_hounds(state)
        total_distance = 0
        for i in hounds:
            r2, c2, = i
            total_distance += self.get_distance(r, c, r2, c2)
        return total_distance

    def get_distance(self, r, c, r1, c1):
        r_diff = r1 - r
        c_diff = abs(c1 - c)
        distance = (r_diff + c_diff) / 2
        return distance

    def number_of_moves_utility(self, state):
        fox_moves = self.get_fox_moves(state)
        return len(fox_moves)

    def path_to_goal_utility(self, state):
        g = self.create_graph()
        hounds = self.get_hounds(state)
        for hound in hounds:
            g.remove_node(hound)

        goals = []

        if g.has_node((0, 1)):
            goals.append((0, 1))
        if g.has_node((0, 3)):
            goals.append((0, 3))
        if g.has_node((0, 5)):
            goals.append((0, 5))
        if g.has_node((0, 7)):
            goals.append((0, 7))

        fox = self.get_fox(state)

        distances = []

        for goal in goals:
            if nx.has_path(g, fox, goal):
                distances.append(nx.dijkstra_path_length(g, fox, goal))

        if len(distances) == 0:
            return -1

        return min(distances)

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

    def create_graph(self):
        g = nx.Graph()
        edges = [((0, 1), (1, 0)), ((0, 1), (1, 2)),
                 ((0, 3), (1, 2)), ((0, 3), (1, 4)),
                 ((0, 5), (1, 4)), ((0, 5), (1, 6)),
                 ((0, 7), (1, 6)),

                 ((1, 0), (2, 1)),
                 ((1, 2), (2, 1)), ((1, 2), (2, 3)),
                 ((1, 4), (2, 3)), ((1, 4), (2, 5)),
                 ((1, 6), (2, 5)), ((1, 6), (2, 7)),

                 ((2, 1), (3, 0)), ((2, 1), (3, 2)),
                 ((2, 3), (3, 2)), ((2, 3), (3, 4)),
                 ((2, 5), (3, 4)), ((2, 5), (3, 6)),

                 ((3, 0), (4, 1)),
                 ((3, 2), (4, 1)), ((3, 2), (4, 3)),
                 ((3, 4), (4, 3)), ((3, 4), (4, 5)),
                 ((3, 6), (4, 5)), ((3, 6), (4, 7)),

                 ((4, 1), (5, 0)), ((4, 1), (5, 2)),
                 ((4, 3), (5, 2)), ((4, 3), (5, 4)),
                 ((4, 5), (5, 4)), ((4, 5), (5, 6)),
                 ((4, 7), (5, 6)),

                 ((5, 0), (6, 1)),
                 ((5, 2), (6, 1)), ((5, 2), (6, 3)),
                 ((5, 4), (6, 3)), ((5, 4), (6, 5)),
                 ((5, 6), (6, 5)), ((5, 6), (6, 7)),

                 ((6, 1), (7, 0)), ((6, 1), (7, 2)),
                 ((6, 3), (7, 2)), ((6, 3), (7, 4)),
                 ((6, 5), (7, 4)), ((6, 5), (7, 6)),
                 ((6, 7), (7, 6))]
        g.add_edges_from(edges)

        return g



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
                  '1....h.h',
                  '....h...',
                  '.f......',
                  '........',
                  '........',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 3 ply'

instances += [FoxAndHounds((
                  '0....h.h',
                  '........',
                  '.f......',
                  '........',
                  '.....h..',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 4 ply'

instances += [FoxAndHounds((
                  '0....h.h',
                  '........',
                  '.......f',
                  '........',
                  '.....h..',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in 6 ply'

instances += [FoxAndHounds((
                  '0....h.h',
                  '........',
                  '........',
                  '....h...',
                  '...f....',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in ? ply'

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
                  '1......h',
                  '........',
                  '........',
                  '........',
                  '........',
                  'h.h.....',
                  '.f......',
                  '..h.....'
                 ))]
instances[-1].label = 'Hounds win in 2 ply'

instances += [FoxAndHounds((
                  '0......h',
                  '........',
                  '........',
                  '........',
                  '...h....',
                  'h.......',
                  '.f......',
                  '..h.....'
                 ))]
instances[-1].label = 'Hounds win in 3 ply'

instances += [FoxAndHounds((
                  '0......h',
                  '........',
                  '..h.....',
                  '....h...',
                  '...f....',
                  '..h.....',
                  '........',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in ? ply'

instances += [FoxAndHounds((
                  '0......h',
                  '........',
                  '..h.....',
                  '....h...',
                  '........',
                  '..h.....',
                  '.......f',
                  '........'
                 ))]
instances[-1].label = 'Fox wins in ? ply'

instances += [FoxAndHounds((
                  '1h.h.h.h',
                  '........',
                  '........',
                  '........',
                  '........',
                  '........',
                  '........',
                  'f.......'
                 ))]
instances[-1].label = 'Full Game'

# instances += [FoxAndHounds(('XO.','.OX','.OX',))]
# instances[-1].label = 'O wins down center'

# Change to your name
name = 'Fannin, Evan'

games = {}

# games['easy'] = {
#     'evaluation' : 'table',
#     'instances' : instances[0:11],
#     'players' : [   # Compare search methods on simple instances.
#         gameSearch.MiniMax(),
#         gameSearch.AlphaBeta(),
#     ]
# }

# games['hardest'] = {
#     'evaluation' : 'table',
#     'instances' : [instances[-1]],
#     'players' : [   # Only use the best method on hard instances.
#         gameSearch.AlphaBeta(6),
#     ]
# }

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
