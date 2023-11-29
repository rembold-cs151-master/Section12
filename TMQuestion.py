# File: TMQuestion.py

"""This module defines a class to represent a single question."""

class TMQuestion:

    def __init__(self, name, text, answers):
        """Creates a new TMQuestion object with these attributes."""
        self._name = name
        self._text = text
        self._answers = answers

    def get_name(self):
        """Returns the name of this question."""
        return self._name

    def get_text(self):
        """Returns the list containing the text of this question."""
        return self._text

    def get_answers(self):
        """Returns the map between a response and the next question."""
        return self._answers.copy()

    
# Implementation notes: read_question
# -----------------------------------
# This method is defined within the TMQuestion.py module but outside the
# TMQuestion class.  Unlike the other methods in the class, read_question
# is not applied to a TMQuestion instance but instead returns a new one.

MARKER = "-----"                             # Marker at end of question text

def read_question(f):
    """Reads the next TMQuestion, returning None at the end."""

    name = f.readline().rstrip()             # Read the question name
    if name == "":                           # Returning None at the end
        return None

    text = [ ]                               # Read the question text
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == MARKER:
            finished = True
        else:
            text.append(line)

    answers = { }                            # Read the answer dictionary
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == "":
            finished = True
        else:
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            response = line[:colon].strip().upper()
            next_question = line[colon + 1:].strip()
            answers[response] = next_question

    return TMQuestion(name, text, answers)  # Return the completed object
