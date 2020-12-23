#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  zbuffer.py
@Time    :  2020/12/16 20:50:28
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  z-buffer消隐算法
'''
import pygame
import sys

LINECOLOR = (29, 244, 255)  # 颜色设置
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKYCOLOR = (255, 212, 238)
LINEWIDTH = 3  # 线宽

points = [[(448, 384), (572, 114), (674, 416)],
          [(374, 56), (236, 188), (732, 214)],
          [(298, 165), (405, 94), (551, 372)]]

pygame.init()
screen = pygame.display.set_mode((920, 640))


class Stack:
    '''
    模拟栈
    push() 把一个元素添加到栈的最顶层
    pop() 删除栈最顶层的元素，并返回这个元素
    peek() 返回最顶层的元素，并不删除它
    isEmpty() 判断栈是否为空
    size() 返回栈中元素的个数
    '''
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def FloodFill(surface, pixel, newColor, boundaryColor, zbuffercolor):
    '''
    种子填充，需自行确定种子，区域太大时递归十分耗时
    '''
    s = Stack()
    s.push(pixel)
    while (not s.isEmpty()):
        pixel = s.pop()  # 出栈
        try:
            if ((surface.get_at(pixel) != newColor) and
                (surface.get_at(pixel) != boundaryColor)) and (
                    surface.get_at(pixel) != zbuffercolor):  # 颜色和边界判断
                surface.set_at(pixel, newColor)  # 着色
                pygame.display.update()  # 一个点更新一次画面，会耗费较大时间，不需要可注释掉
                px = pixel[0]
                py = pixel[1]
                s.push((px - 1, py))  # 入栈
                s.push((px, py + 1))
                s.push((px + 1, py))
                s.push((px, py - 1))
        except Exception as e:
            print("温馨提示： ", e, "， 请按照凸多边形要求取点")
            sys.exit(0)


while True:
    screen.fill(BACKYCOLOR)
    pygame.draw.polygon(screen, RED, points[0])
    pygame.draw.polygon
    pygame.draw.polygon(screen, GREEN, points[1])
    pygame.draw.polygon(screen, BLUE, points[2], 1)
    x = int((points[2][0][0] + points[2][1][0] + points[2][2][0]) / 3)
    y = int((points[2][0][1] + points[2][1][1] + points[2][2][1]) / 3)
    FloodFill(screen, (x, y), BLUE, BLUE, RED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    pygame.display.update()
