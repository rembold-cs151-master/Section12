
"""
Utilizes the NotOpenAI API to retrieve and parse a response from ChatGPT
"""

from notopenai import NotOpenAI
import json

SAMPLE = {'games': [
    {
        'name': 'The Great WU Adventure', 
        'creator': 'Jed Rembord',
        'pub_year': 2026,
        'desc': 'A groundbreaking text adventure about a duck living in the Mill Stream.'
    },
    {
        'name': 'Revenge of the Nutria', 
        'creator': 'Jed Rembord',
        'pub_year': 2026,
        'desc': 'A horror adventure game about zombified nutria'
    },
]
}

CLIENT = NotOpenAI(api_key='your_key')

