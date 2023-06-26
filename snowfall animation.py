import pygame
import random
import numpy

screenWidth = 1200
screenHeight = 800
clock = pygame.time.Clock()


class snowflake:
    def __init__(self):
        self.pos = numpy.array([random.randint(0, screenWidth), random.randint(-100, -1)])
        self.vel = numpy.array([0, 0])
        self.size = int(random.randint(2, 8))
        self.accl = numpy.array([0, 0.01*self.size])


    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 255), (int(self.pos[0]), int(self.pos[1])), self.size, 0)

    def update(self):
        self.pos = numpy.add(self.pos, self.vel)
        self.vel = numpy.add(self.accl, self.vel)


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Νame")
        self.stop = False
        self.snow = []

    def drawWindow(self):
        self.snow.append(snowflake())
        for flake in self.snow:
            flake.draw(self.win)
            flake.update()

        for flake in self.snow:
            if flake.pos[1] > screenHeight:
                self.snow.remove(flake)
        print(len(self.snow))

    def run(self):
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True

            self.win.fill((0, 0, 0))
            self.drawWindow()
            pygame.display.update()


program = Display()
program.run()
