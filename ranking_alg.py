class RankingAlgorithm:
    def __init__(self, au, al, tu, tl, driver, climb, reach, total_teams):
        self.total = total_teams
        self.au = au
        self.al = al
        self.tu = tu
        self.tl = tl
        self.driver = driver
        self.climb = climb
        self.reach = reach
        self.weights = {
            'au': 0.15,
            'al': 0.01,
            'tu': 0.05,
            'tl': 0.05,
            'driver': 0.05,
            'climb': 0.2,
            'reach': 0.1
        }

    def getScore(self):
        return (self.total - self.au)*self.weights['au'] + \
               (self.total - self.al)*self.weights['al'] + \
               (self.total - self.tu) * self.weights['tu'] + \
               (self.total - self.tl) * self.weights['tl'] + \
               (self.total - self.driver)*self.weights['driver'] + \
               (self.total - self.climb)*self.weights['climb'] + \
               (self.total - self.reach)*self.weights['reach']

    def checkWeights(self):
        sum_ = 0
        for key in self.weights:
            sum_ += self.weights[key]
        if sum_ == 1.0:
            return True
        else:
            return False