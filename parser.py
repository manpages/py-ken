from pprint import pprint
import sys
sys.path.append('.')
from reader import read
from validator import isSolved
from simpleSolver import solve

def parseGame(input):
  return dict( { 'cells':      parseCells(input),
                 'cages':      parseCages(input),
                 'dimension':  dimension(input)
               })

##########################################################################

def parseCages(input):
  inputList  = input.split('\n\n')
  return parseOperations( parseCagesMap( inputList[0] ),
                                         inputList[1] )
def parseCagesMap(mapBlock):
  mapBlock1 = mapBlock.split('\n')
  mapBlock1.reverse()
  return parseCagesMapDo(mapBlock1, dimension(mapBlock), {})
def parseCagesMapDo(lines, n, acc):
  if n == 0:
    return acc
  (head, tail) = (lines[0], lines[1:])
  for x in range(0, len(head)):
    if head[x] not in acc:
      acc[head[x]] = { 'cells': [], 'op': '???', 'targetValue': '???' }
    acc[head[x]]['cells'].append((x, n-1))
  return parseCagesMapDo(tail, n-1, acc)

def parseOperations(cagesDict, operationBlock):
  return parseOperationsDo(operationBlock.split('\n'), cagesDict)
def parseOperationsDo(ops, acc):
  if len(ops) == 0:
    return acc
  (head, tail) = (ops[0], ops[1:])
  operationDefinition = head.split(' ')
  cageId          = operationDefinition[0]
  op              = operationDefinition[1]
  targetValue     = operationDefinition[2]
  acc[cageId]['op']          = op
  acc[cageId]['targetValue'] = int(targetValue)
  return parseOperationsDo(tail, acc)

def parseCells(input):
  solutionMaybe = solution(input)
  if solutionMaybe:
    return solutionMaybe
  else:
    return latinSquare(dimension(input))

def dimension(input):
  return len(input.split('\n')[0])

def solution(input):
  inputList = input.split('\n\n')
  if len(inputList) >= 4:
    return solutionDo(inputList[3].split('\n'), 
                      0,
                      {})

def solutionDo(solutionBlock, y, acc):
  if len(solutionBlock) == 0:
    return acc
  (head, tail) = (solutionBlock[0], solutionBlock[1:])
  for x in range(0, len(head)):
    acc[(x,y)] = int(head[x])
  return solutionDo(tail, y + 1, acc)

def latinSquare(n):
  ls = latinSquareDo(n, range(1, n+1), {})
  return ls

def latinSquareDo(n, sample, acc):
  if n == 0:
    return acc
  for x in range(0, len(sample)):
    acc[(x,n-1)] = sample[x]
  return latinSquareDo(n-1, shiftDo(sample), acc)

def shiftDo(xs):
  return xs[1:] + [xs[0]]

if __name__ == '__main__':
  parsed = parseGame(read(sys.argv[1]))
  pprint(parsed)
  solved = solve(parsed)
  pprint(solved)
  pprint(isSolved(solved))
