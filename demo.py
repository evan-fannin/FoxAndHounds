#!/usr/local/bin/python3
import traceback
from inspect import signature
from math import inf, log, log2, trunc
import importlib
import sys
import re

import gameSearch
import utils
from grading.util import print_table

def help():
    print('''
    usage: %s [-s] [-p] [-t] [-g]
        -s: Toggle error skipping (from False)
        -p: Toggle game play (from True)
        -t: Toggle minimax and alpha-beta tests (from True)
        -g: Grading mode (skip errors, don't play)
    ''' % sys.argv[0])
    sys.exit(0)

skipErrors = False
playGames = True
testTrees = True
argc = len(sys.argv)
if (argc > 1):
    for arg in sys.argv[1:argc]:
        if arg == '-h':
            help()
        if arg == '-s':
            skipErrors = not skipErrors
        if arg == '-p':
            playGames = not playGames
        if arg == '-t':
            testTrees = not testTrees
        if arg == '-g':
            skipErrors = True
            playGames = False

rubric = [
    ('compiles', 50),
    ('oneWin', 10),
    ('oneLoss', 5),
    ('onePlyfromWin', 5),
    ('onePlyfromLoss', 5),
    ('2plys', 2),
    ('3plys', 2),
    ('4plys', 2),
    ('6plys', 2),
    ('8plys', 2),
    ('12plys', 2),
    ('16plys', 2),
    ('5percent', 5),
    ('10percent', 5),
    ('2pushes', 5),
    ('3pushes', 5),
]
rNames = [pair[0] for pair in rubric]
rPoints = {pair[0]:pair[1] for pair in rubric}

def add(a, b):
    return sum((a, b))

# accumulation methods
accuMethods = {pair[0]: max for pair in rubric}
accuMethods['allMethods'] = add
accuMethods['heuristic'] = min

def newScores():
    s = {}
    for pair in rubric:
        label = pair[0]
        s[label] = 0
    # s['heuristic'] = rPoints['heuristic']
    return s

def assignFullCredit(sd, key):
    sd[key] = rPoints[key]

def partialCredit(key, minx, maxx, x):
    maxpoints = rPoints[key]
    return max(0,
        min(maxpoints,
            (x-minx) * maxpoints/(maxx-minx)))

outcomes = {
    # depth: {(player, outcome)} unique tuples, e.g.
    # 0: {('X', 'win'), ('O', 'win')},
}

plyMap = {
    0: ['oneWin', 'oneLoss'],
    1: ['onePlyfromWin', 'onePlyfromLoss'],
    2: ['2plys'],
    3: ['3plys'],
    4: ['4plys'],
    5: ['4plys'],
    6: ['6plys'],
    7: ['6plys'],
}
plyMap.update({n: ['8plys'] for n in range(8,12)})
plyMap.update({n: ['12plys'] for n in range(12,16)})

def assignDepthCredit(score, depth, p2uple):
    if depth not in plyMap:
        assignFullCredit(score, '16plys')
    else:
        labels = plyMap[depth]
        if len(labels) == 1:
            assignFullCredit(score, labels[0])
        elif depth not in outcomes:
            assignFullCredit(score, labels[0])
            outcomes[depth] = {p2uple}
        elif p2uple not in outcomes[depth]:
            assignFullCredit(score, labels[1])
            outcomes[depth].update({p2uple})

def scoreList(scores):
    unlabeled = []
    for pair in rubric:
        label = pair[0]
        if label in scores:
            unlabeled.append(scores[label])
        else:
            unlabeled.append(0)
    return unlabeled

comments = []
def addComment(comment):
    global comments
    comments += [comment]

baseSearchList = [
    gameSearch.minimax_decision,
    gameSearch.alphabeta_search,
]

def gradeGame(player, igame, depth, utility):
    info = {}
    score = newScores()
    assignFullCredit(score, 'compiles')
    game = igame.game
    initial = game.initial
    done = game.terminal_test(initial)
    p2move = game.to_move(initial)
    if utility > 0:
        outcome = 'win'
    elif utility < 0:
        outcome = 'loss'
    else:
        outcome = 'tie'
    p2uple = (p2move, outcome)
    assignDepthCredit(score, depth, p2uple)
    # if searcher in standardSearchList:
    #     score['allMethods'] = partialCredit(
    #         'allMethods', 0, len(standardSearchList), 1)
    # admissible, consistent = aAndC(Game, goalNode)
    # sum = admissible + consistent
    # score['heuristic'] = partialCredit('heuristic', 0, 2, sum)
    # if depth == 2:
    #     assignFullCredit(score, '2actions')
    # elif depth > 2:
    #     logDepth = trunc(log2(depth))
    #     minLDI = rNames.index('4-7actions')
    #     maxLDI = rNames.index('64+actions')
    #     LDIndex = minLDI + logDepth - 2
    #     LDIndex = max(minLDI, min(maxLDI, LDIndex))
    #     lBName = rNames[LDIndex]
    #     assignFullCredit(score, lBName)
    # breadth = Game.states
    # logBreadth = trunc(log2(breadth)/2)
    # minLBI = rNames.index('1-3nodes')
    # maxLBI = rNames.index('65536+nodes')
    # LBIndex = minLBI + logBreadth - 1
    # LBIndex = max(minLBI, min(maxLBI, LBIndex))
    # lBName = rNames[LBIndex]
    # assignFullCredit(score, lBName)
    #
    info['score'] = score
    return info

def compare_searchers(games, header,
                      # searchers=[]
                      players=[]
                      ):
    best = {}
    bestNode = {}
    gradeInfo = {}
    for g in games:
        best[g.label] = -inf
        bestNode[g.label] = None
    # def do(searcher, game):
    def do(player, game):
        nonlocal best, bestNode, gradeInfo
        igame = gameSearch.InstrumentedGame(game)
        try:
            ipLabel = igame.label
            if not ipLabel in gradeInfo:
                gradeInfo[ipLabel] = {}
            # utility, bestMoves = searcher(igame)
            utility, bestMoves = player.search(igame)
            depth = len(bestMoves)
            game.predicted_utility = utility
            game.bestMoves = bestMoves
            if len(bestMoves) > 0:
                nextMove = bestMoves[0]
            else:
                nextMove = None
            # gradeInfo[ipLabel][searcher] = \
            #     gradeGame(searcher, igame, utility)
            gradeInfo[ipLabel][player] = \
                gradeGame(player, igame, depth, utility)
            initial = igame.game.initial
            # utility = igame.utility(initial)
            if utility > best[ipLabel]:
                best[ipLabel] = utility
                bestNode[ipLabel] = initial
            return igame, utility, nextMove
        except Exception as e:
            if skipErrors:
                return igame, -inf, None
            print('Game "%s" raised an exception:' % g.label)
            traceback.print_exc()
            print(e)
            sys.exit(1)

    # table = [[utils.name(s)] + [do(s, p) for p in games]
    #          for s in searchers]
    table = [[str(p)] + [do(p, g) for g in games]
             for p in players]
    print_table(table, header)
    print('----------------------------------------')
    for g in games:
        # bestPath = []
        # node = bestNode[g.label]
        # while node != None:
        #     bestPath.append(node.state)
        #     node = node.parent
        summary = 'Best Moves for %s: %s' % (g.label, g.bestMoves)
        # ppFun = getattr(p, "prettyPrint", None)
        # if ppFun == None:
        #     ppFun = str
        # ppSep = ' '
        # pathLength = len(bestPath)
        # if pathLength > 0:
        #     stateLength = len(ppFun(bestPath[0]))
        #     if pathLength * stateLength > 100:
        #         ppSep = "\n"
        # for state in reversed(bestPath):
        #     summary += ppSep + ppFun(state)
        print(summary)
    print('----------------------------------------')
    return gradeInfo

def wellFormed(game):
    if not hasattr(game, 'initial'):
        print('Game "' + game.label + '" has no initial state.')
        return False

    if not hasattr(game, 'actions'):
        print('Game "' + game.label + '" has no actions() method.')
        return False
    gasig = signature(game.actions)
    if len(gasig.parameters) != 1:
        print('in Game "' + game.label + '",')
        print('  actions(...) has the wrong number of parameters.  Define it as:')
        print('  def actions(self, state):')
        return False

    if not hasattr(game, 'result'):
        print('Game "' + game.label + '" has no result() method.')
        return False
    grsig = signature(game.result)
    if len(grsig.parameters) != 2:
        print('in Game "' + game.label + '",')
        print('  result(...) has the wrong number of parameters.  Define it as:')
        print('  def result(self, state, action):')
        return False

    if not hasattr(game, 'utility'):
        print('Game "' + game.label + '" has no utility() method.')
        return False
    gusig = signature(game.utility)
    if len(gusig.parameters) != 2:
        print('in Game "' + game.label + '",')
        print('  utility(...) has the wrong number of parameters.  Define it as:')
        print('  def utility(self, state, player):')
        return False

    if not hasattr(game, 'terminal_test'):
        print('Game "' + game.label + '" has no terminal_test() method.')
        return False
    gtsig = signature(game.terminal_test)
    if len(gtsig.parameters) != 1:
        print('in Game "' + game.label + '",')
        print('  terminal_test(...) has the wrong number of parameters.  Define it as:')
        print('  def terminal_test(self, state):')
        return False
    return True

def getPlayers():
    def playerHelp():
        for line in [
            'Valid player specifications are:',
            '   Query or Query("name")',
            '   Random or Random(seed)',
            '   MiniMax or MiniMax(d), the search depth.',
            '   AlphaBeta or AlphaBeta(d), the search depth.',
        ]:
            print(line)

    def getPlayer(prompt, human):
        commands = {utils.name(s).lower() : utils.name(s)
                    for s in gameSearch.Player.__subclasses__()}
        commands.update({'quit': 'Quit', 'help':'Help'})
        parens = r'\([^(]*\)'

        if human == True:
            s = 'Query("Human")'
        else:
            s = 'AlphaBeta(8)'

        while True:
            # s = input(prompt)
            c = re.sub(parens,'',s)
            # s = s[0].upper() + s[1:].lower()
            if c.lower() not in commands:
                print(('"%s" should be a player specification,'
                + '"quit", or "help".') % c)
                playerHelp()
                continue
            d = commands[c.lower()]
            s = s.replace(c, d)
            if s == 'Quit':
                return None
            if s == 'Help':
                playerHelp()
                continue
            if '(' not in s:
                s = s + '()'
            try:
                t = 'gameSearch.' + s
                p = eval(t)
                return p
            except:
                print('"%s" is not a valid player.' % t)
                playerHelp()

    print('Does anyone want to play?')
    # print('Enter players, "help", or "quit":')
    choice = input("Type 'fox' to play fox, 'hounds' to play hounds, or 'observe'"
                   " to watch a match:  ")
    if choice == 'fox':
        p1 = getPlayer("", True)
        p2 = getPlayer('', False)
        return p1, p2

    if choice == 'hounds':
        p1 = getPlayer("", False)
        p2 = getPlayer('', True)
        return p1, p2

    if choice == 'observe':
        p1 = getPlayer("", False)
        p2 = getPlayer('', False)
        return p1, p2

    print("Bad input.")
    print()
    print()
    getPlayers()

def playGame(batch):
    instance = batch['instance']
    # players = batch['players']
    while True:
        instance.display(instance.initial)
        players = getPlayers()
        if players == None:
            break
        for p in players:
            p.setGame(instance)
        util = gameSearch.play_game(instance, players)
        if util > 0:
            outcome = 'won'
        elif util < 0:
            outcome = 'lost'
        else:
            outcome = 'tied'
        print('%s %s against %s, util = %f'
              % (players[0], outcome, players[1], util))

modName = 'games'

try:
    # http://stackoverflow.com/a/17136796/2619926
    mod = importlib.import_module(modName)
except:
    # print(RenameThisCollection.py is missing or defective.')
    traceback.print_exc()
    sys.exit(1)

scores = {}
# searchMethods = {}
players = {}
gradeInfo = {}
name = mod.name
games = {}

for batch in mod.games:
    messages = ['      Searches for %s: ' % (batch),
                'Search methods for %s: ' % (batch)]
    try:
        evaluation = mod.games[batch]['evaluation']
    except:
        print('games["%s"]["evaluation"] is missing or defective.'
              % (batch))
        if not skipErrors:
            sys.exit(1)
    if evaluation == 'play':
        if not playGames:
            continue
        try:
            playGame(mod.games[batch])
        except:
            print('games["%s"] failed during play:' % (batch))
            traceback.print_exc()
            if not skipErrors:
                sys.exit(1)
        finally:
            print('----------------------------------------')
        continue

    try:
        games[batch] = mod.games[batch]['instances']
        searchLabels = [s.label for s in games[batch]]
        messages[0] += '%s' % (searchLabels)
    except:
        print('games["%s"]["instances"] are missing or defective.'
              % batch)
        if not skipErrors:
            sys.exit(1)
    try:
        # searchMethods[batch] = mod.games[batch]['methods']
        # methodNames = [m.__name__ for m in searchMethods[batch]]
        # if len(searchMethods[batch]) > 0:
        #     messages[1] += '%s' % (methodNames)
        players[batch] = mod.games[batch]['players']
        messages[1] += str(players[batch])
    except:
        print('games["%s"]["players"] are missing or defective.'
              % batch)
        if not skipErrors:
            sys.exit(1)

    for m in messages:
        print(m)
    print('----------------------------------------')

    if not batch in games.keys():
        continue
    scores[batch] = []
    # searchList = []
    # if batch in searchMethods:
    #     searchList += searchMethods[batch]
    playerList = []
    if batch in players:
        playerList += players[batch]
        # for s in searchMethods[student]:
        #     searchList.append(s)
    try:
        glist = games[batch]
        hlist = [[batch], ['']]
        i = 0
        for game in glist:
            if not wellFormed(game):
                continue
            try:
                hlist[0].append(game.label)
            except:
                game.label = 'Game ' + str(i)
                hlist[0].append(game.label)
            i += 1
            headings = gameSearch.InstrumentedGame(game).headings()
            hlist[1].append('(%s, util, move)' % headings)
        gradeInfo[batch] = compare_searchers(
            games=glist,
            header=hlist,
            # searchers=searchList
            players=playerList
        )
    except:
        traceback.print_exc()
        sys.exit(1)


allScores = newScores()
maxScores = {}
for batch in gradeInfo:
    print('Scores for: %s' % batch)
    maxScores[batch] = {}
    for pLabel in gradeInfo[batch]:
        table = []
        maxScores[batch][pLabel] = newScores()
        for searcher in gradeInfo[batch][pLabel]:
            sLabel = utils.name(searcher)
            info = gradeInfo[batch][pLabel][searcher]
            scoreSet = info['score']
            table.append(['%s, %s:' % (sLabel, pLabel),
                          scoreList(scoreSet)])
            for label in scoreSet:
                accumulator = accuMethods[label]
                maxScores[batch][pLabel][label] = accumulator(
                    maxScores[batch][pLabel][label], scoreSet[label])
        if len(table) > 1:
            table.append(['%s summary:' % (pLabel),
                          scoreList(maxScores[batch][pLabel])])
        print_table(table)
        if len(table) > 1:
            print()
        for label in allScores:
            allScores[label] \
                = max(allScores[label], maxScores[batch][pLabel][label])

realName = mod.name
sl = [int(round(x)) for x in scoreList(allScores)]
print(realName, 'summary:', str(sl))
print(realName, '  total:', str(min(100, sum(sl))))
