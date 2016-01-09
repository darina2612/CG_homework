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
rand_color = 0

use_bresenham_to_draw_line = False

def set_pixel(pixel, color = black):
	surface = pygame.display.get_surface()
	pygame.gfxdraw.pixel(surface, pixel[0], pixel[1], color)


def generate_bresenham_line(point_A, point_B, pixels):
    x1, y1 = point_A
    x2, y2 = point_B

    h = abs(x2 - x1)
    v = abs(y2 - y1)

    incX = 1
    incY = 1
    reverse = False

    if x2 < x1 :
        incX = -1
    if y2 < y1:
        incY = -1

    if h < v:
        reverse = True
        a = h
        h = v
        v = a

    inc_up = 2 * v - 2 * h
    inc_dn = 2 * v

    x = x1
    y = y1
    est = 2 * v - h

    for i in range(h):
        pixels.append((x, y))

        if est >= 0:
            est += inc_up
            x += incX
            y += incY
        else:
            est += inc_dn

            if reverse:
                y += incY
            else:
                x += incX


def generate_simple_line(point_A, point_B, pixels):
    x1, y1 = point_A
    x2, y2 = point_B

    h = abs(x2 - x1)
    v = abs(y2 - y1)

    sx = False
    sy = False

    if x2 < x1:
        sx = True
    if y2 < y1:
        sy = True

    reverse = False

    if h < v:
        reverse = True
        a = h
        h = v
        v = a

    if h == 0:
        pixels.append((x1,y1))
        return

    slope = v / h

    for i in range(h):
        x = i
        y = int(math.floor(slope*x + 0.5))

        if reverse:
            a = x
            x = y
            y = a
        if sx:
            x = -x
        if sy:
            y = -y

        pixels.append((x + x1, y + y1))


def draw_line(point_A, point_B, use_bresenham):
    line = []

    if use_bresenham:
        generate_bresenham_line(point_A, point_B, line)
    else:
        generate_simple_line(point_A, point_B, line)

    color = colors[int(random.random() * 10) % colors_count]
    for pixel in line:
        set_pixel(pixel, color)


def compare_methods():
    start_points = []
    end_points = []
    simple_line = []
    br_line = []
    for i in range(10000):
        start_points.append((int(random.random()*140) % 140, int(random.random()*100) % 100))
        end_points.append((int(random.random()*140) % 140, int(random.random()*100) % 100))

    start = time.time()
    for i in range(10000):
        generate_simple_line(start_points[i], end_points[i], simple_line)
    end = time.time()

    print "Time for calculating 10 000 lines by the rounding method: {} s.".format(end - start)
    
    start = time.time()
    for i in range(10000):
        generate_bresenham_line(start_points[i], end_points[i], br_line)
    end = time.time()

    print "Time for calculating 10 000 lines by the Bresenham's method: {} s.".format(end - start)
    
    same_result = (simple_line == br_line)

    res = 'The two methods '
    if not same_result:
        res += 'do not '
    res += 'produce the same result.'

    print res

    use_bresenham_to_draw_line = input('Choose method for drawing:\n Enter \'0\' for using the roundong method.\n Enter \'1\' for using Bresenham\'s method.\n')


compare_methods()

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
        draw_line(first_point, second_point, use_bresenham_to_draw_line)
        first_point = second_point = ()
    
    pygame.display.flip()
