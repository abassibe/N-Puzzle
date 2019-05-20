#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

"""__init__.py"""
from aStar.aStar import aStar
from greedyMulti.greedyMulti import greedyMulti
from ucs.ucs import ucs
from greedySearch.greedySearch import greedy
from utils.solvability import checkSolvability
from utils.randomGenerator import randomGeneration

import numpy as np
import argparse

def parseFile(path):
    initialState = np.array([])
    flatArray = ''
    try:
        puzzleFile = open(path, 'r')
    except FileNotFoundError:
        print('No such file or directory: ' + '\'' + path + '\'')
        exit()
    size = None
    for line in puzzleFile:
        if line.startswith('#') or line.startswith('\n'):
            continue
        if size == None:
            try:
                size = int(line)
                continue
            except ValueError:
                print('Value error: ' + '\'' + line + '\', size expected.')
                exit()
        if line.rfind('#') != -1:
            line = line[:line.rfind('#')] + line[line.rfind('\n'):]
        flatArray += line
    try:
        initialState = np.fromstring(flatArray, int, -1, ' ')
        initialState = np.reshape(initialState, (size, size))
    except ValueError:
        print('Value error')
        exit()

    _, indices = np.unique(initialState, True)
    if len(indices) != size * size:
        print('Error: Array values must be unique.')
        exit()
    i = 0
    while i < size * size:
        if i not in initialState:
            print('Error: Number is missing.')
            exit()
        i += 1
    return initialState, size

def goalStateGeneration(size):
    goalState = np.zeros(shape=(size, size), dtype=np.int32)
    i = 1
    x = 0
    y =  0
    xDepth = 0
    yDepth = 0
    nbrTiles = size * size
    while i != nbrTiles:
        goalState[y][x] = i
        if x < size - 1 and y == yDepth:
            x += 1
        elif y < size - 1 and x == size - 1:
            y += 1
            if x == size - 1 and y == size - 1:
                size -= 1
            if y == size:
                yDepth += 1
        elif y == size and x > xDepth:
            x -= 1
            if x == xDepth:
                xDepth += 1
        elif x == xDepth - 1 and y > yDepth:
            y -= 1   
        i += 1
    return goalState

parser = argparse.ArgumentParser(description='n-Puzzle solver.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-r", "--random", action="store_true", default=False, help="Create a random puzzle and try to solve it. (default True)")
parser.add_argument("-s", "--size", type=int, choices=range(3, 6), default=3, help="Choose a size for the randomly generated map. (default 3)")
parser.add_argument("-p", "--path", type=str, help="Path to the puzzle to solve.")
parser.add_argument("-a", "--algorithm", type=int, choices=[0, 1, 2], default=0, help="Select an algorithm (default A*):\n-0: A* (informed algorithm)\n-1: Uniform-Cost (non-informed algorithm)\n-2: Greedy search (informed algorithm)")
parser.add_argument("-e", "--heuristic", type=int, choices=[0, 1, 2], default=0, help="Select an heuristic for informed algorithm (default Manhattan distance): \n-0: Manhattan distance\n-1: Euclidean distance\n-2: Tiles out-of-place")
parser.add_argument("-v", "--graphicalView", action="store_true", default=False, help="Displays movements in a graphical interface.")

args = parser.parse_args()
size = args.size

goalState = goalStateGeneration(size)

if args.random == True and args.path != None:
    parser.print_help()
    exit()
elif args.path != None:
    initialState, size = parseFile(args.path)
    goalState = goalStateGeneration(size)
else:
    initialState = randomGeneration(size, goalState)

if size < 3 or size > 5:
    print('Size must be between 3 and 5 include.')
    exit()

if args.graphicalView == True and size > 4:
    print("Graphical view is only handled for size 3 and 4, sorry bro !")
    exit()

if checkSolvability(initialState, goalState, size, True) == False:
    exit()

if size > 3:
    greedyMulti(initialState, goalState, size, args.heuristic, args.graphicalView)

elif args.algorithm == 1:
    ucs(initialState, goalState, size, args.graphicalView)

elif args.algorithm == 2:
    greedy(initialState, goalState, size, args.heuristic, args.graphicalView)

else:
    aStar(initialState, goalState, size, args.heuristic, args.graphicalView)
