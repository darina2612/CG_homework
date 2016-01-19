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

CONTOL_LINES_ON = False
CONTROL_COLOR = (0, 51, 51)
SEGMENT_COUNT = 500


def set_pixel(pixel, color = black, pixel_size = 1):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)


def caluclate_bezier_point(p0, p1, p2, t):
    u = 1 - t
    tt = t ** 2;
    uu = u ** 2
    
    xp = (uu * p0[0]) + (2 * u * t * p1[0]) + (tt * p2[0]) 
    yp = (uu * p0[1]) + (2 * u * t * p1[1]) + (tt * p2[1]) 
 
    return (xp, yp)


def calculate_bezier_curve_2deg(p0, p1, p2, curve):
    for i in range(SEGMENT_COUNT):
        t = i / SEGMENT_COUNT
        pixel = caluclate_bezier_point(p0, p1, p2, t)
        curve.append(pixel)


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


def draw_contol_lines(p0, p1, p2):
    lines = []

    generate_simple_line(p0, p1, lines)
    generate_simple_line(p1, p2, lines)

    for pixel in lines:
        set_pixel(pixel, CONTROL_COLOR)

    set_pixel(p0, CONTROL_COLOR, 3)
    set_pixel(p1, CONTROL_COLOR, 3)
    set_pixel(p2, CONTROL_COLOR, 3)

def draw_bezier_curve(p0, p1, p2):
    if CONTOL_LINES_ON:
        draw_contol_lines(p0, p1, p2)

    curve = []
    calculate_bezier_curve_2deg(p0, p1, p2, curve)
    color = colors[int(random.random() * (colors_count + 1)) % colors_count]
    for point in curve:
        set_pixel((int(point[0]), int(point[1])), color)


pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)

first_point = second_point = third_point = ()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if CONTOL_LINES_ON:
                    CONTOL_LINES_ON = False
                else:
                    CONTOL_LINES_ON = True
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if first_point == ():
                first_point = last_click
            elif second_point == ():
                second_point = last_click
            elif third_point == ():
                third_point = last_click
                draw_bezier_curve(first_point, second_point, third_point)
                pygame.display.flip()
                first_point = second_point = third_point = ()
                
    pygame.display.flip()