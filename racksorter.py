#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    racksorter.py
    ~~~~~~~~~~~

    Contains all logic to find fast solutions for sorting a rack
    by only moving one element at a time. See paper for details.

    :copyright: (c) 2017-2018 by Eicke Herbertz, Dominik Hilbers
    :license: MIT, see LICENSE for details

"""

import sys
import time
import itertools as it
from collections import deque
from copy import copy


FACTOR_TIME_X = 1.6
FACTOR_TIME_Y_UP = 3.1
FACTOR_TIME_Y_DOWN = 2.5
LOADING_COST = 4.8

xSize = 3
ySize = 3


def setDimensions(x, y):
    """
    :summary: Sets dimensions of the rack to work with
    :param int x: Number of columns of the rack
    :param int y: Number of rows in the rack

    """
    global xSize, ySize
    xSize = x
    ySize = y


def setTimeFactors(time_x, time_y_up, time_y_down, time_load):
    """
    :summary: Sets moving time factors for cost calculation
    :param float time_x: Movement time for one tile in X direction in seconds
    :param float time_y_up: Movement time for one tile in Y direction upward in seconds
    :param float time_y_down: Movement time for one tile in Y direction downward in seconds
    :param float time_load: Movement time to perform one load/unload cycle in seconds

    """
    global FACTOR_TIME_X, FACTOR_TIME_Y_UP, FACTOR_TIME_Y_DOWN, LOADING_COST
    FACTOR_TIME_X = time_x
    FACTOR_TIME_Y_UP = time_y_up
    FACTOR_TIME_Y_DOWN = time_y_down
    LOADING_COST = time_load


def findChains(stackl, debug=False):
    """
    :summary: Finds chains/cycles in permutation
    :param list stackl: Permutation to find chains in
    :param bool debug: Print chains to stderr
    :rtype: deque
    :return: deque of deques (one deque per chain)

    """
    found = set()
    # Find chains
    chains = deque()
    # for i, n in enumerate(stackl):
    for i, n in enumerate(stackl):
        # Once we have every field in a chain, we can stop
        if len(found) == len(stackl):
            break
        # if we still reach the end, the last field has the arbitrary index of
        # none (which could be replaced by -1 as well, which makes things
        # easier in python and already C++ compatible (TODO))
        if i == len(stackl) - 1:
            i = None
        # if current index is already in a chain, skip it
        if i in found:
            continue
        if debug:
            print(i, end="->", file=sys.stderr)
        # start the chain with the current index
        tchain = deque([i])
        # and add it to our found-set
        found.add(i)
        # now for the actual chain search
        while n != i:
            if debug:
                print(n, end="->", file=sys.stderr)
            # add current value to found-set
            found.add(n)
            # and left-append it to the chain (we are actually reverse-solving
            # this here)
            tchain.appendleft(n)
            # now n is the next index we want to look at, so set
            # n to the value of stack[n]. Also weird None special case
            n = stackl[n] if n is not None else stackl[-1]
        # okay, we found our n to be equal to the i we started with
        # (this is also the case if n was equal to i in the first place
        # in which case the chain would consist of the initial i only)

        # Now, if this is the chain containing None, bring it to the end
        # Also, left-append it to the list of chains so it's the first one
        # This makes the extra search for None in old solutionChain1 obsolete
        if None in tchain:
            tchain.rotate(-(tchain.index(None) + 1))
            chains.appendleft(tchain)
        else:
            chains.append(tchain)
        if debug:
            print("{}\nChain {} length {} at {} done {}/{}"
                  .format(n, len(chains), len(tchain), i, len(found),
                          len(stackl)), file=sys.stderr)
    return chains


def distance(a, b):
    """
    :summary: Distance/cost calculation
    :param int a: list index of first element
    :param int b: list index of second element
    :rtype: float
    :return: time needed to perform movement from a to b

    """
    if a is None:
        a = xSize * ySize - 1
    if b is None:
        b = xSize * ySize - 1
    a_row = a // xSize
    a_col = a % ySize
    b_row = b // xSize
    b_col = b % ySize
    # Upward movement?
    row_cost = abs(a_row - b_row) * FACTOR_TIME_Y_DOWN
    if a_row > b_row:
        row_cost = abs(a_row - b_row) * FACTOR_TIME_Y_UP
    col_cost = abs(a_col - b_col)
    return max(row_cost, col_cost) + LOADING_COST


def solutionChainAndCost(stack, chains, cost=0, path=[], startIdx=None):
    """
    :summary: Calculates primitive, static solution for given permutation
    :param list stack: the permutation to solve
    :param list chains: chains/cycles of the given permutation
    :param float cost: cost to prepend to the solution
    :param list path: path to prepend to the solution
    :param int startIdx: index of permutation to start first movement from
    :rtype: tuple(list, float)
    :return: tuple of complete solution list and it's cost

    """
    # first, remove all length one chains (those are already placed)
    realChainz = [c for c in chains if len(c) > 1]
    solutionChain = path
    totalDistance = 0
    # We are ready to start sorting now
    for i, chain in enumerate(realChainz):
        # Maybe append None?
        noneFlag = False
        if chain[-1] is not None:
            chain.append(chain[0])
            chain.append(None)
            noneFlag = True

        for j, n in enumerate(chain):
            # i is current chain
            # j is current index of chain
            # n is both the value to move and the target index
            # except when it isn't: when we had to append None
            # the target index is None for the very first element
            # n_j+1 is the source position of element n_j
            #
            # Assuming start on the first element of the first chain
            # there are two distance options there:
            # a) move element to correct position: dist(n_j+1, n_j)
            # b) move element to position None: dist(n_j+1, None)
            #    (if None had to be appended)
            # For every other chain, b is the only option
            #
            # For any other element, we have to add the distance from
            # the recent drop off position as well:
            # To move element n_j from position n_j+1 to position n_j,
            # we have to travel from n_j-1 were we stopped to n_j+1, first
            # so it's: dist(n_j-1, n_j+1) + dist(n_j+1, n_j)
            #
            # For the second element though, there is again another case
            # for when None had to be appended:
            # dist(None, n_j+1) + dist(n_j+1, n_j)
            #
            # Obviously, when reaching None as the last element, we break
            # and go to the next chain
            if n is None:
                startIdx = chain[j - 1]
                break
            elif j is 0 and noneFlag:
                totalDistance += distance(startIdx, chain[j + 1])
                totalDistance += distance(chain[j + 1], None)
            elif j is 0:
                totalDistance += distance(startIdx, chain[j + 1])
                totalDistance += distance(chain[j + 1], n)
            elif j is 1 and noneFlag:
                totalDistance += distance(None, chain[j + 1])
                totalDistance += distance(chain[j + 1], n)
            else:
                totalDistance += distance(chain[j - 1], chain[j + 1])
                totalDistance += distance(chain[j + 1], n)
            solutionChain.append(n)
    # Done with the chains
    solutionChain.append(None)
    return (solutionChain, cost + totalDistance)


def findShortestPath(stack):
    """
    :summary: Finds the shortest solution to sort the given permutation
    :param list stack: the permutation to solve
    :rtype: tuple(list, float)
    :return: tuple of complete solution list and it's cost

    """
    if len(stack) != xSize * ySize:
        print("Stack size doesn't match dimensions {},{}".format(xSize, ySize))
        print("Expected {}, got {}".format(xSize * ySize, len(stack)))
    else:
        start = time.time()
        shortestPath = findShortestPathRecursive(stack, 0, [], None)
        t = (time.time() - start) * 1000
        print("Shortest path is {} with {} steps".format(*shortestPath))
        print("Chains were: ", list(map(list, findChains(stack))))
        print("Finished in ", t, " milliseconds")
        return shortestPath


def findShortestPathRecursive(stack, cost, path, startIdx):
    """
    :summary: Recursive part of solution searching
    :param list stack: the permutation to solve
    :param float cost: cost to prepend to the solution
    :param list path: path to prepend to the solution
    :param int startIdx: index of permutation to start first movement from
    :rtype: tuple(list, float)
    :return: tuple of complete solution list and it's cost

    """
    chains = findChains(stack)
    realChains = [c for c in chains if len(c) > 1]
    if len(realChains) is 0:
        newPath = copy(path)
        newPath.append(None)
        return (newPath, cost)
    firstChainHasNone = realChains[0][-1] is None
    if firstChainHasNone:
        toTest = [realChains[0][0]]
    else:
        toTest = []
    chainsToTest = realChains[1:] if firstChainHasNone else realChains
    toTest += list(it.chain.from_iterable(chainsToTest))
    toTest = [t for t in toTest if t not in path]
    if len(toTest) is 0 or (len(toTest) is 1 and firstChainHasNone):
        return solutionChainAndCost(stack, chains, cost, path, startIdx)

    cheapestSolution = (path, 10000)
    for n in toTest:
        newStack = copy(stack)
        newPath = copy(path)
        newCost = cost
        pN = newStack.index(n)
        # print("Moving from {} to {} at {}".format(startIdx, n, pN))
        newCost += distance(startIdx, pN)
        pNone = newStack.index(None)
        # print("Moving {} from {} to {}...".format(n, pN, pNone))
        newCost += distance(pN, pNone)
        newStack[pNone], newStack[pN] = n, None
        newPath.append(n)
        if newCost > cheapestSolution[1]:
            continue
        result = findShortestPathRecursive(newStack, newCost, newPath, pNone)
        if result[1] < cheapestSolution[1]:
            # print("New cheapest solution cost {}:".format(result[1]))
            # print(result[0], result[1])
            cheapestSolution = result
    return cheapestSolution
