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


def solveOneByOne(stack, chains):
    # basically old solutionChain1
    # first, remove all length one chains (those are already placed)
    realChainz = [c for c in chains if len(c) > 1]
    # Now, 


def solveTogether(stack, chains):
    pass


def main(debug=False):
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    nonecnt = 0
    print("Creating all possible Rack permutations")
    rackPermutations = list(itertools.permutations(
                            [0, 1, 2, 3, 4, 5, 6, 7, None]))
    print("Crunching all permutations...")
    for perm in rackPermutations:
        # WHAT DO WE WANT TO KNOW ABOUT THIS SHIT
        d = 0
        i = 0
        chains = findChains(perm)
        # Solve different ways:
        # 1: work whole chain, append next one
        solveOneByOne(copy(perm), chains)
        # 2: concatenate all chains, work one chain
        # 3: clever concatenation should do the trick
        realChainz = [c for c in chains if len(c) > 1]
        if len(realChainz) == 1:
            count[1] += 1
            noneflag = False
            c = realChainz[0]
            if None not in c:
                c.append(c[0])
                c.append(None)
                noneflag = True
                nonecnt += 1
            for i, n in enumerate(c):
                if n is None:
                    break
                elif i is 0 and noneflag:
                    # SONDERFALLBEHANDLUNG
                    d += distance(None, c[i + 1])
                elif i is 1 and noneflag:
                    d += distance(None, n)
                    d += distance(c[i + 1], n)
                else:
                    d += distance(c[i - 1], n)
                    d += distance(n, c[i - 1])
            # print("Distance for solving: {} on {} long chain {}".format(
            #       d, len(c), "with None" if noneflag else ""))

    for i in range(10):
        print("{} of {} permutations ({}%) have {} chains"
              .format(count[i], len(rackPermutations),
                      count[i] / len(rackPermutations) * 100.0, i))
    print("{} of {} permutations with None in Mainchain"
          .format(nonecnt, len(rackPermutations)))
    # print("Done finding {} chain groups!".format(len(chainGroups)))