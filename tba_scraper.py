import tbapy as frc
from secrets import X_TBA_Auth_Key

tba = frc.TBA(X_TBA_Auth_Key)

teams = {}
scores = []

fout = open(r'teams.txt', 'w')
fout.write("Lets do this!\n")

our_events = tba.team_events(1261, 2018)
event_lists = [tba.events(year) for year in range(2002, 2019)]
for eventlist in event_lists:
    for event in eventlist:
        for match in tba.event_matches(event.key):
            for alliance in match.alliances:
                for team in match.alliances[alliance]['team_keys']:
                    try:
                        score = int(match.alliances[alliance]['score'])
                        teams[team] += score
                        scores.append(score)
                    except KeyError:
                        teams[team] = 0

teamlist = sorted(teams, key=lambda team: teams[team], reverse=True)

average = sum(scores) / len(scores)
fout.write("The average score was " + str(average) + '\n')

fout.write("Final Rankings!\n")
for count, team in enumerate(teamlist):
    fout.write(str(count) + ". " + str(team) + ": " + str(teams[team]))

fout.close()