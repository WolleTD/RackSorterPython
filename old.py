#!/usr/bin/env python

import random
import time
import itertools
from collections import deque
from copy import copy

stack1 = [[None, 0, 1],
          [2, 3, 4],
          [5, 6, 7]]

stack2 = [[5, 1, 3],
          [7, 6, None],
          [4, 2, 0]]


# Not so black magic
def findChains(stackl, debug=False):
    found = set()
    # stackl = list(itertools.chain(*stack))
    # Find chains
    chains = list()
    # for i, n in enumerate(stackl):
    for i, n in enumerate(stackl):
        if len(found) == len(stackl):
            break
        if i == len(stackl) - 1:
            i = None
        if i in found:
            continue
        if debug:
            print(i, end="->")
        tchain = deque([i])
        found.add(i)
        while n != i:
            if debug:
                print(n, end="->")
            found.add(n)
            tchain.appendleft(n)
            n = stackl[n] if n is not None else stackl[-1]
        if None in tchain:
            tchain.rotate(-(tchain.index(None) + 1))
        chains.append(tchain)
        if debug:
            print("{}\nChain {} length {} at {} done {}/{}"
                  .format(n, len(chains), len(tchain), i, len(found),
                          len(stackl)))
    return chains


# Somewhat black magic
def findBetterChains(stack, debug=False):
    stackl = list(itertools.chain(*stack))
    unplaced = set(stackl)
    # Find chains
    chains = list()
    while len(unplaced) > 0:
        if len(chains) > 0:
            start = unplaced.pop()
        else:
            start = stackl.index(None)
            # Hotfix
            if stackl[start] is stackl[-1]:
                start = None
            unplaced.remove(start)
        tchain = [start]
        if debug:
            print(start, end="->")
        i = stackl.index(start)
        if stackl[i] is stackl[-1]:
            i = None
        while i != start:
            if debug:
                print(i, end="->")
            tchain.append(i)
            try:
                unplaced.remove(i)
            except KeyError:
                print("\nError removing {} from unplaced".format(i))
                printArray(stack)
                exit()
            i = stackl.index(i)
            if stackl[i] is stackl[-1]:
                i = None
        if debug:
            print(start)
        chains.append(tchain)
    return chains


# dark black magic
def solutionChain1(stack, debug=False):
    # chains = list(c for c in findBetterChains(stack, debug) if len(c) > 1)
    chains = deque(c for c in findChains(stack, debug) if len(c) > 1)
    for i, c in enumerate(chains):
        if None in c:
            if debug:
                print("Rotating", i)
            chains.rotate(-i)
            break
    print("Stack has {} chains".format(len(chains)))
    workStack = list(stack)
    # workStack = list(itertools.chain(*stack))
    for i, ch in enumerate(chains):
        print("\nSorting Chain {:2}".format(i), end="")
        for j, n in enumerate(ch):
            if n is None:
                if i + 1 < len(chains):
                    chains[i + 1].append(chains[i + 1][0])
                    chains[i + 1].append(None)
                break
            else:
                # ./sorter.py  362,51s user 0,42s system 99% cpu 6:05,70 total
                # pNone = workStack.index(None)
                # workStack[workStack.index(n)] = None
                # workStack[pNone] = n
                #
                # ./sorter.py  369,93s user 0,54s system 99% cpu 6:12,90 total
                pNone = workStack.index(None)
                pN = workStack.index(n)
                workStack[pNone], workStack[pN] = n, None
                # print(n, end="->")
            print("\rSorting Chain {:2} ({:5}/{:5})".format(i, j, len(ch) - 2),
                  end="")
    return [workStack]


def printArray(stack):
    for r in stack:
        for i in r:
            print("_" if i is None else i, end=" ")
        print()


def concatChains(stack, chains):
    # In theory, this has many different candidates
    # Get all chains >1
    realChainz = [c for c in chains if len(c) > 1]
    if len(realChainz) is 0:
        return []
    # To concatenate the chains, we have to move one element of
    # each chain to None
    # if the first chain contains none, it is not part of our business
    start = 1 if realChainz[0][-1] is None else 0
    changeLists = it.chain.from_iterable(map(it.permutations,
                                             concatRecursive([], realChainz,
                                                             start)))
    stackCandidates = []
    for clist in changeLists:
        newStack = copy(stack)
        cost = 0
        pNone = None
        for n in clist:
            pN = newStack.index(n)
            cost += distance(pNone, pN)
            pNone = newStack.index(None)
            cost += distance(pN, pNone)
            newStack[pNone], newStack[pN] = n, None
        if newStack in stackCandidates:
            print("Weird...", newStack)
        else:
            stackCandidates.append((newStack, cost, pNone, clist))
    return stackCandidates


def concatRecursive(changelist, chainlist, chainidx):
    candidates = []
    if chainidx is len(chainlist):
        return [changelist]
    for n in chainlist[chainidx]:
        newChangeList = copy(changelist)
        newChangeList.append(n)
        candidates += concatRecursive(newChangeList, chainlist, chainidx + 1)
    return candidates


def main(debug=False):
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print("Creating all possible Rack permutations")
    rackPermutations = list(itertools.permutations(
                            [0, 1, 2, 3, 4, 5, 6, 7, None]))
    print("Crunching all permutations...")
    for perm in rackPermutations:
        chains = findChains(perm)
        realChainz = [c for c in chains if len(c) > 1]
        count[len(realChainz)] += 1

    for i in range(10):
        print("{} of {} permutations ({}%) have {} chains"
              .format(count[i], len(rackPermutations),
                      count[i] / len(rackPermutations) * 100.0, i))


def testmain(debug=False):
    print("Array 1:")
    printArray(stack1)
    print("Chain 1:")
    printArray(findChains(stack1, debug))
    printArray(findBetterChains(stack1, debug))
    printArray(solutionChain1(stack1, debug))
    print("Array 2:")
    printArray(stack2)
    print("Chain 2:")
    printArray(findChains(stack2, debug))
    printArray(findBetterChains(stack2, debug))
    printArray(solutionChain1(stack2, debug))
    print("Generating random array...")
    s = list(range(100))
    s[-1] = None
    random.shuffle(s)
    # printArray(findChains([s], debug))
    # printArray(findBetterChains([s], debug))
    printArray(solutionChain1([s], True))
    print("Fun part")
    print("Generating random array...")
    for N in [10, 40, 50, 70, 100, 200, 500, 1000]:
        s = list(range(N))
        s[-1] = None
        times1 = []
        times2 = []
        for i in range(0, 1000):
            random.shuffle(s)
            start = time.time()
            findChains([s])
            t = (time.time() - start) * 1000
            print("\r{:4} F: {:7.4} ms".format(i, t), end=" ")
            times1.append(t)
            start = time.time()
            findBetterChains([s])
            t = (time.time() - start) * 1000
            print("B: {:7.4} ms".format(t), end="")
            times2.append(t)
        print("\rN={}:{}".format(N, "      " * 10))
        print("Forward:  {:7.4}ms".format(sum(times1) / len(times1)))
        print("Backward: {:7.4}ms".format(sum(times2) / len(times2)))


if __name__ == '__main__':
    main()
