#!/usr/bin/env python

import json
import itertools as it
from collections import deque
from copy import copy, deepcopy


def findChains(stackl, debug=False):
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
            print(i, end="->")
        # start the chain with the current index
        tchain = deque([i])
        # and add it to our found-set
        found.add(i)
        # now for the actual chain search
        while n != i:
            if debug:
                print(n, end="->")
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
                          len(stackl)))
    return chains


def distance(a, b):
    if a is None:
        a = 8
    if b is None:
        b = 8
    a_row = a // 3
    a_col = a % 3
    b_row = b // 3
    b_col = b % 3
    return max(abs(a_row - b_row), abs(a_col - b_col))


def solutionChainAndCost(stack, chains, cost=0, path=[], startIdx=None):
    # basically old solutionChain1
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
    shortestPath = findShortestPathRecursive(stack, 0, [], None)
    printStack(stack)
    print("Shortest path is {} with {} steps".format(*shortestPath))
    print("Chains were: ", list(map(list, findChains(stack))))


def findShortestPathRecursive(stack, cost, path, startIdx):
    chains = findChains(stack)
    cheapestSolution = solutionChainAndCost(stack, deepcopy(chains), cost,
                                            copy(path), startIdx)
    if cheapestSolution[1] == cost:
        return (path, cost)

    realChains = [c for c in chains if len(c) > 1]
    firstChainHasNone = realChains[0][-1] is None
    if firstChainHasNone:
        toTest = [realChains[0][0]]
    else:
        toTest = []
    chainsToTest = realChains[1:] if firstChainHasNone else realChains
    toTest += list(it.chain.from_iterable(chainsToTest))
    toTest = [t for t in toTest if t not in path]

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


def printStack(stack):
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            print("{}".format("_" if stack[idx] is None else stack[idx]),
                  end="|")
        print("\n––––––")


def main(debug=False):
    costs = dict()
    solutions = []
    print("Creating all possible Rack permutations")
    rackPermutations = list(map(list, it.permutations(
                            [0, 1, 2, 3, 4, 5, 6, 7, None])))
    lenPerms = len(rackPermutations)
    print("Crunching all permutations...")
    for i, perm in enumerate(rackPermutations):
        path, shortestPath = findShortestPathRecursive(perm, 0, [], None)
        print("\r{}/{}".format(i, lenPerms), end="")
        if shortestPath in costs.keys():
            costs[shortestPath] += 1
        else:
            costs[shortestPath] = 1
        # 2: concatenate all chains, work one chain
        # 3: clever concatenation should do the trick
        # print("Distance for solving: {} on {} long chain {}".format(
        #       d, len(c), "with None" if noneflag else ""))
        solutions.append((perm, path, shortestPath))
    for k, v in costs.items():
        print("Solved in {:2} steps: {}".format(k, v))

    outfile = open("solutionDump.json", "w")
    json.dump(solutions, outfile)
    outfile.close()
    print(costs)
    """for i in range(10):
        print("{} of {} permutations ({}%) have {} chains"
              .format(count[i], len(rackPermutations),
                      count[i] / len(rackPermutations) * 100.0, i))
    print("{} of {} permutations with None in Mainchain"
          .format(nonecnt, len(rackPermutations)))"""
    # print("Done finding {} chain groups!".format(len(chainGroups)))


if __name__ == '__main__':
    main()
