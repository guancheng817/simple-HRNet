class people(object):
    out = 3
    def __init__(self):
        self.one = 1
        self.two =2
        self.three = 3
        self.four = 4

    def second(self):
        self.fours = 5

    def Three(self):
        five = self.fours
        print('five', five)


class person(people):
    def __init__(self):
        super().__init__()
        self.six = 6
        #self.second()
        #print('self.fours', self.fours)

    def Four(self):
        print('self.one',self.one)

p = person()
p.Four()