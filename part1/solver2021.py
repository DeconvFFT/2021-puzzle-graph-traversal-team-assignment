#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: mehtasau mehtasau@iu.edu
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
from copy import deepcopy
from queue import PriorityQueue
from scipy.spatial.distance import cdist
from timeit import default_timer
import heapq

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# All possible moves permitted for the board

# rotate a row left by 1
def rotate_left(state, row, step):
    state[row,:] = np.roll(state[row,:], -step)

# rotate a row left by 1
def rotate_right(state, row, step):
    state[row,:] = np.roll(state[row,:], step)

# rotate column up by 1
def move_up(state,column, step):
    state[:,column] = np.roll(state[:,column], -step)

# rotate column down by 1
def move_down(state,column, step):
    state[:,column] = np.roll(state[:,column], step)

# rotate outer ring clockwise
def rotate_outer_clock(state,nrows, ncols, step):
    step%=nrows
    tl = state[0,0]
    tr = state[0,ncols-1]
    bl = state[nrows-1,0]
    br = state[nrows-1,ncols-1]

    # rotate first row
    state[0,:][step:] = state[0,:][:-step]
    # rotate first column up
    state[:,0][:-step] = state[:,0][step:]
    # rotate last row left
    state[nrows-1,:][:-step] = state[nrows-1,:][step:]
    # rotate last column down 
    state[:,ncols-1][step:] = state[:,ncols-1][:-step]
    state[0+1,ncols-1] = tr

# rotate outer ring counter clockwise
# rotate outer ring clockwise
def rotate_outer_counterclock(state,nrows, ncols, step):
    step%=nrows
    tl = state[0,0]
    tr = state[0,ncols-1]
    bl = state[nrows-1,0]
    br = state[nrows-1,ncols-1]

    # rotate first row
    state[0,:][:-step]= state[0,:][step:] 
    # rotate first column up
    state[:,0][step:] = state[:,0][:-step]
    # rotate last row left
    state[nrows-1,:][step:] = state[nrows-1,:][:-step]
    # rotate last column down 
    state[:,ncols-1][:-step] = state[:,ncols-1][step:]

    state[0+1,0] = tl
    state[nrows-2,ncols-1] = br
    state[nrows-1,0+1] = bl

# rotate innner ring clockwise
def rotate_inner_clock(state,nrows, ncols, step):
    step%=nrows
    minrow = 0
    mincol = 0
    tl = state[minrow+1,mincol+1]
    tr = state[minrow+1,ncols-2]
    bl = state[nrows-2,mincol+1]
    br = state[nrows-2,ncols-2]

    # rotate first inner row
    state[minrow+1,mincol+1:ncols-1][step:] = state[minrow+1,mincol+1:ncols-1][:-step]
    # # rotate first inner column up
    state[minrow+1:nrows-1,mincol+1][:-step] = state[minrow+1:nrows-1,mincol+1][step:]
    # # rotate last inner row left
    state[nrows-2,mincol+1:ncols-1][:-step] = state[nrows-2,mincol+1:ncols-1][step:]
    # # rotate last inner column down 
    state[minrow+1:nrows-1,ncols-2][step:] = state[minrow+1:nrows-1,ncols-2][:-step]
    state[minrow+2,ncols-2] = tr


# rotate inner ring counter clockwise
def rotate_inner_counterclock(state,nrows, ncols, step):
    step%=nrows
    minrow = 0
    mincol = 0
    tl = state[minrow+1,mincol+1]
    tr = state[minrow+1,ncols-2]
    bl = state[nrows-2,mincol+1]
    br = state[nrows-2,ncols-2]

    # rotate first row
    state[minrow+1,mincol+1:ncols-1][:-step]= state[minrow+1,mincol+1:ncols-1][step:] 
    # rotate first column up
    state[minrow+1:nrows-1,mincol+1][step:] = state[minrow+1:nrows-1,mincol+1][:-step]
    # rotate last row left
    state[nrows-2,mincol+1:ncols-1][step:] = state[nrows-2,mincol+1:ncols-1][:-step]
    # rotate last column down 
    state[minrow+1:nrows-1,ncols-2][:-step] = state[minrow+1:nrows-1,ncols-2][step:]

    state[minrow+2,mincol+1] = tl
    state[nrows-3,ncols-2] = br
    state[nrows-2,mincol+2] = bl


# heuristic function
# calculates number of misplaced tiles
def misplaced_tiles(state, goal, cost_so_far):
    diffarray = np.subtract(state, goal)
    # These lines of code were inspired from https://numpy.org/doc/stable/reference/generated/numpy.count_nonzero.html
    return np.count_nonzero(diffarray)+cost_so_far


# # calculate row distances

# # calculates manhatten distance of elements
def total_moves(state,goal, cost_sofar, move_str):
    total_dist = 0
    rows = ROWS
    for r in range(len(state)):
        for c in range(len(state[0])):

            idx1 = (r,c)
            idx2 = np.where(goal == state[r][c])
            ri = (idx1[0]-idx2[0])%rows
            ci = (idx1[1]-idx2[1])%rows

            rj = (idx2[0]-idx1[0])%rows
            cj = (idx2[1]-idx1[1])%rows

            rici = ri+ci
            ricj = ri+cj
            rjci = rj+ci
            rjcj = rj+cj

            manhatten = min(rici,ricj,rjci,rjcj)[0]

            total_dist+=manhatten
    if("I" in move_str):
        total_dist//=8
    if ("O" in move_str):
        total_dist//=16
    if("L" in move_str or "R" in move_str or "U" in move_str or "D" in move_str):
        total_dist//=5
    print("total_dist: {}".format(total_dist))
    return total_dist+cost_sofar

# # calculates manhatten distance of elements

def total_moves1(state,goal, cost_sofar):
    total_dist = 0
    rows = ROWS
    lmoves = []
    rmoves = []
    umoves = []
    dmoves = []
    for r in range(len(state)):
        for c in range(len(state[0])):
            idx1 = (r,c)
            idx2 = np.where(goal == state[r][c])
            idx1 = (r,c)
            idx2 = np.where(goal == state[r][c])
            ri = (idx1[0]-idx2[0])%rows
            ci = (idx1[1]-idx2[1])%rows

            rj = (idx2[0]-idx1[0])%rows
            cj = (idx2[1]-idx1[1])%rows

            rici = ri+ci
            ricj = ri+cj
            rjci = rj+ci
            rjcj = rj+cj

            manhatten = min(rici,ricj,rjci,rjcj)[0]
            #print("r: {}, c:{}, ri: {}, rj:{}, ci:{}, cj:{}, rici: {}, ricj: {}, rjci: {}, rjcj: {}, manhatten: {}".format(r,c,ri,rj,ci,cj, rici, ricj, rjci, rjcj,manhatten))

            total_dist+=manhatten
        
    
    diffarray = np.subtract(state, goal)
    misplaced = np.count_nonzero(diffarray)
    if(misplaced<=5):
        total_dist//=5
    elif(misplaced >5 and misplaced <=16):
        total_dist//=8
    elif(misplaced>16):
        total_dist//=16

    print("total_dist: {}".format(total_dist))

    return total_dist+cost_sofar



# return a list of possible successor states
def successors(state):
    #print(state)
    successor_list = []
    row = 0
    col = 0
    state_row = state[row]
    
    for r in range(ROWS):
        #rotate row left
        state_new = deepcopy(state)

        rotate_left(state_new,r,1)
        move_str = "L"+str(r+1)
        successor_list.append((state_new, move_str))

        # rotate row right
        state_new = deepcopy(state)
        rotate_right(state_new,r, 1)

        move_str = "R"+str(r+1)
        successor_list.append((state_new, move_str))

    for c in range(COLS):
        # rotate column up
        state_new = deepcopy(state)
        move_up(state_new, c, 1)
        move_str = "U"+str(c+1)
        successor_list.append((state_new, move_str))

        # rotate column down
        state_new = deepcopy(state)
        move_down(state_new, c, 1)
        move_str = "D"+str(c+1)
        successor_list.append((state_new, move_str))

    # outer ring clockwise
    state_new = deepcopy(state)
    rotate_outer_clock(state_new, ROWS, COLS, 1)
    move_str = "Oc"
    successor_list.append((state_new, move_str))
    # outer ring counterclockwise
    state_new = deepcopy(state)
    rotate_outer_counterclock(state_new, ROWS, COLS, 1)
    move_str = "Occ"
    successor_list.append((state_new, move_str))

    # inner ring clockwise
    state_new = deepcopy(state)
    rotate_inner_clock(state_new, ROWS, COLS, 1)
    move_str = "Ic"
    successor_list.append((state_new, move_str))
    # inner ring counter clockwise
    state_new = deepcopy(state)
    rotate_inner_counterclock(state_new, ROWS, COLS, 1)
    move_str = "Icc"
    successor_list.append((state_new, move_str))

    return successor_list

# check if we've reached the goal
def is_goal(state, goal):
    flat_state = list(state.flatten())
    #flat_goal = list(goal.flatten())
    #print("flat_state: {}, flat_goal: {}", flat_state,sorted(flat_state) )
    if(sorted(flat_state) == flat_state):  
        return True
    return False



def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    fringe = PriorityQueue()
    
    #fringe = []
    # cost of the path travelled so far
    dist = 0

    from itertools import count

    # a global
    tiebreaker = count()
    #print(type(initial_board))
    state_mat = np.asarray(initial_board).reshape(5,5)
    #print("state_mat: {}".format(state_mat))
    goal_mat = np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])
    movestr = []
    init_priority = total_moves(state_mat, goal_mat,0, "")
    #init_priority = total_moves1(state_mat, goal_mat,0)

    #return 10
    fringe.put((init_priority, state_mat.tostring(),""))

    #fringe.append((init_priority, state_mat.tostring(),""))
    #heapq.heapify(fringe)
    
    
    count = 0
    visited = {}
    
    # store the predcessors of the current state
    predecessors = dict()
    ms = ""
    while not fringe.empty():
        (cost, state, route_so_far) = fringe.get()
        visited[state] = cost
        if(is_goal(np.fromstring(state,int).reshape(5,5), goal_mat)):
            routelist = route_so_far.split(" ")
            print("routelist: {}".format(routelist))

            return routelist
        else:
            for (s,move_str) in successors(np.fromstring(state,int).reshape(5,5)):
                #break
                route = ""
                if(route_so_far == ""):
                    route = move_str
                else:
                    route=str( route_so_far + " " + move_str )
                cost_so_far=len(route_so_far.split())
                f = total_moves(s,goal_mat,cost_so_far, move_str)
                #f = total_moves1(s,goal_mat,cost_so_far)

                #print("h: {}, move: {}".format(f, route))

                print("state: {}, h: {}, moves: {}".format(s, f,route))

                #total_mahnatten_distance(s,goal_mat)
                if s.tostring() not in visited:
                    #visited[s.tostring()] = h+cost+1

                    elem_list = [x[1] for x in fringe.queue]
                    # #print("elem_list: {}".format(elem_list))
                    if(s.tostring() in elem_list):
                        #print("elem_list.index(s.tostring()): {}".format(elem_list.index(s.tostring())))
                        idx = elem_list.index(s.tostring())
                        #print("cost_so_far: {}, len(fringe.queue[idx][2]): {}".format(cost_so_far,len(fringe.queue[idx][2].split(" "))))
                        
                        #if(cost_so_far<len(fringe.queue[idx][2].split(" "))):
                        if(f < fringe.queue[idx][0]):
                            #print("before, fringe.queue[idx], fringe.queue[0]: {}",fringe.queue[idx], fringe.queue[0])

                            fringe.queue[idx], fringe.queue[0] = fringe.queue[0], fringe.queue[idx]
                            #print("after, fringe.queue[idx], fringe.queue[0]: {}",fringe.queue[idx], fringe.queue[0])
                            fringe.get()

                    # if s.tostring() not in fringe.queue:
                    fringe.put((f, s.tostring(),route))
                    count+=1

                # if(count>=1):
                #    break

    return False

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    print(type(start_state))

    start_solve = default_timer()
    route = solve(tuple(start_state))
    end_solve = default_timer()

    solve_time = end_solve - start_solve
    print("Time take to reach the solution: {}".format(solve_time))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
