class Camera:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def follow(self, target):
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2

    def apply(self, rect):
        #print(f"Camera X: {self.x}, Camera Y: {self.y}")
        return rect.move(-self.x, -self.y)