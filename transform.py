## Predicting OBOS Damallsvenskan 2019 results
## -------------------------------------------

## transform.py is used to prepare the match data for training
## and testing classifiers

import numpy as np
import pandas as pd

def transform(filename):
    df = pd.read_csv(filename, delimiter = ';')
    return df

def to_csv(df, filename):
    df.to_csv(filename)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Transform match data from <input> and store in <output>.')
    parser.add_argument('input', nargs = 1, help = 'filename of .csv file with match data')
    parser.add_argument('output', nargs = 1, help = 'filename of .csv file with transformed match data')

    args = parser.parse_args()
    to_csv(transform(args.input[0]), args.output[0])
