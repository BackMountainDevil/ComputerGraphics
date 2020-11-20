#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mpline.py
@Time    :   2020/11/19 19:09:22
@Author  :   Kearney
@Version :   0.0.0
@Contact :   191615342@qq.com
@License :   GPL 3.0
@Desc    :   计算机图形学-DAA改进后的中点算法实现，基于pygame的鼠标事件，
             鼠标点下一个点后画点，再点下一个点后由中点算法划线，可划多条，右键清空画面重置
             首先画出来的是由pygame划线函数画出来的红线，延时1s后用中点算法划白线，以此作为对比

             参考《计算机图形学基础 OpenGL版》 徐文鹏 清华大学出版社
             3.1.4 中点划线法
'''
import time
import pygame
import sys

width = 920     # 画板宽度
height = 640    # 画版高度
isp = False
x1 = y1 = x2 = y2 = -1
ps = (x1, y1)
pe = (x2, y2)


# 交换两个变量的值
def swap(a, b):
    return b, a


# 中点划线法画白线
def MidPointLine(sur, x1, y1, x2, y2):
    tag = 0
    dx = x2 - x1
    dy = y2 - y1
    if (abs(dx) < abs(dy)):  # 如果 |k| >1 ，坐标互换
        x1, y1 = swap(x1, y1)
        x2, y2 = swap(x2, y2)
        tag = 1
    if (x1 > x2):  # 确保x1 < x2
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
    a = y1 - y2
    b = x2 - x1
    d = a + (b / 2)
    if (y1 < y2):  # 斜率 > 0
        x = x1
        y = y1
        while (x < x2):
            if (d < 0):
                y = y + 1
                x = x + 1
                d = d + a + b
            else:
                d = d + a
                x = x + 1
            if (tag):  # 斜率 > 1
                pygame.draw.circle(sur, (255, 255, 255), (y, x), 1, 1)  # 互换
            else:
                pygame.draw.circle(sur, (255, 255, 255), (x, y), 1, 1)
    else:  # 斜率 <= 0
        x = x2
        y = y2
        while (x > x1):
            if (d < 0):
                y = y + 1
                x = x - 1
                d = d - a + b
            else:
                x = x - 1
                d = d - a
            if (tag):
                pygame.draw.circle(sur, (255, 255, 255), (y, x), 1, 1)
            else:
                pygame.draw.circle(sur, (255, 255, 255), (x, y), 1, 1)


pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("MidPointLine_Kearney")

# 三个画点效果对比
# pygame.draw.circle(screen, (255, 255, 255), (20, 15), 1, 1)
# pygame.draw.rect(screen, (255, 255, 255), [40, 15, 1, 1], 1)
# screen.set_at((60, 15), (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if x1 < 0:
                x1, y1 = event.pos
            else:
                x2, y2 = event.pos
            pygame.draw.circle(screen, (255, 255, 255), event.pos, 1, 1)
            print('(', x1, ',', y1, ')', '  (', x2, ',', y2, ')')
            if (x2 > 0):
                pygame.draw.line(screen, (255, 0, 0), (x1, y1),
                                 (x2, y2))  # 调用内置函数划线画红线
                pygame.display.update()
                isp = True
            if (pygame.mouse.get_pressed()[2]):  # 鼠标右键按下，重置
                x1 = y1 = x2 = y2 = -1
                screen.fill((0, 0, 0))
                print("Reset done")
    if (isp):
        isp = False
        time.sleep(1)  # 延时1s后在启动中点划线法画白线
        MidPointLine(screen, x1, y1, x2, y2)
        x1 = y1 = x2 = y2 = -1
    pygame.display.update()
sys.exit()
