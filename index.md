---
title: "Section 12: Compounding APIs"
author: Jed Rembold
date: "Week of November 17th"
slideNumber: true
theme: monokai
highlightjs-theme: monokai
width: 1920
height: 1080
transition: slide
css:
  - css/codetrace.css
  - css/roberts.css
content_url: https://github.com/rembold-cs151-master/Section12
---

# Problem 1
## Navigating Compound Data Structures
- Project 5 requires reading in and working with a large, nested data structure that holds all of the existing content that comprises a given story.
- Navigating your way around that structure, looping over and selecting out the pieces of information that you need, will be the most conceptually difficult task in the first milestones.
- This first problem is intended to get you some practice thinking about, and working with these nested structures.

## Space Missions
:::{style='font-size:.9em'}
- Your data in this problem comes in a JSON format, and represents a collection of fictional space missions
- Each mission contains information about:
  - the crew involved, including
    - their names (which are unique)
    - their role on the mission
    - their certifications
  - various pieces of hardware and some diagnostics, including
    - the hardware name
    - the hardware type (what category it belongs to)
    - any diagnostics, which include
      - the status of the hardware
      - the power emitted by the hardware in watts
:::

## Visualizing the Data
- It can be useful to visualize the structure to help organize it in your thoughts, and provide a reference for various names

![](./images/space_mission_structure.svg)

## Parts of a Mission

Part A
: Write a function called `load_data` that loads in the data from the JSON and returns the dictionary.

Part B
: Write a function called `eva_count` which counts and returns the number of **different** crew members who have an `"EVA"` certification and participated in a mission that began with an "A".

Part C
: Write a function called `power_missions` which returns a set of all the mission names where the **Navigation** hardware averaged over 100 W of power.

## Possible Solutions
```{.python style='font-size:.7em; max-height: 900px'}
import json

def load_data():
    with open('./space_missions.json') as fh:
        data = json.load(fh)
    return data


def eva_count(data):
    """
    How many _different_ crew members have EVA certification and have served
    on missions that begin with an A?
    """
    eva_crew = set() # Accounting for duplicate crew across missions
    for mission_name, mission_data in data.items():
        if mission_name.startswith("A"):
            for crew_dict in mission_data["crew"]:
                if "EVA" in crew_dict["certifications"]:
                    eva_crew.add(crew_dict["name"])
    return len(eva_crew)


def power_missions(data):
    """
    What are the unique mission names where Navigation equipment, on average,
    was drawing more than 100 W?
    """
    missions = set()
    for mission_name, mission_data in data.items():
        nav_power_readings = []
        for item_dict in mission_data["hardware"]:
            if item_dict["type"] == "Navigation":
                nav_power_readings.append(item_dict["diagnostics"]["power_W"])
        if sum(nav_power_readings) / len(nav_power_readings) > 100:
            missions.add(mission_name)
    return missions
```

# Problem 2

## Talking to the Web
- The modern web is built on applications being able to communicate and pass information back and forth
- The HTML standard defines a variety of ways that communication can be passed, of which two main methods dominate:
  - A _GET_ request retrieves information from a specified online source
  - A _POST_ request sends information to a specified online source (and then sometimes receives information back)
- In Python, the `requests` library handles both of these methods (and more)
  - Not part of the default installed libraries. Will need to install like we did with `pillow` at the beginning of the semester. Generally with `pip install requests`.


## Application Programming Interfaces
- While the HTML standard defines **how** things communicate, it doesn't specify **what** is communicating
- Web sources are usually dominated by what are called "application programming interfaces", or APIs
  - Imagine a bit of code that is running on a computer/server, just waiting for someone to contact it and send back a response!
- Programming can design how these APIs function:
  - What web addresses do they live at?
  - What information can they return or process?
  - How is a user allowed to interact with the API?

## Post Up
- In the Infinite Adventure, we are utilizing the NotOpenAI library, which makes a _POST_ request to the ChatGPT servers
  - We need to **send** the desired prompt, hence the need for a POST request
  - We package the prompt up in a little dictionary (generally formatted as JSON), which is called the _payload_.
- The API we contact then sends us back a response, which we then need to parse to extract out the important parts.


## The Section 12 API
- In this problem, you will be "contacting" a special API written just for this section
- This API "lives" at a particular web address: 
  ```text
  https://section12api-production.up.railway.app/generate
  ```
- Interactions:
  - The API expects a payload with three keys:
    - `"name"` - Your name
    - `"class_year"` - Your class year, Freshman - Senior
    - `"favorite_animal"` - Your favorite animal
  - The API will return to you JSON with a single key: `"content"`
    - The value associated with `"content"` is a dictionary converted to a string

## The Content Dictionary
- The NotOpenAI library returns a similar dictionary in a string format to you, which in that case holds your newly created scene information
- To convert that string of JSON into something usable in Python, you will want to use the `loads` method from the `json` library:
  ```mypython
  import json

  content_dict = json.loads(|||string dictionary|||)
  ```
- This resulting dictionary should have several keys in it. You want to extract the `"fun_fact"` key and print its corresponding value.


## Overall Gameplan
Thus, to complete this problem you need to:

#. Craft your payload dictionary
#. Make the POST request, providing the payload
#. Check the status of the returned message, to be sure it was successful
#. Convert the content key back to a dictionary
#. Extract and print out the value of the "fun_fact" key

## Possible Solution
```{.python style='font-size:.8em; max-height: 900px;'}
import requests
import json

URL = "https://section12api-production.up.railway.app/generate"

payload = {
    "name": "Jed",
    "class_year": "super senior",
    "favorite_animal": "snow leopard"
}

# Making the request and getting the response
resp = requests.post(URL, json=payload)

if resp.status_code == 200: # A good response
    data = resp.json() # Get the returned dictionary
    content = json.loads(data['content']) # Convert content to dict
    print(content['fun_fact'])
else: # If the response code was bad
    print(f"Oh no! A {resp.status_code} error occurred!")

```
