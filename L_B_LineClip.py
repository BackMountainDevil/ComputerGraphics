#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   L_B_LineClip.py
@Time    :   2020/11/26 14:29:16
@Author  :   Kearney
@Version :   0.0
@Contact :   191615342@qq.com
@License :   GPL 3.0
@Desc    :   Liang-Barskey算法的 python3-pygame实现
             1、画矩形确定显示区域
             2、点出两点自动画线
             然后自动识别在框内的线，然后自动裁剪只显示区域内的线段。
             鼠标右键可清除线
'''
import pygame
import sys
import time

width = 920  # 画板宽度
height = 640  # 画版高度
delaytime = 0.3  # 线条切割间隔时间，可以设置为0，单位s

# 颜色配置
CBAG = (245, 245, 220)  # 背景色
CFOL = (54, 190, 179)  # 显示区域框线颜色
CLINE = (0, 0, 0)  # 线段颜色
CFIL = (0, 255, 0)  # 区内线段颜色

XL = XR = YB = YT = -1
x1 = y1 = x2 = y2 = -1
polygon = []  # 每一条线段的坐标
iswin = False  # 显示区域是否确定
isadd = False  # LB算法是否执行

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Liang-Barskey_LineClip_Kearney")
screen.fill(CBAG)


def clipTest(p, q, u1, u2):
    retVal = True
    if (p < 0):
        r = q / p
        if (r > u2):
            retVal = False
        elif (r > u1):
            u1 = r
    elif (p > 0):
        r = q / p
        if (r < u1):
            retVal = False
        elif (r < u2):
            u2 = r
    elif q < 0:
        retVal = False
    return (u1, u2, retVal)


# 对在显示区域外的部分线段进行裁剪
def L_B_LineClip(x1, y1, x2, y2, XL, XR, YB, YT):
    # print('(', x1, ',', y1, ')', '  (', x2, ',', y2, ')')
    u1 = 0
    u2 = 1
    dx = x2 - x1
    dy = y2 - y1
    (u1, u2, bool) = clipTest(-dx, x1 - XL, u1, u2)  # 计算左边界交点参数，更新u
    if bool:
        (u1, u2, bool) = clipTest(dx, XR - x1, u1, u2)  # 计算右边界交点参数，更新u
        if bool:
            (u1, u2, bool) = clipTest(-dy, y1 - YB, u1, u2)  # 计算下边界交点参数，更新u
            if bool:
                (u1, u2, bool) = clipTest(dy, YT - y1, u1, u2)  # 计算上边界交点参数，更新u
                if bool:
                    if u2 < 1:  # 计算终点坐标
                        x2 = (int)(x1 + u2 * dx)
                        y2 = (int)(y1 + u2 * dy)
                    if u1 > 0:  # 计算起点坐标
                        x1 = (int)(x1 + u1 * dx)
                        y1 = (int)(y1 + u1 * dy)
                    return (x1, y1, x2, y2)
                else:
                    return (-1, -1, -1, -1)
            else:
                return (-1, -1, -1, -1)
        else:
            return (-1, -1, -1, -1)
    else:  # -1用来避免TypeError：cannot unpack non-iterable NoneType object
        return (-1, -1, -1, -1)


if __name__ == '__main__':
    while True:
        if isadd:  # 重新绘制显示框和保留线条
            isadd = False
            time.sleep(delaytime)
            screen.fill(CBAG)
            if XL > 0:  # 保留显示区域
                pygame.draw.rect(screen, CFOL, [XL, YB, XR - XL, YT - YB], 1)
            length = len(polygon)
            for i in range(length):
                pygame.draw.line(screen, CFIL, (polygon[i][0], polygon[i][1]),
                                 (polygon[i][2], polygon[i][3]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x1 < 0:
                    x1, y1 = event.pos
                else:
                    x2, y2 = event.pos
                pygame.draw.circle(screen, CLINE, event.pos, 1, 1)
                if iswin and x2 > 0:  # 显示区域完成后
                    pygame.draw.line(screen, CLINE, (x1, y1), (x2, y2))
                    (x1, y1, x2, y2) = L_B_LineClip(x1, y1, x2, y2, XL, XR, YB,
                                                    YT)
                    if x1 > 0:
                        pygame.display.update()
                        time.sleep(delaytime)
                        print('(', x1, ',', y1, ')', '  (', x2, ',', y2, ')')
                        pygame.draw.line(screen, CFIL, (x1, y1), (x2, y2))
                        polygon.append([x1, y1, x2, y2])
                        x1 = y1 = x2 = y2 = -1
                    else:
                        print("在显示区域之外")
                    isadd = True
                if (pygame.mouse.get_pressed()[2]):  # 鼠标右键按下，清除线条
                    polygon.clear()
                    isadd = False
                    x1 = y1 = x2 = y2 = -1
                    screen.fill(CBAG)
                    if XL > 0:  # 保留显示区域
                        pygame.draw.rect(screen, CFOL,
                                         [XL, YB, XR - XL, YT - YB], 1)
                    print("Reset Line done")
            elif event.type == pygame.MOUSEMOTION:  # 设置显示区域
                x, y = pygame.mouse.get_pos()
                if not iswin:
                    if x1 > 0 and x2 < 0:
                        screen.fill(CBAG)
                        pygame.draw.rect(screen, CFOL,
                                         [x1, y1, x - x1, y - y1], 1)
                    elif x1 > 0 and x2 > 0:
                        if (x2 > x1 and y2 > y1):
                            XL = x1
                            XR = x2
                            YB = y1
                            YT = y2
                            screen.fill(CBAG)
                            pygame.draw.rect(screen, CFOL,
                                             [XL, YB, XR - XL, YT - YB], 1)
                            x1 = y1 = x2 = y2 = -1  # 重置坐标，开始划线
                            iswin = True
                        else:
                            print("无效操作！！！请重新画框")
                            screen.fill(CBAG)
                            x1 = y1 = x2 = y2 = -1  # 重置坐标，开始划线
        pygame.display.update()
