import pandas as pd
import numpy as np
import random

# Generates fake gender-neutral names
def get_data(filename):
    '''
    Loads csv with possible names
    @param filename: name of the file to load
    '''
    data = pd.read_csv(filename, sep = ',')
    data = pd.DataFrame(data)
    data = np.array(data.iloc[:, 0])
    return data

def generate_name():
    '''
    Generates a fake name
    @return: fake name string 
    '''
    # Load data
    first_names = get_data('first_names.csv')
    last_names = get_data('last_names.csv')
    # Randomly choose a first and last name
    first = first_names[random.randint(0, len(first_names) - 1)]
    last = last_names[random.randint(0, len(last_names) - 1)]
    return first + ' ' + last
