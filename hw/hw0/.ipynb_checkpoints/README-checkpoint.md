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

Run the autograder to grade your answers on your machine:

```bash
python autograder.py
```

Access all code and supporting files in the `src` directory: [📁](./src/)

## Welcome to Pacman

Run Pacman:

```bash
python pacman.py
```

Test a simple agent:

```bash
python pacman.py --layout testMaze --pacman GoWestAgent
```

For help:

```bash
python pacman.py -h
```

## New Syntax

Example function with type annotations:

```python
def my_function(a: int, b: Tuple[int, int], c: List[List], d: Any, e: float=1.0):
```

## Q1 (3 pts): Finding a Fixed Food Dot using Depth First Search

Run depth-first search (DFS):

```bash
python pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
```

Implement DFS in `search.py`. Run tests:

```bash
python autograder.py -q q1
```

## Q2 (3 pts): Breadth First Search 

Run breadth-first search (BFS):

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
```

Implement BFS in `search.py`. Run tests:

```bash
python autograder.py -q q2
```

## Q3 (3 pts): Varying the Cost Function

Run uniform-cost search (UCS):

```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
```

Implement UCS in `search.py`. Run tests:

```bash
python autograder.py -q q3
```

## Q4 (3 pts): A* search

Run A* search:

```bash
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
```

Implement A* in `search.py`. Run tests:

```bash
python autograder.py -q q4
```

## Q5 (3 pts): Finding All the Corners

Run corner search:

```bash
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
```

Implement `CornersProblem` in `searchAgents.py`. Run tests:

```bash
python autograder.py -q q5
```

## Q6 (3 pts): Corners Problem: Heuristic

Run A* with corners heuristic:

```bash
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
```

Implement `cornersHeuristic` in `searchAgents.py`. Run tests:

```bash
python autograder.py -q q6
```

## Q7 (4 pts): Eating All The Dots

Run food search problem:

```bash
python pacman.py -l testSearch -p AStarFoodSearchAgent
```

Implement `foodHeuristic` in `searchAgents.py`. Run tests:

```bash
python autograder.py -q q7
```

## Q8 (3 pts): Suboptimal Search

Run greedy closest dot agent:

```bash
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5
```

Implement `findPathToClosestDot` in `searchAgents.py`. Run tests:

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


