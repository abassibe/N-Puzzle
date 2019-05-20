#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

"""__init__.py"""
from utils.printPath import printPath
from .node import Node
import numpy as np

closeList = {}
openList = np.array([])

def createChildren(size, heuristic, goalState):
    global closeList
    global openList
    parentHash = hash(np.array2string(openList[0].currentState))
    closeList[parentHash] = openList[0]
    currentState = openList[0].currentState
    indexZero = np.where(currentState == 0)
    x = indexZero[1][0]
    y = indexZero[0][0]
    children = np.array([])
    if y > 0:
        childState = np.copy(currentState)
        childState[y - 1][x] = 0
        childState[y][x] = currentState[y - 1][x]
        if hash(np.array2string(childState)) not in closeList:
            children = np.append(children, Node(
                heuristic, childState, goalState, size, parentHash))
    if y < size - 1:
        childState = np.copy(currentState)
        childState[y + 1][x] = 0
        childState[y][x] = currentState[y + 1][x]
        if hash(np.array2string(childState)) not in closeList:
            children = np.append(children, Node(
                heuristic, childState, goalState, size, parentHash))
    if x > 0:
        childState = np.copy(currentState)
        childState[y][x - 1] = 0
        childState[y][x] = currentState[y][x - 1]
        if hash(np.array2string(childState)) not in closeList:
            children = np.append(children, Node(
                heuristic, childState, goalState, size, parentHash))
    if x < size - 1:
        childState = np.copy(currentState)
        childState[y][x + 1] = 0
        childState[y][x] = currentState[y][x + 1]
        if hash(np.array2string(childState)) not in closeList:
            children = np.append(children, Node(
                heuristic, childState, goalState, size, parentHash))
    openList = np.delete(openList, 0)
    return children

def greedy(initialState, goalState, size, heuristic, isVisual):
    global closeList
    global openList

    currentNode = Node(heuristic, initialState, goalState, size, 0)
    openList = np.append(openList, currentNode)
    maxOpen = openList.size

    while True:
        if currentNode.hScore == 0:
            break
        childNodes = createChildren(size, heuristic, goalState)
        for child in childNodes:
            if len(openList) == 0:
                openList = np.insert(openList, 0, child)
                continue
            for i, currNode in enumerate(openList):
                if child.hScore <= currNode.hScore:
                    openList = np.insert(openList, i, child)
                    break
            if len(openList) - 1 == i:
                openList = np.insert(openList, i, child)
        if openList.size > maxOpen:
            maxOpen = openList.size
        currentNode = openList[0]
    printPath(currentNode, closeList, maxOpen, size, isVisual)
