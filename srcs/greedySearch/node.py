#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np

class Node(object):
    def __init__(self, heuristic, currentState, goalState, size, parentHash):
        self.currentState = currentState
        self.parentHash = parentHash
        self.heuristic = heuristic
        self.hScore = self.__computH__(goalState, size)

    def __computH__(self, goalState, size):
        # Tiles-Out heuristic
        if self.heuristic == 2:
            return np.count_nonzero(goalState - self.currentState)
        
        # Euclidean heuristic
        elif self.heuristic == 1:
            total = 0
            x = 0
            y = 0
            while x < size:
                while y < size:
                    coordinates = np.where(goalState == self.currentState[y][x])
                    absXDistance = abs(coordinates[1][0] - x)
                    absYDistance = abs(coordinates[0][0] - y)
                    total += absXDistance if absXDistance >= absYDistance else absYDistance
                    y += 1
                y = 0
                x += 1
            return total

        # Manhattan heuristic
        else:
            total = 0
            x = 0
            y = 0
            while x < size:
                while y < size:
                    if self.currentState[y][x] == 0:
                        y += 1
                        continue
                    coordinates = np.where(goalState == self.currentState[y][x])
                    xToReach = coordinates[1][0]
                    yToReach = coordinates[0][0]
                    total += abs(xToReach - x)
                    total += abs(yToReach - y)
                    y += 1
                x += 1
                y = 0
            return total
