# csp.py
# ------
# MAI 5100 HW1, Part B: a general constraint satisfaction problem (CSP) solver.
#
# You will implement backtracking search, variable and value ordering
# heuristics, forward checking, arc consistency (AC-3), and min-conflicts
# local search. Everything you write here is reused in Part C
# (timetable.py) to schedule University of Guyana exams.
#
# Fill in every section marked "*** YOUR CODE HERE ***". Do not change the
# names or signatures of the provided classes and functions.

import random


class SearchLimitReached(Exception):
    """Raised when csp.nassigns exceeds csp.maxAssigns (if set)."""


class CSP:
    """
    A binary CSP.

    variables:   list of variable names (any hashable values)
    domains:     dict variable -> list of allowed values
    neighbors:   dict variable -> list of variables that share a constraint
    constraint:  function (A, a, B, b) -> True if A=a and B=b are consistent.
                 It is only called for pairs where B is in neighbors[A].
    unary:       optional function (var, value) -> True if value is allowed
                 for var on its own. Applied once, by makeNodeConsistent().

    The solver counts work so we can compare algorithms:
      self.nassigns     number of times a variable was assigned a value
                        (increment it by calling self.countAssign())
      self.nchecks      number of times constraint() was called
    Use self.consistent(...) instead of calling self.constraint directly so
    that checks are counted.
    """

    def __init__(self, variables, domains, neighbors, constraint, unary=None):
        self.variables = list(variables)
        self.domains = {v: list(domains[v]) for v in self.variables}
        self.neighbors = {v: list(neighbors.get(v, [])) for v in self.variables}
        self.constraint = constraint
        self.unary = unary
        self.nassigns = 0
        self.nchecks = 0
        self.maxAssigns = None  # optional cap used by experiments; see countAssign()

    def countAssign(self):
        """
        Call this every time you assign a value to a variable (in
        backtrackingSearch and minConflicts). It increments nassigns and stops
        the search if an optional limit has been set.
        """
        self.nassigns += 1
        if self.maxAssigns is not None and self.nassigns > self.maxAssigns:
            raise SearchLimitReached()

    def consistent(self, A, a, B, b):
        """Counted wrapper around the constraint function."""
        self.nchecks += 1
        return self.constraint(A, a, B, b)

    def makeNodeConsistent(self):
        """Remove values that violate the unary constraint. Provided for you."""
        if self.unary is not None:
            for v in self.variables:
                self.domains[v] = [x for x in self.domains[v] if self.unary(v, x)]

    def isConsistentWith(self, var, value, assignment):
        """
        True if var=value does not conflict with any already-assigned
        neighbor in `assignment` (a dict var -> value).
        """
        "*** YOUR CODE HERE ***"
        raise NotImplementedError

    def nConflicts(self, var, value, assignment):
        """
        Number of assigned neighbors of var that conflict with var=value.
        Used by min-conflicts and least-constraining-value.
        """
        "*** YOUR CODE HERE ***"
        raise NotImplementedError

    def isSolution(self, assignment):
        """True if every variable is assigned and no constraint is violated."""
        if set(assignment) != set(self.variables):
            return False
        for A in self.variables:
            for B in self.neighbors[A]:
                if not self.constraint(A, assignment[A], B, assignment[B]):
                    return False
        return True


# ---------------------------------------------------------------------------
# Q6: Backtracking search with ordering heuristics
# ---------------------------------------------------------------------------

def firstUnassignedVariable(csp, assignment, domains):
    """Static ordering: the first variable (in csp.variables order) not yet assigned."""
    for v in csp.variables:
        if v not in assignment:
            return v


def mrv(csp, assignment, domains):
    """
    Minimum remaining values: choose the unassigned variable with the fewest
    values left in `domains`. Break ties by the most unassigned neighbors
    (the degree heuristic), then by order in csp.variables.
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def unorderedDomainValues(csp, var, assignment, domains):
    """Values in their current domain order."""
    return list(domains[var])


def lcv(csp, var, assignment, domains):
    """
    Least constraining value: order var's values so that the value that rules
    out the fewest choices for var's unassigned neighbors comes first.
    For each value a, count, over every unassigned neighbor B and every value
    b in domains[B], how many (B, b) pairs would become inconsistent.
    Break ties by the original domain order (Python's sort is stable).
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def noInference(csp, var, value, assignment, domains):
    """Do nothing. Returns an empty list of removals."""
    return []


def forwardChecking(csp, var, value, assignment, domains):
    """
    After assigning var=value, remove from each unassigned neighbor's domain
    every value that is inconsistent with var=value.

    Modify `domains` in place. Return a list of (variable, removedValue)
    pairs so the caller can undo them, or None if some neighbor's domain
    becomes empty (a dead end).
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def backtrackingSearch(csp, selectVariable=firstUnassignedVariable,
                       orderValues=unorderedDomainValues, inference=noInference):
    """
    Return a complete, consistent assignment (dict var -> value), or None.

    selectVariable(csp, assignment, domains) -> variable
    orderValues(csp, var, assignment, domains) -> list of values to try
    inference(csp, var, value, assignment, domains) -> list of removals or None

    Keep a working copy of the domains (dict var -> list). Each time you
    assign a variable, call csp.countAssign(). When you backtrack, undo both
    the assignment and any domain removals made by inference.
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Q7: Arc consistency (AC-3)
# ---------------------------------------------------------------------------

def revise(csp, domains, Xi, Xj):
    """
    Remove every value x from domains[Xi] for which no value y in
    domains[Xj] satisfies the constraint between Xi=x and Xj=y.
    Return True if anything was removed.
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def ac3(csp, domains=None, queue=None):
    """
    Enforce arc consistency. `domains` defaults to csp.domains and is
    modified in place. `queue` defaults to every arc (Xi, Xj) with Xj a
    neighbor of Xi. Return False if some domain becomes empty, else True.
    """
    if domains is None:
        domains = csp.domains
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


def mac(csp, var, value, assignment, domains):
    """
    Maintaining arc consistency: an inference function for
    backtrackingSearch. After var=value, restrict domains[var] to [value],
    then run AC-3 starting from the arcs (B, var) for every unassigned
    neighbor B of var.

    Return a list of (variable, removedValue) pairs (including the values
    removed from var itself), or None on failure. On success, leave
    `domains` modified. On failure, restore every value you removed before
    returning None, so `domains` is exactly as it was before the call.
    (forwardChecking follows the same contract.)
    """
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Q8: Min-conflicts local search
# ---------------------------------------------------------------------------

def minConflicts(csp, maxSteps=10000, seed=0):
    """
    Local search. Start from a complete random assignment (each variable gets
    a random value from csp.domains). Then repeat up to maxSteps times:
      - if the assignment is a solution, return it
      - pick a random conflicted variable
      - set it to the value that minimizes nConflicts, breaking ties randomly
    Return None if no solution is found. Use rng = random.Random(seed) for all
    randomness so results are reproducible. Call csp.countAssign() for every
    assignment, including the initial ones.
    """
    rng = random.Random(seed)
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Example problems (provided)
# ---------------------------------------------------------------------------

def different(A, a, B, b):
    return a != b


# Region borders from OpenStreetMap administrative boundaries (admin_level=4),
# (c) OpenStreetMap contributors, ODbL. Retrieved Nov 2026.
GUYANA_REGIONS = {
    "Barima-Waini": ["Cuyuni-Mazaruni", "Pomeroon-Supenaam"],  # Region 1
    "Pomeroon-Supenaam": ["Barima-Waini", "Cuyuni-Mazaruni", "Essequibo Islands-West Demerara"],  # Region 2
    "Essequibo Islands-West Demerara": ["Cuyuni-Mazaruni", "Demerara-Mahaica", "Pomeroon-Supenaam", "Upper Demerara-Berbice"],  # Region 3
    "Demerara-Mahaica": ["Essequibo Islands-West Demerara", "Mahaica-Berbice", "Upper Demerara-Berbice"],  # Region 4
    "Mahaica-Berbice": ["Demerara-Mahaica", "East Berbice-Corentyne", "Upper Demerara-Berbice"],  # Region 5
    "East Berbice-Corentyne": ["Mahaica-Berbice", "Potaro-Siparuni", "Upper Demerara-Berbice", "Upper Takutu-Upper Essequibo"],  # Region 6
    "Cuyuni-Mazaruni": ["Barima-Waini", "Essequibo Islands-West Demerara", "Pomeroon-Supenaam", "Potaro-Siparuni", "Upper Demerara-Berbice"],  # Region 7
    "Potaro-Siparuni": ["Cuyuni-Mazaruni", "East Berbice-Corentyne", "Upper Demerara-Berbice", "Upper Takutu-Upper Essequibo"],  # Region 8
    "Upper Takutu-Upper Essequibo": ["East Berbice-Corentyne", "Potaro-Siparuni"],  # Region 9
    "Upper Demerara-Berbice": ["Cuyuni-Mazaruni", "Demerara-Mahaica", "East Berbice-Corentyne", "Essequibo Islands-West Demerara", "Mahaica-Berbice", "Potaro-Siparuni"],  # Region 10
}


def guyanaMapCSP(colors=("Red", "Green", "Blue", "Yellow")):
    """Color Guyana's ten administrative regions so no two neighbors match."""
    regions = list(GUYANA_REGIONS)
    return CSP(regions, {r: list(colors) for r in regions}, GUYANA_REGIONS, different)


def nQueensCSP(n):
    """Variable c = column c; value = row of the queen in that column."""
    cols = list(range(n))

    def ok(A, a, B, b):
        return a != b and abs(a - b) != abs(A - B)
    return CSP(cols, {c: list(range(n)) for c in cols},
               {c: [d for d in cols if d != c] for c in cols}, ok)


def sudokuCSP(grid):
    """
    grid: 81-character string, digits 1-9 or '.'/'0' for blanks, row-major.
    Variables are (row, col) pairs.
    """
    cells = [(r, c) for r in range(9) for c in range(9)]
    domains = {}
    for i, (r, c) in enumerate(cells):
        ch = grid[i]
        domains[(r, c)] = [int(ch)] if ch in "123456789" else list(range(1, 10))
    neighbors = {}
    for (r, c) in cells:
        peers = set()
        for k in range(9):
            peers.add((r, k))
            peers.add((k, c))
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for dr in range(3):
            for dc in range(3):
                peers.add((br + dr, bc + dc))
        peers.discard((r, c))
        neighbors[(r, c)] = sorted(peers)
    return CSP(cells, domains, neighbors, different)


def printSudoku(assignment):
    for r in range(9):
        print(" ".join(str(assignment[(r, c)]) for c in range(9)))


if __name__ == "__main__":
    import time
    configs = [
        ("plain backtracking", dict()),
        ("MRV + LCV", dict(selectVariable=mrv, orderValues=lcv)),
        ("MRV + LCV + forward checking", dict(selectVariable=mrv, orderValues=lcv, inference=forwardChecking)),
        ("MRV + LCV + MAC (AC-3)", dict(selectVariable=mrv, orderValues=lcv, inference=mac)),
    ]
    puzzle = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
    for name, kwargs in configs:
        for label, make in (("Guyana map", guyanaMapCSP), ("8-queens", lambda: nQueensCSP(8)),
                            ("Sudoku", lambda: sudokuCSP(puzzle))):
            if label == "Sudoku" and "inference" not in kwargs:
                print("%-30s %-12s (skipped: can take minutes without inference; try it yourself)" % (name, label))
                continue
            csp = make()
            t0 = time.perf_counter()
            sol = backtrackingSearch(csp, **kwargs)
            ms = (time.perf_counter() - t0) * 1000
            print("%-30s %-12s solved=%-5s assigns=%-7d checks=%-9d %.1f ms"
                  % (name, label, sol is not None and csp.isSolution(sol), csp.nassigns, csp.nchecks, ms))
    csp = nQueensCSP(50)
    sol = minConflicts(csp, seed=1)
    print("min-conflicts 50-queens solved=%s assigns=%d" % (sol is not None and csp.isSolution(sol), csp.nassigns))
