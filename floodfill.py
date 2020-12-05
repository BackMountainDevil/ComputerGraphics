#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  floodfill.py
@Time    :  2020/12/05 09:07:38
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  种子填充算法。基于pygame
            鼠标左键确定凸多边形的点，右键封闭图形开始种子填充
            surface.get_at(pixel)返回点的RGBA颜色值，可直接忽略和RGB比较是否相等
            种子目前的确定方法是开始三个点的中点，因此画凸多边形没毛病，凹多边形会存在bug，
            可以考虑使用鼠标点种子点
ref:    [python有栈吗](https://www.php.cn/python-tutorials-424395.html)
        [获取pygame中图像的单个像素的颜色](http://cn.voidcc.com/question/p-nwvuldtn-bs.html)
'''
import pygame
import sys


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


def FloodFill(surface, pixel, newColor, boundaryColor):
    '''
    种子填充，需自行确定种子，区域太大时递归十分耗时
    '''
    s = Stack()
    s.push(pixel)
    while (not s.isEmpty()):
        pixel = s.pop()  # 出栈
        try:
            if ((surface.get_at(pixel) != newColor)
                    and (surface.get_at(pixel) != boundaryColor)):  # 颜色和边界判断
                surface.set_at(pixel, newColor)  # 着色
                px = pixel[0]
                py = pixel[1]
                s.push((px - 1, py))  # 入栈
                s.push((px, py + 1))
                s.push((px + 1, py))
                s.push((px, py - 1))
        except Exception as e:
            print("温馨提示： ", e, "， 请按照凸多边形要求取点")
            sys.exit(0)


# 颜色设置
FILLCOLOR = (0, 255, 0)
BOUNDARYCOLOR = (255, 0, 0)
# 窗体大小设置
WIDTH = 920
HEIGHT = 640
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pixels = []  # 存储点的列表
isdone = False  # 取点是否完成

while True:

    # 内外边框的大规模递归示例，耗时有些长
    # pygame.draw.rect(screen, BOUNDARYCOLOR, [60, 60, 100, 100], 1)
    # pygame.draw.rect(screen, BOUNDARYCOLOR, [20, 20, WIDTH - 40,
    #                                               HEIGHT - 40], 1)
    # FloodFill(screen, (270, 70), FILLCOLOR, BOUNDARYCOLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (pygame.mouse.get_pressed()[0]) and not isdone:  # 鼠标左键按下，画点
                pos = pygame.mouse.get_pos()
                pixels.append(pos)
                screen.set_at(pos, BOUNDARYCOLOR)
                print("Left btn ", pos, len(pixels), pixels)
            if (pygame.mouse.get_pressed()[2]) and not isdone:  # 鼠标右键按下，重置
                if len(pixels) > 2:
                    length = len(pixels)
                    pygame.draw.line(screen, BOUNDARYCOLOR, pixels[length - 1],
                                     pixels[0], 1)
                    print("Right btn")
                    isdone = True
                    x = y = 0
                    for i in range(0, 3):  # 求种子点，必需逆时针画点，求开始三个点的中点
                        x = x + pixels[i][0]
                        y = y + pixels[i][1]
                    FloodFill(screen, (x // 3, y // 3), FILLCOLOR,
                              BOUNDARYCOLOR)
                else:
                    print("点数太少，请继续pick一个点")

    if len(pixels) > 1:
        length = len(pixels)
        # print(length)
        pygame.draw.line(screen, BOUNDARYCOLOR, pixels[length - 2],
                         pixels[length - 1], 1)
    pygame.display.update()
