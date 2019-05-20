import numpy as np
import random
from .solvability import checkSolvability

def randomGeneration(size, goalState):
    listNumber = []
    sizeMax = size * size
    i = 0
    while i < sizeMax:
        listNumber.append(i)
        i += 1
    random.shuffle(listNumber)
    randomArray = np.array(listNumber)
    randomArray = np.reshape(randomArray, (size, size))
    if checkSolvability(randomArray, goalState, size, False) == False:
        return randomGeneration(size, goalState)
    return randomArray
