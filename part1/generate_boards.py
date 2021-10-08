import numpy as np
import random
from copy import deepcopy
import re

def generate_new(board):
    copyboard = deepcopy(board)
    random.shuffle(copyboard)
    return copyboard

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

def move_board(state, move, step):
    
    print("move.split: {}",move)
    if "U" in move:
        column = re.findall('\d+', move)[0]
        column = int(column)
        print(column)
        move_up(state, column-1, 1)
    elif "D" in move:
        column = re.findall('\d+', move)[0]
        column = int(column)
        move_down(state, column-1, 1)
    elif "L" in move:
        row = re.findall('\d+', move)[0]
        row = int(row)
        rotate_left(state, row-1, 1)
    elif "R" in move:
        row = re.findall('\d+', move)[0]
        row = int(row)
        rotate_right(state, row-1, 1)
    elif "Occ" in move:
        rotate_outer_counterclock(state, 5, 5, 1)
    elif "Oc" in move:
        rotate_outer_clock(state, 5,5,1)
    elif "Icc" in move:
        rotate_inner_counterclock(state, 5,5,1)
    else:
        rotate_inner_clock(state, 5, 5, 1)

if __name__ == "__main__":
    
    start_state_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    start_state = np.array(start_state_list).reshape(5,5)

    new_state = deepcopy(start_state)

    #,"R2","Occ","U3","D4"
    moves = ["Icc","U2","R2","Occ","U3","D4"]
    print("start_state: {}".format(start_state))
    
    for move in moves:
        move_board(new_state, move, 1)
    print("new_state: {}".format(new_state))

    #new_state_arr = np.array(new_state).reshape(5,5)
    #print("new_state_arr: {}".format(new_state_arr))

    with open('board4.txt', 'w+') as file:
        for i in range(5):
            for j in range(5):
                file.write(str(new_state[i][j]))
                if(j < 4):
                    file.write(" ")
            file.write('\n')

