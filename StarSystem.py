from Star import Star


class StarSystem:

    def __init__(self):
        self.stars = []
        self.system_trajectories = None

    def getStars(self):
        return self.stars

    def addStar(self, star: Star):
        self.stars.append(star)

    def addStars(self, starList):
        for star in starList:
            self.stars.append(star)

    def getStarCount(self):
        return len(self.stars)

    def calculateTrajectories(self, method = "RKScipy"):
        return None

