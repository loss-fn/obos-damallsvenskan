## Predicting OBOS Damallsvenskan 2019 results
## -------------------------------------------

## transform.py is used to prepare the match data for training
## and testing classifiers

import numpy as np
import pandas as pd

def transform(filename):
    df = pd.read_csv(filename, delimiter = ',')

    ## we'll start with transformations to take the data from:
    ## Omgång 1;2019-04-13;Kungsbacka KUN;Kopparbergs / Göteborg KOP;0-3
    
    ## to something along the lines of
    ## ... ,0,4,2,0,3

    ## Round => Round_ (removing the "Omgång " text);
    df['Round_'] = df['Round'].apply(lambda x: x.split()[1])

    ## Date = 2019-04-13 (no touching this field);
    ## Home => HomeCat (transforming the team name to a categorical number);
    df['Home_'] = df['Home'].astype('category').cat.codes
    ## Away => AwayCat (see above);
    df['Away_'] = df['Away'].astype('category').cat.codes

    ## Score = 0 (home and away score split into two fields);
    ## Score = 3 (see above)
    df['HomeScore'] = df['Score'].apply(lambda x: x.split('-')[0])
    df['AwayScore'] = df['Score'].apply(lambda x: x.split('-')[-1])

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
