# Part 2

This assignment was part of the Elements of AI course, taught by Dr. David Crandall

## Description

This is my report explaining how I implemented the part 2 of the assignment

### Segments

Here, the heuristic function we used was total haversine distance from the successor node divide by the maximum segment length in the `road_segment` dataset. Here, the heuristic function is admissible as we will never overestimate the cost here. Dividing the Haversine distane between the successor node and the end node with the maximum length of a single segment gives us the minimum number of segments we might need to reach to the end goal.

The real challenge in this section was getting the optimal answer in short amount of time. As using any other variable to calculate the heuristic was being proven non-admissible.

The total cost would be calculated using 

`heuristic_cost + current_cost + 1(For each node)`

### Distance

Here, the heuristic function we used was calculating haversine distance between successor node and the end node. Here, our heuristic function is always admissible as we are calculating the minimum distance we have to cover to reach tho the end goal. So, here we are underestimating the cost.

Solution for this cost function was easy to find overall. 

The total cost would be calculated by heuristic cost, current_cost(in this total distance covered taken to reach to the current node), and segment length of successor node from the current node given in the `road_segment` dataset

`heuristic_cost + current_cost + segment_length`


### Time

Here, the heuristic function we used was calculating haversine distance between successor node and the end node, and divided it with the maximum number of speed limit which gave us the minium time(in hours) required to reach to the end goal. Here, our heuristic function is always admissible as we are using maximum speed limit given in the `road_segment` dataset and that will always give us the value where we would be underestimating the cost.

This portion wasn't much of a challenge as compared to the segments section as we were able to come up with a admissible heuristic function quire easily.

The total cost would be calculated by heuristic cost, current_cost(in this case the time taken to reach to the current node), and time it will take to reach to successor node from the current node, 

`heuristic_cost + current_cost + succesor_time`

### Delivery

Here, the heuristic fucntion we use was calculating the haversine distance between successor node and the end nore, and vibided it with the maximum number of speed limit which gave us the minimum time