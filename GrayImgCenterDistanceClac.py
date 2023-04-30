# -*- encoding: utf-8 -*-
"""
图片中心距和不变矩的计算
2021年1月10日
by littlefean
"""
import math

from PIL import Image
from math import log
from test import addImgArr
from test import imToName
import numpy as np
import matplotlib.pyplot as plt


def testMain():
    x = np.linspace(-1, 1, 50)  # 用到了numpy库，创建50个点
    y1 = x ** 2
    y2 = 2 * x + 1

    plt.figure()  # 有多个窗口的时候，要在每个plot前面加上figure()
    plt.plot(x, y1)

    plt.figure(num=3, figsize=(8, 5))  # 参数num决定窗口的顺序，参数figsize决定窗口大小
    plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--')  # 红线，虚线，线粗1.0
    plt.show()


def main():

    plt.xlabel('n level')
    plt.ylabel('value')
    # ---------

    imgList1 = addImgArr('卡牌识别\\单个卡牌图')
    imgList2 = addImgArr('不变矩\\旋转后')

    for i in range(len(imgList1)):
        ys = test(imgList1[i])
        xs = [j for j in range(7)]
        plt.plot(xs, ys, linewidth=1)
    # plt.show()

    print("-" * 20)
    plt.show()
    pass


def test(im):
    """传入一个图片，以列表的形式返回这个图片的 7 个不变矩"""
    img2D = []
    for y in range(im.height):
        line = []
        for x in range(im.width):
            c = im.getpixel((x, y))
            line.append((c[0] + c[1] + c[2]) / 3)
        img2D.append(line)

    def imToM(pNumber, qNumber):
        """返回图像的p+q阶矩 未归一化"""
        m = 0
        for _y in range(im.height):
            for _x in range(im.width):
                m += _x ** pNumber * _y ** qNumber * img2D[_y][_x]
        return m

    m10 = imToM(1, 0)
    m01 = imToM(0, 1)
    m00 = imToM(0, 0)

    def imToU(pNum, qNum):
        """返回归一化的p+q阶矩"""
        u = 0
        x_ = m10 / m00
        y_ = m01 / m00
        for _y in range(im.height):
            for _x in range(im.width):
                u += (_x - x_) ** pNum * (_y - y_) ** qNum * img2D[_y][_x]
        return u

    u00 = imToU(0, 0)

    def n(p, q):
        """返回n值"""
        return imToU(p, q) / u00 ** ((p + q) / 2 + 1)

    n20 = n(2, 0)
    n02 = n(0, 2)
    n11 = n(1, 1)
    n30 = n(3, 0)
    n12 = n(1, 2)
    n21 = n(2, 1)
    n03 = n(0, 3)
    faiArr = [
        n20 + n02,
        (n20 - n02) ** 2 + 4 * n11 ** 2,
        (n30 - 3 * n12) ** 2 + (3 * n21 - n03) ** 2,
        (n30 + n12) ** 2 + (n21 + n03) ** 2,
        (n30 - 3 * n12) * (n30 + n12) * ((n30 + n12) ** 2 - 3 * (n21 + n03) ** 2)
        + (3 * n21 - n03) * (n21 + n03) * (3 * (n30 + n12) ** 2 - (n21 + n03) ** 2),
        (n20 - n02) * ((n30 + n12) ** 2 - (n21 + n03) ** 2) + 4 * n11 * (n30 + n12) * (n21 + n03),
        (3 * n21 - n03) * (n30 + n12) * ((n30 + n12) ** 2 - 3 * (n21 + n03) ** 2)
        + (3 * n12 - n30) * (n21 + n03) * (3 * (n30 + n12) ** 2 - (n21 + n03) ** 2)
    ]

    # return faiArr
    arr = []
    print(faiArr)
    for i in faiArr:
        arr.append(round(log(abs(i)), 4))
        # arr.append(round(i, 4))
    print(arr)
    return arr


if __name__ == '__main__':
    main()
    # testMain()
