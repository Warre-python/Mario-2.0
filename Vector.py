class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def set(self, x, y):
        self.x = x
        self.y = y
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y

    def get(self):
        return self.x, self.y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def add(self, x, y):
        self.x += x
        self.y += y
    
    def sub(self, x, y):
        self.x -= x
        self.y -= y

    def mult(self, x, y):
        self.x *= x
        self.y *= y

    def div(self, x, y):
        self.x /= x
        self.y /= y