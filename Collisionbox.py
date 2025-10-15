from Vector import Vector

class Collisionbox:
    def __init__(self, pos, dim):
        self.pos = pos
        self.dim = dim
    
    def checkPointCollision(self, player_pos, dim):
        if self.pos.getX() + self.dim.getX() > player_pos.getX() and \
        self.pos.getX() < player_pos.getX() + dim.getX() and \
        self.pos.getY() + self.dim.getY() > player_pos.getY() and \
        self.pos.getY() < player_pos.getY() + dim.getY():
            return True
        return False
