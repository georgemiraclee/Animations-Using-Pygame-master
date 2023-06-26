import pygame
import random
import numpy
import heapq
factor = 2
screenWidth = int(200 / factor)
screenHeight = int(200 / factor)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dA = 1
dB = 0.5
feed = 0.055
kill = 0.062
delta_t = 1


class pixel:
    def __init__(self):
        self.a = 1
        self.b = 0


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Reaction_Diffusion")
        self.stop = False
        self.frame = 0
        self.grid = [[pixel() for i in range(screenWidth)] for j in
                     range(screenHeight)]
        self.next = [[pixel() for i in range(screenWidth)] for j in
                     range(screenHeight)]
        for i in range(int(10 / factor)):
            for j in range(int(10 / factor)):
                self.grid[int(100 / factor) + i][int(100 / factor) + j].b = 1
        # for i in range(10):
        #     for j in range(10):
        #         self.grid[180 + i][180 + j].a = 1

    def laplaceA(self, i, j):
        sum = self.grid[i][j].a * -1
        sum += (self.grid[i + 1][j].a + self.grid[i - 1][j].a + self.grid[i][j + 1].a + self.grid[i][j - 1].a) * 0.2
        sum += (self.grid[i + 1][j - 1].a + self.grid[i + 1][j + 1].a + self.grid[i - 1][j + 1].a + self.grid[i - 1][
            j - 1].a) * 0.05
        return sum

    def laplaceB(self, i, j):
        sum = self.grid[i][j].b * -1
        sum += (self.grid[i + 1][j].b + self.grid[i - 1][j].b + self.grid[i][j + 1].b + self.grid[i][j - 1].b) * 0.2
        sum += (self.grid[i + 1][j - 1].b + self.grid[i + 1][j + 1].b + self.grid[i - 1][j + 1].b + self.grid[i - 1][
            j - 1].b) * 0.05
        return sum

    def drawWindow(self):
        for i in range(1, screenHeight - 1):
            for j in range(1, screenWidth - 1):
                a = self.grid[i][j].a
                b = self.grid[i][j].b
                self.next[i][j].a = a + (dA * self.laplaceA(i, j) - a * b * b + feed * (1 - a)) * delta_t
                self.next[i][j].b = b + (dB * self.laplaceB(i, j) + a * b * b - (kill + feed) * b) * delta_t
                self.next[i][j].a = constrain(self.next[i][j].a, 0, 1)
                self.next[i][j].b = constrain(self.next[i][j].b, 0, 1)
                q1 = self.next[i][j].a
                q2 = self.next[i][j].b
                c = int((q1 - q2) * 255)
                c = constrain(c, 0, 255)
                self.win.set_at((i, j), (c, c, c))

        pygame.display.update()
        self.grid = self.next

    def run(self):
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True
            self.drawWindow()


program = Display()
program.run()
