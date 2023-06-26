import pygame
import random
import numpy
import time

screenWidth = 1200
screenHeight = 800
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class Display:
    def __init__(self):
        self.speed = 0.02
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Νame")
        self.stop = False
        self.time = 0
        self.array = []
        self.arraypoints = 600
        self.loops = 1
        self.clock = pygame.time.Clock()

    def drawWindow(self):
        x = 200
        y = 200
        for i in range(self.loops):
            prevx = x
            prevy = y
            n = 2 * i + 1
            radius = int(100 * (4 / (n * numpy.pi)))
            pygame.draw.circle(self.win, white, (prevx, prevy), radius, 2)
            x += int(radius * numpy.cos(n * self.time))
            y += int(radius * numpy.sin(n * self.time))
            pygame.draw.circle(self.win, white, (x, y), 4, 0)
            pygame.draw.line(self.win, white, (prevx, prevy), (x, y), 2)
        self.array.insert(0, y)

        for i in range(len(self.array)):
            pygame.draw.circle(self.win, white, (400 + i, self.array[i]), 1, 0)
        pygame.draw.line(self.win, white, (x, y), (400, self.array[0]), 1)
        if len(self.array) > self.arraypoints:
            self.array = self.array[:self.arraypoints]

    def run(self):

        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True

            self.time += self.speed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.speed += 0.01
                pygame.time.delay(100)
            if keys[pygame.K_DOWN]:
                self.speed -= 0.01
                pygame.time.delay(100)
            if keys[pygame.K_SPACE]:
                self.loops += 1
                pygame.time.delay(100)
            if keys[pygame.K_TAB]:
                pygame.time.delay(100)
                if self.loops>0:
                    self.loops -= 1


            self.win.fill(black)

            self.drawWindow()
            self.clock.tick(40)
            pygame.display.update()



program = Display()
program.run()
