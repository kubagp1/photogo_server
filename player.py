import gen

class Player:
    def __init__(self, nicknname, isOwner=False):
        self.id = gen.genId()
        self.token = gen.genToken()
        self.nicknname = nicknname
        self.isOwner = isOwner