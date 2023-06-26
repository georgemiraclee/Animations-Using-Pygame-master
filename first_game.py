import pygame
import random

g = "Game/"
e = "E"
walkRight = [pygame.image.load(f'{g}R1.png'),
             pygame.image.load(f'{g}R2.png'),
             pygame.image.load(f'{g}R3.png'),
             pygame.image.load(f'{g}R4.png'),
             pygame.image.load(f'{g}R5.png'),
             pygame.image.load(f'{g}R6.png'),
             pygame.image.load(f'{g}R7.png'),
             pygame.image.load(f'{g}R8.png'),
             pygame.image.load(f'{g}R9.png')]

walkLeft = [pygame.image.load(f'{g}L1.png'),
            pygame.image.load(f'{g}L2.png'),
            pygame.image.load(f'{g}L3.png'),
            pygame.image.load(f'{g}L4.png'),
            pygame.image.load(f'{g}L5.png'),
            pygame.image.load(f'{g}L6.png'),
            pygame.image.load(f'{g}L7.png'),
            pygame.image.load(f'{g}L8.png'),
            pygame.image.load(f'{g}L9.png')]


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self, win):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load(f'{g}R1{e}.png'),
                 pygame.image.load(f'{g}R2{e}.png'),
                 pygame.image.load(f'{g}R3{e}.png'),
                 pygame.image.load(f'{g}R4{e}.png'),
                 pygame.image.load(f'{g}R5{e}.png'),
                 pygame.image.load(f'{g}R6{e}.png'),
                 pygame.image.load(f'{g}R7{e}.png'),
                 pygame.image.load(f'{g}R8{e}.png'),
                 pygame.image.load(f'{g}R9{e}.png'),
                 pygame.image.load(f'{g}R10{e}.png'),
                 pygame.image.load(f'{g}R11{e}.png')]

    walkLeft = [pygame.image.load(f'{g}L1{e}.png'),
                pygame.image.load(f'{g}L2{e}.png'),
                pygame.image.load(f'{g}L3{e}.png'),
                pygame.image.load(f'{g}L4{e}.png'),
                pygame.image.load(f'{g}L5{e}.png'),
                pygame.image.load(f'{g}L6{e}.png'),
                pygame.image.load(f'{g}L7{e}.png'),
                pygame.image.load(f'{g}L8{e}.png'),
                pygame.image.load(f'{g}L9{e}.png'),
                pygame.image.load(f'{g}L10{e}.png'),
                pygame.image.load(f'{g}L11{e}.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((500, 480))
        pygame.display.set_caption("First Game")
        self.bg = pygame.image.load(f'{g}bg.jpg')
        self.char = pygame.image.load(f'{g}standing.png')
        self.clock = pygame.time.Clock()
        self.bulletSound = pygame.mixer.Sound("Game/bullet.wav")
        self.hitSound = pygame.mixer.Sound("Game/hit.wav")
        self.score = 0
        self.font = pygame.font.SysFont('comicsans', 30, True)
        self.shootLoop = 0
        self.bullets = []
        self.run = True
        self.man = player(200, 410, 64, 64)
        self.goblin = enemy(100, 410, 64, 64, 450)

    def redrawGameWindow(self):
        self.win.blit(self.bg, (0, 0))
        text = self.font.render('Score: ' + str(self.score), 1, (0, 0, 0))
        self.win.blit(text, (350, 10))
        self.man.draw(self.win)
        self.goblin.draw(self.win)
        for bullet in self.bullets:
            bullet.draw(self.win)

        pygame.display.update()

    def Run(self):
        while self.run:
            self.clock.tick(27)
            if self.goblin.visible:
                if self.man.hitbox[1] < self.goblin.hitbox[1] + self.goblin.hitbox[3] and self.man.hitbox[1] + \
                        self.man.hitbox[3] > self.goblin.hitbox[1]:
                    if self.man.hitbox[0] + self.man.hitbox[2] > self.goblin.hitbox[0] and self.man.hitbox[0] < \
                            self.goblin.hitbox[0] + self.goblin.hitbox[2]:
                        self.man.hit(self.win)

                        self.goblin.x = random.randint(0,self.man.x-60)
                        self.score -= 5
            if self.shootLoop > 0:
                self.shootLoop += 1
            if self.shootLoop > 3:
                self.shootLoop = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            for bullet in self.bullets:
                if bullet.y - bullet.radius < self.goblin.hitbox[1] + self.goblin.hitbox[
                    3] and bullet.y + bullet.radius > self.goblin.hitbox[1]:
                    if bullet.x + bullet.radius > self.goblin.hitbox[0] and bullet.x - bullet.radius < \
                            self.goblin.hitbox[0] + self.goblin.hitbox[2]:
                        self.hitSound.play()
                        self.goblin.hit()
                        self.score += 1
                        self.bullets.pop(self.bullets.index(bullet))

                if 500 > bullet.x > 0:
                    bullet.x += bullet.vel
                else:
                    self.bullets.pop(self.bullets.index(bullet))

            if not self.goblin.visible:
                self.goblin.health = 10
                self.goblin.visible = True

                self.goblin.x = random.randint(0, 300)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and self.shootLoop == 0:
                self.bulletSound.play()
                if self.man.left:
                    facing = -1
                else:
                    facing = 1

                if len(self.bullets) < 5:
                    self.bullets.append(
                        projectile(round(self.man.x + self.man.width // 2), round(self.man.y + self.man.height // 2), 6,
                                   (0, 0, 0), facing))

                self.shootLoop = 1

            if keys[pygame.K_LEFT] and self.man.x > self.man.vel:
                self.man.x -= self.man.vel
                self.man.left = True
                self.man.right = False
                self.man.standing = False
            elif keys[pygame.K_RIGHT] and self.man.x < 500 - self.man.width - self.man.vel:
                self.man.x += self.man.vel
                self.man.right = True
                self.man.left = False
                self.man.standing = False
            else:
                self.man.standing = True
                self.man.walkCount = 0

            if not self.man.isJump:
                if keys[pygame.K_UP]:
                    self.man.isJump = True
                    self.man.right = False
                    self.man.left = False
                    self.man.walkCount = 0
            else:
                if self.man.jumpCount >= -10:
                    neg = 1
                    if self.man.jumpCount < 0:
                        neg = -1
                    self.man.y -= (self.man.jumpCount ** 2) * 0.5 * neg
                    self.man.jumpCount -= 1
                else:
                    self.man.isJump = False
                    self.man.jumpCount = 10

            self.redrawGameWindow()


game = Game()
game.Run()

pygame.quit()
