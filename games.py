import gameSearch

class RenameThisGame(gameSearch.Game):
    '''
    Describe your game here.
    Include a reference to the exact rules.
    '''
    emptyState = None   # The setup at the beginning of a full game.

    def __init__(self, initial=None):
        if initial == None:
            self.initial = self.emptyState
        else:
            self.initial = initial

    def actions(self, state):
        return []

    def result(self, state, move):
        return state

    def utility(self, state, player):
        return 0

    def terminal_test(self, state):
        return True

    def to_move(self, state):
        return '?'

instances = []
# Copy, paste and CHANGE to add successively more complex
# instances here.
# The first instance(s) should be game(s) lost or won.
# Include additional instances one move from the end,
# 2-4 moves from the end, etc.

instances += [RenameThisGame('?')]
instances[-1].label = 'CopyPasta, tsk, tsk!'

instances += [RenameThisGame('?')]
instances[-1].label = 'CopyPasta, tsk, tsk!'

instances += [RenameThisGame('?')]
instances[-1].label = 'CopyPasta, tsk, tsk!'

instances += [RenameThisGame('?')]
instances[-1].label = 'CopyPasta, tsk, tsk!'

# Change to your name
name = 'Aardvark, Aaron'

games = {}

games['easy'] = {
    'evaluation' : 'table',
    'instances' : instances[0:1],
    'players' : [   # Compare search methods on simple instances.
        gameSearch.MiniMax(),
        gameSearch.AlphaBeta(),
    ]
}

games['hardest'] = {
    'evaluation' : 'table',
    'instances' : instances[-2:],
    'players' : [   # Only use the best method on hard instances.
        gameSearch.AlphaBeta(6),
    ]
}

games['fun'] = {
    'evaluation' : 'play',
    'instance' : RenameThisGame(),
    'players' : [   # uncomment two  Players
        gameSearch.Query('Aaron'),
        gameSearch.Random(),            # Add seed in ()'s for a repeatable game
        # gameSearch.MiniMax(),         # Add horizon in ()'s if != 4
        # gameSearch.AlphaBeta(),       # Add horizon in ()'s if != 4
        # gameSearch.Query('Aamy'),
    ]
}

###################################################

# Modules in the examples folder
# Import them for testing only.
#
from examples import aimaTTT
name = aimaTTT.name
games = aimaTTT.games
#
# from examples import tictactoe
# name = tictactoe.name
# games = tictactoe.games
