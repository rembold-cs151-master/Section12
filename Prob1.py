
"""
Reading in and working with the Space Missions JSON data
"""

import json


def load_data():
    """Loads in the space_missions.json data and returns the corresponding dictionary
    
    Inputs:
        None
    Outputs:
        (dict) - The JSON dictionary
    """


def eva_count(data):
    """Computes how many different crew members have EVA certification and have served
    on missions that begin with an A.

    Inputs:
        data (dict) - The space missions dictionary
    Outputs:
        (int) - The count of the number of unique crew members
    """


def power_missions(data):
    """Filters to find the unique mission names where Navigation equipment, on average,
    was drawing more than 100 W.

    Inputs:
        data (dict) - The space missions dictionary
    Outputs:
        (set of str) - The unique set of mission names
    """



if __name__ == '__main__':
    data = load_data()
    # print(eva_count(data))
    # print(power_missions(data))
