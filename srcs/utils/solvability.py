import numpy as np

def getInversionCount(flattenState):
    inversionCount = 0
    i = 0
    arrayLen = len(flattenState)
    while i < arrayLen:
        if flattenState[i] == 0:
            i += 1
        j = i + 1
        while j < arrayLen:
            if flattenState[i] > flattenState[j] and flattenState[j] != 0:
                inversionCount += 1
            j += 1
        i += 1
    return inversionCount

def printUnsolvableCase(initialState, size):
    print("# This puzzle is unsolvable")
    print(size)
    print(initialState)

def checkSolvability(initialState, goalState, size, isDisplay):
    flattenState = np.ravel(initialState)
    flattenGoal = np.ravel(goalState)
    inversionStateCount = getInversionCount(flattenState)
    inversionGoalCount = getInversionCount(flattenGoal)
    if size % 2 == 0:
        inversionStateCount += np.where(initialState == 0)[0][0]
        inversionGoalCount += np.where(goalState == 0)[0][0]
    if inversionStateCount % 2 == inversionGoalCount % 2:
        return True
    if isDisplay == True:
        printUnsolvableCase(initialState, size)
    return False
    