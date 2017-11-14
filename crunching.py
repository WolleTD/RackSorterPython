#!/usr/bin/env python

import json
import racksorter
import itertools as it


def findShortestPath(stack):
    shortestPath = racksorter.findShortestPathRecursive(stack, 0, [], None)
    printStack(stack)
    print("Shortest path is {} with {} steps".format(*shortestPath))
    print("Chains were: ", list(map(list, racksorter.findChains(stack))))


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
        path, shortestPath = racksorter.findShortestPathRecursive(perm, 0, [],
                                                                  None)
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
