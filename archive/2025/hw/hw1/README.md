# MAI 5100 Homework 1: Multi-Agent Search

Welcome to homework 1, where you’ll explore:
- Multi-Agent Search
- Minimax
- Alpha-Beta Pruning
- Expectimax
- Evaluation Function

**Structure**:  
1. **Coding Portion**: PACMAN game with Multi-Agent Search.
2. **Written Problem-Solving** (Part 2): CSPs, Adversarial Search, and Evaluation Functions.

**Due:** **April 27, 2025** at **11:59 PM (Guyana time)**

![Pacman chased by ghosts](https://inst.eecs.berkeley.edu/~cs188/fa24/assets/projects/pacman_multi_agent.png)

## Table of Contents

- [Introduction](#introduction)
- [Welcome to Multi-Agent Pacman](#welcome-to-multi-agent-pacman)
- [Q1 (4 pts): Reflex Agent](#q1-4-pts-reflex-agent)
- [Q2 (5 pts): Minimax](#q2-5-pts-minimax)
  - [Hints and Observations](#hints-and-observations)
- [Q3 (5 pts): Alpha-Beta Pruning](#q3-5-pts-alpha-beta-pruning)
- [Q4 (5 pts): Expectimax](#q4-5-pts-expectimax)
- [Q5 (6 pts): Evaluation Function](#q5-6-pts-evaluation-function)
- [Grading & Submission](#grading--submission)

## Introduction

In this project, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will implement both minimax and expectimax search and try your hand at evaluation function design.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

```bash
python autograder.py
```

It can be run for one particular question, such as q2, by:

```bash
python autograder.py -q q2
```

It can be run for one particular test by commands of the form:

```bash
python autograder.py -t test_cases/q2/0-small-tree
```

By default, the autograder displays graphics with the `-t` option, but doesn’t with the `-q` option. You can force graphics by using the `--graphics` flag, or force no graphics by using the `--no-graphics` flag.

The code for this project consists of several Python files, some of which you will need to read and understand in order to complete the assignment, and some of which you can ignore. You can download all the code and supporting files by forking the course repository and cloning it to your local machine.

**Files you'll edit:**

- `multiAgents.py`: Where all of your multi-agent search agents will reside.

**Files you might want to look at:**

- `pacman.py`: The main file that runs Pacman games. This file also describes a Pacman GameState type, which you will use extensively in this project.
- `game.py`: The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.
- `util.py`: Useful data structures for implementing search algorithms. You don't need to use these for this project, but may find other functions defined here to be useful.

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
- `multiagentTestClasses.py`: Project 3 specific autograding test classes

Access all code and supporting files in the `src` directory: [📁](./src/)

**Files to Edit and Submit**: You will fill in portions of `multiAgents.py` during the assignment. Once you have completed the assignment, you will submit these files to Gradescope (for instance, you can upload all `.py` files in the folder). Please do not change the other files in this distribution.

**Evaluation**: Your code will be autograded for technical correctness. Please do not change the names of any provided functions or classes within the code, or you will wreak havoc on the autograder. However, the correctness of your implementation – not the autograder’s judgements – will be the final judge of your score.

## Welcome to Multi-Agent Pacman

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

## Q1 (4 pts): Reflex Agent

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

## Q2 (5 pts): Minimax

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

### Hints and Observations

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

## Q3 (5 pts): Alpha-Beta Pruning

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

## Q4 (5 pts): Expectimax

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

## Q5 (6 pts): Evaluation Function

Write a better evaluation function for Pacman in the provided function `betterEvaluationFunction`. The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did. With depth 2 search, your evaluation function should clear the `smallClassic` layout with one random ghost more than half the time and still run at a reasonable rate (to get full credit, Pacman should be averaging around 1000 points when he’s winning).

You can try your agent out under these conditions with

```bash
python autograder.py -q q5
```

To run it without graphics, use:

```bash
python autograder.py -q q5 --no-graphics
```

## Part 2: Written Problem-Solving

1. **R&N Problem 5.12: (8 points)**
Describe how the minimax and alpha–beta algorithms change for two-player, non-zero-sum
games in which each player has a distinct utility function and both utility functions are known
to both players. If there are no constraints on the two terminal utilities, is it possible for any
node to be pruned by alpha–beta? What if the player’s utility functions on any state differ by at
most a constant k, making the game almost cooperative?

2. **R&N Problem 6.8: (8 points)**
Consider the graph with 8 nodes $A1 , A2 , A3 , A4 , H, T, F1 , F2$ . $Ai$ is connected to $Ai+1$ for all $i$,
each $Ai$ is connected to $H$, $H$ is connected to $T$, and $T$ is connected to each $Fi$ . Find a 3-coloring
of this graph by hand using the following strategy: backtracking with conflict-directed
backjumping, the variable order $A1 , H, A4 , F1 , A2 , F2 , A3 , T$ , and the value order $R, G, B$.

3. **Course Scheduling (14 points)**
You are in charge of scheduling for computer science classes that meet Mondays, Wednesdays and Fridays. There
are 5 classes that meet on these days and 3 professors who will be teaching these classes. You are constrained
by the fact that each professor can only teach one class at a time.

The classes are:
1. Class 1 - Intro to Programming: meets from 8:00-9:00am
2. Class 2 - Intro to Artificial Intelligence: meets from 8:30-9:30am
3. Class 3 - Natural Language Processing: meets from 9:00-10:00am
4. Class 4 - Computer Vision: meets from 9:00-10:00am
5. Class 5 - Machine Learning: meets from 10:30-11:30am

The professors are:
1. Professor A, who is qualified to teach Classes 1, 2, and 5.
2. Professor B, who is qualified to teach Classes 3, 4, and 5.
3. Professor C, who is qualified to teach Classes 1, 3, and 4.

---

1. Formulate this problem as a CSP problem in which there is one variable per class, stating the domains
(after enforcing unary constraints), and binary constraints. Constraints should be specified formally and
precisely, but may be implicit rather than explicit.

2. Draw the constraint graph associated with your CSP.

## Grading & Submission

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

