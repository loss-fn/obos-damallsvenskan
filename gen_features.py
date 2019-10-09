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

def add_weight_to_rounds(df, rounds = None):
    if rounds is None:
        return

    for round in rounds:
        rows = df[df['Round'] == 'Omgång %d' % (round)]
        df = pd.concat([df, rows], axis = 0, ignore_index = False)

    return df.sort_values(by = ['Date'], inplace = False)

def calc_points(df, team):
    points_total, points_home, points_away = 0, 0, 0
    n_home, n_away = 0, 0
    for score in df[df['Home'] == team]['Score']:
        h, a = score.split('-')
        h, a = int(h), int(a)
        n_home += 1
        if h == a:
            points_home += 1
            points_total += 1
        elif h > a:
            points_home += 3
            points_total += 3

    for score in df[df['Away'] == team]['Score']:
        h, a = score.split('-')
        h, a = int(h), int(a)
        n_away += 1
        if h == a:
            points_away += 1
            points_total += 1
        elif a > h:
            points_away += 3
            points_total += 3

    return points_total, points_home / n_home, points_away / n_away

def transform(filename):
    df = pd.read_csv(filename, delimiter = ',')

    ## goal difference columns
    df = df.assign(GDH = 0, # Goal Difference (Home team)
                   GDA = 0, # Goal Difference (Away team)
                   GFTH = 0, # Goal For, Total (Home team)
                   GFTA = 0, # Goal For, Total (Away team)
                   GATH = 0, # Goal Against, Total (Home team)
                   GATA = 0, # Goal Against, Total (Away team)
                   GFH = 0, # Goal For, Home (Home team)
                   GFA = 0, # Goal For, Away (Away team)
                   GAH = 0, # Goal Against, Home (Home team)
                   GAA = 0) # Goal Against, Away (Away team)

#    ## points columns
#    df = df.assign(PTSH = 0, # PoinTS, total (Home team)
#                   PTSA = 0, # PoinTS, total (Away team)
#                   EPTSH = 0, # Expected PoinTS, total (Home team)
#                   EPTSA = 0) # Expected PoinTS, total (Away team)

    for team in df['Home'].unique():
        goal_difference, goals_for, goals_against, \
        goals_for_home, goals_for_away, \
        goals_against_home, goals_against_away = calc_goal_difference(df, team)

        df.loc[df['Home'] == team, 'GDH'] = goal_difference
        df.loc[df['Away'] == team, 'GDA'] = goal_difference
        df.loc[df['Home'] == team, 'GFTH'] = goals_for
        df.loc[df['Away'] == team, 'GFTA'] = goals_for
        df.loc[df['Home'] == team, 'GFH'] = goals_for_home
        df.loc[df['Away'] == team, 'GFA'] = goals_for_away

        df.loc[df['Home'] == team, 'GATH'] = goals_against
        df.loc[df['Away'] == team, 'GATA'] = goals_against
        df.loc[df['Home'] == team, 'GAH'] = goals_against_home
        df.loc[df['Away'] == team, 'GAA'] = goals_against_away

#        points_total, expected_points_home, expected_points_away = calc_points(df, team)

#        df.loc[df['Home'] == team, 'PTSH'] = points_total
#        df.loc[df['Away'] == team, 'PTSA'] = points_total

#        df.loc[df['Home'] == team, 'EPTSH'] = expected_points_home
#        df.loc[df['Away'] == team, 'EPTSA'] = expected_points_away

    return df

def to_csv(df, filename):
    df.to_csv(filename, index = False)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description = 'Generate features from match data in <input> and store in <output>.')
    parser.add_argument('input', nargs = 1, help = 'filename of .csv file with match data')
    parser.add_argument('output', nargs = 1, help = 'filename of .csv file with transformed match data')

    args = parser.parse_args()
    to_csv(add_weight_to_rounds(transform(args.input[0]), rounds = [16,17,18]), args.output[0])
