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
            https://wenku.baidu.com/view/ce28831e0508763230121275.html
            https://www.cnblogs.com/Penglimei/p/9750390.html
'''
import pygame
import sys
import numpy as np
import math

# 长方体的八个点(x, y ,z, 1)，其他点数的立体图形需要修改draw的参数
points = [[0, 0, 200, 1], [200, 0, 200, 1], [200, 0, 0, 1], [0, 0, 0, 1],
          [0, 200, 200, 1], [200, 200, 200, 1], [200, 200, 0, 1],
          [0, 200, 0, 1]]

onepoint = []  # 一点透视后的二维坐标
twopoint = []  # 两点透视后的二维坐标
threepoint = []  # 三点透视后的二维坐标

# 一点透视参数
L = 100  # 平移位置L, M, N
M = 100
N = 100
D = 300  # 视距
# 两点透视参数
P = 2
R = 3
xita = math.pi / 180 * 65  # 角度xita
Q = 1.5  # 三点透视参数
five = math.pi / 180 * 80  # 角度five，三点透视参数

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
    [[math.cos(xita), 0, 0,
      (P * math.cos(xita) - R * math.sin(xita))], [0, 1, 0, 0],
     [math.sin(xita), 0, 0, (P * math.sin(xita) + R * math.cos(xita))],
     [(L * math.cos(xita) + N * math.sin(xita)), M, 0,
      (P * (L * math.cos(xita) + N * math.sin(xita))) +
      (R * (N * math.cos(xita) + L * math.sin(xita))) + 1]],
    dtype='float32')
# 两点透视降维变换
for e in range(0, len(points)):
    tmp = np.matmul(np.array(points[e], dtype='float32'), twoMatrix)
    tmp = tmp / tmp[3]  # 齐次化
    tmp = tmp * 500  # 非必须：放大，太小看不见
    tmp[0] += 200  # 非必须：整体向右平移，不然和一位透视挡在一起了
    twopoint.append(tmp.tolist()[:2])

# 三点透视变换矩阵
# 平移到LMN
mtranslation = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [L, M, N, 1]], dtype='float32')
# 沿y轴旋转
mrotatey = np.array([[math.cos(xita), 0, -math.sin(xita), 0], [0, 1, 0, 0],
                     [math.sin(xita), 0, math.cos(xita), 0], [0, 0, 0, 1]],
                    dtype='float32')
# 沿x轴旋转
mrotatex = np.array(
    [[1, 0, 0, 0], [0, math.cos(five), math.sin(five), 0],
     [0, -math.sin(five), math.cos(five), 0], [0, 0, 0, 1]],
    dtype='float32')
# 透视
mperspective = np.array(
    [[1, 0, 0, P], [0, 1, 0, Q], [0, 0, 1, R], [0, 0, 0, 1]], dtype='float32')
# 向xoy平面做正投影
mprojectionxy = np.array(
    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], dtype='float32')
threeMatrix = np.matmul(
    np.matmul(np.matmul(np.matmul(mtranslation, mrotatey), mrotatex),
              mperspective), mprojectionxy)

# 三点透视降维变换
for e in range(0, len(points)):
    tmp = np.matmul(np.array(points[e], dtype='float32'), threeMatrix)
    tmp = tmp / tmp[3]  # 齐次化
    tmp = tmp * 800  # 非必须：放大，太小看不见
    tmp[0] += 600  # 非必须：整体向右平移，不然和一点透视挡在一起了
    tmp[1] += 100  # 非必须：整体向下平移，不然和一点透视挡在一起了
    threepoint.append(tmp.tolist()[:2])

LINECOLOR = (29, 244, 255)  # 颜色设置
BACKYCOLOR = (255, 212, 238)
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

    pygame.draw.lines(screen, LINECOLOR, False, threepoint, LINEWIDTH)
    pygame.draw.line(screen, BACKYCOLOR, threepoint[3], threepoint[4],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[0], threepoint[3],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[4], threepoint[7],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[0], threepoint[1],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[0], threepoint[1],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[0], threepoint[4],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[3], threepoint[7],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[2], threepoint[6],
                     LINEWIDTH)
    pygame.draw.line(screen, LINECOLOR, threepoint[1], threepoint[5],
                     LINEWIDTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    pygame.display.update()
