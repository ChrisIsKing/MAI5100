# guyanaRoutes.py
# ---------------
# MAI 5100 HW0, Part C: route planning on the Guyana road network.
#
# You will reuse the search algorithms you wrote in search.py on a real-world
# problem that has nothing to do with Pacman. Fill in every section marked
# "*** YOUR CODE HERE ***".

import math
import os
import time

import search
import util

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "guyana_roads.txt")
EARTH_RADIUS_KM = 6371.0


class RoadMap:
    """
    Reads the road network from data/guyana_roads.txt.

    Attributes:
      coords: dict mapping town name -> (latitude, longitude)
      roads:  dict mapping town name -> list of (neighbor, km, hours, is_ferry)
    Roads are two-way, so every road appears in both towns' lists.
    """

    def __init__(self, path=DATA_FILE):
        self.coords = {}
        self.roads = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                kind, rest = line.split(" ", 1)
                fields = [x.strip() for x in rest.split("|")]
                if kind == "TOWN":
                    name, lat, lon = fields
                    self.coords[name] = (float(lat), float(lon))
                    self.roads.setdefault(name, [])
                elif kind == "ROAD":
                    a, b, km, hours, ferry = fields
                    is_ferry = ferry.lower() == "yes"
                    self.roads.setdefault(a, []).append((b, float(km), float(hours), is_ferry))
                    self.roads.setdefault(b, []).append((a, float(km), float(hours), is_ferry))

    def towns(self):
        return sorted(self.coords)


def haversineKm(coord1, coord2):
    """Great-circle (straight-line) distance in km between two (lat, lon) points."""
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    a = (math.sin((lat2 - lat1) / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2)
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


class GuyanaRouteProblem(search.SearchProblem):
    """
    Find a route between two towns.

    A state is simply a town name (a string). An action is the name of the
    neighboring town you drive to next, so a solution is the list of towns
    visited after the start, ending at the goal.

    costMode controls the step cost of each road:
      "km"    : the road distance in kilometres
      "hours" : the estimated travel time in hours (ferries are slow!)
    """

    def __init__(self, roadMap, start, goal, costMode="km"):
        if start not in roadMap.coords or goal not in roadMap.coords:
            raise ValueError("Unknown town: %s or %s" % (start, goal))
        if costMode not in ("km", "hours"):
            raise ValueError("costMode must be 'km' or 'hours'")
        self.roadMap = roadMap
        self.start = start
        self.goal = goal
        self.costMode = costMode
        self._expanded = 0  # do not change; used for analysis and grading

    def getStartState(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        Return a list of (successor, action, stepCost) triples, one per road
        leaving `state`. The action is the successor town's name. The step
        cost depends on self.costMode.
        """
        self._expanded += 1  # do not change
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        Total cost of following `actions` (a list of town names) from the start.
        Return 999999 if any step is not a road.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def straightLineHeuristic(state, problem):
    """
    An admissible heuristic for costMode == "km": the straight-line
    (great-circle) distance from `state` to the goal. Use haversineKm and
    problem.roadMap.coords.

    For costMode == "hours" you must still return an admissible estimate.
    Think about the fastest any vehicle could possibly travel in this network,
    and justify your choice in your written answers.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def runExperiment(start, goal, costMode="km"):
    """
    Compare search algorithms on one query. Prints a table of solution cost,
    number of nodes expanded, and runtime. Use the output in your Part C
    write-up. You do not need to modify this function.
    """
    roadMap = RoadMap()
    algorithms = [
        ("BFS", lambda p: search.breadthFirstSearch(p)),
        ("DFS", lambda p: search.depthFirstSearch(p)),
        ("UCS", lambda p: search.uniformCostSearch(p)),
        ("Greedy", lambda p: greedySearch(p, straightLineHeuristic)),
        ("A*", lambda p: search.aStarSearch(p, straightLineHeuristic)),
    ]
    print("%s -> %s (cost in %s)" % (start, goal, costMode))
    print("%-8s %10s %10s %10s  %s" % ("Alg", "Cost", "Expanded", "ms", "Route"))
    for name, alg in algorithms:
        problem = GuyanaRouteProblem(roadMap, start, goal, costMode)
        t0 = time.perf_counter()
        path = alg(problem)
        ms = (time.perf_counter() - t0) * 1000
        cost = problem.getCostOfActions(path)
        print("%-8s %10.1f %10d %10.2f  %s" % (name, cost, problem._expanded, ms, " -> ".join([start] + path)))


def greedySearch(problem, heuristic):
    """
    Greedy best-first search: always expand the node with the lowest h(n).
    Graph search (keep a set of expanded states).
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        runExperiment(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "km")
    else:
        runExperiment("Georgetown", "Lethem", "km")
