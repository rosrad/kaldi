#!/usr/bin/env python
# encoding: utf-8

# Draw a moving cosine curve.

import math
import pygame
from pygame.locals import *

WINSIZE = [960, 540]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_curve(surface, dx, color):
    w, h = WINSIZE
    hh = h / 2.0
    scale = 100.0  # one period = (2*pi*scale) pixels
    for i in range(w):
        y = int(hh * -math.cos((i+dx)/scale) + hh)
        surface.set_at((i, y), BLACK)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption('Draw a curve')
    screen = pygame.display.set_mode(WINSIZE,
        pygame.HWSURFACE|pygame.DOUBLEBUF)

    dx = 0
    screen.fill(WHITE)
    draw_curve(screen, dx, BLACK)
    pygame.display.update()

    quit = False
    while not quit:
        dx += 2
        screen.fill(WHITE)
        draw_curve(screen, dx, BLACK)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit = True
                break
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
