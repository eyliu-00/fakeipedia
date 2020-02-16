from detect import *
from generate_text import *
from random import randrange
from fake_name_generator import *

import sys

def make_prefix(prompt, type='item'):
    """
    Given an item or location, generates an appropriate prefix for
    the text of an article about it.
    """
    if type == 'item':
        if prompt == 'person':
            fake_name = generate_name()   # Create fake entry about person
            return fake_name + "is"
        rand = randrange(3)
        if rand == 0:
            return prompt.capitalize() + "s are"
        if rand == 1:
            prompt = "A " + prompt + "is a"
        if rand == 2:
            prompt = "A " + prompt + "is"
    if type == 'town':
        rand = randrange(3)
        if rand == 0:
            return prompt.capitalize() + ", California is"
        if rand == 1:
            prompt = prompt.capitalize() + "is the"
        if rand == 2:
            prompt = prompt.capitalize() + "is a"
    return prompt


def main():

    # Check that a photo was given
    if len(sys.argv) < 2:
        print("usage: python3 {} filename".format(sys.argv[0]))
        return
    filename = sys.argv[1]

    # Get item in image and assosiated probability
    item, probability = get_final_detection(filename)

    # Get location where image was taken
    location = get_location(filename)

    # Initialize text generator
    generator = Text_Generator()

    if probability < 0.5 and location:
        print(location)
        generator.generate_entry(make_prefix(location))
    else:
        print(detection)
        generator.generate_entry(make_prefix(item))


if __name__ == '__main__':
    main()
