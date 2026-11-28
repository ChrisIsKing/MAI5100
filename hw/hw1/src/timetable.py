# timetable.py
# ------------
# MAI 5100 HW1, Part C: University of Guyana exam timetabling as a CSP.
#
# The data in data/ is SYNTHETIC. It is generated to look like a UG
# end-of-semester exam period (course codes, Turkeyen and Berbice campus rooms,
# realistic class sizes), but no real student or course data is used.
#
# You will model the problem as a CSP and solve it with the solver you
# wrote in csp.py. Fill in every section marked "*** YOUR CODE HERE ***".

import json
import os
import time

import csp as cspmod

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


class ExamData:
    """
    Loads an exam timetabling instance from a JSON file.

    Attributes
      courses:    dict code -> {"title", "lecturer", "enrolment"}
      students:   dict student_id -> list of course codes
      slots:      list of slot ids, e.g. "Mon-1 AM" (in chronological order)
      days:       dict slot id -> day index (two slots on the same day share it)
      rooms:      dict room name -> capacity
      unavailable: dict lecturer -> list of slot ids they cannot invigilate
    Derived (computed for you)
      clashes:    dict course -> set of courses that share at least one student
      shared:     dict (course A, course B) -> number of students taking both
    """

    def __init__(self, path):
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        self.name = d.get("name", os.path.basename(path))
        self.courses = d["courses"]
        self.students = d["students"]
        self.slots = d["slots"]
        self.days = d["days"]
        self.rooms = d["rooms"]
        self.unavailable = d.get("unavailable", {})
        self.clashes = {c: set() for c in self.courses}
        self.shared = {}
        for courses in self.students.values():
            for i, a in enumerate(courses):
                for b in courses[i + 1:]:
                    self.clashes[a].add(b)
                    self.clashes[b].add(a)
                    key = (min(a, b), max(a, b))
                    self.shared[key] = self.shared.get(key, 0) + 1

    def sharedStudents(self, a, b):
        return self.shared.get((min(a, b), max(a, b)), 0)


def loadInstance(name):
    return ExamData(os.path.join(DATA_DIR, name + ".json"))


# ---------------------------------------------------------------------------
# Q9: Model the timetable as a CSP
# ---------------------------------------------------------------------------
#
# Variables: one per course (the course code).
# Values:    (slot, room) pairs.
# Hard constraints:
#   H1 Two courses that share a student must be in different slots.
#   H2 Two courses cannot use the same room in the same slot.
#   H3 A course's enrolment must fit its room's capacity.       (unary)
#   H4 A course cannot be in a slot its lecturer is unavailable. (unary)
#   H5 Two courses with the same lecturer must be in different slots.
#
# H3 and H4 involve one variable, so they belong in the unary function.
# H1, H2 and H5 are binary. Think carefully about which pairs of courses are
# neighbors: two courses must be neighbors if ANY binary constraint could
# rule out a pair of their values.

def buildCSP(data):
    """Return a csp.CSP for this instance, with makeNodeConsistent() already applied."""
    "*** YOUR CODE HERE ***"
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Provided: validation and scoring
# ---------------------------------------------------------------------------

def hardViolations(data, timetable):
    """
    List every hard-constraint violation in `timetable` (dict course -> (slot, room)).
    An empty list means the timetable is feasible. This is what the
    autograder uses, so it is the definition of "correct".
    """
    problems = []
    for c in data.courses:
        if c not in timetable:
            problems.append("H0 %s is not scheduled" % c)
    for c, (slot, room) in timetable.items():
        if slot not in data.slots:
            problems.append("H0 %s uses unknown slot %s" % (c, slot))
        if room not in data.rooms:
            problems.append("H0 %s uses unknown room %s" % (c, room))
            continue
        if data.courses[c]["enrolment"] > data.rooms[room]:
            problems.append("H3 %s (%d students) does not fit in %s (%d seats)"
                            % (c, data.courses[c]["enrolment"], room, data.rooms[room]))
        if slot in data.unavailable.get(data.courses[c]["lecturer"], []):
            problems.append("H4 %s lecturer %s is unavailable in %s" % (c, data.courses[c]["lecturer"], slot))
    items = sorted(timetable.items())
    for i, (a, (sa, ra)) in enumerate(items):
        for b, (sb, rb) in items[i + 1:]:
            if sa != sb:
                continue
            if b in data.clashes[a]:
                problems.append("H1 %s and %s share %d student(s) but are both in %s"
                                % (a, b, data.sharedStudents(a, b), sa))
            if ra == rb:
                problems.append("H2 %s and %s are both in %s during %s" % (a, b, ra, sa))
            if data.courses[a]["lecturer"] == data.courses[b]["lecturer"]:
                problems.append("H5 %s and %s share lecturer %s in %s" % (a, b, data.courses[a]["lecturer"], sa))
    return problems


def backToBack(data, timetable):
    """
    Soft constraint: the number of student-exam pairs where a student sits two
    exams on the same day (in consecutive slots). Lower is better.
    """
    index = {s: i for i, s in enumerate(data.slots)}
    total = 0
    for courses in data.students.values():
        times = sorted(index[timetable[c][0]] for c in courses if c in timetable)
        for x, y in zip(times, times[1:]):
            if y == x + 1 and data.days[data.slots[x]] == data.days[data.slots[y]]:
                total += 1
    return total


def printTimetable(data, timetable):
    for slot in data.slots:
        here = sorted((room, c) for c, (s, room) in timetable.items() if s == slot)
        print("%-10s %s" % (slot, ", ".join("%s@%s" % (c, room) for room, c in here) or "-"))


# ---------------------------------------------------------------------------
# Q10 (optional challenge, not autograded): reduce back-to-back exams
# ---------------------------------------------------------------------------

def improveTimetable(data, timetable, steps=2000, seed=0):
    """
    Optional: start from a feasible timetable and use local search (for
    example hill climbing or simulated annealing) to reduce backToBack while
    keeping hardViolations empty. Return the improved timetable. Describe
    your method and results in written.md for bonus credit.
    """
    return dict(timetable)


def runExperiment(name="ug_small", maxAssigns=50000):
    """
    Compare solver configurations on one instance. Use the output in your write-up.
    Backtracking gives up after maxAssigns assignments (reported as "gave up").
    """
    data = loadInstance(name)
    configs = [
        ("plain backtracking", dict()),
        ("MRV", dict(selectVariable=cspmod.mrv)),
        ("MRV + LCV", dict(selectVariable=cspmod.mrv, orderValues=cspmod.lcv)),
        ("MRV + forward checking", dict(selectVariable=cspmod.mrv, inference=cspmod.forwardChecking)),
        ("MRV + MAC", dict(selectVariable=cspmod.mrv, inference=cspmod.mac)),
    ]
    print("Instance %s: %d courses, %d students, %d slots, %d rooms"
          % (data.name, len(data.courses), len(data.students), len(data.slots), len(data.rooms)))
    print("%-26s %8s %10s %12s %9s %6s" % ("Solver", "solved", "assigns", "checks", "ms", "b2b"))
    for label, kwargs in configs:
        problem = buildCSP(data)
        problem.maxAssigns = maxAssigns
        t0 = time.perf_counter()
        try:
            sol = cspmod.backtrackingSearch(problem, **kwargs)
            status = sol is not None and not hardViolations(data, sol)
        except cspmod.SearchLimitReached:
            sol, status = None, "gave up"
        ms = (time.perf_counter() - t0) * 1000
        print("%-26s %8s %10d %12d %9.1f %6s" % (label, status, problem.nassigns, problem.nchecks, ms,
                                                  backToBack(data, sol) if status is True else "-"))
    problem = buildCSP(data)
    t0 = time.perf_counter()
    sol = cspmod.minConflicts(problem, maxSteps=20000, seed=0)
    ms = (time.perf_counter() - t0) * 1000
    ok = sol is not None and not hardViolations(data, sol)
    print("%-26s %8s %10d %12d %9.1f %6s" % ("min-conflicts", ok, problem.nassigns, problem.nchecks, ms,
                                              backToBack(data, sol) if ok else "-"))


if __name__ == "__main__":
    import sys
    runExperiment(sys.argv[1] if len(sys.argv) > 1 else "ug_small",
                  int(sys.argv[2]) if len(sys.argv) > 2 else 50000)
