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
        if self.rect.x <= win_width - 80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.rect.y <= win_height - 80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png', 15, 5, self.rect.right, self.rect.centery, 15)
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
        if self.rect.x > win_width+10:
            self.kill()

GREY = (111, 127, 134)
YELLOW = (18, 176, 255)
RED = (255, 0, 51)

w1 = GameSprite('w1.png', 125, 525, 150, 0)
w2 = GameSprite('w1.png', 125, 525, 400, 175)
w3 = GameSprite('w2.png', 325, 100, 525, 370)
player = Player('gg.png', 70, 70, 10, 10, 0, 0)
final = GameSprite('fin.png', 100, 100, 530, 550)
monster1 = EnemyX('enemy1.png', 70, 70, 0, 590, 5, 0, 272)
monster2 = EnemyY('enemy2.png', 70, 70, 300, 300, 3, 300, 570)
monster3 = EnemyX('enemy1.png', 70, 70, 350, 75, 10, 350, 800)
monster4 = EnemyY('enemy2.png', 70, 70, 900, 100, 5, 100, 525)
monster5 = EnemyX('enemy1.png', 70, 70, 550, 295, 7, 550, 900)

font.init()
font = font.SysFont('verdana', 140)
win = font.render('YOU WIN', True, RED)
lose = font.render('GAME OVER', True, YELLOW)

barriers = sprite.Group()
barriers.add(w1, w2, w3)
monsters = sprite.Group()
monsters.add(monster1, monster2, monster3, monster4, monster5)
bullets = sprite.Group()

win_width = 1000
win_height = 700
window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')

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
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            player.y_speed = 0
            player.x_speed = 0

    if finish != True:
        window.fill(GREY)

        player.reset()
        player.update()
        final.reset()

        time.delay(50)
        display.update()

        monsters.update()
        monsters.draw(window)

        barriers.update()
        barriers.draw(window)

        bullets.update()
        bullets.draw(window)

        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (170, 170))

        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(lose, (90, 170))

    display.update()

