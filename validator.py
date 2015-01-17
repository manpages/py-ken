import functools
from itertools import permutations
from pprint import pprint
import sys
from math import sqrt
sys.path.append('.')

def isSolved(game):
  #pprint(game)
  for v in game['cages']:
    cage = game['cages'][v]
    #pprint('Testing cage ' + v)
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
  #pprint({ 'Testing row ' + str(y): rowValues})
  for i in range(1, n):
    if i not in rowValues:
      return False
  return True

def colComplies(gameCells, n, x):
  #pprint('Testing col ' + str(x))
  colValues = getColValues(gameCells, x)
  for i in range(1, n):
    if i not in colValues:
      return False
  return True

def isSolvedCage(cage, gameCells):
  pprint({ 'TestingCage': cage })
  targetValue = int(cage['targetValue'])
  if isCommutative(cage['op']):
    return myReduce(cage['cells'], gameCells, opToFunction(cage['op'])) == targetValue
  else:
    return targetValue in permuteReduce(cage['cells'], gameCells, opToFunction(cage['op']))

def myReduce(cageCellAddresses, gameCells, f):
  cellValues = getCellValues(cageCellAddresses, gameCells)
  return functools.reduce(f, cellValues, 0)

def permuteReduce(cageCellAddresses, gameCells, f):
  cellValuesPerm = permutations(getCellValues(cageCellAddresses, gameCells))
  pprint(cellValuesPerm)
  return map(lambda x: functools.reduce(f, x), cellValuesPerm)

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
