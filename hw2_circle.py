from __future__ import division
import pygame
import sys
import math
import random
import time
from pygame import gfxdraw


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (255, 0, 255)
aquamarine = (0, 255, 255)
yellow = (255, 255, 0)
colors = [black, red, green, blue, purple, yellow, aquamarine]
colors_count = len(colors)

use_bresenham_to_draw_circle = False

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def set_pixel(pixel, color = black, size = 1):
    surface = pygame.display.get_surface()
    for i in range(size):
        for j in range(size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)

def four_symmetric(xc, yc, x, y, pixels):
    pixels.append((xc + x, yc + y))
    pixels.append((xc - x, yc - y))
    pixels.append((xc - x, yc + y))
    pixels.append((xc + x, yc - y))

def eight_symmetric(xc, yc, x, y, pixels):
    four_symmetric(xc, yc, x, y, pixels)
    four_symmetric(xc, yc, y, x, pixels)

def generate_bresenham_circle(center, r, pixels):
    cx, xy = center

   

def generate_simple_circle(center, r, pixels):
    xc, yc = center
    x = 0
    y = r
    pixels.append((int(xc), int(yc + r)))
    pixels.append((xc, yc - r))
    pixels.append((xc + r, yc))
    pixels.append((xc - r, yc))

    while(x < y):
        x += 1

        y = int(math.sqrt(float(r * r - x* x)))
        eight_symmetric(xc, yc, x, y, pixels)

    if x == y:
        four_symmetric(xc, yc, x, y, pixels)

def draw_circle(center, r, use_bresenham):
    circle = []

    if use_bresenham:
        generate_bresenham_circle(center, r, circle)
    else:
        generate_simple_circle(center, r, circle)

    color = colors[int(random.random() * 10) % colors_count]
    for pixel in circle:
        set_pixel(pixel, color)   

pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)
first_point = second_point = ()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            set_pixel(last_click)
            if first_point == ():
                first_point = last_click
            elif second_point == ():
                second_point = last_click


    if first_point != () and second_point != ():
        draw_circle(first_point, int(distance(first_point, second_point)), use_bresenham_to_draw_circle)
        first_point = second_point = ()
    
    pygame.display.flip()