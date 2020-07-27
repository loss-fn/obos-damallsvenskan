# calculate ELO ratings per game and team (using the 400-algorithm)
# we're assuming that all teams have an ELO rating of 1000

import pandas as pd

teams = {   'UME' : 'Umeå IK FF',
            'PIT' : 'Piteå IF DFF',
            'LIN' : 'Linköpings FC',
            'VÄX' : 'Växjö DFF',
            'UPP' : 'IK Uppsala',
            'DJU' : 'Djurgårdens IF FF',
            'ÖRE' : 'KIF Örebro DFF',
            'ESK' : 'Eskilstuna United DFF',
            'ROS' : 'FC Rosengård',
            'VIT' : 'Vittsjö GIK',
            'KOP' : 'Kopparbergs/Göteborg FC',
            'KRI' : 'Kristianstads DFF'  }

def calculate_stats(df, team, upto = None):
    w, d, l = 0, 0, 0
    for column in ['Team(H)', 'Team(A)']:
        for index, row in df.loc[df[column] == team].iterrows():
            if upto and row['Round'] > upto:
                continue 

            if row['Goals(H)'] > row['Goals(A)']:
                # Home team wins
                if column == 'Team(H)':
                    w += 1
                else:
                    l += 1

            elif row['Goals(H)'] < row['Goals(A)']:
                # Away team wins
                if column == 'Team(A)':
                    w += 1
                else:
                    l += 1

            else:
                # Draw
                d += 1

    # calculate ELO according to 400-algorithm
    return ((w * 1400) + (d * 1000) + (l * 600))/ (w + d + l), w, d, l

if __name__ == "__main__":
    df = pd.read_csv('data.csv')
    for team in teams.values():
        print(team)
        for i in range(1,7):
            print(i, calculate_stats(df, team, i))
