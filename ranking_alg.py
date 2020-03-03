class RankingAlgorithm:
    def __init__(self, low, high, driver, climb, auto, reach, total_teams):
        self.total = total_teams
        self.low = low
        self.high = high
        self.driver = driver
        self.climb = climb
        self.auto = auto
        self.reach = reach
        self.weights = {
            'low': 0.15,
            'high': 0.3,
            'driver': 0.05,
            'climb': 0.2,
            'auto': 0.2,
            'reach': 0.1
        }

    def getScore(self):
        return (self.total - self.low)*self.weights['low'] + \
               (self.total - self.high)*self.weights['high'] + \
               (self.total - self.driver)*self.weights['driver'] + \
               (self.total - self.climb)*self.weights['climb'] + \
               (self.total - self.auto)*self.weights['auto'] + \
               (self.total - self.reach)*self.weights['reach']

    def checkWeights(self):
        sum_ = 0
        for key in self.weights:
            sum_ += self.weights[key]
        if sum_ == 1.0:
            return True
        else:
            return False