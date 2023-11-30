
from tokenscanner import TokenScanner
import random

quote = """Tomorrow, and tomorrow, and tomorrow
           Creeps in this petty pace from day to day
           To the last syllable of recorded time;"""

def create_model(text):
    """Parses the text to create a simple language model dictionary.

    Args:
        text (str): the text to parse
    Returns:
        (dict): the language model
    """


def generate_text(model, start_word, max_words = 100):
    """Uses a language model to generate text from a starting word

    Args:
        model (dict): the language model dictionary
        start_word (str): the word to begin the generate sentence
        max_words (int): the max number of words to generate in the sentence
    Returns:
        (str): the generated text
    """
    n_words = 0
    current = start_word
    output = start_word
    while n_words < max_words and current is not None:
        choices = model[current]
        if len(choices) == 0:
            current = None
        else:
            current = random.choice(choices)
            output += " " + current
            n_words += 1
    return output


if __name__ == '__main__':
    model = create_model(quote)
    print(model)

    # text = generate_text(model, "tomorrow", 50)
    # print(text)
