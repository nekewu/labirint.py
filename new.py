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
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)

        bullets.add(bullet)

class EnemyX(GameSprite):
    def __init__(self, picture, w, h, x, y, speed, xmax, xmin):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.xmax = xmax
        self.xmin = xmin
    def update(self):
        if self.rect.x <= self.xmax:
            self.direction = 'right'
        if self.rect.x >= self.xmin:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class EnemyY(GameSprite):
    def __init__(self, picture, w, h, x, y, speed, ymax, ymin):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.ymax = ymax
        self.ymin = ymin
    def update(self):
        if self.rect.y <= self.ymax:
            self.direction = 'bottom'
        if self.rect.y >= self.ymin:
            self.direction = 'top'
        if self.direction == 'top':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= win_width:
            self.kill()

DARK_BLUE = (0, 51, 102)
YELLOW = (250, 227, 17)
RED = (255, 0, 51)

w1 = GameSprite('w1.png', 100, 300, 800, 200)
w2 = GameSprite('w2.png', 300, 50, 300, 300)
w3 = GameSprite('w3.png', 50, 400, 100, 20)
player = Player('gg.png', 70, 70, 10, 10, 0, 0)
final = GameSprite('fin.png', 50, 50, 950, 650)
monster1 = EnemyX('enemy1.png', 70, 70, 470, 570, 3, 470, 570)
monster2 = EnemyX('enemy1.png', 70, 70, 350, 100, 3, 150, 265)
monster3 = EnemyY('enemy2.png', 70, 70, 600, 105, 5, 45, 105)
monster4 = EnemyY('enemy2.png', 70, 70, 100, 505, 5, 505, 605)

font.init()
font = font.SysFont('verdana', 140)
win = font.render('YOU WIN', True, YELLOW)
lose = font.render('GAME OVER', True, RED)


bullets = sprite.Group()

barriers = sprite.Group()
barriers.add(w1, w2, w3)

monsters = sprite.Group()
monsters.add(monster1, monster2, monster3, monster4)

win_width = 1000
win_height = 700
window = display.set_mode((win_width, win_height))
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
        if e.type == K_SPACE:
            player.fire()
    if finish != True:
        window.fill(DARK_BLUE)
        barriers.draw(window)
        player.reset()
        player.update()
        final.reset()
        time.delay(50)
        display.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (170, 170))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (110, 170))
    display.update()
