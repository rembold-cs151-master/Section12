---
title: "Section 12: The Adventure Project"
author: Jed Rembold and Eric Roberts
date: "Week of November 27th"
slideNumber: true
theme: monokai
highlightjs-theme: monokai
width: 1920
height: 1080
transition: fade
css:
  - css/codetrace.css
  - css/roberts.css
content_url: https://github.com/rembold-cs151-master/Section12
---


## The Adventure Begins
- In terms of the amount of code to write, Adventure is roughly comparable to the Enigma project. What makes Adventure challenging is the interconnection of its data structures.
- The project includes separate classes:
  - `AdvGame`
  - `AdvRoom`
  - `AdvObject`
  
  each of which internally utilize Python lists, dictionaries, and tuples

## Adventure Strategies:
- Ensure that you thoroughly understand the `TeachingMachine.py` program before moving on to Adventure. Most of the parts you need are already there, you just need to determine how to adapt them.
- Don't try to keep the entire data structure in your head all at once. Consider each class, figure out what it does, and then think abstractly about what that class represents rather than worrying about the details
- Keep close track of what Python types your variables are storing. Choose good variable names that help you remember specifically what a particular variable is storing. Students thinking a variable has one thing in it when it is actually storing a different data type is a very common source of confusion with Adventure.


## Understanding the Teaching Machine
:::{style='font-size:.9em'}
- Like the Adventure project, the `TeachingMachine.py` program is data-driven, encoding the details of its operation in data files rather than in the program itself
- The `TeachingMachine.py` program begins by reading in a data file and translating the human-readable contents of the file into an internal data structure, shown on the next slide.
- When designing the internal data structure for data-driven applications, you should consider what types of common operations the structure needs to support.
  - In the Teaching Machine, each question specifies a collection of possible answers, each of which directs to a new question. Such a relationship suggests a dictionary would be useful.
  - Similarly, the course as a whole consists of a collection of questions referenced by a unique name. Thus, once again a dictionary seems like the best internal structure.
:::


## Teaching Structure
![](./images/TeachingMachine.svg)


## Problem 1
- As a first step toward making the conversion to the Adventure program, it is useful to draw out a similar diagram showing the desired internal data structure for the Adventure game
- In this problem you'll just focus on the `AdvRoom` class.
  - The next slide shows the contents of the first room of the `TinyRooms.txt` data file, one of the three supplied to you with the Adventure project. Draw a pencil-and-paper diagram showing what a **filled** internal data structure would look like.
  - The format of the data file has something extra that the Teaching Machine did not have: a short description. How should you incorporate that?
  - Clearly indicate the new names you will assign to each of the attributes


## `TinyRooms.txt` (Room 1)
```{.text style='max-height:900px; font-size:.8em'}
OutsideBuilding
Outside building
You are standing at the end of a road before a small brick
building.  A small stream flows out of the building and
down a gully to the south.  A road runs up a small hill
to the west.
-----
WEST: EndOfRoad
UP: EndOfRoad
NORTH: InsideBuilding
IN: InsideBuilding
SOUTH: Valley
DOWN: Valley
```

## Problem 1: One Solution
![](./images/AdvRooms.svg)


## Problem 2
:::incremental
- Currently, the `TeachingMachine.py` program gives no feedback when the user gives an incorrect answer.
  - Quickly brainstorm some ways you could try to implement this? What extra data structures might you need?
- There are many possible strategies, but the one Will Crowther arrived at was reusing the `AdvRoom` class (`TMQuestion` here)
  - Want the new "question" to display text to the screen, but **not** to prompt the user for a response
  - Instead, a `FORCED` response in the `answers` dictionary indicates that the program should **immediately** proceed to the indicated question
:::


## Forced Questions
- An example of such a question might look like:
  ```text
  Q3Resp
  You forgot to divide by 2.
  -----
  FORCED: Q3
  ```
- Implementing this in `TMCourse.py` requires only a small change:
  - The `run` method for `TMCourse` is shown on the next slide. Identify on what lines changes will need to be made.
  - Make the changes to allow for `FORCED` questions in the Teaching Machine.


## `TMCourse.run` {data-auto-animate=true}
```{.mypython style='max-height:950px; font-size:.8em' data-id='mycode' data-line-numbers=true}
def run(self):
    """Steps through the questions in this course."""
    current = "START"
    while current != "EXIT":
        question = self._questions[current]
        for line in question.get_text():
            print(line)
        answers = question.get_answers()
        response = input("> ").strip().upper()
        next_question = answers.get(response, None)
        if next_question is None:
            next_question = answers.get("*", None)
        if next_question is None:
            print("I don't understand that response.")
        else:
            current = next_question
```

## `TMCourse.run` {data-auto-animate=true}
```{.mypython style='max-height:950px; font-size:.8em' data-id='mycode' data-line-numbers='9-10|19-20'}
def run(self):
    """Steps through the questions in this course."""
    current = "START"
    while current != "EXIT":
        question = self._questions[current]
        for line in question.get_text():
            print(line)
        answers = question.get_answers()
        forced_question = answers.get("FORCED", None)
        if forced_question is None:
            response = input("> ").strip().upper()
            next_question = answers.get(response, None)
            if next_question is None:
                next_question = answers.get("*", None)
            if next_question is None:
                print("I don't understand that response.")
            else:
                current = next_question
        else:
            current = forced_question
```

## Problem 3
- The primary computing story throughout most of 2023 has revolved around generative AI and large-language models.
- While the underlying software for something like ChatGPT is much more complex, the core technology is based on a _large-language model_ (LLM) that scans a massive volume of text and then uses that data to create sentences in which new words are chosen based on the frequency in which they appear in the context of the words already generated.
- ChatGPT uses complex contextual information to predict the next word, but one can construct a much simpler language-generation model that uses only the previous word to guess what word comes next.


## Building the Model
- To build a simplified language model that uses a single word as the context, all you need to do is create a dictionary in which each key is a word that appears in your text (often called the _corpus_) and the corresponding value is a list of all the words that follow that key.
- To get a sense for how this process works, it helps to start with a small corpus, which might consist of the following three lines from Shakespeare's _Macbeth_:

  ```text
  Tomorrow, and tomorrow, and tomorrow
  Creeps in this petty pace from day to day
  To the last syllable of recorded time;
  ```
- The dictionary that serves as our model must show, for example, that the word `"tomorrow"` appears three times, twice followed by the word `"and"` and once followed by `"creeps"`.


## The "MacBeth" Language Model
- The complete dictionary would look like:
  ```mypython
  {
      "and": ["tomorrow", "tomorrow"],
      "creeps": ["in"],
      "day": ["to", "to"],
      "from": ["day"],
      "in": ["this"],
      "last": ["syllable"],
      "of": ["recorded"],
      "pace": ["from"],
      "petty": ["pace"],
      "recorded": ["time"],
      "syllable": ["of"],
      "the": ["last"],
      "this": ["petty"],
      "time": [],
      "to": ["day", "the"],
      "tomorrow": ["and", "and", "creeps"]
  }
  ```

## Token Building
- To build such a dictionary, you need to select off one word at a time from your corpus, appending it to the correct list in your dictionary.
- This is an excellent time to make use of the TokenScanner library and class!
- Remember that to do so you need to initialize the TokenScanner, and then iterate through as long as their remain tokens, retrieving each as you go.
- Write a function called `create_model(text)` which uses the TokenScanner library to parse the provided text to create a simple dictionary language model, as shown on the previous slide.


## Token Solution
```{.mypython style='max-height: 900px; font-size:.9em'}
def create_model(text):
    """Returns the language-model dictionary 
    for the provided text."""
    scanner = TokenScanner(text)
    model = { }
    previous = None
    while scanner.has_more_tokens():
        word = scanner.next_token().lower()
        if word.isalpha():
            if word not in model:
                model[word] = [ ]
            if previous is not None:
                model[previous].append(word)
            previous = word
    return model
```
