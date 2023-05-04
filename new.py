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
        platforms_touch = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for i in platforms_touch:
                self.rect.right = min(self.rect.right, i.rect.left)
        elif self.x_speed < 0:
            for i in platforms_touch:
                self.rect.left = min(self.rect.left, i.rect.right)
        self.rect.y += self.y_speed
        platforms_touch = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for i in platforms_touch:
                self.rect.bottom = min(self.rect.bottom, i.rect.top)
        elif self.y_speed < 0:
            for i in platforms_touch:
                self.rect.top = min(self.rect.top, i.rect.bottom)


DARK_BLUE = (25, 15, 44)
YELLOW = (250, 227, 17)

w1 = GameSprite('w1.png', 100, 300, 800, 200)
w2 = GameSprite('w2.png', 300, 50, 300, 300)
w3 = GameSprite('w3.png', 50, 400, 100, 20)
player = Player('gg.png', 70, 70, 10, 10, 0, 0)
final = GameSprite('fin.png', 50, 50, 950, 650)

font.init()
font = font.SysFont('verdana', 65)
win = font.render('YOU WIN', True, YELLOW)
#win = transform.scale(image.load('win.png'), (1000, 700)), ((0, 0))

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)


window = display.set_mode((1000, 700))
display.set_caption('Первый проект')
run = True
finish = False
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
    if finish != True:
        window.fill(DARK_BLUE)
        barriers.draw(window)
        player.reset()
        player.update()
        final.reset()
        time.delay(50)
        display.update()

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (0, 0))
