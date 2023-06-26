import pygame
import random
import numpy
from numpy import array
from numpy import cos, sin
from numpy import linalg, deg2rad

screenWidth = 1000
screenHeight = 600


class Particle:
    def __init__(self):
        self.pos = array([250, 250])
        self.vel = 5
        self.angle = 0
        self.viewangle=60

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 0), self.pos, 1, 1)

        for ray in self.rays:
            ray.display(win)
        for i in range (len(self.ray_distance)):
            b = int(255 * (1 - (self.ray_distance[i] / 100000000)))
            pygame.draw.line(win,
                             (255,255,255),
                             (screenWidth//2 * (1 + i/120),300-(self.ray_distance[i]//2)),
                             (screenWidth//2 * (1 + i/120),300+(self.ray_distance[i]//2)),b)

            # pygame.draw.rect(win,
            #                  (b,b,b),
            #                  ((screenWidth//2 * (1 + i/120)),0,screenWidth/120,screenHeight),
            #                   1)

    def look(self, screen, walls):
        self.rays = []
        self.ray_distance = []
        for i in range(-60 + self.angle, 60 + self.angle, 1):
            self.rays.append(Ray(self.pos[0], self.pos[1], deg2rad(i)))

        for ray in self.rays:
            closest = 100000000
            closest_point = None

            for wall in walls:
                pt = ray.cast(wall)

                if pt is not None:
                    dis = linalg.norm(pt - self.pos)
                    if dis < closest:
                        closest = dis
                        closest_point = pt

            if closest_point is not None:
                pygame.draw.line(screen, (255, 255, 255), self.pos, array(closest_point, int), 2)
            self.ray_distance.append(closest)



class Ray:
    def __init__(self, x, y, radius):
        self.pos = [x, y]
        self.dir = array([cos(radius), sin(radius)])

    def display(self, win):
        pygame.draw.line(win, (255, 255, 255), self.pos, self.pos + self.dir, 1)

    def cast(self, wall):
        x1, y1 = wall.a[0], wall.a[1]
        x2, y2 = wall.b[0], wall.b[1]
        x3, y3 = self.pos[0], self.pos[1]
        x4, y4 = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)

        if den == 0:
            return None
        t = num / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            pot = array([x, y])
            return pot


class Limits:
    def __init__(self, x1, y1, x2, y2):
        self.a = [x1, y1]
        self.b = [x2, y2]

    def draw(self, win):
        pygame.draw.line(win, (255, 255, 255), self.a, self.b, 2)


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))

        self.walls = []
        for i in range(5):
            x1 = numpy.random.randint(0, screenWidth // 2)
            y1 = numpy.random.randint(0, screenHeight)

            x2 = numpy.random.randint(0, screenWidth // 2)
            y2 = numpy.random.randint(0, screenHeight)

            self.walls.append(Limits(x1, y1, x2, y2))

        self.walls.append(Limits(0, 0, screenWidth // 2, 0))
        self.walls.append(Limits(0, 0, 0, screenHeight))
        self.walls.append(Limits(0, screenHeight, screenWidth // 2, screenHeight))
        self.walls.append(Limits(screenWidth // 2, 0, screenWidth // 2, screenHeight))
        self.particle = Particle()
        self.clock = pygame.time.Clock()
        self.stop = True

    def redrawGameWindow(self):
        for wall in self.walls:
            wall.draw(self.win)
        self.particle.draw(self.win)

    def run(self):
        while self.stop:
            self.win.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.particle.angle -= 5

            elif keys[pygame.K_RIGHT]:
                self.particle.angle += 5

            elif keys[pygame.K_UP]:
                self.particle.pos[0] += self.particle.vel * cos(deg2rad(self.particle.angle))
                self.particle.pos[1] += self.particle.vel * sin(deg2rad(self.particle.angle))
            elif keys[pygame.K_DOWN]:
                self.particle.pos[0] -= self.particle.vel * cos(deg2rad(self.particle.angle))
                self.particle.pos[1] -= self.particle.vel * sin(deg2rad(self.particle.angle))

            self.particle.look(self.win, self.walls)
            self.redrawGameWindow()
            self.clock.tick(100)
            pygame.display.update()


a = Display()
a.run()
