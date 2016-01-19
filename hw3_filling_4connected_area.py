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

def distance(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def set_pixel(pixel, color = black, pixel_size = 1):
    surface = pygame.display.get_surface()
    for i in range(pixel_size):
        for j in range(pixel_size):
            pygame.gfxdraw.pixel(surface, pixel[0] + i, pixel[1] + j, color)


def get_pixel(pixel):
    surface = pygame.display.get_surface()
    return surface.get_at(pixel)

def put_pixel_row(xleft, xright, y, color):
    for x in range(xleft, xright + 1):
        set_pixel((x, y), color)
    time.sleep(0.1)


def four_symmetric(xc, yc, x, y, pixels):
    pixels.append((xc + x, yc + y))
    pixels.append((xc - x, yc - y))
    pixels.append((xc - x, yc + y))
    pixels.append((xc + x, yc - y))


def eight_symmetric(xc, yc, x, y, pixels):
    four_symmetric(xc, yc, x, y, pixels)
    four_symmetric(xc, yc, y, x, pixels)


def generate_simple_circle(center, r, pixels):
    xc, yc = center
    x = 0
    y = r
    pixels.append((xc, yc + r))
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
    generate_simple_circle(center, r, circle)
    for pixel in circle:
        set_pixel(pixel, black)


def stacked_boundary_fill(pixel, color, border_color):
    x, y = pixel

    point_stack = []
    point_stack.append(pixel)

    while point_stack:
        x, y = point_stack.pop()
        
        if get_pixel((x, y)) == color:
            continue
        
        xleft = xright = x

        while get_pixel((xleft - 1, y)) != border_color:
            xleft -= 1
        while  get_pixel((xright + 1, y)) != border_color:
            xright += 1

        put_pixel_row(xleft, xright, y, color)
        pygame.display.flip()

        for nexty in range(y - 1, y + 2, 2):
            p1 = get_pixel((xleft, nexty))

            for x in range(xleft, xright):
                p2 = get_pixel((x + 1, nexty))

                if p1 != border_color and p1 != color and (p2, p2) != (color, border_color):
                    point_stack.append((x, nexty))
                p1 = p2


num_circles_to_intersect = input("Enter nunber of circles to be intersected:\n")

pygame.init()

screen_size = width, height = 640, 480

screen = pygame.display.set_mode(screen_size)

screen.fill(white)

first_point = second_point = ()
current_number_of_circles = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            last_click = pygame.mouse.get_pos()
            if current_number_of_circles < num_circles_to_intersect:
                if first_point == ():
                    first_point = last_click
                    pygame.display.flip()
                elif second_point == ():
                    second_point = last_click
                    draw_circle(first_point, int(distance(first_point, second_point)), True)
                    first_point = second_point = ()
                    current_number_of_circles += 1
                    pygame.display.flip()
            else:
                stacked_boundary_fill(last_click, colors[int(random.random() * colors_count) % colors_count], black)
                pygame.display.flip()
                first_point = second_point = ()
                current_number_of_circles = 0
                
    pygame.display.flip()