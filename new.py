from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
       self.rect.x += self.x_speed
       self.rect.y += self.y_speed

DARK_BLUE = (25, 15, 44)

w1 = GameSprite('w1.png', 100, 300, 600, 20)
w2 = GameSprite('w2.png', 300, 50, 200, 300)
w3 = GameSprite('w3.png', 50, 400, 100, 20)
player = Player('gg.png', 25, 25, 100, 125, 10, 10)

window = display.set_mode((700, 500))
display.set_caption('Первый проект')
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_w:
                player.y_speed -= 10
            elif e.key == K_s:
                player.y_speed += 10
            elif e.key == K_a:
                player.x_speed -= 10
            elif e.key == K_d:
                player.x_speed += 10
        elif e.type == KEYUP:
            player.y_speed = 0
            player.x_speed = 0
    window.fill(DARK_BLUE)
    w1.reset()
    w2.reset()
    w3.reset()
    player.reset()
    player.update()
    time.delay(50)
    display.update()



