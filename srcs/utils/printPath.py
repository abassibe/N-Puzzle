#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
from .visualizer import Visualizer

def printPath(currentNode, closeList, maxOpen, puzzleSize, isVisual):
    finalCount = []
    while currentNode.parentHash != 0:
        finalCount.append(currentNode.currentState)
        currentNode = closeList[currentNode.parentHash]
    finalCount.append(currentNode.currentState)
    if isVisual == True:
        Visualizer(finalCount, puzzleSize)
    else:
        size = len(finalCount) - 1
        while size >= 0:
            i = 0
            while i < puzzleSize:
                j = 0
                while j < puzzleSize:
                    print("%-3d" % (finalCount[size][i][j]), end='')
                    j += 1
                print()
                i += 1
            print()
            size -= 1
        print('Complexity in size (Max node in Open list):', maxOpen)
        print('Complexity in time (Total node in Close list):', len(closeList))
        if len(finalCount) == 1:
            print('Solved in: 1 move')
        else:
            print('Solved in:', len(finalCount), 'moves')
