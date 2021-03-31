from gen import genId

class Picture:
    def __init__(self, absPath, team):
        self.absPath = absPath
        self.team = team
        self.solved = False # Will be set to True when solved by oponent team
        self.id = genId()

    def open(self):
        return open(self.absPath, 'r')