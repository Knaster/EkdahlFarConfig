class Averager:
    def __init__(self):
        self.averages = []
        self.maxCount = 1
        self.max = 0
        self.min = 0
        self.average = 0

    def addValue(self, value):
        value = int(value)

        self.averages.append(value)
        if len(self.averages) > self.maxCount:
            del self.averages[0]

        if value > self.max:
            self.max = value

        if (value < self.min) or (self.min == 0):
            self.min = value

        self.average = 0
        for v in self.averages:
            self.average += v
        self.average /= len(self.averages)
        self.average = round(self.average)

    def clear(self):
        self.averages.clear()
        self.max = 0
        self.min = 0