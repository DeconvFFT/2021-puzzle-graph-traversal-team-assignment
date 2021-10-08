#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Madhav Jariwala 2000930237
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#

import numpy as np
from math import radians, cos, sin, asin, sqrt
from math import tanh

def get_data_from_road_segments():
    with open('road-segments.txt','r') as f:
        return [data.split(' ') for data in [line.rstrip('\n') for line in f.readlines()]]

def get_data_from_city_gps():
    with open('city-gps.txt','r') as f:
        return [data.split(' ') for data in [line.rstrip('\n') for line in f.readlines()]]
    
def find_possible_next_step(current_position,road_segments,city_gps):
    all_possible_roads_first_way = [i for i in range(len(road_segments)) if road_segments[i][0]==current_position]
    all_possible_roads_second_way = [i for i in range(len(road_segments)) if road_segments[i][1]==current_position]
    return [all_possible_roads_first_way,all_possible_roads_second_way]

# def segments_heuristic(road_segments,current_position,end,city_gps):
#     possible_step_one_way,possible_step_second_way = find_possible_next_step(current_position,road_segments,city_gps)
#     if possible_step_one_way!=[]:
#         for i in range(len(possible_step_one_way)):
#             if road_segments[possible_step_one_way[i]][1]==end:
#                 return 1
#     if possible_step_second_way!=[]:
#         for i in range(len(possible_step_second_way)):
#             if road_segments[possible_step_second_way[i]][0]==end:
#                 return 1
#     return 2

def segments_heuristic(road_segments,current_position,end,city_gps,ending_city_gps_info):
    if current_position in [k[0] for k in city_gps]:
        next_current_position_gps = [j for j in city_gps if j[0]==current_position][0]
        distance = haversine_distance(next_current_position_gps[1],next_current_position_gps[2],ending_city_gps_info[1],ending_city_gps_info[2])*0.62137
        maximum_length_segment = np.array([road_segments[i][2] for i in range(len(road_segments))],dtype='float').max()
        return distance/maximum_length_segment
    else:
        return 0

#The following code was taken from stackoverflow from this link https://stackoverflow.com/a/15737218
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1 = float(lat1)
    lat2 = float(lat2)
    lon1 = float(lon1)
    lon2 = float(lon2)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km
#the copied code ended here

# def time_heuristic(road_segments,previous_position,current_position,city_gps,ending_city_gps_info):
#     try:
#         next_current_position_gps = [j for j in city_gps if j[0]==current_position][0]
#         distance = haversine_distance(next_current_position_gps[1],next_current_position_gps[2],ending_city_gps_info[1],ending_city_gps_info[2])*0.62137
#         speed_limit = np.array([road_segments[i][3] for i in range(len(road_segments))],dtype='float').max()
#         return (distance/speed_limit)
#     except:
#         return 0

def time_heuristic(road_segments,previous_position,current_position,city_gps,ending_city_gps_info):
    if current_position in [k[0] for k in city_gps]:
        next_current_position_gps = [j for j in city_gps if j[0]==current_position][0]
        distance = haversine_distance(next_current_position_gps[1],next_current_position_gps[2],ending_city_gps_info[1],ending_city_gps_info[2])*0.62137
        speed_limit = np.array([road_segments[i][3] for i in range(len(road_segments))],dtype='float').max()
        return distance/speed_limit
    else:
        return 0

def distance_heuristic(road_segments_length,previous_position,current_position,city_gps,ending_city_gps_info):
    try:
        next_current_position_gps = [j for j in city_gps if j[0]==current_position][0]
        return (haversine_distance(next_current_position_gps[1],next_current_position_gps[2],ending_city_gps_info[1],ending_city_gps_info[2])*0.62137)
    except:
#         next_current_position_gps = [j for j in city_gps if j[0]==current_position][0]
        return 0

def segments(start,end):
    city_gps = get_data_from_city_gps()
    road_segments = get_data_from_road_segments()
    starting_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==start][0]]
    ending_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==end][0]]
    
    current_position = starting_city_gps_info[0]
    heu = segments_heuristic(road_segments,start,end,city_gps,ending_city_gps_info)
    curr_cost = 0
    curr_f = heu+curr_cost
    route_taken = []
    fringe = [(current_position,curr_cost,heu,curr_f,route_taken)]
    closed = set()
    while fringe:
        if fringe!=[]:
            if fringe[-1][3] <= np.min(np.array(fringe,dtype='object')[:,3]):
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop()
            else:
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop(np.argmin(np.array(fringe,dtype='object')[:,3]))
            closed.add(current_position)
            if current_position==end:
                return(current_position,route_taken)
            possible_step_one_way,possible_step_second_way = find_possible_next_step(current_position,road_segments,city_gps)
            if possible_step_second_way!=[]:
                for i in range(len(possible_step_second_way)):
                    if road_segments[possible_step_second_way[i]][0] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h = segments_heuristic(road_segments,road_segments[possible_step_second_way[i]][0],end,city_gps,ending_city_gps_info)
                        curr_f = curr_h+curr_cost+1
                        temp_route_taken.append((road_segments[possible_step_second_way[i]],road_segments[possible_step_second_way[i]][0]))
                        fringe.append((road_segments[possible_step_second_way[i]][0],curr_cost+1,curr_h,curr_f,temp_route_taken))
            if possible_step_one_way!=[]:
                for i in range(len(possible_step_one_way)):
                    if road_segments[possible_step_one_way[i]][1] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h = segments_heuristic(road_segments,road_segments[possible_step_one_way[i]][1],end,city_gps,ending_city_gps_info)
                        curr_f = curr_h+curr_cost+1
                        temp_route_taken.append((road_segments[possible_step_one_way[i]],road_segments[possible_step_one_way[i]][1]))   
                        fringe.append((road_segments[possible_step_one_way[i]][1],curr_cost+1,curr_h,curr_f,temp_route_taken))
                        
def distance(start,end):
    city_gps = get_data_from_city_gps()
    road_segments = get_data_from_road_segments()
    starting_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==start][0]]
    ending_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==end][0]]
    
    heu = distance_heuristic(0,start,start,city_gps,ending_city_gps_info)
    current_position = starting_city_gps_info[0]
    curr_cost = 0
    curr_f = heu+curr_cost
    route_taken = []
    fringe = [(current_position,curr_cost,heu,curr_f,route_taken)]
    closed = set()
    
    while fringe:
        if fringe!=[]:
            if fringe[-1][3] <= np.min(np.array(fringe,dtype='object')[:,3]):
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop()
            else:
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop(np.argmin(np.array(fringe,dtype='object')[:,3]))
            closed.add(current_position)
            if current_position==end:
                return(current_position,route_taken)
            possible_step_one_way,possible_step_second_way = find_possible_next_step(current_position,road_segments,city_gps)
            if possible_step_second_way!=[]:
                for i in range(len(possible_step_second_way)):
                    if road_segments[possible_step_second_way[i]][0] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h = float(distance_heuristic(float(road_segments[possible_step_second_way[i]][2]),route_taken,road_segments[possible_step_second_way[i]][0],city_gps,ending_city_gps_info))
                        curr_f = curr_h+curr_cost + float(road_segments[possible_step_second_way[i]][2])
                        temp_route_taken.append((road_segments[possible_step_second_way[i]],road_segments[possible_step_second_way[i]][0]))
                        fringe.append((road_segments[possible_step_second_way[i]][0],curr_cost+float(road_segments[possible_step_second_way[i]][2]),curr_h,curr_f,temp_route_taken))
            if possible_step_one_way!=[]:
                for i in range(len(possible_step_one_way)):
                    if road_segments[possible_step_one_way[i]][1] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h =float(distance_heuristic(float(road_segments[possible_step_one_way[i]][2]),route_taken,road_segments[possible_step_one_way[i]][1],city_gps,ending_city_gps_info))
                        curr_f = curr_h+curr_cost + float(road_segments[possible_step_one_way[i]][2])
                        temp_route_taken.append((road_segments[possible_step_one_way[i]],road_segments[possible_step_one_way[i]][1]))
                        fringe.append((road_segments[possible_step_one_way[i]][1],curr_cost+float(road_segments[possible_step_one_way[i]][2]),curr_h,curr_f,temp_route_taken))

def time(start,end):
    city_gps = get_data_from_city_gps()
    road_segments = get_data_from_road_segments()
    starting_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==start][0]]
    ending_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==end][0]]
    
    heu = time_heuristic(road_segments,start,start,city_gps,ending_city_gps_info)
    current_position = starting_city_gps_info[0]
    curr_cost = 0
    curr_f = heu+curr_cost
    route_taken = []
    fringe = [(current_position,curr_cost,heu,curr_f,route_taken)]
    closed = set()
    
    while fringe:
        if fringe!=[]:
            if fringe[-1][3] <= np.min(np.array(fringe,dtype='object')[:,3]):
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop()
            else:
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop(np.argmin(np.array(fringe,dtype='object')[:,3]))
            closed.add(current_position)
            if current_position==end:
                return(current_position,route_taken)
            possible_step_one_way,possible_step_second_way = find_possible_next_step(current_position,road_segments,city_gps)
            if possible_step_second_way!=[]:
                for i in range(len(possible_step_second_way)):
                    if road_segments[possible_step_second_way[i]][0] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h = float(time_heuristic(road_segments,route_taken,road_segments[possible_step_second_way[i]][0],city_gps,ending_city_gps_info))
                        time_taken = float(road_segments[possible_step_second_way[i]][2])/float(road_segments[possible_step_second_way[i]][3])
                        curr_f = curr_h+curr_cost +time_taken
                        temp_route_taken.append((road_segments[possible_step_second_way[i]],road_segments[possible_step_second_way[i]][0]))
                        fringe.append((road_segments[possible_step_second_way[i]][0],curr_cost+time_taken,curr_h,curr_f,temp_route_taken))
            if possible_step_one_way!=[]:
                for i in range(len(possible_step_one_way)):
                    if road_segments[possible_step_one_way[i]][1] not in closed:
                        temp_route_taken = route_taken.copy()
                        curr_h =float(time_heuristic(road_segments,route_taken,road_segments[possible_step_one_way[i]][1],city_gps,ending_city_gps_info))
                        time_taken = float(road_segments[possible_step_one_way[i]][2])/float(road_segments[possible_step_one_way[i]][3])
                        curr_f = curr_h+curr_cost + time_taken
                        temp_route_taken.append((road_segments[possible_step_one_way[i]],road_segments[possible_step_one_way[i]][1]))
                        fringe.append((road_segments[possible_step_one_way[i]][1],curr_cost+time_taken,curr_h,curr_f,temp_route_taken))
    
def delivery_heuristic(time_taken,length,speed_limit,curr_cost):
    if speed_limit>=50:
        return time_taken + (tanh(length/1000))*2*(time_taken+curr_cost)
    else:
        return 0
        
    
def delivery(start,end):
    city_gps = get_data_from_city_gps()
    road_segments = get_data_from_road_segments()
    starting_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==start][0]]
    ending_city_gps_info = city_gps[[i for i in range(len(city_gps)) if city_gps[i][0]==end][0]]
    
    curr_cost = 0
    heu = delivery_heuristic(0,0,0,curr_cost)
    current_position = starting_city_gps_info[0]
    curr_f = heu+curr_cost
    route_taken = []
    fringe = [(current_position,curr_cost,heu,curr_f,route_taken)]
    closed = set()
    
    while fringe:
        if fringe!=[]:
            if fringe[-1][3] <= np.min(np.array(fringe,dtype='object')[:,3]):
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop()
            else:
                (current_position, curr_cost, curr_h,curr_f,route_taken) = fringe.pop(np.argmin(np.array(fringe,dtype='object')[:,3]))
            closed.add(current_position)
            if current_position==end:
                return(current_position,route_taken)
            possible_step_one_way,possible_step_second_way = find_possible_next_step(current_position,road_segments,city_gps)
            if possible_step_second_way!=[]:
                for i in range(len(possible_step_second_way)):
                    if road_segments[possible_step_second_way[i]][0] not in closed:
                        temp_route_taken = route_taken.copy()
                        length = float(road_segments[possible_step_second_way[i]][2])
                        speed_limit = float(road_segments[possible_step_second_way[i]][3])
                        time_taken = length/speed_limit
                        curr_h = float(delivery_heuristic(time_taken,length,speed_limit,curr_cost))
                        curr_f = curr_h+curr_cost +time_taken
                        temp_route_taken.append((road_segments[possible_step_second_way[i]],road_segments[possible_step_second_way[i]][0]))
                        fringe.append((road_segments[possible_step_second_way[i]][0],curr_cost+time_taken,curr_h,curr_f,temp_route_taken))
            if possible_step_one_way!=[]:
                for i in range(len(possible_step_one_way)):
                    if road_segments[possible_step_one_way[i]][1] not in closed:
                        temp_route_taken = route_taken.copy()
                        length = float(road_segments[possible_step_one_way[i]][2])
                        speed_limit = float(road_segments[possible_step_one_way[i]][3])
                        time_taken = length/speed_limit
                        curr_h = float(delivery_heuristic(time_taken,length,speed_limit,curr_cost))
                        curr_f = curr_h+curr_cost + time_taken
                        temp_route_taken.append((road_segments[possible_step_one_way[i]],road_segments[possible_step_one_way[i]][1]))
                        fringe.append((road_segments[possible_step_one_way[i]][1],curr_cost+time_taken,curr_h,curr_f,temp_route_taken))

    
    
    
# !/usr/bin/env python3
import sys
def get_route(start, end, cost):
    if cost =='segments':
        result = segments(start,end)
    elif cost == 'distance':
        result = distance(start,end)
    elif cost=='time':
        result = time(start,end)
    else:
        result = delivery(start,end)
    

        
    total_segments = len(result[1])
    total_miles = 0
    total_hours = 0
    route_taken = []
    total_delivery_hours = 0

    for i in range(len(result[1])):
        total_miles+=float(result[1][i][0][2])
        time_taken = (float(result[1][i][0][2])/float(result[1][i][0][3]))
        route_taken.append((result[1][i][1],str(result[1][i][0][4])+" for "+str(result[1][i][0][2])+" miles"))
        if float(result[1][i][0][3]) >=50:
            total_delivery_hours+= (time_taken + tanh(float(result[1][i][0][2])/1000)*2*(time_taken+total_hours))
        else:
            total_delivery_hours+=time_taken
        total_hours+=time_taken

    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    
#     route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
#                    ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
#                    ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    # print('result is:', result)
    return {"total-segments" : total_segments, 
            "total-miles" : total_miles, 
            "total-hours" : total_hours, 
            "total-delivery-hours" : total_delivery_hours, 
            "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])