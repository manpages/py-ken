import functools
from itertools import permutations
from pprint import pprint
import sys
from math import sqrt
sys.path.append('.')

def isSolved(game):
  for v in game['cages']:
    cage = game['cages'][v]
    if not isSolvedCage(cage, game['cells']):
      return False
  for i in range(0, game['dimension']):
    if not rowComplies(game['cells'], game['dimension'], i):
      return False
    if not colComplies(game['cells'], game['dimension'], i):
      return False
  return True

##########################################################################

def rowComplies(gameCells, n, y):
  rowValues = getRowValues(gameCells, y)
  for i in range(1, n):
    if i not in rowValues:
      return False
  return True

def colComplies(gameCells, n, x):
  colValues = getColValues(gameCells, x)
  for i in range(1, n):
    if i not in colValues:
      return False
  return True

def isSolvedCage(cage, gameCells):
  targetValue = int(cage['targetValue'])
  f = opToFunction(cage['op'])
  if isCommutative(cage['op']):
    return myReduce(cage['cells'], gameCells, f) == targetValue
  else:
    return targetValue in permuteReduce(cage['cells'], gameCells, f)

def myReduce(cageCellAddresses, gameCells, f):
  cellValues = getCellValues(cageCellAddresses, gameCells)
  if (len(cellValues) == 0):
    return []
  return functools.reduce(f, cellValues[1:], cellValues[0])

def permuteReduce(cageCellAddresses, gameCells, f):
  def reductor(tup):
    xs = list(tup)
    if (len(xs) == 0):
      return []
    return functools.reduce(f, xs[1:], xs[0])
  cellValuesPerm = permutations(getCellValues(cageCellAddresses, gameCells))
  return list(map(reductor, cellValuesPerm))

def getCellValues(cageCellAddresses, gameCells):
  cellValues = []
  for (x,y) in cageCellAddresses:
    if type(gameCells[(x,y)]) is int:
      cellValues.append(gameCells[(x,y)])
  return cellValues

def getColValues(gameCells, x):
  result = []
  for (cX,cY) in gameCells:
    if cX == x:
      if type(gameCells[(cX,cY)]) is int:
        result.append(gameCells[(cX, cY)])
  return result

def getRowValues(gameCells, y):
  result = []
  for (cX,cY) in gameCells:
    if cY == y:
      if type(gameCells[(cX,cY)]) is int:
        result.append(gameCells[(cX, cY)])
  return result

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
