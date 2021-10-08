#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
import random



#returns all the successor function:
def succ(state):
    all_succ = []
    for i in range(len(state)-1):


        if len(state[i].split('-'))<3:
            for j in range(i+1, len(state)):
                # print(all_succ)
                # print(state[i])
                # print(len(state[i]))
                if len(state[i].split('-')) + len(state[j].split('-')) < 4:
                    temp_arr = state.copy()
                    temp_arr[i] = temp_arr[i]+ '-' + temp_arr[j]
                    temp_arr.pop(j)
                    all_succ.append(temp_arr)

    return all_succ


#returns the cost:
def cost(succ_step, team_wanted, random_teammates_number,not_to_work_with):
    cost = len(succ_step)*5
    #print(succ_step)



    #is the same team?
    count_for_wrong_teammate = 0
    count_for_wrong_team_size = 0
    count_for_assigned_to_not_to_work_with = 0

    for succ_team in succ_step:
        count = 0
        for succ_team_member in succ_team.split('-'):
            #count number of 'xxx' and skip the cost increment for that many times if team member is random
            
            for requested_team_member in team_wanted[succ_team_member]:
                if requested_team_member not in succ_team.split('-'):
                    if count >= random_teammates_number[succ_team_member]:
                        cost = cost + 3
                        count_for_wrong_teammate +=1
                    else:
                        count = count+1
    #is team size same
    for succ_team in succ_step:
        for succ_team_member in succ_team.split('-'):
            if len(succ_team.split('-')) != len(team_wanted[succ_team_member]):
                cost = cost+2
                count_for_wrong_team_size +=1
        
    #Student assigned to someone they DO NOT want to work with
    for succ_team in succ_step:
        for succ_team_member in succ_team.split('-'):
            #print("succ_team_member:",succ_team_member)
            #print("not_to_work_with[succ_team_member]:",not_to_work_with[succ_team_member])
            for team_member in not_to_work_with[succ_team_member]:
                
                if team_member in succ_team.split('-'):
                    cost = cost + 10   
                    count_for_assigned_to_not_to_work_with +=1 

    # print("succ_step:",succ_step)
    # print("count_for_wrong_teammate:",count_for_wrong_teammate)
    # print("count_for_wrong_team_size:",count_for_wrong_team_size)
    # print("count_for_assigned_to_not_to_work_with:",count_for_assigned_to_not_to_work_with)
    # print("Cost:", cost)
    return cost


def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """

    # Simple example. First we yield a quick solution
    #yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
    #           "total-cost" : 12})

    # Then we think a while and return another solution:
    # time.sleep(10)
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
    #            "total-cost" : 10})



    grups_survey = []
    team_wanted = {}
    username = []
    not_to_work_with = {}
    random_teammates_number_xxx = {}
    random_teammates_number_zzz = {}
    random_teammates_number = {}

    succ_step = {}

    with open(input_file) as my_file:
        for line in my_file:
            grups_survey.append(line.split())
    
    
    for i in range(len(grups_survey)):
        username.append(grups_survey[i][0])
        team_wanted[grups_survey[i][0]] = grups_survey[i][1].split("-")
        not_to_work_with[grups_survey[i][0]] = grups_survey[i][2].split(",")
        random_teammates_number_xxx[grups_survey[i][0]] = grups_survey[i][1].split("-").count("xxx")
        random_teammates_number_zzz[grups_survey[i][0]] = grups_survey[i][1].split("-").count("zzz")

    # print(sum(random_teammates_number_zzz.values()))
    # print(sum(random_teammates_number_xxx.values()))
    
    if sum(random_teammates_number_zzz.values()) > sum(random_teammates_number_xxx.values()):
        random_teammates_number = random_teammates_number_zzz
    else:
        random_teammates_number = random_teammates_number_xxx

    #print(username)


    #main while loop after initials:
    initial_team = username
    initial_team.sort()
    fringe = []
    fringe.append(initial_team)
    closed = []
    closed.append(initial_team)



    last_team = []
    last_team_cost = 99999999999 #some large value
    

    while True:
        
        if fringe == [[]]:
            break
        team = fringe.pop()
        cost_of_team = cost(team, team_wanted, random_teammates_number,not_to_work_with)

        if cost_of_team < last_team_cost:
            last_team_cost = cost_of_team
            last_team = team
            #print(last_team, last_team_cost)
            yield({"assigned-groups": last_team,"total-cost" : last_team_cost})
        
        #print(len(fringe))
        #print("Fringe:",fringe)
        successor = succ(team)
        

        #calculate the minimum cost from the successor and append minimum cost to the fringe:
        min_succ = []
        min_cost = 9999999999999
        for i in successor:
            cost_of_successor = cost(i,team_wanted, random_teammates_number,not_to_work_with)
            if min_cost > cost_of_successor:
                min_succ = i
                min_cost = cost_of_successor

        
        fringe.append(min_succ)
        closed.append(min_succ)

    #to remove the last empty list
    if closed[-1] == []:
            closed.pop()
    



    print("-----")
    #second loop to restart randomly:
    while True:
        #print(len(closed))
        fringe = []

        #go to a random team and start iterating using local search
        random_number = random.randint(0,len(closed)-1)
        random_successors = succ(closed[random_number])
        
        if len(random_successors) == 0:
            continue

        # print("Closed:",closed[random_number])
        # print("length of successor:", len(random_successors))
        # print(closed)
        random_number = random.randint(0,len(random_successors)-1)
        random_team_from_random_successors = random_successors[random_number]

        #print('random_team_from_random_successors',random_team_from_random_successors)



        if random_team_from_random_successors in closed:
            continue


        closed.append(random_team_from_random_successors)
        fringe.append(random_team_from_random_successors)



        #print('Length of fringe',len(closed))
        while True:
            if fringe == [[]]:
                break
            #print(fringe)
            team = fringe.pop()
            cost_of_team = cost(team, team_wanted, random_teammates_number,not_to_work_with)

            if cost_of_team < last_team_cost:
                last_team_cost = cost_of_team
                last_team = team
                #print(last_team)
                yield({"assigned-groups": last_team,"total-cost" : last_team_cost})            
            #print(len(fringe))
            #print("Fringe:",fringe)
            successor = succ(team)
            

            #calculate the minimum cost from the successor and append minimum cost to the fringe:
            min_succ = []
            min_cost = 9999999999999
            for i in successor:
                cost_of_successor = cost(i,team_wanted, random_teammates_number,not_to_work_with)
                if min_cost > cost_of_successor:
                    min_succ = i
                    min_cost = cost_of_successor

            
            fringe.append(min_succ)
            closed.append(min_succ)
            #print(fringe)
        #to remove the last empty list if there
        if closed[-1] == []:
            closed.pop()
        





    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    # while True:
    #     pass




    
    # yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
    #            "total-cost" : 9})

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])