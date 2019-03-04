import database as db

class RankingAlgorithm:
    def __init__(self):
        self.weights = {
            'cargo': 0.15,
            'hatch': 0.15,
            'driver_skill': 0.05,
            'total_score': 0.03,
            'average_score': 0.03,
            'team_likability_index': 0.2,
            'autonomous': 0.1,
            'climbing_ability': 0.1,
            'robot_type': 0.1,
            'rank': 0.09
        }
        self.teamData = {}
        self.bestData = {}

    def algorithm(self, team):
        self.obtainTeamData(team)
        t = self.teamData
        b = self.bestData
        scw = self.weights['scale']
        sww = self.weights['switch']
        vw = self.weights['vault']
        dsw = self.weights['driver_skill']
        tSw = self.weights['total_score']
        aSw = self.weights['average_score']
        tLIw = self.weights['team_likability_index']
        aw = self.weights['autonomous']
        cAw = self.weights['climbing_ability']
        rTw = self.weights['robot_type']
        rw = self.weights['rank']
        tLI = 0.9 # TODO CALCULATE TEAM LIKABILITY INDEX
        a = t['a']
        cA = t['cA']
        rT = t['rT']
        r = t['r']
        return (scw*(t['sc']/b['sc']) + sww*(t['sw']/b['sw']) + vw*(t['v']/b['v']) + dsw*(t['ds']/10.0) +
                tSw*(t['tS']/b['tS']) + aSw*(t['aS']/b['aS']) + tLIw*(tLI)) / ((a*aw)(cA*cAw)(rT+rTw)(r*rw))

    def checkWeights(self):
        sum_ = 0
        for key in self.weights:
            sum_ += self.weights[key]
        if sum_ == 1.0:
            return True
        else:
            return False

    def obtainTeamData(self, team):
        self.teamData = {
            'sc': 3,
            'sw': 3,
            'v': 3,
            'ds': 3,
            'tS': 3,
            'aS': 3,
            'a': 3,
            'cA': 3,
            'rT': 3,
            'r': 3
        }

    def obtainBestData(self):
        self.bestData = {

        }

alg = RankingAlgorithm()
print(alg.checkWeights())
