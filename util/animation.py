class Animation:
    def __init__(self, names, lengthOfTime):
        self.names = names
        self.frame = 0
        self.lengthOfTime = lengthOfTime
        self.time = 0
    
    def nextFrame(self, dt):
        self.time += dt
        if self.time >= self.lengthOfTime:
            self.time = 0
            self.frame += 1
            if self.frame >= len(self.names):
                self.frame = 0
        
        return self.names[self.frame]
        
