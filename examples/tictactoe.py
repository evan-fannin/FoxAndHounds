import gameSearch

class TicTacToe(gameSearch.Game):
    '''
    Describe your game here.
    Include a reference to the exact rules.
    '''
    emptyState = ('...','...','...',)   # The setup at the beginning of a full game.
    blank = '.'

    def __init__(self, initial=None):
        if initial == None:
            self.initial = self.emptyState
        else:
            self.initial = initial
        assert len(self.initial) == 3
        assert [len(row)
                for row in self.initial] == [3,3,3]

    def actions(self, state):
        moves = []
        for r in (0,1,2):
            for c in (0,1,2):
                if state[r][c] == self.blank:
                    moves += [(r,c)]
        return moves

    def result(self, state, move):
        board = [[c for c in row]
                 for row in state]
        player = self.to_move(state)
        r, c = move
        board[r][c] = player
        newState = tuple([''.join(row)
                          for row in board])
        return newState

    def utility(self, state, player):
        xu = self.xUtility(state)
        if player == 'X':
            return xu
        else:
            return -xu

    def terminal_test(self, state):
        xu = self.xUtility(state)
        if xu != 0:
            return True
        count = self.countAll(state)
        if count['.'] == 0:
            return True
        return False

    def to_move(self, state):
        count = self.countAll(state)
        if count['X'] > count['O']:
            return 'O'
        return 'X'

    def countAll(self, state):
        count = {'X':0,'O':0,'.':0,}
        for r in (0,1,2):
            for c in (0,1,2):
                cell = state[r][c]
                count[cell] += 1
        return count

    def xUtility(self, state):
        for row in state:
            if row == 'XXX':
                return 1
            if row == 'OOO':
                return -1
        for c in (0,1,2):
            col = ''.join([state[r][c]
                           for r in (0,1,2)])
            if col == 'XXX':
                return 1
            if col == 'OOO':
                return -1
        rDiag = ''.join([state[0][0],state[1][1],state[2][2]])
        if rDiag == 'XXX':
            return 1
        if rDiag == 'OOO':
            return -1
        lDiag = ''.join([state[0][2],state[1][1],state[2][0]])
        if lDiag == 'XXX':
            return 1
        if lDiag == 'OOO':
            return -1
        return 0

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

instances += [TicTacToe(('XXX','OO.','...',))]
instances[-1].label = 'X wins across top'

instances += [TicTacToe(('XO.','.OX','.OX',))]
instances[-1].label = 'O wins down center'

instances += [TicTacToe(('XXO','OX.','..O',))]
instances[-1].label = 'One Ply From Win'

instances += [TicTacToe(('OXO','XOX','X..',))]
instances[-1].label = 'One Ply From Loss'

instances += [TicTacToe(('XXO','OX.','...',))]
instances[-1].label = 'Two Plys From Win'

instances += [TicTacToe(('O.O','XOX','X..',))]
instances[-1].label = 'Two Plys From Loss'

instances += [TicTacToe(('XX.','O..','...',))]
instances[-1].label = 'Four Plys From Win'

instances += [TicTacToe(('..O','X.X','...',))]
instances[-1].label = 'Five Plys From Loss'

instances += [TicTacToe(('X..','O..','...',))]
instances[-1].label = 'Six Plys From Win Corner'

instances += [TicTacToe(('.O.','.X.','...',))]
instances[-1].label = 'Six Plys From Win Center'

instances += [TicTacToe()]
instances[-1].label = 'New Game'

# Change to your name
name = 'Aardvark, Aaron'

games = {}

games['easy'] = {
    'evaluation' : 'table',
    'instances' : instances[0:4],
    'players' : [   # Compare search methods on simple instances.
        # gameSearch.minimax_decision,
        # gameSearch.alphabeta_search,
        gameSearch.MiniMax(),
        gameSearch.AlphaBeta(),
    ],
}

games['hardest'] = {
    'evaluation' : 'table',
    'instances' : instances[-5:-1],
    'players' : [   # Only use the best method on hard instances.
        # gameSearch.alphabeta_search,
        gameSearch.AlphaBeta(8),
    ],
}

games['short'] = {
    'evaluation' : 'play',
    # don't play a full instance until you are sure it works
    # 'instance' : TicTacToe(),
    'instance' : TicTacToe(('.O.','.X.','...',)),
}
