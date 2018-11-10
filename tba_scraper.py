import tbapy as frc
from secrets import X_TBA_Auth_Key

tba = frc.TBA(X_TBA_Auth_Key)

competition_code = "2018gaalb" # needs to be changed after each event

'''

Common Competition Codes for 1261:

Replace year with current year

2018gaalb - Albany
2018gacmp - GA District Championship
2018gacol - Columbus
2018gadal - Dalton
2018gadul - Duluth (deprecated)
2018gagai - Gainesville
2018gagr - GRITS
2019gafor - Forsyth/Cumming
2018arc - Archimedes
2018cars - Carson
2018cur - Curie
2018dal - Daly
2018dar - Darwin
2018tes - Tesla
2018carv - Carver
2018gal - Galileo
2018hop - Hopper
2018new - Newton
2018roe - Roebling
2018tur - Turing
2018cmptx - Houston Einsteins Championship, hopefully we'll be using this one!

'''


class TBAData():
    def __init__(self, comp):
        self.competition = comp  # current competition code, for example, "2018gaalb"

        self.teams = {}
        self.rankings = {}
        self.scores = []
        self.matches = {}

    def reset(self):
        self.teams = {}
        self.rankings = {}
        self.scores = []
        self.matches = {}

    def calculate(self):
        self.reset()
        for match in tba.event_matches(self.competition):
            for alliance in match.alliances:
                for team in match.alliances[alliance]['team_keys']:
                    try:
                        score = int(match.alliances[alliance]['score'])
                        self.teams[team] += score
                        self.scores.append(score)
                    except KeyError:
                        self.teams[team] = 0

        for teamdata in tba.event_rankings(self.competition)['rankings']:
            self.rankings[teamdata['team_key']] = teamdata['rank']
            self.matches[teamdata['team_key']] = teamdata['matches_played']

    def getTotalScore(self, team_num):
        self.calculate()
        team_code = str("frc" + str(team_num))
        return self.teams[team_code]

    def getAverageEventScore(self):
        self.calculate()
        return sum(self.scores) / len(self.scores)

    def getAverageScore(self, team_num):
        self.calculate()
        team_code = str("frc" + str(team_num))
        return self.teams[team_code] / float(self.matches[team_code])

    def getRanking(self, team_num):
        self.calculate()
        team_code = str("frc" + str(team_num))
        return self.rankings[team_code]

competition_data = TBAData(competition_code)