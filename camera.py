class Camera:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.left = 0.3
        self.right = 0.7

        self.up = 0.15
        self.down = 0.5

    def follow(self, target):

        # X-axis dead zone
        player_screen_x = target.x - self.x
        if player_screen_x < self.width * self.left:
            self.x = target.x - self.width * self.left
        elif player_screen_x > self.width * self.right:
            self.x = target.x - self.width * self.right

        # Y-axis dead zone
        player_screen_y = target.y - self.y
        if player_screen_y < self.height * self.up:
            self.y = target.y - self.height * self.up
        elif player_screen_y > self.height * self.down:
            self.y = target.y - self.height * self.down

    def apply(self, rect):
        #print(f"Camera X: {self.x}, Camera Y: {self.y}")
        return rect.move(-self.x, -self.y)