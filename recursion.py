# -*- encoding: utf-8 -*-
"""
十字递归切割图片
2021年1月20日
by littlefean
"""
from PIL import Image
from PIL import ImageDraw
from math import floor, ceil


class React:
    """矩形类"""
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.sum = width * height

    def __str__(self):
        return f"<{self.left} {self.top} {self.width} {self.height}>"

    __repr__ = __str__


def main():
    # cardList = addImgArr('卡牌识别\\单个卡牌图')
    # level = int(30)
    # for im in cardList:
    #     split4(im, level).save(f'十字压缩\\{level}\\{imToName(im)}.png')
    im = Image.open('卡牌识别\\单个卡牌图\\冰雪精灵.png')
    im = Image.open(r'D:\理刃科技\图片\littlefean头像\贤哥.jpg')
    split4(im, 20).save("D:\\桌面\\20.png")
    pass


def split4(im: Image, default):
    """传入一个图片和一个容错参数，返回该图片的边缘图"""
    finalImg = Image.new('RGB', (im.width, im.height), (0, 0, 0))
    draw = ImageDraw.Draw(finalImg)
    # 准备好绘制图片
    cX, cY = int(im.width / 2), int(im.height / 2)
    width = int(im.width / 2)
    height = int(im.height / 2)
    # 把整个图片切成四份
    lt = React(0, 0, width, height)
    rt = React(cX, 0, width, height)
    ld = React(0, cY, width, height)
    rd = React(cX, cY, width, height)
    reactArr = [lt, rt, ld, rd]

    # 遍历四份矩形 递归
    deepth = 0

    def deep(reacts, dth):
        for react in reacts:
            eveC = eveColor(im, react)  # 计算此份的颜色平均值
            # 处理 12 13 情况
            if not isColorSameInReact(im, react, eveC, default) and not (react.width == 1 or react.height == 1):
                # 继续把这个矩形分成四份
                sonReacts = rect4(react)
                dth += 1
                deep(sonReacts, dth)

            else:
                # 填充左上角的点和右下角的点
                gray = min(255, int(dth**2))
                # finalImg.putpixel((react.left, react.top), (gray, gray, gray))
                # finalImg.putpixel(
                #     (react.left + react.width - 1, react.top + react.height - 1),
                #     (gray, gray, gray)
                # )
                finalImg.putpixel(
                    (int((react.left * 2 + react.width) / 2), int((react.top * 2 + react.height) / 2)),
                    (0, gray, 0)
                )
                # 在这个矩形范围内填充平均值
                # draw.rectangle(
                #     xy=(react.left, react.top, react.left + width, react.top + height),
                #     fill=(gray, gray, gray),
                #     # outline=(dth, dth * 10, dth)
                # )

    deep(reactArr, deepth)
    return finalImg


def rect4(rect: React):
    """把一个矩形分成四份并返回的方法"""
    if rect.width % 2 == 0:
        widthL = widthR = int(rect.width / 2)
    else:
        widthL, widthR = ceil(rect.width / 2), floor(rect.width / 2)
    if rect.height % 2 == 0:
        heightT = heightB = int(rect.height / 2)
    else:
        heightT, heightB = ceil(rect.height / 2), floor(rect.height / 2)
    return [
        React(rect.left, rect.top, widthL, heightT),
        React(rect.left + widthL, rect.top, widthR, heightT),
        React(rect.left, rect.top + heightT, widthL, heightB),
        React(rect.left + widthL, rect.top + heightT, widthR, heightB)
    ]


def isColorSameInReact(im: Image, react: React, eveC, Fault):
    """传入一个图片，一个平均值，一个矩形区域，判断该矩形区域里的所有像素点是否符合要求"""
    for y in range(react.top, react.top + react.height):
        for x in range(react.left, react.left + react.width):
            if not isColorSame(im.getpixel((x, y)), eveC, Fault):
                return False
    return True


def eveColor(im: Image, rec: React):
    """计算一个图片中一个矩形区域内颜色的平均值，返回该平均值颜色"""
    rSum, gSum, bSum = 0, 0, 0
    for y in range(rec.top, rec.top + rec.height):
        for x in range(rec.left, rec.left + rec.width):
            c = im.getpixel((x, y))
            rSum += c[0]
            gSum += c[1]
            bSum += c[2]
    return int(rSum / rec.sum), int(gSum / rec.sum), int(bSum / rec.sum)


def isColorSame(c1, c2, rgbFault):
    """返回两个颜色是否接近"""
    return abs(c1[0] + c1[1] + c1[2] - (c2[0] + c2[1] + c2[2])) < rgbFault


if __name__ == '__main__':
    main()
