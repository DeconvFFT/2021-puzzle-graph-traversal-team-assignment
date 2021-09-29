import numpy as np
def rotate(nums, k) -> None:
    k %= len(nums)
    nums[k:], nums[:k] = nums[:-k], nums[-k:]

def distance(val, idx1,len_my_list,l2):
    # val = l1[0][1]
    idx1 = idx1
    idx2 = np.where(l2 == val)
    ri = (idx1[0]-idx2[0])%len_my_list
    ci = (idx1[1]-idx2[1])%len_my_list

    rj = (idx2[0]-idx1[0])%len_my_list
    cj = (idx2[1]-idx1[1])%len_my_list

    rici = ri+ci
    ricj = ri+cj
    rjci = rj+ci
    rjcj = rj+cj
    print(val,idx1,min(rici,ricj,rjci,rjcj))

    #j = rj+cj
    # i = (idx_1 - idx_2) % len_my_list
    # j = (idx_2 - idx_1) % len_my_list
    return min(rici,ricj,rjci,rjcj)[0]

if __name__ == '__main__':
    nums = np.array([[2,3,4,5,10],
    [6,7,8,9,1]])
    nums2 = np.array([[4,5,3,10,6],
    [1,7,2,9,8]])


    #5x5 
    init = np.array([[2,23,4,5,10],
    [1,7,3,9,11],
    [6,13,8,15,20],
    [12,17,14,19,25],
    [16,21,22,18,24]])

    goal = np.array([[1,2,3,4,5],
    [6,7,8,9,10],
    [11,12,13,14,15],
    [16,17,18,19,20],
    [21,22,23,24,25]])

    dist = {}
    for r in range(len(init)):
        for c in range(len(init[0])):
            d = distance(init[r][c], (r,c),len(init), goal)
            #print(d)
            dist[init[r][c]] = d
    
    
    dist_vals = list(dist.values())
    print("distances: {}".format(dist_vals))
    print(sum(dist_vals), sum(dist_vals)/5)
    k = 1
    
    #print(distance(init, 5,goal))