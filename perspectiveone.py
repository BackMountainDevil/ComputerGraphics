#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  perspectiveone.py
@Time    :  2020/12/11 21:45:11
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  一点透视、两点透视
            画布横轴x向右增大，纵轴y向下增大
    ref:    https://blog.csdn.net/mylovestart/article/details/8352105
'''
import pygame
import sys
import numpy as np
import math

# 长方体的八个点(x, y ,z, 1)
points = [[0, 0, 200, 1], [200, 0, 200, 1], [200, 0, 0, 1], [0, 0, 0, 1],
          [0, 200, 200, 1], [200, 200, 200, 1], [200, 200, 0, 1],
          [0, 200, 0, 1]]
onepoint = []  # 一点透视后的二维坐标
twopoint = []  # 两点透视后的二维坐标

# 一点透视参数
L = 100  # 平移位置L, M, N
M = 100
N = 100
D = 300  # 视距
# 两点透视参数
P = 2
R = 3
degree = 45

# 一点透视变换矩阵
transMatrix = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1 / D], [L, M, 0, 1 + (N / D)]],
    dtype='float32')

# 一点透视：将三维坐标映射到二维
for e in range(0, len(points)):
    tmp = np.matmul(np.array(points[e], dtype='float32'), transMatrix)
    tmp = tmp / tmp[3]  # 齐次化
    onepoint.append(tmp.tolist()[:2])

# 两点透视变换矩阵
twoMatrix = np.array(
    [[math.cos(degree), 0, 0,
      (P * math.cos(degree) - R * math.sin(degree))], [0, 1, 0, 0],
     [math.sin(degree), 0, 0, (P * math.sin(degree) + R * math.cos(degree))],
     [(L * math.cos(degree) + N * math.sin(degree)), M, 0,
      (P * (L * math.cos(degree) + N * math.sin(degree))) +
      (R * (N * math.cos(degree) + L * math.sin(degree))) + 1]],
    dtype='float32')
# 两点透视降维变换
for e in range(0, len(points)):
    tmp = np.matmul(np.array(points[e], dtype='float32'), twoMatrix)
    tmp = tmp / tmp[3]  # 齐次化
    tmp = tmp * 500  # 非必须：放大，太小看不见
    tmp[0] += 200  # 非必须：整体向右平移，不然和一位透视挡在一起了
    twopoint.append(tmp.tolist()[:2])

LINECOLOR = (0, 255, 0)  # 颜色设置
BACKYCOLOR = (255, 0, 0)
LINEWIDTH = 3  # 线宽
pygame.init()
screen = pygame.display.set_mode((920, 640))

while True:
    screen.fill(BACKYCOLOR)
    # 一点透视的图
    pygame.draw.lines(screen, LINECOLOR, False, onepoint, LINEWIDTH)  # 懒人划线
    pygame.draw.line(screen, BACKYCOLOR, onepoint[3], onepoint[4],
                     LINEWIDTH)  # 遮瑕
    # 补全剩下的线条
    pygame.draw.line(screen, LINECOLOR, onepoint[0], onepoint[3], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[4], onepoint[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[0], onepoint[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[0], onepoint[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[0], onepoint[4], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[3], onepoint[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[2], onepoint[6], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, onepoint[1], onepoint[5], LINEWIDTH)

    # 两点透视的图
    pygame.draw.lines(screen, LINECOLOR, False, twopoint, LINEWIDTH)
    pygame.draw.line(screen, BACKYCOLOR, twopoint[3], twopoint[4], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[0], twopoint[3], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[4], twopoint[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[0], twopoint[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[0], twopoint[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[0], twopoint[4], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[3], twopoint[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[2], twopoint[6], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, twopoint[1], twopoint[5], LINEWIDTH)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    pygame.display.update()
