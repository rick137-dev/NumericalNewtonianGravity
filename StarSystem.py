from Star import Star


class StarSystem:

    def __init__(self, merge_distance =0):
        self.stars = []
        self.star_count =0
        self.system_trajectories = None
        self.merge_distance = merge_distance

    def getStars(self):
        return self.stars

    def setMergeDistance(self, distance):
        self.merge_distance = distance


    def getStarCount(self):
        return self.star_count

    def addStar(self, star: Star):
        self.stars.append(star)

    def addStars(self, starList):
        for star in starList:
            self.stars.append(star)

    def calculateTrajectories(self, method = "RKScipy"):
        pass

