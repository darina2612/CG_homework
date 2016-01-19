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


def draw_line(point_A, point_B, color = black):
    line = []

    generate_bresenham_line(point_A, point_B, line)

    #color = black #colors[int(random.random() * 10) % colors_count]
    for pixel in line:
        set_pixel(pixel, color)


def draw_200_x_100_rectangle(middle_point):
    a = (int(middle_point[0] - 100), int(middle_point[1] - 50))
    b = (int(middle_point[0] + 100), int(middle_point[1] - 50))
    c = (int(middle_point[0] + 100), int(middle_point[1] + 50))
    d = (int(middle_point[0] - 100), int(middle_point[1] + 50))

    draw_line(a, b)
    draw_line(b, c)
    draw_line(c, d)
    draw_line(d, a)


def rectangle_diagonal_by_given_center(center):
    return (int(center[0] - 100), int(center[1] - 50)), (int(center[0] + 100), int(center[1] + 50))


left = 1
right = 2
bottom = 4 
top = 8

def get_code(point, down_left, up_right):
    x, y = point
    xl, yl = down_left
    xh, yh = up_right
    code = 0

    if x < xl:
        code |= left
    elif x > xh:
        code |= right
    if y < yl:
        code |= bottom
    elif y > yh:
        code |= top

    return code


def cohen_suttherland_cutting(point1, point2, rect_point_a, rect_point_c):
    x1, y1 = point1
    x2, y2 = point2

    xl, yl = rect_point_a
    xh, yh = rect_point_c

    outcode1 = get_code((x1, y1), rect_point_a, rect_point_c)
    outcode2 = get_code((x2, y2), rect_point_a, rect_point_c)

    accept = 0

    while 1:
        #m = float((y2 - y1) / (x2 - x1))

        if not (outcode1 | outcode2):
            accept = 1
            break
        elif (outcode1 & outcode2) != 0:
            break
        else:
            x = y = 0
            temp = 0
            if outcode1 == 0:
                temp = outcode2
            else:
                temp = outcode1
        
            if (temp & top):
                x = x1 + (x2 - x1) * (yh - y1) / (y2 - y1) 
                y = yh
            elif (temp & bottom):
                x = x1 + (x2 - x1) * (yl - y1) / (y2 - y1)
                y = yl
            elif (temp & left):
                x = xl
                y =  y1 + (y2 - y1) * (xl - x1) / (x2 - x1)
            elif (temp & right):
                x = xh
                y = y1 + (y2 - y1) * (xh - x1) / (x2 - x1)
            if temp == outcode1:
                x1 = int(x)
                y1 = y
                outcode1 = get_code((x1, y1), rect_point_a, rect_point_c)
            else:
                x2 = int(x)
                y2 = int(y)
                outcode2 = get_code((x2, y2), rect_point_a, rect_point_c)

    if accept:
        time.sleep(0.5)
        draw_line((int(x1), int(y1)), (int(x2), int(y2)), red)
        pygame.display.flip()


pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)
first_point = second_point = third_point = ()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            set_pixel(last_click)
            if first_point == ():
                first_point = last_click
                draw_200_x_100_rectangle(first_point)
                pygame.display.flip()
            elif second_point == ():
                second_point = last_click
            elif third_point == ():
                third_point = last_click
                draw_line(second_point, third_point)
                pygame.display.flip()
                diagonal = rectangle_diagonal_by_given_center(first_point)
                cohen_suttherland_cutting(second_point, third_point, diagonal[0], diagonal[1])
                first_point = second_point = third_point = ()

    pygame.display.flip()