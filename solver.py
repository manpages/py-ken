import functools
from itertools import permutations
from pprint import pprint
import sys
from validator import isSolved, isSolvedCage, getColValues, getRowValues, getCellValues
sys.path.append('.')

def solve(game):
  return solveDo(initialPartial(game))

##########################################################################

def solveDo(partial):
  pprint(partial)
  if isSolved(partial):
    return partial
  partial1 = solveEasiest(partial)
  if not partial1:
    return False
  return solveDo(partial1)

def solveEasiest(game):
  cid = easiestCageId(game)
  return solveEasiestDo(game, cid)

def solveEasiestDo(game, cid):
  # Here we need to bruteforce the tree of candidates
  # and return False if the cage is unsolvable.
  # For instance, if we have three lists of candidates
  # (0,0) -> [ 1, 2, 3 ]
  # (0,1) -> [ 2, 3, 4 ]
  # (1,0) -> [ 1, 5, 6, 7 ]
  # And the solution is 2, 3, 6
  # we, just brute force tree of possibilities, taking
  # legality of game state into the consideration, at every
  # step of brute force. So that we don't check solution 1, 2, 1
  # or 2, 2, 7.
  "???"

def easiestCageId(game):
  # The easiest cage is the one
  # that has the least amount of
  # candidates.
  "???"

def initialPartial(game):
  return recalculate(annul(game))

def annul(game):
  for x in game['cells']:
    game['cells'][x] = None
  return game

def recalculate(game):
  game = recalculateXY(game)
  game = recalculateCages(game)
  return fix(game)

def fix(game):
  cs = game['cells']
  for k in cs:
    if type(cs[k]) is list:
      if len(cs[k]) == 0:
        return False
      if len(cs[k]) == 1:
        cs[k] = cs[k][0]
  return game

def recalculateCages(game):
  for cid in game['cages']:
    game = recalculateCage(cid, game)
  return game

def recalculateCage(cid, game):
  cage        = game['cages'][cid]
  cells       = cage['cells']
  op          = cage['op']
  targetValue = cage['targetValue']
  dimension   = game['dimension']
  cageSize    = len(cage['cells'])
  candidates  = cageCandidates(op, cageSize, targetValue, dimension)
  fixedPoints = getCellValues(cells, game['cells'])
  for (x,y) in cells:
    if game['cells'][(x,y)] == None:
      game['cells'][(x,y)] = candidates
    if type(game['cells'][(x,y)]) is list:
      game['cells'][(x,y)] = list(set.intersection(set(game['cells'][(x,y)]), set(candidates)))
      game['cells'][(x,y)] = [ x for x in game['cells'][(x,y)] if x not in fixedPoints ]
  return game

def cageCandidates(op, cageSize, targetValue, dimension):
  if cageSize == 1:
    if targetValue > dimension:
      raise Exception("[A] Can't assert values larger than dimension")
    return [targetValue]
  if op == '-':
    return minusCandidates(cageSize, targetValue, dimension)
  if op == '+':
    return plusCandidates(cageSize, targetValue, dimension)
  if op == '*':
    return timesCandidates(cageSize, targetValue, dimension)
  if op == '/':
    return overCandidates(cageSize, targetValue, dimension)

def minusCandidates(cageSize, targetValue, dimension):
  if targetValue > dimension:
    raise Exception("[-] Target value should be less or equal to dimension")
  result = []
  for i in range(1, dimension+1):
    if cageSize >= i + targetValue:
      result.append(i)
  return result

def plusCandidates(cageSize, targetValue, dimension):
  if targetValue <= 0:
    raise Exception("[+] Gonna be hard to add several positive numbers and get a non-positive one :/")
  if(cageSize > targetValue):
    raise Exception("[+] You're making me add N+K positive numbers to get N. To work with negative quantities, you need an anti-matter computer.")
  result = []
  for i in range(1, targetValue-cageSize):
    result.append(i)
  return result

def timesCandidates(cageSize, targetValue, dimension):
  return range(1, dimension + 1)

def overCandidates(cageSize, targetValue, dimension):
  return range(1, dimension + 1)

def recalculateXY(game):
  used = { 'cols': [], 'rows': [] }
  for i in range(0, game['dimension']):
    used['cols'].append( getColValues(game['cells'], i) )
    used['rows'].append( getRowValues(game['cells'], i) )
  for (x,y) in game['cells']:
    cs = game['cells'][(x,y)]
    if type(cs) is list:
      game['cells'][(x,y)] = [ c for c in cs if c not in used['cols'][x] ]
      cs                   = game['cells'][(x,y)]
      game['cells'][(x,y)] = [ c for c in cs if c not in used['rows'][y] ]
  return game
