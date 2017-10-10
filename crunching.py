#!/usr/bin/env python

import itertools
from collections import deque
from copy import copy


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


def solveOneByOne(stack, chains, startIdx=None):
    # basically old solutionChain1
    # first, remove all length one chains (those are already placed)
    realChainz = [c for c in chains if len(c) > 1]
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
    # Done with the chains
    return totalDistance


def testChain(l):
    stacks = concatChains(l, findChains(l))
    for stack, cost, startIdx in stacks:
        totalCost = solveOneByOne(stack, findChains(stack), startIdx) + cost
        print(stack, findChains(stack), totalCost, cost, startIdx)
    print(l, findChains(l), solveOneByOne(l, findChains(l)))


def concatChains(stack, chains):
    # In theory, this has many different candidates
    # Get all chains >1
    realChainz = [c for c in chains if len(c) > 1]
    # To concatenate the chains, we have to move one element of
    # each chain to None
    # if the first chain contains none, it is not part of our business
    start = 1 if realChainz[0][-1] is None else 0
    changeLists = concatRecursive([], realChainz, start)
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
            stackCandidates.append((newStack, cost, pNone))
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
    nonecnt = 0
    print("Creating all possible Rack permutations")
    rackPermutations = list(itertools.permutations(
                            [0, 1, 2, 3, 4, 5, 6, 7, None]))
    print("Crunching all permutations...")
    for perm in rackPermutations:
        # WHAT DO WE WANT TO KNOW ABOUT THIS SHIT
        i = 0
        chains = findChains(perm)
        # Solve different ways:
        # 1: work whole chain, append next one
        d = solveOneByOne(copy(perm), chains)
        print("{}: {}".format(perm, d))
        # 2: concatenate all chains, work one chain
        # 3: clever concatenation should do the trick
        # print("Distance for solving: {} on {} long chain {}".format(
        #       d, len(c), "with None" if noneflag else ""))

    for i in range(10):
        print("{} of {} permutations ({}%) have {} chains"
              .format(count[i], len(rackPermutations),
                      count[i] / len(rackPermutations) * 100.0, i))
    print("{} of {} permutations with None in Mainchain"
          .format(nonecnt, len(rackPermutations)))
    # print("Done finding {} chain groups!".format(len(chainGroups)))


if __name__ == '__main__':
    main()
