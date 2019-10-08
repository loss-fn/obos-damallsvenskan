## Predicting OBOS Damallsvenskan 2019 results
## -------------------------------------------

## gen_featuers.py is used to generate more features for
## training and testing classifiers.

import numpy as np
import pandas as pd

def calc_goal_difference(df, team):
    goals_for_home = sum([int(x.split('-')[0]) for x in df[df['Home'] == team]['Score']])
    goals_for_away = sum([int(x.split('-')[1]) for x in df[df['Away'] == team]['Score']])
    goals_against_home = sum([int(x.split('-')[1]) for x in df[df['Home'] == team]['Score']])
    goals_against_away = sum([int(x.split('-')[0]) for x in df[df['Away'] == team]['Score']])

    goals_for = goals_for_home + goals_for_away
    goals_against = goals_against_home + goals_against_away
    goal_difference = goals_for - goals_against
    return goal_difference, goals_for, goals_against, goals_for_home, goals_for_away, goals_against_home, goals_against_away

def transform(filename):
    df = pd.read_csv(filename, delimiter = ',')
    df = df.assign(GD = 0, GF = 0, GA = 0, GFH = 0, GFA = 0, GAH = 0, GAA = 0)

    for team in df['Home'].unique():
        goal_difference, goals_for, goals_against, \
        goals_for_home, goals_for_away, \
        goals_against_home, goals_against_away = calc_goal_difference(df, team)

        df.loc[df['Home'] == team, 'GD'] = goal_difference
        df.loc[df['Away'] == team, 'GD'] = goal_difference
        df.loc[df['Home'] == team, 'GF'] = goals_for
        df.loc[df['Away'] == team, 'GF'] = goals_for
        df.loc[df['Home'] == team, 'GFH'] = goals_for_home
        df.loc[df['Away'] == team, 'GFA'] = goals_for_away

        df.loc[df['Home'] == team, 'GA'] = goals_against
        df.loc[df['Away'] == team, 'GA'] = goals_against
        df.loc[df['Home'] == team, 'GAH'] = goals_against_home
        df.loc[df['Away'] == team, 'GAA'] = goals_against_away

    return df

def to_csv(df, filename):
    df.to_csv(filename, index = False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Generate features from match data in <input> and store in <output>.')
    parser.add_argument('input', nargs = 1, help = 'filename of .csv file with match data')
    parser.add_argument('output', nargs = 1, help = 'filename of .csv file with transformed match data')

    args = parser.parse_args()
    to_csv(transform(args.input[0]), args.output[0])
