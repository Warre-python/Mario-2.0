from Vector import Vector

class collisionbox:
    def __init__(self, pos, dim):
        self.pos = pos
        self.dim = dim
    
    def checkPointCollision(self, player_pos):
        if (player_pos.getX() >= self.pos.getX()  and player_pos.getX() < self.pos.getX() + self. width) and (player_pos.getX() >= self.pos.getX()  and player_pos.getX() < self.pos.getX() + self. height):
            return True
        else:
            return False