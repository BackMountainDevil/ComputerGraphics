#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  bezier.py
@Time    :  2020/12/16 20:50:32
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  贝塞尔曲线
            用鼠标左键确定几个点，右键后画出由这些点确定的贝塞尔曲线
            按下空格后重新开始取点
            https://zhuanlan.zhihu.com/p/203408475
'''
import pygame
from pygame.locals import K_SPACE
import sys
import numpy as np
LINECOLOR = (29, 244, 255)  # 颜色设置
POINTCLOLOR = (0, 150, 150)
BACKYCOLOR = (255, 212, 238)
LINEWIDTH = 3  # 线宽
points = []


def B_nx(n, i, x):
    if i > n:
        return 0
    elif i == 0:
        return (1 - x)**n
    elif i == 1:
        return n * x * ((1 - x)**(n - 1))
    return B_nx(n - 1, i, x) * (1 - x) + B_nx(n - 1, i - 1, x) * x


def get_value(p, canshu):
    sumx = 0.
    sumy = 0.
    length = len(p) - 1
    for i in range(0, len(p)):
        sumx += (B_nx(length, i, canshu) * p[i][0])
        sumy += (B_nx(length, i, canshu) * p[i][1])
    return sumx, sumy


def get_newxy(p, x):
    xx = [0] * len(x)
    yy = [0] * len(x)
    for i in range(0, len(x)):
        print('x[i]=', x[i])
        a, b = get_value(p, x[i])
        xx[i] = a
        yy[i] = b
        print('xx[i]=', xx[i])
    return xx, yy


pygame.init()
screen = pygame.display.set_mode((920, 640))
screen.fill(BACKYCOLOR)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 退出程序
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (pygame.mouse.get_pressed()[2]):  # 鼠标右键按下绘制贝塞尔曲线
                x = np.linspace(0, 1, 101)
                xx, yy = get_newxy(points, x)
                print(type(xx), len(xx), type(yy), len(yy))
                for i in range(len(xx) - 1):
                    pygame.draw.line(screen, LINECOLOR, (xx[i], yy[i]),
                                     (xx[i + 1], yy[i + 1]), LINEWIDTH)
                print("R")
            else:  # 鼠标其它键按下时画点纪录
                x, y = event.pos
                pygame.draw.circle(screen, POINTCLOLOR, (x, y), 3, 0)
                points.append([x, y])
                print("L")
        # 按下空格重新开始取点
        if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_SPACE]:
            screen.fill(BACKYCOLOR)
            points.clear()

    pygame.display.update()
