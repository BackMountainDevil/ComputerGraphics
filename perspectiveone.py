#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :  perspectiveone.py
@Time    :  2020/12/11 21:45:11
@Author  :  Kearney
@Version :  0.0.0
@Contact :  191615342@qq.com
@License :  GPL 3.0
@Desc    :  一点透视
            画布横轴x向右增大，纵轴y向下增大
    ref:    https://blog.csdn.net/mylovestart/article/details/8352105
'''
import pygame
import sys
import numpy as np

# 长方体的八个点(x, y ,z, 1)
points = [[0, 0, 200, 1], [200, 0, 200, 1], [200, 0, 0, 1], [0, 0, 0, 1],
          [0, 200, 200, 1], [200, 200, 200, 1], [200, 200, 0, 1],
          [0, 200, 0, 1]]

L = 100  # 平移位置L, M, N
M = 100
N = 100
D = 300  # 视距

# 变换矩阵
transMatrix = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1 / D], [L, M, 0, 1 + (N / D)]],
    dtype='float32')

# 将三维坐标映射到二维
for e in range(0, len(points)):
    tmp = np.matmul(np.array(points[e], dtype='float32'), transMatrix)
    tmp = tmp / tmp[3]  # 归一化
    points[e] = tmp.tolist()[:2]  # 取x，y
    print("p", e, " : ", points[e])

LINECOLOR = (0, 255, 0)  # 颜色设置
BACKYCOLOR = (255, 0, 0)
LINEWIDTH = 3  # 线宽

pygame.init()
screen = pygame.display.set_mode((920, 640))

while True:
    screen.fill(BACKYCOLOR)
    pygame.draw.lines(screen, LINECOLOR, False, points, LINEWIDTH)  # 懒人划线
    pygame.draw.line(screen, BACKYCOLOR, points[3], points[4], LINEWIDTH)  # 遮瑕
    # 补全剩下的线条
    pygame.draw.line(screen, LINECOLOR, points[0], points[3], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[4], points[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[0], points[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[0], points[1], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[0], points[4], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[3], points[7], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[2], points[6], LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, points[1], points[5], LINEWIDTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    pygame.display.update()
