import pygame
import random
import numpy

screenWidth = 1200
screenHeight = 800
clock = pygame.time.Clock()
length = 21


class Toothpick:
    def __init__(self, center_x, center_y, dir):
        self.x = center_x
        self.y = center_y
        self.dir = dir
        self.new = True
        if self.dir == 1:
            self.ax, self.ay = self.x - (length / 2), self.y
            self.bx, self.by = self.x + (length / 2), self.y
        else:
            self.ax, self.ay = self.x, self.y - (length / 2)
            self.bx, self.by = self.x, self.y + (length / 2)

    def draw(self, win):
        if self.new:
            pygame.draw.line(win, (0, 0, 255),
                             (self.ax, self.ay),
                             (self.bx, self.by), 4)
        else:
            pygame.draw.line(win, (0, 0, 0),
                             (self.ax, self.ay),
                             (self.bx, self.by), 1)

    def intersects(self, x, y):
        if self.ax == x and self.ay == y:
            return True
        elif self.bx == x and self.by == y:
            return True
        else:
            return False

    def createA(self, arr):
        available = True
        for pick in arr:
            if pick != self and pick.intersects(self.ax, self.ay):
                available = False
        if available:
            return Toothpick(self.ax,self.ay,self.dir*-1)

    def createB(self, arr):
        available = True
        for pick in arr:
            if pick != self and pick.intersects(self.bx, self.by):
                available = False
        if available:
            return Toothpick(self.bx,self.by,self.dir*-1)


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Toothpickanimation")
        self.stop = False
        self.picks = []
        t = Toothpick(screenWidth / 2, screenHeight / 2, 1)
        self.picks.append(t)

    def drawWindow(self):
        for i in self.picks:
            i.draw(self.win)

    def run(self):

        while not self.stop:
            nextpicks = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True
            self.win.fill((255, 255, 255))

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]:
            for pick in self.picks:
                if pick.new:
                    A = pick.createA(self.picks)
                    B = pick.createB(self.picks)
                    if A is not None:
                        nextpicks.append(A)
                    if B is not None:
                        nextpicks.append(B)
                    pick.new = False
            self.picks += nextpicks

            self.drawWindow()

            pygame.display.update()


program = Display()
program.run()
