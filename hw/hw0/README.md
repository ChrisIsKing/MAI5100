# MAI 5100 Homework 0: Search Algorithms

Welcome to your first homework, where you’ll explore:
- Depth-first search
- Breadth-first search
- Uniform-cost search
- A* search
- Heuristics
- Suboptimal search

**Structure**:  
1. **Coding Portion**: PACMAN game with search algorithms.
2. **Written Problem-Solving** (Part 2): Analyzing search algorithms.

**Due:** **March 25, 2025** at **11:59 PM (Guyana time)**

![Pacman in a maze](https://inst.eecs.berkeley.edu/~cs188/sp25/assets/projects/maze.png)

## Table of Contents

- [Introduction](#introduction)
- [Welcome to Pacman](#welcome-to-pacman)
- [New Syntax](#new-syntax)
- [Q1 (3 pts): Finding a Fixed Food Dot using Depth First Search (Lecture 2)](#q1-3-pts-finding-a-fixed-food-dot-using-depth-first-search-lecture-2)
- [Q2 (3 pts): Breadth First Search (Lecture 2)](#q2-3-pts-breadth-first-search-lecture-2)
- [Q3 (3 pts): Varying the Cost Function (Lecture 2)](#q3-3-pts-varying-the-cost-function-lecture-2)
- [Q4 (3 pts): A* search (Lecture 3)](#q4-3-pts-a-search-lecture-3)
- [Q5 (3 pts): Finding All the Corners (Lecture 3)](#q5-3-pts-finding-all-the-corners-lecture-3)
- [Q6 (3 pts): Corners Problem: Heuristic (Lecture 3)](#q6-3-pts-corners-problem-heuristic-lecture-3)
- [Q7 (4 pts): Eating All The Dots](#q7-4-pts-eating-all-the-dots)
- [Q8 (3 pts): Suboptimal Search](#q8-3-pts-suboptimal-search)
- [Part 2: Written Problem-Solving](#part-2-written-problem-solving)
- [Grading & Submission](#grading--submission)

## Introduction

In this project, your Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. You will build general search algorithms and apply them to Pacman scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```bash
python autograder.py
```

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore. You can download all the code and supporting files by forking the course repository and cloning it to your local machine.

**Files you'll edit:**

- `search.py`: Where all of your search algorithms will reside.
- `searchAgents.py`: Where all of your search-based agents will reside.

**Files you might want to look at:**

- `pacman.py`: The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.
- `game.py`: The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
- `util.py`: Useful data structures for implementing search algorithms.

**Supporting files you can ignore:**

- `graphicsDisplay.py`: Graphics for Pacman
- `graphicsUtils.py`: Support for Pacman graphics
- `textDisplay.py`: ASCII graphics for Pacman
- `ghostAgents.py`: Agents to control ghosts
- `keyboardAgents.py`: Keyboard interfaces to control Pacman
- `layout.py`: Code for reading layout files and storing their contents
- `autograder.py`: Project autograder
- `testParser.py`: Parses autograder test and solution files
- `testClasses.py`: General autograding test classes
- `test_cases/`: Directory containing the test cases for each question
- `searchTestClasses.py`: Project 1 specific autograding test classes

Access all code and supporting files in the `src` directory: [📁](./src/)

## Welcome to Pacman

Run Pacman:

After forking the repo, copying the code and creating and changing to the submissions directory, you should be able to play a game of Pacman by typing the following at the command line:

```bash
python pacman.py
```

Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman’s first step in mastering his domain.

The simplest agent in searchAgents.py is called the GoWestAgent, which always goes West (a trivial reflex agent). This agent can occasionally win:

```bash
python pacman.py --layout testMaze --pacman GoWestAgent
```

But, things get ugly for this agent when turning is required:

```bash
python pacman.py --layout tinyMaze --pacman GoWestAgent
```

If Pacman gets stuck, you can exit the game by typing `CTRL-c` into your terminal.

Soon, your agent will solve not only `tinyMaze`, but any maze you want.

Note that `pacman.py` supports a number of options that can each be expressed in a long way (e.g., `--layout`) or a short way (e.g., `-l`). You can see the list of all options and their default values via:

```bash
python pacman.py -h
```

## New Syntax

You may not have seen this syntax before:

```python
def my_function(a: int, b: Tuple[int, int], c: List[List], d: Any, e: float=1.0):
```

This is a Python 3 function definition. The `:` after the variable name indicates the type of the variable. For example, `a: int` means that `a` is an integer. The `Tuple[int, int]` means that `b` is a tuple of two integers. The `List[List]` means that `c` is a list of lists. The `Any` type means that `d` can be any type. The `float=1.0` means that `e` is a float with a default value of 1.0.

```python
my_function(1, (2, 3), [['a', 'b'], [None, my_class], [[]]], ('h', 1)) 
```

The above call fits the type annotations, and doesn’t pass anything in for e. Type annotations are meant to be an adddition to the docstrings to help you know what the functions are working with. Python itself doesn’t enforce these. When writing your own functions, it is up to you if you want to annotate your types; they may be helpful to keep organized or not something you want to spend time on.



## Q1 (3 pts): Finding a Fixed Food Dot using Depth First Search

In `searchAgents.py`, you’ll find a fully implemented `SearchAgent`, which plans out a path through Pacman’s world and then executes that path step-by-step. The search algorithms for formulating a plan are not implemented—that’s your job.

First, test that the `SearchAgent` is working correctly by running:

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
```

The command above tells the `SearchAgent` to use `tinyMazeSearch` as its search algorithm, which is implemented in `search.py`. Pacman should navigate the maze successfully.

Now it’s time to write full-fledged generic search functions to help Pacman plan routes! Pseudocode for the search algorithms you’ll write can be found in the lecture slides. Remember that a search node must contain not only a state but also the information necessary to reconstruct the path (plan) which gets to that state.

**Important note:** All of your search functions need to return a list of actions that will lead the agent from the start to the goal. These actions all have to be legal moves (valid directions, no moving through walls).

**Important note:** Make sure to use the `Stack`, `Queue`, and `PriorityQueue` data structures provided to you in `util.py`! These data structure implementations have particular properties which are required for compatibility with the autograder.

**Hint:** Each algorithm is very similar. Algorithms for DFS, BFS, UCS, and A* differ only in the details of how the fringe is managed. So, concentrate on getting DFS right, and the rest should be relatively straightforward. Indeed, one possible implementation requires only a single generic search method which is configured with an algorithm-specific queuing strategy. (Your implementation need not be of this form to receive full credit.)

Implement the **depth-first search (DFS)** algorithm in the `depthFirstSearch` function in `search.py`. To make your algorithm complete, write the graph search version of DFS, which avoids expanding any already visited states.

Your code should quickly find a solution for:

```bash
python pacman.py -l tinyMaze -p SearchAgent

python pacman.py -l mediumMaze -p SearchAgent

python pacman.py -l bigMaze -z .5 -p SearchAgent
```

The Pacman board will show an overlay of the states explored, and the order in which they were explored (brighter red means earlier exploration). Is the exploration order what you would have expected? Does Pacman actually go to all the explored squares on his way to the goal?

**Hint:** If you use a `Stack` as your data structure, the solution found by your DFS algorithm for `mediumMaze` should have a length of **130** (provided you push successors onto the fringe in the order provided by `getSuccessors`; you might get **246** if you push them in the reverse order). Is this a least-cost solution? If not, think about what depth-first search is doing wrong.

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q1
```


## Q2 (3 pts): Breadth First Search

Implement the **breadth-first search (BFS)** algorithm in the `breadthFirstSearch` function in `search.py`. Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for depth-first search.

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs

python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
```

Does BFS find a least-cost solution? If not, check your implementation.

**Hint:** If Pacman moves too slowly for you, try the option `--frameTime 0`.

**Note:** If you’ve written your search code generically, your code should work equally well for the eight-puzzle search problem without any changes.

```bash
python eightpuzzle.py
```

Grading: Please run the below command to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q2
```

## Q3 (3 pts): Varying the Cost Function

While BFS will find a fewest-actions path to the goal, we might want to find paths that are “best” in other senses. Consider `mediumDottedMaze` and `mediumScaryMaze`.

By changing the cost function, we can encourage Pacman to find different paths. For example, we can charge more for dangerous steps in ghost-ridden areas or less for steps in food-rich areas, and a rational Pacman agent should adjust its behavior in response.

Implement the **uniform-cost graph search** algorithm in the `uniformCostSearch` function in `search.py`. We encourage you to look through `util.py` for some data structures that may be useful in your implementation. You should now observe successful behavior in all three of the following layouts, where the agents below are all UCS agents that differ only in the cost function they use (the agents and cost functions are written for you):

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs

python pacman.py -l mediumDottedMaze -p StayEastSearchAgent

python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
```

**Note:** You should get very low and very high path costs for the `StayEastSearchAgent` and `StayWestSearchAgent` respectively, due to their exponential cost functions (see `searchAgents.py` for details).

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q3
```

## Q4 (3 pts): A* search

Implement **A\* search** in the empty function `aStarSearch` in `search.py`. A\* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The `nullHeuristic` heuristic function in `search.py` is a trivial example.

You can test your A\* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic (implemented already as `manhattanHeuristic` in `searchAgents.py`).

**Hint:** In addition to keeping track of the visited state, you may also want to keep track of the best path cost to that state so far. Some nodes may need to be expanded more than once to find the optimal path.

```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

You should see that A* finds the optimal solution slightly faster than uniform cost search (about 549 vs. 620 search nodes expanded in our implementation, but ties in priority may make your numbers differ slightly). What happens on `openMaze` for the various search strategies?

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q4
```

## Q5 (3 pts): Finding All the Corners

The real power of A* will only be apparent with a more challenging search problem. Now, it’s time to formulate a new problem and design a heuristic for it.

In corner mazes, there are four dots, one in each corner. Our new search problem is to find the shortest path through the maze that touches all four corners (whether the maze actually has food there or not). Note that for some mazes like `tinyCorners`, the shortest path does not always go to the closest food first! **Hint:** The shortest path through `tinyCorners` takes **28** steps.

**Note:** Make sure to complete `Question 2` before working on `Question 5`, because `Question 5` builds upon your answer for `Question 2`.

Implement the `CornersProblem` search problem in `searchAgents.py`. You will need to choose a state representation that encodes all the information necessary to detect whether all four corners have been reached. Now, your search agent should solve:

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem

python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

To receive full credit, you need to define an abstract state representation that does **not** encode irrelevant information (like the position of ghosts, where extra food is, etc.). In particular, **do not** use a Pacman `GameState` as a search state. Your code will be very, very slow if you do (and also wrong).

An instance of the `CornersProblem` class represents an entire search problem, not a particular state. Particular states are returned by the functions you write, and your functions return a data structure of your choosing (e.g., tuple, set, etc.) that represents a state.

Furthermore, while a program is running, remember that many states simultaneously exist, all on the queue of the search algorithm, and they should be independent of each other. In other words, you should not have only one state for the entire `CornersProblem` object; your class should be able to generate many different states to provide to the search algorithm.

**Hint 1:** The only parts of the game state you need to reference in your implementation are the starting Pacman position and the location of the four corners.

**Hint 2:** When coding up `getSuccessors`, make sure to add children to your successors list with a cost of 1.

Our implementation of `breadthFirstSearch` expands just under **2000** search nodes on `mediumCorners`. However, heuristics (used with A* search) can reduce the amount of searching required.

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q5
```

## Q6 (3 pts): Corners Problem: Heuristic

**Note:** Make sure to complete `Question 4` before working on `Question 6`, because `Question 6` builds upon your answer for `Question 4`.

Implement a non-trivial heuristic for the `CornersProblem` in `cornersHeuristic`.

```bash
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

**Note:** `AStarCornersAgent` is a shortcut for:

```bash
-p SearchAgent -a fn=aStarSearch,prob=CornersProblem,heuristic=cornersHeuristic
```

**Admissibility:** Remember, heuristics are just functions that take search states and return numbers that estimate the cost to a nearest goal. More effective heuristics will return values closer to the actual goal costs. To be **admissible**, the heuristic values must be lower bounds on the actual shortest path cost to the nearest goal (and non-negative).

**Non-Trivial Heuristics:** The trivial heuristics are the ones that return zero everywhere (UCS) and the heuristic which computes the true completion cost. The former won’t save you any time, while the latter will timeout the autograder. You want a heuristic which reduces total compute time, though for this assignment the autograder will only check node counts (aside from enforcing a reasonable time limit).

**Grading:** Your heuristic must be a non-trivial non-negative heuristic to receive any points. Make sure that your heuristic returns 0 at every goal state and never returns a negative value. Depending on how few nodes your heuristic expands, you’ll be graded:

| Number of nodes expanded | Grade |
|--------------------------|-------|
| more than 2000           | 0/3   |
| at most 2000             | 1/3   |
| at most 1600             | 2/3   |
| at most 1200             | 3/3   |

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q6
```

## Q7 (4 pts): Eating All The Dots

Now we’ll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we’ll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food, and Pacman. (Of course, ghosts can ruin the execution of a solution! We’ll get to that in the next project.)

If you have written your general search methods correctly, A* with a null heuristic (equivalent to uniform-cost search) should quickly find an optimal solution to `testSearch` with no code change on your part (total cost of **7**).

```bash
python pacman.py -l testSearch -p AStarFoodSearchAgent
```

**Note:** `AStarFoodSearchAgent` is a shortcut for:

```bash
-p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=foodHeuristic
```

You should find that UCS starts to slow down even for the seemingly simple `tinySearch`. As a reference, our implementation takes 2.5 seconds to find a path of length **27** after expanding **5057** search nodes.

**Note:** Make sure to complete `Question 4` before working on `Question 7`, because `Question 7` builds upon your answer for `Question 4`.

Fill in `foodHeuristic` in `searchAgents.py` with a heuristic for the `FoodSearchProblem`. Try your agent on the `trickySearch` board:

```bash
python pacman.py -l trickySearch -p AStarFoodSearchAgent
```

Our UCS agent finds the optimal solution in about **13 seconds**, exploring over **16,000** nodes.

Any non-trivial non-negative heuristic will receive **1 point**. Make sure that your heuristic returns **0** at every goal state and never returns a negative value. Depending on how few nodes your heuristic expands, you’ll get additional points:

| Number of nodes expanded | Grade                               |
|--------------------------|-------------------------------------|
| more than 15000          | 1/4                                 |
| at most 15000            | 2/4                                 |
| at most 12000            | 3/4                                 |
| at most 9000             | 4/4 (full credit; medium)           |
| at most 7000             | 5/4 (optional extra credit; hard)   |

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q7
```

## Q8 (3 pts): Suboptimal Search

Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we’d still like to find a reasonably good path quickly. In this section, you’ll write an agent that always greedily eats the closest dot. `ClosestDotSearchAgent` is implemented for you in `searchAgents.py`, but it’s missing a key function that finds a path to the closest dot.

Implement the function `findPathToClosestDot` in `searchAgents.py`. Our agent solves this maze (suboptimally!) in under a second with a path cost of **350**:

```bash
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
```

**Hint:** The quickest way to complete `findPathToClosestDot` is to fill in the `AnyFoodSearchProblem`, which is missing its goal test. Then, solve that problem with an appropriate search function. The solution should be very short!

Your `ClosestDotSearchAgent` won’t always find the shortest possible path through the maze. Make sure you understand why, and try to come up with a small example where repeatedly going to the closest dot does not result in finding the shortest path for eating all the dots.

**Grading:** Please run the command below to see if your implementation passes all the autograder test cases.

```bash
python autograder.py -q q8
```

## Part 2: Written Problem-Solving

1. **R&N Problem 3.15 (10 points)**  
   Consider a state space where the start state is number 1 and each state $k$ has two successors: numbers $2k$ and $2k + 1$.

   1. Draw the portion of the state space for states 1 to 15.  
   2. Suppose the goal state is 11. List the order in which nodes will be visited for breadth-first search, depth-limited search with limit 3, and iterative deepening search.  
   3. How well would bidirectional search work on this problem? What is the branching factor in each direction of the bidirectional search?  
   4. Does the answer to (3) suggest a reformulation of the problem that would allow you to solve the problem of getting from state 1 to a given goal state with almost no search?  
   5. Call the action going from $k$ to $2k$ **Left**, and the action going to $2k + 1$ **Right**. Can you find an algorithm that outputs the solution to this problem without any search at all?

2. **R&N Problem 3.27 (10 points)**  
   $n$ vehicles occupy squares $(1,1)$ through $(n,1)$ (i.e., the bottom row) of an $n \times n$ grid. The vehicles must be moved to the top row but in reverse order; so the vehicle $i$ that starts in $(i,1)$ must end up in $(n - i + 1, n)$. On each time step, every one of the $n$ vehicles can move one square up, down, left, or right, or stay put; but if a vehicle stays put, one other adjacent vehicle (but not more than one) can hop over it. Two vehicles cannot occupy the same square.

   1. Calculate the size of the state space as a function of $n$.  
   2. Calculate the branching factor as a function of $n$.  
   3. Suppose that vehicle $i$ is at $(x,y)$. Write a nontrivial admissible heuristic $h_i$ for the number of moves it will require to get to its goal location $(n - i + 1, n)$, assuming no other vehicles are on the grid.  
   4. Which of the following heuristics are admissible for the problem of moving all $n$ vehicles to their destinations? Explain.  
      1. $\sum h_i$  
      2. $\max(h_1, \dots, h_n)$  
      3. $\min(h_1, \dots, h_n)$

### 3. “Manual” Search Tree Generation (20 points)

Consider the **U.S. map** shown below. The purple lines indicate major highways with the labeled mileages between the connected cities:

- **Cities**: Chicago, Detroit, Buffalo, Syracuse, Boston, Providence, New York, Philadelphia, Baltimore, Pittsburgh, Cleveland, Columbus, Indianapolis, and Portland (ME).
- **Step Costs**: Miles between cities along the purple highway segments (e.g., Chicago → Cleveland is 345 miles, Cleveland → Pittsburgh is 134 miles, etc.).

<p align="center">
  <img src="map.png" alt="U.S. map" width="500"/>
</p>

1. **Goal**: Plan a route from **Chicago** to **Boston** using each of the following search methods:
   - **Breadth-first Search (BFS)**
   - **Depth-first Search (DFS)**
   - **Uniform-Cost Search (UCS)**
   - **A\* Search**

2. **Procedure**:
   - **Manually generate the search tree** for each strategy.  
   - **Label** nodes in the order they are expanded (node 1 = root, node 2 = the second expanded, etc.).  
   - **Include** path costs (mileage so far) on each branch in your tree.
   - **Mark or shade** any “failure” or pruned nodes as you discover they cannot lead to a better solution (for UCS or A\*, for example).  
   - For A\*, you must provide the **heuristic** values $h(n)$ you used as you expand each node. A suitable heuristic would be the straight-line distance or a rough “driving distance” estimate from each city to Boston.  

3. **Solution Reporting**:  
   - **Solution Path**: Indicate which path your search finds from **Chicago** to **Boston**.
   - **Total Route Cost**: Provide the final total mileage.
   - **Optimality**: State whether or not the solution found is **optimal** for each search method (hint: BFS and UCS typically guarantee optimality under standard assumptions; DFS does not; A\* is optimal if your $h(n)$ is admissible and consistent).

## Grading & Submission

### Practice Using Git

Throughout this homework, you are required to use git to document your progress. Make sure to commit your changes frequently with detailed commit messages that reflect the work you have done. This will help you track your progress and make it easier to identify where things might have gone wrong if you need to debug your code.

Here are some examples of good commit messages:
- "Implemented depth-first search algorithm in search.py"
- "Fixed bug in breadth-first search implementation"
- "Added comments to explain uniform-cost search logic"
- "Refactored A* search to improve readability"

### Final Submission

For your final submission, you will create a pull request (PR) to the repository. Your PR should include:
1. A detailed description of the changes you made.
2. Answers to the following questions:
   - What challenges did you run into?
   - Which section was most fun and why?
   - How did you approach debugging your code?
   - What did you learn from this assignment?

### Steps to Submit Your Work

1. **Fork the Repository**: Create a fork of the course repository to your GitHub account.

2. **Create a Custom Named Folder**: Add your submission in a custom named folder in the `submissions` directory, e.g., `submissions/christopher_clarke`. This folder is where you will add your code and any other files related to the homework. **Do not make changes to the original files in the repository**.

3. **Commit Your Changes**: Ensure all your changes are committed with detailed messages.
   ```bash
   git add .
   git commit -m "Your detailed commit message here"
   ```

4. **Push Your Changes**: Push your changes to your forked repository.
   ```bash
   git push origin your-branch-name
   ```

5. **Create a Pull Request**: Go to your forked repository on GitHub and create a pull request to the main branch of the original repository. Include a detailed description and answer the interactive questions mentioned above.

6. **Submit the Written Portion**: Submit the written portion of the homework to Moodle or email it to christopher.clarke@uog.edu.gy.

7. **Review and Submit**: Once your PR is created, review it to ensure all changes are correctly documented. Submit the PR for review.

Remember, the focus is on your learning growth and understanding of the material, not just getting the right solution. Good luck!
