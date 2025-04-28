# MAI 5100 Homework 1: Multi-Agent Search Submission

Implementing pacman using
- Minimax
- Alpha-Beta Pruning
- Expectimax
-  creating Evaluation Function
## 1. **Coding Portion**: PACMAN game with Multi-Agent Search.

### **Minimax Alpha-beta Expectimax Evaluation Function**:
### **Most fun**:
   he first evaluation function was most fun of all The second was not(I believe I was trying to use too little lines of code ),  As I started  finding ways to increase value, I could see changes in pac-man's play gradually\
   improving. This  motivated min to continue trying more and more  to win game where there were two ghosts were present. the most won was two out of 10
   while it was fun to keep improving the evaluation  function  I had to move on to  questions 2 to five.
### **challenges**:
   Minimax: Minimax agent was quite the challenge,  At first I was evaluating each level(depth) of play  and store the result in a matrix iteratively. the move of each agent is distributed
   randomly  between (North, South, East, west, stop) it was becoming increasingly complex to reserve dynamic memory based on  random depth  provided upon execution.  Once realised that it
   is only the final depth(leaves) that need to be evaluated and then propagated. The recursive function became apparent.
   The **alpha beta** pruning was simple in essence once mimimax was completed however the algorithm provided in the README.md has an issue(the same on both alphna and beta). **lines 5 and six needed to be interchanged**.  That is.  we need to update alpha before pruning, ensuring that alpha is  equal to the returned value(maximum).
   A different challenge was experienced in the **Expectimax** agent. in contrast to minimax and alpha beta expectimax does not choose an action until it is propagate to the root. My implementation issue was  i was choosing  the action with the highest probability of  play  on  each level. when this is propagated to the root pac-man ended up dying  almost always. once the probability was returned on behalf of the branch and not on  a specific leaf it passed all test.
### **Debugging**:
   In this second homework I also used the print function to understand the changing value of the evaluation functions
   I also used **type** and **dir** to understand each returned value  and how the could be used what function calls are available.
   this came in very handy i found out the big dots were called capsules.


## 2. **Written Problem-Solving** (Part 2): CSPs, Adversarial Search, and Evaluation Functions.
     Of the Three written questions,  conceptualizing  **question 1**, I failed to realized that when agent1 used agent2 utility function it was to  ne used on all levels (mx and min) not only on the adverse level. that is when u1 is maximizing, u2 is also maximizing.  
     In the execution of **Question2**  backtracking was beginning to confuse me. As I backtracking multiple nodes in instances where i only needed to backtrack, in the first attempt I ended up generating more that forty iterations and still didn't reach a terminal state which is when i realised i was backtracking multiple nodes. Once this bug  in my interaction was observed.
     I started over and  reached and reached the terminal state after sixteen iterations, this was a relief.
