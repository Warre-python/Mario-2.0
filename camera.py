class Camera:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def follow(self, target):
        # X-axis dead zone
        player_screen_x = target.x - self.x
        if player_screen_x < self.width * 0.2:
            self.x = target.x - self.width * 0.2
        elif player_screen_x > self.width * 0.8:
            self.x = target.x - self.width * 0.8

        # Y-axis dead zone
        player_screen_y = target.y - self.y
        if player_screen_y < self.height * 0.2:
            self.y = target.y - self.height * 0.2
        elif player_screen_y > self.height * 0.5:
            self.y = target.y - self.height * 0.5

    def apply(self, rect):
        #print(f"Camera X: {self.x}, Camera Y: {self.y}")
        return rect.move(-self.x, -self.y)