#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time

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
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
               "total-cost" : 12})

    # Then we think a while and return another solution:
    time.sleep(10)
    yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
               "total-cost" : 10})

    # This solution will never befound, but that's ok; program will be killed eventually by the
    #  test script.
    while True:
        pass
    
    yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
               "total-cost" : 9})

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
