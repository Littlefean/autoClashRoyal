# -*- encoding: utf-8 -*-
"""
自动操作库的集成包--屏幕检测包
2020年10月29日
by littlefean
"""
from PIL import ImageGrab

"""
检测屏幕某一范围内是否全是某一个颜色
获取屏幕内某一范围内的颜色平均值
根据颜色来获取h值
"""


def main():
    # print(isColorBlockInScr(Rectangle((300, 20), 100, 100), (12, 13), (255, 0, 0, 255)))
    pass


class Rectangle:
    """定义矩形类，用来表示屏幕内的一片区域"""

    def __init__(self, loc, width, height):
        """
        矩形类的构造方法
        :param loc: tuple，左上角顶点的位置
        :param width: int，矩形的宽度
        :param height: int，矩形的高度
        """
        self.x1 = loc[0]
        self.y1 = loc[1]
        self.x2 = self.x1 + width - 1
        self.y2 = self.y1 + height - 1
        self.leftTop = (self.x1, self.y1)
        self.rightTop = (self.x2, self.y1)
        self.rightBottom = (self.x2, self.y2)
        self.leftBottom = (self.x1, self.y2)


def getScreen():
    """
    获取屏幕全屏截图
    此函数运行后将截屏一次并返回截屏后的图片
    :return: 图片
    """
    return ImageGrab.grab()


def isColorInScr(rectangle: Rectangle, color):
    """
    输入一个矩形对象 rectangle，判断屏幕内rectangle矩形范围内是否含有颜色 color
    :param rectangle: Rectangle类对象，矩形
    :param color: tuple，是否含有的颜色
    :return: bool，屏幕某一范围内是否含有一个颜色
    """
    x1, x2, y1, y2 = rectangle.x1, rectangle.x2, rectangle.y1, rectangle.y2
    img = getScreen()
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if img.load()[x, y] == color:
                return True
    return False


def isColorHRangeInScr(rectangle: Rectangle, HRange):
    """
    输入一个矩形对象，检测屏幕内矩形范围内是否含有H值范围的颜色
    :param rectangle: 矩形对象
    :param HRange: 元组或列表，比如(192, 200)
    :return: 是否含有
    """
    x1, x2, y1, y2 = rectangle.x1, rectangle.x2, rectangle.y1, rectangle.y2
    img = getScreen()
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if toH(img.load()[x, y]) in range(HRange[0], HRange[1]):
                return True
    return False


def isColorAllScr(rectangle: Rectangle, color):
    """
    检测屏幕某一范围内是否都是同一个颜色
    :param rectangle: 矩形
    :param color: 是否是这个颜色
    :return: 是否
    """
    x1, x2, y1, y2 = rectangle.x1, rectangle.x2, rectangle.y1, rectangle.y2
    img = getScreen()
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            if img.load()[x, y] != color:
                return False
    return True


def isColorBlockInScr(scrRectangle: Rectangle, colorBlock, color):
    """
    检测屏幕某一范围内是否含有一个一定大小的矩形纯色块
    :param scrRectangle: 屏幕矩形区域
    :param colorBlock: 纯色块矩形的宽和高，例如(15, 4)，注意：先宽后高！
    :param color: 颜色
    """
    img = getScreen()
    for y in range(scrRectangle.y1, scrRectangle.y2 + 1):
        for x in range(scrRectangle.x1, scrRectangle.x2 + 1):
            if img.load()[x, y] == color:
                num = 0  # 表示正确颜色像素的数量
                for yy in range(y, y + colorBlock[1] + 1):
                    for xx in range(x, x + colorBlock[0] + 1):
                        if img.load()[xx, yy] == color:
                            num += 1
                if num >= colorBlock[0] * colorBlock[1]:
                    return True
    return False


def isColorHsBlockInScr(scrRectangle: Rectangle, colorBlock, h, miss):
    """
    检测屏幕某一范围内是否含有一个一定大小的矩形H值颜色的色块，按H值判断
    :param scrRectangle: 屏幕矩形区域
    :param colorBlock: 纯色块矩形的宽和高，例如(15, 4)，注意：先宽后高！
    :param h: 颜色h值
    :param miss: 颜色差值
    """
    img = getScreen()
    for y in range(scrRectangle.y1, scrRectangle.y2 + 1):
        for x in range(scrRectangle.x1, scrRectangle.x2 + 1):
            if toH(img.load()[x, y]) in range(h - miss, h + miss):
                num = 0  # 表示正确颜色像素的数量
                for yy in range(y, y + colorBlock[1] + 1):
                    for xx in range(x, x + colorBlock[0] + 1):
                        if toH(img.load()[x, y]) in range(h - miss, h + miss):
                            num += 1
                if num >= colorBlock[0] * colorBlock[1]:
                    return True
    return False


def getColorByPixel(loc):
    """
    获取屏幕上某一点的像素颜色
    :param loc: 屏幕上的位置 (x, y)元组
    :return: 颜色值 (r, g, b)
    """
    # todo 能够检测参数的数量，如果是两个参数，那么就是一个是x一个是y
    im = ImageGrab.grab()
    color = im.getpixel(loc)
    return color


def getColorByAverage(rectangle: Rectangle):
    """
    获取屏幕上某一片区域内像素的平均值
    :param rectangle: 矩形
    :return: (r, g, b)
    """
    x1, x2, y1, y2 = rectangle.x1, rectangle.x2, rectangle.y1, rectangle.y2
    im = ImageGrab.grab()
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    color_list = []
    for i in range(height):
        for j in range(width):
            color_list.append(im.load()[x1 + j, y1 + i])
    r_sum, g_sum, b_sum = 0, 0, 0
    for i in range(len(color_list)):
        r_sum += color_list[i][0]
        g_sum += color_list[i][1]
        b_sum += color_list[i][2]
    r = int(r_sum / len(color_list))
    g = int(g_sum / len(color_list))
    b = int(b_sum / len(color_list))
    color = (r, g, b)
    return color


def isColorSimilar(color1, color2, d):
    """
    判断两个颜色是否接近，按照 r ± d, g ± d, b ± d
    :param color1: 颜色1
    :param color2: 颜色2
    :param d: 差值
    :return: 是否接近
    """
    r_is_similar = (color1[0] in range(color2[0] - d, color2[0] + d))
    g_is_similar = (color1[1] in range(color2[1] - d, color2[1] + d))
    b_is_similar = (color1[2] in range(color2[2] - d, color2[2] + d))
    if r_is_similar and g_is_similar and b_is_similar:
        return True
    else:
        return False


def isColorHSimilar(color1, color2, dh):
    """
    判断两个颜色的H值是否接近
    :param color1:
    :param color2:
    :param dh: H 的允许差值
    :return: 是否接近
    """
    return dh >= abs(toH(color1) - toH(color2))


def toH(color):
    """
    获取rgb的H值
    :param color: 颜色
    :return: 0~360
    """
    r, g, b = color[0], color[1], color[2]
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h = 0
    mx = max(r, g, b)
    mn = min(r, g, b)
    m = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        if g >= b:
            h = ((g - b) / m) * 60
        else:
            h = ((g - b) / m) * 60 + 360
    elif mx == g:
        h = ((b - r) / m) * 60 + 120
    elif mx == b:
        h = ((r - g) / m) * 60 + 240
    return h


def hToRGB(h):
    """
    输入一个 h 值，转化成一个纯饱和度的图片
    :param h: 颜色的h值
    :return: rgb颜色
    """

    pass


if __name__ == '__main__':
    main()
