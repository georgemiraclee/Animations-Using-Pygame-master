import pygame
import random
import numpy

pygame.init()

screenWidth = 1000
screenHeight = 600
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sorting")
clock = pygame.time.Clock()


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    return merge(left, right)


def merge(A, B):
    i, j = 0, 0
    c = list()
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            c.append(A[i])
            i += 1
        elif A[i] > B[j]:
            c.append(B[j])
            j += 1
        else:
            c.append(A[i])
            c.append(B[j])
            i += 1
            j += 1
    while i < len(A):
        c.append(A[i])
        i += 1
    while j < len(B):
        c.append(B[j])
        j += 1

    return c


def partition(arr, start, end):
    pivot = arr[end]
    pivot_index = start - 1
    for i in range(start, end):
        if arr[i] < pivot:
            pivot_index += 1
            arr[i], arr[pivot_index] = arr[pivot_index], arr[i]

    arr[end], arr[pivot_index + 1] = arr[pivot_index + 1], arr[end]
    return pivot_index + 1


class Display:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Sorting")

        self.bars = []
        for i in range(screenWidth):
            self.bars.append(random.randint(10, screenHeight))

        self.stop = False
        self.i = 0

    def drawWindow(self):
        self.win.fill((0, 0, 0))
        for i in range(len(self.bars)):
            pygame.draw.line(self.win, (255, 255, 255), [i, screenHeight], [i, screenHeight - self.bars[i]],
                             1)
        pygame.display.update()

    def quickSort(self, start, end):
        if start < end:
            index = partition(self.bars, start, end)
            self.quickSort(start, index - 1)
            self.quickSort(index + 1, end)
            self.drawWindow()

    def partition(self,arr, start, end):
        pivot = arr[end]
        pivot_index = start - 1
        for i in range(start, end):
            if arr[i] < pivot:
                pivot_index += 1
                arr[i], arr[pivot_index] = arr[pivot_index], arr[i]
                self.drawWindow()

        arr[end], arr[pivot_index + 1] = arr[pivot_index + 1], arr[end]
        return pivot_index + 1

    def run(self):
        while not self.stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop = True

            self.drawWindow()
            t = len(self.bars) - 1
            self.quickSort(0, t)


program = Display()
program.run()
