import sys
sys.path.append('.')
import functools
from pprint import pprint
from validator import isSolved, getColValues, getRowValues, getCellValues, isSolvedCage

def solve(game):
  return solveDo(game, [candidates0(game)])

def solveDo(game, xss):
  solutionMaybe = xss2game(xss, game)
  if isSolved(solutionMaybe):
    return solutionMaybe
  if contradicts(solutionMaybe):
    return solveDo(game, removeCandidate(xss))
  else:
    return solveDo(game, addCandidates(xss, game))

def removeCandidate(xss):
  xss[-1].pop(0)
  if len(xss[-1]) == 0:
    return removeCandidate(xss[:-1])
  return xss

def addCandidates(xss, game):
  xss.append(candidates0(game))
  return xss

def xss2game(xss, game):
  def n2xy(n):
    return divmod(n - 1, game['dimension'])
  game = annul(game)
  i = 1
  for xs in xss:
    game['cells'][n2xy(i)] = xs[0]
    i = i + 1
  return game

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
