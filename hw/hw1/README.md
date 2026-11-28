# MAI 5100 Homework 1: Constraint Satisfaction and Adversarial Search

**Released:** Saturday, November 28, 2026
**Due:** **Wednesday, December 16, 2026 at 11:59 PM (Guyana time)**

![Pacman chased by ghosts](https://inst.eecs.berkeley.edu/~cs188/fa26/assets/projects/pacman_multi_agent.png)

This homework covers Weeks 4 and 5: constraint satisfaction problems (backtracking, variable and value ordering, forward checking, arc consistency), local search (min-conflicts, hill climbing, simulated annealing), and adversarial search (minimax, alpha-beta pruning, expectimax, evaluation functions). You will build a CSP solver from scratch, use it to schedule University of Guyana exams, write game-playing agents for Pacman, and work through the theory by hand.

**Suggested order:** the CSP lecture is first (Nov 28), so start with **Parts B and C**. Start Part A after the adversarial search lecture on Dec 5. Part D covers both.

| Part | What you do | Points |
|---|---|---|
| [A. Multi-Agent Pacman](#part-a-multi-agent-pacman-25-pts) | Reflex, minimax, alpha-beta, and expectimax agents and an evaluation function (autograded, q1–q5) | 25 |
| [B. Build a CSP Solver](#part-b-build-a-csp-solver-25-pts) | Backtracking, MRV, LCV, forward checking, AC-3, and min-conflicts (autograded, q6–q8) | 25 |
| [C. UG Exam Timetabling](#part-c-ug-exam-timetabling-25-pts) | Model a real scheduling problem as a CSP, solve it, and run experiments (autograded q9, plus analysis) | 25 |
| [D. Written Problems](#part-d-written-problems-20-pts) | Hand traces, proofs, and analysis of CSPs, local search, and game trees | 20 |
| [Submission quality](#grading) | Git history, PR description, GenAI log | 5 |
| **Total** | | **100** |

## Table of Contents

- [Getting Started](#getting-started)
- [Part A: Multi-Agent Pacman (25 pts)](#part-a-multi-agent-pacman-25-pts)
- [Part B: Build a CSP Solver (25 pts)](#part-b-build-a-csp-solver-25-pts)
- [Part C: UG Exam Timetabling (25 pts)](#part-c-ug-exam-timetabling-25-pts)
- [Part D: Written Problems (20 pts)](#part-d-written-problems-20-pts)
- [Grading](#grading)
- [Submission](#submission)
- [Academic Integrity and Generative AI](#academic-integrity-and-generative-ai)

## Getting Started

You need **Python 3.10+** and **Git**. No external packages are required.

1. **Sync your fork** with the course repository, so you have `hw/hw1`.
2. **Create your submission folder** (use `firstname_lastname`):
   ```bash
   cd hw/hw1
   mkdir -p submissions/firstname_lastname
   cp -R src submissions/firstname_lastname/src
   cp written_template.md submissions/firstname_lastname/written.md
   cd submissions/firstname_lastname/src
   ```
3. **Check that everything runs** (you should see 0 points):
   ```bash
   python autograder.py --no-graphics
   ```

Work **only** inside your submission folder. Run a single question with `python autograder.py -q q6`, or a single test with `python autograder.py -t test_cases/q6/5_mrv`.

**Files you will edit:**

| File | Part | What goes in it |
|---|---|---|
| `src/multiAgents.py` | A | Reflex, minimax, alpha-beta, and expectimax agents; evaluation function |
| `src/csp.py` | B | CSP solver: consistency, MRV, LCV, forward checking, backtracking, AC-3, MAC, min-conflicts |
| `src/timetable.py` | C | `buildCSP` for exam timetabling (and the optional `improveTimetable`) |
| `written.md` | C, D | Experiments, analysis, written answers, GenAI log |

**Files you might want to look at:** `pacman.py` (`GameState`), `game.py`, `util.py`, and `data/*.json` (the timetabling instances for Part C).

---

## Part A: Multi-Agent Pacman (25 pts)

*Lecture 5. Autograded: q1–q5. Adapted from UC Berkeley CS 188 Project 2.*

In this part, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will implement minimax and expectimax search and try your hand at evaluation function design.

### Welcome to Multi-Agent Pacman

First, play a game of classic Pacman by running the following command:

```bash
python pacman.py
```

and using the arrow keys to move. Now, run the provided ReflexAgent in multiAgents.py

```bash
python pacman.py -p ReflexAgent
```

Note that it plays quite poorly even on simple layouts:

```bash
python pacman.py -p ReflexAgent -l testClassic
```

Inspect its code (in `multiAgents.py`) and make sure you understand what it’s doing.

### Q1 (4 pts): Reflex Agent

Improve the `ReflexAgent` in `multiAgents.py` to play respectably. The provided reflex agent code provides some helpful examples of methods that query the `GameState` for information. A capable reflex agent will have to consider both food locations and ghost locations to perform well. Your agent should easily and reliably clear the `testClassic` layout:

```bash
python pacman.py -p ReflexAgent -l testClassic
```

Try out your reflex agent on the default `mediumClassic` layout with one ghost or two (and animation off to speed up the display):

```bash
python pacman.py --frameTime 0 -p ReflexAgent -k 1
```

```bash
python pacman.py --frameTime 0 -p ReflexAgent -k 2
```

How does your agent fare? It will likely often die with 2 ghosts on the default board, unless your evaluation function is quite good.

*Note*: Remember that `newFood` has the function `asList()`

*Note*: As features, try the reciprocal of important values (such as distance to food) rather than just the values themselves.

*Note*: The evaluation function you’re writing is evaluating state-action pairs; in later parts of the project, you’ll be evaluating states.

*Note*: You may find it useful to view the internal contents of various objects for debugging. You can do this by printing the objects’ string representations. For example, you can print `newGhostStates` with `print(newGhostStates)`.

Options: Default ghosts are random; you can also play for fun with slightly smarter directional ghosts using `-g DirectionalGhost`. If the randomness is preventing you from telling whether your agent is improving, you can use `-f` to run with a fixed random seed (same random choices every game). You can also play multiple games in a row with `-n`. Turn off graphics with `-q` to run lots of games quickly.

```bash
python autograder.py -q q1
```

To run it without graphics, use:

```bash
python autograder.py -q q1 --no-graphics
```

Don’t spend too much time on this question, though, as the meat of the project lies ahead.

### Q2 (5 pts): Minimax

Now you will write an adversarial search agent in the provided `MinimaxAgent` class stub in `multiAgents.py`. Your minimax agent should work with any number of ghosts, so you’ll have to write an algorithm that is slightly more general than what you’ve previously seen in lecture. In particular, your minimax tree will have multiple min layers (one for each ghost) for every max layer.

Your code should also expand the game tree to an arbitrary depth. Score the leaves of your minimax tree with the supplied `self.evaluationFunction`, which defaults to `scoreEvaluationFunction`. `MinimaxAgent` extends `MultiAgentSearchAgent`, which gives access to `self.depth` and `self.evaluationFunction`. Make sure your minimax code makes reference to these two variables where appropriate as these variables are populated in response to command line options.

*Important*: A single search ply is considered to be one Pacman move and all the ghosts’ responses, so depth 2 search will involve Pacman and each ghost moving two times (see diagram below).

![Minimax tree with depth 2](https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/minimax_depth.png)

*Grading*: We will be checking your code to determine whether it explores the correct number of game states. This is the only reliable way to detect some very subtle bugs in implementations of minimax. As a result, the autograder will be very picky about how many times you call `GameState.generateSuccessor`. If you call it any more or less than necessary, the autograder will complain. To test and debug your code, run

```bash
python autograder.py -q q2
```

This will show what your algorithm does on a number of small trees, as well as a pacman game. To run it without graphics, use:

```bash
python autograder.py -q q2 --no-graphics
```

#### Hints and Observations

- Implement the algorithm recursively using helper function(s).
- The correct implementation of minimax will lead to Pacman losing the game in some tests. This is not a problem: as it is correct behaviour, it will pass the tests.
- The evaluation function for the Pacman test in this part is already written (`self.evaluationFunction`). You shouldn’t change this function, but recognize that now we’re evaluating states rather than actions, as we were for the reflex agent. Look-ahead agents evaluate future states whereas reflex agents evaluate actions from the current state.
- The minimax values of the initial state in the `minimaxClassic` layout are 9, 8, 7, -492 for depths 1, 2, 3 and 4 respectively. Note that your minimax agent will often win (665/1000 games for us) despite the dire prediction of depth 4 minimax.
  ```bash
  python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
  ```
- Pacman is always agent 0, and the agents move in order of increasing agent index.
- All states in minimax should be `GameStates`, either passed in to `getAction` or generated via `GameState.generateSuccessor`. In this project, you will not be abstracting to simplified states.
- On larger boards such as `openClassic` and `mediumClassic` (the default), you’ll find Pacman to be good at not dying, but quite bad at winning. He’ll often thrash around without making progress. He might even thrash around right next to a dot without eating it because he doesn’t know where he’d go after eating that dot. Don’t worry if you see this behavior, question 5 will clean up all of these issues.
- When Pacman believes that his death is unavoidable, he will try to end the game as soon as possible because of the constant penalty for living. Sometimes, this is the wrong thing to do with random ghosts, but minimax agents always assume the worst:
  ```bash
  python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
  ```
  Make sure you understand why Pacman rushes the closest ghost in this case.

### Q3 (5 pts): Alpha-Beta Pruning

Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree, in `AlphaBetaAgent`. Again, your algorithm will be slightly more general than the pseudocode from lecture, so part of the challenge is to extend the alpha-beta pruning logic appropriately to multiple minimizer agents.

You should see a speed-up (perhaps depth 3 alpha-beta will run as fast as depth 2 minimax). Ideally, depth 3 on `smallClassic` should run in just a few seconds per move or faster.

```bash
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
```

The `AlphaBetaAgent` minimax values should be identical to the `MinimaxAgent` minimax values, although the actions it selects can vary because of different tie-breaking behavior. Again, the minimax values of the initial state in the `minimaxClassic` layout are 9, 8, 7 and -492 for depths 1, 2, 3 and 4 respectively.

**You must not prune on equality in order to match the set of states explored by the autograder.** (Indeed, alternatively, but incompatible with our autograder, would be to also allow for pruning on equality and invoke alpha-beta once on each child of the root node, but this will not match the autograder.)

The pseudo-code below represents the algorithm you should implement for this question.

![Alpha-Beta Implementation](https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/alpha_beta_impl.png)

To test and debug your code, run

```bash
python autograder.py -q q3
```

This will show what your algorithm does on a number of small trees, as well as a pacman game. To run it without graphics, use:

```bash
python autograder.py -q q3 --no-graphics
```

The correct implementation of alpha-beta pruning will lead to Pacman losing some of the tests. This is not a problem: as it is correct behaviour, it will pass the tests.

### Q4 (5 pts): Expectimax

Minimax and alpha-beta are great, but they both assume that you are playing against an adversary who makes optimal decisions. As anyone who has ever won tic-tac-toe can tell you, this is not always the case. In this question you will implement the `ExpectimaxAgent`, which is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

As with the search and problems yet to be covered in this class, the beauty of these algorithms is their general applicability. To expedite your own development, we’ve supplied some test cases based on generic trees. You can debug your implementation on small the game trees using the command:

```bash
python autograder.py -q q4
```

Debugging on these small and manageable test cases is recommended and will help you to find bugs quickly.

Once your algorithm is working on small trees, you can observe its success in Pacman. Random ghosts are of course not optimal minimax agents, and so modeling them with minimax search may not be appropriate. `ExpectimaxAgent` will no longer take the min over all ghost actions, but the expectation according to your agent’s model of how the ghosts act. To simplify your code, assume you will only be running against an adversary which chooses amongst their `getLegalActions` uniformly at random.

To see how the ExpectimaxAgent behaves in Pacman, run:

```bash
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
```

You should now observe a more cavalier approach in close quarters with ghosts. In particular, if Pacman perceives that he could be trapped but might escape to grab a few more pieces of food, he’ll at least try. Investigate the results of these two scenarios:

```bash
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
```

```bash
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
```

You should find that your `ExpectimaxAgent` wins about half the time, while your `AlphaBetaAgent` always loses. Make sure you understand why the behavior here differs from the minimax case.

The correct implementation of expectimax will lead to Pacman losing some of the tests. This is not a problem: as it is correct behaviour, it will pass the tests.

### Q5 (6 pts): Evaluation Function

Write a better evaluation function for Pacman in the provided function `betterEvaluationFunction`. The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did. With depth 2 search, your evaluation function should clear the `smallClassic` layout with one random ghost more than half the time and still run at a reasonable rate (to get full credit, Pacman should be averaging around 1000 points when he’s winning).

You can try your agent out under these conditions with

```bash
python autograder.py -q q5
```

To run it without graphics, use:

```bash
python autograder.py -q q5 --no-graphics
```


---

## Part B: Build a CSP Solver (25 pts)

*Lecture 4. Autograded: q6 (backtracking and ordering, 6), q7 (arc consistency, 5), q8 (min-conflicts, 4). Rescaled to 25.*

CS 188 has no CSP coding project, so this part is our own. In `csp.py` you will write a **general** CSP solver, one that works for any binary CSP, and test it on three problems that are already defined for you:

- **Guyana map colouring:** colour Guyana's ten administrative regions so that no two bordering regions share a colour (borders from OpenStreetMap).
- **N-queens:** place *n* queens on an *n × n* board so that none attack each other.
- **Sudoku.**

A `CSP` has `variables`, `domains`, `neighbors`, and a binary `constraint(A, a, B, b)` function. Always call `csp.consistent(...)` instead of `constraint` directly, and call `csp.countAssign()` every time you assign a variable. The autograder uses these counts to check that your heuristics and inference actually **reduce the work** the solver does, not just that it finds an answer.

Once you have implemented the functions, run `python csp.py` to see your solver on all three problems with different configurations. (Before then it stops with `NotImplementedError`, which is expected.)

### Q6 (6 pts): Backtracking with ordering and forward checking

Implement, in order:

1. `CSP.isConsistentWith` and `CSP.nConflicts`.
2. `backtrackingSearch`. It takes the variable-selection, value-ordering, and inference strategies as arguments, so one function supports every combination. Keep a working copy of the domains and undo inference when you backtrack.
3. `mrv`: minimum remaining values, with the **degree heuristic** as the tie-breaker.
4. `lcv`: least constraining value.
5. `forwardChecking`: return the removals so they can be undone, or `None` (with the domains restored) on a dead end.

```bash
python autograder.py -q q6
```

One test checks that your solver correctly reports **no solution** when Guyana is coloured with only two colours. Why can't it be done? You will answer this in Part D.

### Q7 (5 pts): Arc consistency

Implement `revise`, `ac3`, and `mac` (maintaining arc consistency during backtracking). The hardest test is a Sudoku that plain backtracking takes minutes on. With MAC, it should take well under a second.

```bash
python autograder.py -q q7
```

### Q8 (4 pts): Min-conflicts local search

Implement `minConflicts`. Use the provided `rng` for every random choice so your results are reproducible. Your solver should solve **200-queens** in a few hundred steps, which is something backtracking cannot do in any reasonable time.

```bash
python autograder.py -q q8
```

---

## Part C: UG Exam Timetabling (25 pts)

*Autograded: q9 (15 pts after rescaling). Experiments and analysis in `written.md` (10 pts).*

Every semester, the University of Guyana has to fit hundreds of exams into a two-week exam period. No student can sit two exams at once, every exam needs a room big enough for its class, and lecturers have to be available to invigilate. This is a classic CSP, and you now have a solver for it.

The instances in `src/data/` (`ug_tiny`, `ug_small`, `ug_medium`) are **synthetic**. They were generated to look like a UG exam period, with real-style course codes, Turkeyen and Berbice campus rooms, and plausible class sizes, but they contain **no real student or course data**. Each file lists courses (with lecturer and enrolment), students (with the courses they take), exam slots (two per day), rooms (with capacities), and the slots each lecturer is unavailable.

### Q9 (8 pts): Model the problem

Complete `buildCSP(data)` in `timetable.py`. Variables are courses; values are `(slot, room)` pairs. The hard constraints are:

| | Constraint | Type |
|---|---|---|
| H1 | Two courses that share a student are in different slots | binary |
| H2 | Two courses cannot use the same room in the same slot | binary |
| H3 | A course's enrolment fits its room's capacity | unary |
| H4 | A course is not scheduled when its lecturer is unavailable | unary |
| H5 | Two courses taught by the same lecturer are in different slots | binary |

`hardViolations(data, timetable)` is provided. It lists every violation in a timetable and is exactly what the autograder uses. Think carefully about **which pairs of courses must be neighbors**: if two courses are not neighbors, your solver never checks the constraint between them.

```bash
python autograder.py -q q9
python timetable.py ug_small
```

### C2. Experiments and analysis (10 pts)

`python timetable.py <instance>` compares plain backtracking, MRV, MRV + LCV, MRV + forward checking, MRV + MAC, and min-conflicts. Backtracking gives up after 50,000 assignments; you can raise the limit with a second argument.

In `written.md`:

1. **Results table (3 pts).** Run all three instances and report, for each solver: solved, assignments, constraint checks, time, and back-to-back exams.
2. **Analysis (5 pts).** Which techniques made the biggest difference, and why? Explain each with reference to the constraint graph. Note when a technique **reduced assignments but increased constraint checks**, and whether that was worth it. Why does min-conflicts work so well here, and what can it **not** tell you that backtracking can?
3. **Formulation critique (2 pts).** Real UG timetabling has constraints we left out. Name two (for example, students with special accommodations, combined exams across campuses, or a limit of one exam per student per day). For one of them, say exactly how you would add it to the model and whether it is a hard or soft constraint.

**Bonus (up to +3 pts):** implement `improveTimetable` using hill climbing or simulated annealing to reduce `backToBack` while keeping the timetable feasible. Report the improvement on `ug_medium` and describe your method.

---

## Part D: Written Problems (20 pts)

*Write all answers in `written.md`. Show your work. Clear photos of hand-drawn trees and graphs are fine.*

### D1. Arc consistency by hand (5 pts)

Colour Guyana's regions with **three** colours {Red, Green, Blue}. Region 4 (Demerara-Mahaica) is fixed to **Red** and Region 10 (Upper Demerara-Berbice) is fixed to **Green**. The borders are in `GUYANA_REGIONS` in `csp.py`.

1. Draw the constraint graph.
2. Run AC-3 by hand. Show the queue and every domain reduction, in the order they happen.
3. What does AC-3 alone tell you about this problem? Does it solve it?
4. Explain why Guyana **cannot** be coloured with two colours, by pointing to a specific structure in the graph.

### D2. Problem formulation (4 pts) — R&N 6.8 (adapted)

Consider the graph with 8 nodes $A_1, A_2, A_3, A_4, H, T, F_1, F_2$. $A_i$ is connected to $A_{i+1}$ for all $i$, each $A_i$ is connected to $H$, $H$ is connected to $T$, and $T$ is connected to each $F_i$. Find a 3-colouring by hand using backtracking with **forward checking**, the variable order $A_1, H, A_4, F_1, A_2, F_2, A_3, T$, and the value order R, G, B. Show the domains after each assignment, and mark every backtrack.

### D3. Local search (4 pts)

1. In simulated annealing, a move that worsens the objective by $\Delta E > 0$ is accepted with probability $e^{-\Delta E / T}$. Compute this probability for $\Delta E = 2$ at $T = 10$, $T = 1$, and $T = 0.1$, and explain what the temperature schedule does over the course of a run.
2. Give an example (for example, in N-queens or timetabling) of a **local minimum** that hill climbing gets stuck in, and explain how random restarts or simulated annealing help.

### D4. Game trees (7 pts)

1. **Alpha-beta by hand (4 pts).** For the game tree below (MAX at the root, then MIN, then MAX, leaves left to right), run alpha-beta pruning left to right. Give the minimax value of the root, the action MAX should take, and list every leaf that is **not** evaluated.

   ```
                       MAX
            /           |           \
          MIN          MIN          MIN
         /   \        /   \        /   \
       MAX   MAX    MAX   MAX    MAX   MAX
       / \   / \    / \   / \    / \   / \
      3  12 8   2  4   6 16  5  2  1  7   9
   ```

2. **Expectimax vs. minimax (2 pts).** Replace every MIN node in the tree with a CHANCE node that picks each child with equal probability. What is the new root value and action? Give one reason Pacman might prefer expectimax against real ghosts.
3. **Non-zero-sum games (1 pt) — R&N 5.12 (short).** If two players have different utility functions, can alpha-beta still prune? Explain in two or three sentences.

---

## Grading

| Component | Points | How it is graded |
|---|---|---|
| Part A (q1–q5) | 25 | Autograder |
| Part B (q6–q8) | 25 | Autograder (15 points, rescaled to 25), plus hidden tests |
| Part C: q9 | 15 | Autograder (8 points, rescaled to 15), plus hidden instances |
| Part C: C2 | 10 | Written, by rubric |
| Part D | 20 | Written, by rubric |
| Submission quality | 5 | Meaningful commit history, complete PR description, honest GenAI log |
| **Total** | **100** | (+3 bonus) |

The autograder in this repository is a **self-check**. Final grades also use hidden test cases (including new timetabling instances), and code may be reviewed by hand. The correctness of your implementation, not the autograder's judgement, determines your score.

**Late policy:** Homeworks cannot be turned in late unless an extension is granted at least 24 hours before the deadline. The midterm is on December 19, so plan to finish early.

---

## Submission

Submit by opening a **pull request** from your fork to `ChrisIsKing/MAI5100` before the deadline.

1. Commit as you go with descriptive messages. Your commit history is part of your grade.
2. Your submission folder must contain:
   ```
   hw/hw1/submissions/firstname_lastname/
   ├── src/            # your full copy of the starter code, with your solutions
   └── written.md      # Parts C2 and D, plus your GenAI log
   ```
3. Do **not** modify anything outside your own submission folder.
4. Open a pull request titled `HW1: Firstname Lastname` and fill in the pull request template.

---

## Academic Integrity and Generative AI

- You may discuss ideas with classmates, but **all code and written answers must be your own**.
- Generative AI may be used as a **collaborator**, for example to explain a concept or help debug, but you must **log every use** in the GenAI section of `written.md`.
- You must understand everything you submit. You may be asked to explain your code or answers.
- Solutions to the original CS 188 project exist online. Copying them, or submitting AI-generated code you cannot explain, is an academic violation.

---

*Part A and the Pacman framework are adapted from the [UC Berkeley CS 188 Pac-Man Projects](https://inst.eecs.berkeley.edu/~cs188/fa26/projects/) by John DeNero, Dan Klein, Pieter Abbeel, and others, used for educational purposes. Guyana region borders © OpenStreetMap contributors (ODbL). Timetabling data is synthetic.*
