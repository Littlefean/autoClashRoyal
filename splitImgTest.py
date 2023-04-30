# -*- encoding: utf-8 -*-
"""
分割图片求平均值测试
2021年1月20日
by littlefean
"""
from PIL import Image
from test import addImgArr
import matplotlib.pyplot as plt


def main():
    plt.rc("font", family='MicroSoft YaHei', weight="bold")
    N = 10
    plt.title(f"将卡牌分成{N ** 2}份，每份切图的平均值")
    plt.xlabel('卡牌的第x块')
    plt.ylabel('该块的平均值')
    cardList = addImgArr('卡牌识别\\单个卡牌图')
    # for card in cardList:
    #     c4 = split4(card)
    #     cn4 = []
    #     for c in c4:
    #         cn4.append(rgbToNum(c))
    #     print(cn4)
    #     plt.plot([x for x in range(4)], cn4, linewidth=0.5)
    for card in cardList:
        plt.plot([x for x in range(N**2)], splitN(card, N), linewidth=0.5)
    plt.show()
    pass


def rgbToNum(color):
    """将rgb色彩转化为一个255进制大数"""
    return color[0] * 255 ** 2 + color[1] * 255 + color[2]


def rgbRange(img: Image):
    """计算一张图片的rgb颜色平均值"""
    r, g, b = 0, 0, 0
    pixNum = img.height * img.width
    for y in range(img.height):
        for x in range(img.width):
            c = img.getpixel((x, y))
            r += c[0]
            g += c[1]
            b += c[2]
    return r / pixNum, g / pixNum, b / pixNum


def splitN(im: Image, n):
    """将图片沿着边长均等切割成n份，总共会有 n**2 份，返回每一份的rgb平均值"""
    xL = int(im.width / n)  # 每一段x的长度
    yL = int(im.height / n)  # 每一段y的长度
    eve = []
    for y in range(n):
        for x in range(n):
            eve.append(rgbToNum(rgbRange(im.crop((x * xL, y * yL, x * xL + xL, y * yL + yL)))))
    return eve


def split4(im: Image):
    """对传入图片进行四等分，分别求每一部分的颜色平均值"""
    centerX, centerY = int(im.width / 2), int(im.height / 2)
    leftTop = im.crop((0, 0, centerX, centerY))
    rightTop = im.crop((centerX, 0, im.width, centerY))
    leftBottom = im.crop((0, centerY, centerX, im.height))
    rightBottom = im.crop((centerX, centerY, im.width, im.height))

    return [rgbRange(leftTop), rgbRange(rightTop), rgbRange(leftBottom), rgbRange(rightBottom)]


if __name__ == '__main__':
    main()
