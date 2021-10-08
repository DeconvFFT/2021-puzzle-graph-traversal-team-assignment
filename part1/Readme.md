# Part 1: 2021 puzzle

## Formulating search problem

**How did we formulate the search problem?**

We broke of the 2021 puzzle problems into a sub problem of moving individual tiles into their goal position.

**Initial State**: 

A configuration of 2021 puzzle from the input file

**Goal State**: 

Ascending sorted arrangment of 2021 puzzle from 1 to 25.

**Successor Function**:

 A function that takes the current configuration(state) of 2021 puzzle and generates next states from that. Successor function applies a set of moves and generates new configurations of the current state. The possible moves that a successor can apply on L1, L2, L3, L4, L5, R1, R2, R3, R4, R5, U1, U2, U3, U4, U5, D1, D2, D3, D4, D5, Ic, Icc, Oc, Occ.  The moves with L will rotate the row left, moves with R will rotate the row to the right, the moves with U will rotate the column up and the moves with D with rotate the column down. Moves with I will rotate the inner ring in either clock or anti-clock wise. The moves with O will rotate the outer ring in either clock or anti-clock wise. 

**Set of states**: 

Set of all possible configurations of the 2021 puzzle

**Heuristic function**: 

Sum of walking distances between the current state of a tiles in the puzzle to the goal state of the tiles in the puzzle, divided by the number of tiles that can be moved from each move. For example, L, R, U, D moves will move 5 tiles from their current position. So h(s) will be ```math \frac{\sum(walking_distance)}{5}```. Moves Ic and Icc will move 8 tiles from their current position. So h(s) will be  ```math \frac{\sum(walking_distance)}{8}``` . Similarly, moves Occ and Oc will move 16 tiles from their current position. So h(s) will be  ```math \frac{\sum(walking_distance)}{16}```. 

**Cost function**: 

Cost of reaching the goal configuration from the initial configuration. It is taken as f(s) = h(s) + g(s). Here, g(s) is the length of the route travelled so far to reach the current state. For example, we reach a state with the moves L1, R2, Icc; then g(s) for that state would be 3. and f(s) would be h(s)+3.

## Working of the search algorithm
Search algorithm works as follows:
- Check if the initial state is the goal state.
- If it is, return "" 
- If not, calculate heuristic for that state and add it to thr fringe.
- Till the fringe is not empty, Repeat:
    - Remove a state from the fringe and check if it is a goal state.
    - If it is, return the new route to the goal state.
    - If not, generate the successors of that state as follows:
        - Generate a new state for each possible move that can be made on the current board. 
        - For each successor, do the following: 
            - Calculate heuristic for the successor.
            - Insert that successor into the fringe.


## Experiments 

### Experiments that we did before arriving at an admissible heuristic:

**A.) Heuristic function experiments:**

**1. Misplaced tiles**: 

For heuristic function, we first tried the heuristic of number of misplaced tiles. But this heuristic will overestimate by a lot as your number of misplaced tiles will almost always be more than the number of moves that can be made. Surprisingly, this heuristic produced correct number of moves for [a board 0](board0.txt) in 0.00095 seconds and for [a board 0.5](board0.5.txt) in 1.1409 seconds; because for smaller boards, A* with a non admissible heuristic acts as a greedy best first search. 

**2. Sum of walking distance divided by number of misplaced tiles**: 

We then tried the heuristic where we divided the sum of walking distances of all tiles with the number of misplaced tiles. But this heuristic will underestimate  by a lot and the running time for the [a board 0.5](board0.5.txt) exceeds 3 minutes. Thus we ended up with a very poor admissible heuristic. This heuristic is still admissible as it will never overestimate the true cost to the goal.

**3. Sum of walking distance divided by the number of tiles that are displaced with that move**:

We then tried the heuristic where we divided the sum  of walking distances of all tiles with the number of tiles that are moved/ displaced from their current position following a move to generate that successor. or example, L, R, U, D moves will move 5 tiles from their current position. So h(s) will be ```math \frac{\sum(walking_distance)}{5}```. Moves Ic and Icc will move 8 tiles from their current position. So h(s) will be  ```math \frac{\sum(walking_distance)}{8}``` . Similarly, moves Occ and Oc will move 16 tiles from their current position. So h(s) will be  ```math \frac{\sum(walking_distance)}{16}```.  This heuristic is admissible because it will never overestimate the true cost to the goal. 



### Experiments on different boards for the admissible heuristic:

We experimented with different boards with our admissible heuristics. We created some test cases of our own for boards with solutions to goal in 5,6,7,8 moves. Some of these files can be found here: [a board 8_0](board13.txt), [a board 8_1](board81.txt), [a board 8_2](board82.txt),[a board 6](board4.txt)
We also tried running our algorithm on board1, but it didn't return any solution for 30 minutes so we stopped the execution.

### Experiments with search algorithm

We tried using search algorithm 2 and search algorithm 3 to solve this problem. What we found from our experiment is that search algorithm 3 takes a lot of time to find the solution as compared to search algorithm 2. It might be the case that our heuristic is admissible but not consistent. As search algorithm 2 gave solution for most boards in a reasonable amount of time, we went ahead with search algorithm 2.

### Interesting findings from the experiments

We found some very insteresting results when running our experiments. 
- For [a board 8_2](board82.txt), we had generated the board using 8 moves but we got a solution in 5 moves. We traced those moves back and were able to generate the original board back. So, the solution returned by our algoritm was valid one.
- For [a board 8_0](board13.txt), we weren't able to generate a solution in under 30 minutes even though it was generated using 8 moves. This could be because we had too many ring operations on that board. For relatively simpler boards with around 2-3 ring moves, we can get a solution in under 5 minutes.

### What is the branching factor of this algorithm?
The branching factor is 24, because we are generating 24 states from each board. 

### If the solution can be reached in 7 moves,  about  how  many  states  would  we  need  to  explore  before  wefound it if we used BFS instead of A* search?

If we end up finding a solution after the first move after exploring 24^6 states, we would end up exploring only 24^6 states, if we end up exploring every state on the 7th level, we would need to explore 24^6+x states, and we would end up exploring 24^7 in the worst case.

So, we would end up exploring 24^7 states.