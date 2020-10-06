"""Games, or Adversarial Search (Chapter 5)"""

import random, sys
import time

infinity = float('inf')

# ______________________________________________________________________________
# Minimax Search


def minimax_decision(game, state=None, d=4):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""
    if state == None:
        state = game.initial
    player = game.to_move(state)

    def max_value(state, depth):
        if depth > d or game.terminal_test(state):
            return game.utility(state, player), []
        v = -infinity
        vpath = []
        for a in game.actions(state):
            u, path = min_value(game.result(state, a), depth + 1)
            if u > v:
                v = u
                vpath = [a] + path
        return v, vpath

    def min_value(state, depth):
        if depth > d or game.terminal_test(state):
            return game.utility(state, player), []
        v = infinity
        vpath = []
        for a in game.actions(state):
            u, path = max_value(game.result(state, a), depth + 1)
            if u < v:
                v = u
                vpath = [a] + path
        return v, vpath

    # Body of minimax_decision:
    # return argmax(game.actions(state),
    #               key=lambda a: min_value(game.result(state, a), 1))
    # return max_value(state, 0)
    mv, ma =  max_value(state, 0)
    return mv, ma

# ______________________________________________________________________________

def alphabeta_search(game, state=None, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    if state == None:
        state = game.initial
    player = game.to_move(state)

    def def_cutoff_test(state, depth):
        if depth > d:
            return True
        return game.terminal_test(state)
    cutoff_test = cutoff_test or def_cutoff_test

    def def_eval_fn(state):
        return game.utility(state, player)
    eval_fn = eval_fn or def_eval_fn

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state), []
        v = -infinity
        vpath = []
        for a in game.actions(state):
            u, path = min_value(game.result(state, a),
                          alpha, beta, depth + 1)
            if u > v:
                v = u
                vpath = [a] + path
            if v >= beta:
                return v, []
            alpha = max(alpha, v)
        return v, vpath

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state), []
        v = infinity
        vpath = []
        for a in game.actions(state):
            u, path = max_value(game.result(state, a),
                          alpha, beta, depth + 1)
            if u < v:
                v = u
                vpath = [a] + path
            if v <= alpha:
                return v, []
            beta = min(beta, v)
        return v, vpath

    mv, ma = max_value(state, -infinity, infinity, 0)
    return mv, ma

# ______________________________________________________________________________
# Players, Object Oriented version

class Player:
    game = None

    def setGame(self, game):
        self.game = game

    def checkGame(self):
        if self.game == None:
            raise Exception("You must specify {... 'instance': gameInstance, ...}")

    def move(self, state):
        "Return a valid move"
        raise NotImplementedError

    def eval(self, game):
        "Evaluate a game instance"
        raise NotImplementedError

class Query(Player):
    "Make a move by querying standard input."
    def __init__(self, name='Chump'):
        self.name = name[0].upper() + name[1:].lower()
        self.helped = False

    def help(self):
        print('To print the current state, enter "board".')
        print('For a list of legal moves, enter "moves".')
        self.helped = True

    def move(self, state):
        self.checkGame()
        if not self.helped:
            self.help()
        while True:
            legalMoves = self.game.actions(state)
            while True:
                move_string = input('Your move, %s: ' % self.name)
                if move_string == 'board':
                    self.game.display(state)
                elif move_string == 'moves':
                    print('Moves must be entered exactly as shown.')
                    print('Legal moves are: %s' % str(legalMoves))
                else:
                    break
            try:
                move = eval(move_string)
            except NameError:
                move = move_string
            if move in legalMoves:
                break
            else:
                print('"%s" is not a legal move.' % str(move))
                self.help()
        return move

    def __str__(self):
        return 'Query("%s")' % self.name

class Random(Player):
    "A player that chooses a legal move at random."
    def __init__(self, seed=None):
        if seed == None:
            # produce an arbitrary 5-digit seed
            seed = time.clock_gettime_ns(time.CLOCK_UPTIME_RAW) \
                   % 90000 + 10000;
            # print('Reproduce this player with: Random(%s)' % str(seed))
        self.seed = seed
        random.seed(seed)

    def move(self, state):
        self.checkGame()
        return random.choice(self.game.actions(state))

    def __str__(self):
        return 'Random(%s)' % self.seed

class MiniMax(Player):
    def __init__(self, depth=4):
        self.depth = depth

    def move(self, state):
        self.checkGame()
        _ignore_, vpath = minimax_decision(self.game, state, self.depth)
        return (vpath + [None])[0]

    def search(self, game):
        util, vpath = minimax_decision(game, game.initial, self.depth)
        return util, vpath

    def __str__(self):
        return 'MiniMax(%d)' % self.depth

class AlphaBeta(Player):
    def __init__(self, depth=4, cutoff_test=None, eval_fn=None):
        self.depth = depth
        self.cutoff = cutoff_test
        self.eval = eval_fn

    def move(self, state):
        self.checkGame()
        _ignore_, vpath = \
            alphabeta_search(self.game, state, self.depth,
                             self.cutoff, self.eval)
        return (vpath + [None])[0]

    def search(self, game):
        util, vpath = alphabeta_search(game, game.initial, self.depth,
                             self.cutoff, self.eval)
        return util, vpath

    def __str__(self):
        desc = 'AlphaBeta(%d' % self.depth
        if self.cutoff != None:
            desc += ',c=' + str(self.cutoff)
        if self.cutoff != None:
            desc += ',f=' + str(self.eval)
        return desc + ')'

def play_game(game, players):
    """Play an n-person, move-alternating game."""
    state = game.initial
    while True:
        for player in players:
            if game.terminal_test(state):
                game.display(state)
                return game.utility(state, game.to_move(game.initial))
            move = player.move(state)
            print('%s moves %s.' % (str(player), (move)))
            state = game.result(state, move)

# ______________________________________________________________________________
# Some Sample Games


class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        "Return a list of the allowable moves at this point."
        raise NotImplementedError

    def result(self, state, move):
        "Return the state that results from making a move from a state."
        raise NotImplementedError

    def utility(self, state, player):
        "Return the value of this state to player."
        raise NotImplementedError

    def terminal_test(self, state):
        "Return True if this is a final state for the game."
        return not self.actions(state)

    def to_move(self, state):
        "Return the player whose move it is in this state."
        raise NotImplementedError

    def display(self, state):
        "Print or otherwise display the state."
        print(state)

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

# ______________________________________________________________________________
# Code to compare searchers on various games.


class InstrumentedGame(Game):

    """Delegates to a game, and keeps statistics."""

    def __init__(self, game):
        self.game = game
        self.initial = game.initial
        self.succs = self.terminal_tests = self.states = 0
        self.found = None

    def actions(self, state):
        self.succs += 1
        return self.game.actions(state)

    def result(self, state, action):
        self.states += 1
        return self.game.result(state, action)

    def utility(self, state, player):
        return self.game.utility(state, player)

    def terminal_test(self, state):
        self.terminal_tests += 1
        result = self.game.terminal_test(state)
        if result:
            self.found = state
        return result

    def to_move(self, state):
        return self.game.to_move(state)

    def __getattr__(self, attr):
        return getattr(self.game, attr)

    def headings(self):
        return '<succ/term/stat/play>'

    def __repr__(self):
        player = self.to_move(self.initial)
        return '<%4d/%4d/%4d/%4s>' % (self.succs, self.terminal_tests,
                                     self.states, str(player))
