import pygame
import random
import numpy

screenWidth = 1200
screenHeight = 800
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 1

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (self.y * 1 + 10, self.x * 4 + 10), self.r, 0)


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Νame")
        self.stop = False
        self.points = []
        self.d = {}

    def drawWindow(self):
        for point in self.points:
            point.draw(self.win)
        pygame.display.update()

    def ack(self, m, n):

        if (m,n) not in self.d:

            self.points.append(Point(m, n))
            self.drawWindow()
        if (m, n) in self.d:
            
            return self.d[m, n]
        elif m == 0:
            return n + 1
        elif n == 0:
            if (m - 1, 1) in self.d:
                return self.d[m - 1, 1]
            else:
                self.d[m - 1, 1] = self.ack(m - 1, 1)
                return self.d[m - 1, 1]
        else:
            if (m, n - 1) in self.d:
                if (m - 1, self.d[m, n - 1]) in self.d:
                    return self.d[m - 1, self.d[m, n - 1]]
                else:
                    self.d[m - 1, self.d[m, n - 1]] = self.ack(m - 1, self.d[m, n - 1])
                    return self.d[m - 1, self.d[m, n - 1]]
            else:
                self.d[m, n - 1] = self.ack(m, n - 1)
                if (m - 1, self.d[m, n - 1]) in self.d:
                    return self.d[m - 1, self.d[m, n - 1]]
                else:
                    self.d[m - 1, self.d[m, n - 1]] = self.ack(m - 1, self.d[m, n - 1])
                    return self.d[m - 1, self.d[m, n - 1]]

    def run(self):
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True

            self.win.fill(black)

            self.drawWindow()
            M, N = 4,3
            if (M, N) not in self.d:
                t = self.ack(M, N)
                self.d[M, N] = t



program = Display()
program.run()
