#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

"""__init__.py"""
from utils.printPath import printPath
from .node import Node
import numpy as np
from threading import Thread

closeList = {}
openList = np.array([])

class Child(Thread):
    def __init__(self, currentNode, goalState, closeList, heuristic, size):
        Thread.__init__(self)
        self.currentNode = currentNode
        self.goalState = goalState
        self.closeList = closeList
        self.heuristic = heuristic
        self.size = size

    def run(self):
        currentState = self.currentNode.currentState
        parentHash = hash(np.array2string(currentState))
        indexZero = np.where(currentState == 0)
        x = indexZero[1][0]
        y = indexZero[0][0]
        self.children = []
        if y > 0:
            childState = np.copy(currentState)
            childState[y - 1][x] = 0
            childState[y][x] = currentState[y - 1][x]
            if hash(np.array2string(childState)) not in self.closeList:
                self.children.append(Node(
                    self.heuristic, childState, self.goalState, self.size, self.currentNode.gScore + 1, parentHash))
        if y < self.size - 1:
            childState = np.copy(currentState)
            childState[y + 1][x] = 0
            childState[y][x] = currentState[y + 1][x]
            if hash(np.array2string(childState)) not in self.closeList:
                self.children.append(Node(
                    self.heuristic, childState, self.goalState, self.size, self.currentNode.gScore + 1, parentHash))
        if x > 0:
            childState = np.copy(currentState)
            childState[y][x - 1] = 0
            childState[y][x] = currentState[y][x - 1]
            if hash(np.array2string(childState)) not in self.closeList:
                self.children.append(Node(
                    self.heuristic, childState, self.goalState, self.size, self.currentNode.gScore + 1, parentHash))
        if x < self.size - 1:
            childState = np.copy(currentState)
            childState[y][x + 1] = 0
            childState[y][x] = currentState[y][x + 1]
            if hash(np.array2string(childState)) not in self.closeList:
                self.children.append(Node(
                    self.heuristic, childState, self.goalState, self.size, self.currentNode.gScore + 1, parentHash))


    def join(self):
        Thread.join(self)
        return self.children

def greedyMulti(initialState, goalState, size, heuristic, isVisual):
    global closeList
    global openList

    currentNode = Node(heuristic, initialState, goalState, size, 0, 0)  
    openList = np.append(openList, currentNode)
    maxOpen = openList.size

    while True:
        if currentNode.hScore == 0:
            break
        childNodes = []
        node1 = None
        node2 = None
        node3 = None
        node4 = None
        if openList.size > 0:
            node1 = openList[0]
            openList = np.delete(openList, 0)
            parentHash = hash(np.array2string(node1.currentState))
            closeList[parentHash] = node1
        if openList.size > 0:
            node2 = openList[0]
            openList = np.delete(openList, 0)
            parentHash = hash(np.array2string(node2.currentState))
            closeList[parentHash] = node2
        if openList.size > 0:
            node3 = openList[0]
            openList = np.delete(openList, 0)
            parentHash = hash(np.array2string(node3.currentState))
            closeList[parentHash] = node3
        if openList.size > 0:
            node4 = openList[0]
            openList = np.delete(openList, 0)
            parentHash = hash(np.array2string(node4.currentState))
            closeList[parentHash] = node4
        if node1 != None:
            t1 = Child(node1, goalState, closeList, heuristic, size)
            t1.start()
        if node2 != None:
            t2 = Child(node2, goalState, closeList, heuristic, size)
            t2.start()
        if node3 != None:
            t3 = Child(node3, goalState, closeList, heuristic, size)
            t3.start()
        if node4 != None:
            t4 = Child(node4, goalState, closeList, heuristic, size)
            t4.start()
        if node1 != None:
            childNodes += t1.join()
        if node2 != None:
            childNodes += t2.join()
        if node3 != None:
            childNodes += t3.join()
        if node4 != None:
            childNodes += t4.join()
        for child in childNodes:
            if len(openList) == 0:
                openList = np.insert(openList, 0, child)
                continue
            for i, currNode in enumerate(openList):
                if child.fScore <= currNode.fScore:
                    openList = np.insert(openList, i, child)
                    break
            if len(openList) - 1 == i:
                openList = np.insert(openList, i, child)
        if openList.size > maxOpen:
            maxOpen = openList.size
        currentNode = openList[0]
    printPath(currentNode, closeList, maxOpen, size, isVisual)
