from detect import *
from generate_text import *
from random import randrange

import sys

def main():

    if len(sys.argv) < 2:
        print("usage: python3 {} filename".format(sys.argv[0]))
        return

    filename = sys.argv[1]
    detection = get_detection(filename)[0]
    print(detection)
    generator = Text_Generator()
    prompt = "A " + detection + " is"
    n = randrange(3)
    if n == 0:
        prompt = detection.capitalize() + "s are"
    if n == 1:
        prompt = "A " + detection + "is a"
    generator.generate_entry(prompt, n_samples = 1, top_k = 1)

if __name__ == '__main__':
    main()
