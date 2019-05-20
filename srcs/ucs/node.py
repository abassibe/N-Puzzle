#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import numpy as np

class Node(object):
    def __init__(self, currentState, goalState, gScore, parentHash):
        self.currentState = currentState
        self.gScore = gScore
        self.parentHash = parentHash
        self.gScore = gScore
        self.isSorted = True if np.count_nonzero(goalState - self.currentState) == 0 else False
        