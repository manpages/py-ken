import sys
sys.path.append('.')
import functools
from pprint import pprint
from validator import isSolved, getColValues, getRowValues, getCellValues, isSolvedCage

def solve(game):
  return tryNext(annul(game), candidates0(game), (0,0))

def tryNext(game, candidates, leftmostEmpty):
  if isSolved(game):
    return game
  if len(candidates) == 0:
    return False
  (head, tail) = (candidates[0], candidates[1:])
  game['cells'][leftmostEmpty] = head
  if contradicts(game):
    game['cells'][leftmostEmpty] = None
    return tryNext(game, tail, leftmostEmpty)
  else:
    return tryNext(game, candidates0(game), next(leftmostEmpty, game['dimension']))  
    
def contradicts(game):
  return contradictsRows(game) or contradictsCols(game) or contradictsCages(game)
  
def contradictsRows(game):
  for x in range(0, game['dimension']):
    if hasDuplicates(getRowValues(game['cells'], x)):
      return True
  return False
  
def contradictsCols(game):
  for x in range(0, game['dimension']):
    if hasDuplicates(getColValues(game['cells'], x)):
      return True
  return False
  
def contradictsCages(game):
  for cage in game['cages']:
    if contradictsCage(game['cages'][cage], game['cells']):
      return True
  return False
  
def contradictsCage(cage, gameCells):
  if cageHasNone(cage, gameCells):
    return False
  return not isSolvedCage(cage, gameCells)
  
def cageHasNone(cage, gameCells):
  for coord in cage['cells']:
    if gameCells[coord] is None:
      return True
  return False
    
def hasDuplicates(xs):
  seen = []
  for x in xs:
    if x in seen:
      return True
    seen.append(x)
  return False

def next((x, y), n):
  if x < (n - 1):
    return (x + 1, y)
  return (0, y + 1)
  
def candidates0(game):
  return range(1, game['dimension'] + 1)

def annul(game):
  for x in game['cells']:
    game['cells'][x] = None
  return game
