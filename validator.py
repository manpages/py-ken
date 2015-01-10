import functools
from itertools import permutations
from pprint import pprint
import sys
sys.path.append('.')

def isSolved(game):
  for v in game['cages']:
    cage = game['cages'][v]
    if not isSolvedCage(cage, game):
      return False
  return True

##########################################################################

def isSolvedCage(v, game):
  pprint('Testing')
  pprint(v)
  targetValue = int(v['targetValue'])
  pprint(targetValue)
  if isCommutative(v['op']):
    pprint('Under commutative operation')
    return myReduce(v['cells'], game, opToFunction(v['op'])) == targetValue
  else:
    pprint('Under non-commutative operation')
    return targetValue in transposeReduce(v['cells'], game, opToFunction(v['op']))

def myReduce(cells, game, f):
  cellValues = getCellValues(cells, game['cells'])
  pprint(cellValues)
  return functools.reduce(f, cellValues)

def transposeReduce(cells, game, f):
  cellValuesPerm = permutations(getCellValues(cells, game['cells']))
  return map(lambda x: functools.reduce(f, x), cellValuesPerm)

def getCellValues(cells, gameCells):
  cellValues = []
  for (x,y) in cells:
    cellValues.append(int(gameCells[(x,y)]))
  return cellValues

def isCommutative(x):
  if x == '+' or x == '*':
    return True
  else:
    return False

def opToFunction(x):
  if x == '+': return lambda a,b: a + b
  if x == '*': return lambda a,b: a * b
  if x == '-': return lambda a,b: a - b
  if x == '/': return lambda a,b: a / b
