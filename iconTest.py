# -*-encoding: utf-8-*-
"""
检测图标存在屏幕内的范围
2021年1月19日
by littlefean
"""
from PIL import Image


def main():
    iconInPic(Image.open('物体检测/小.png'), Image.open('物体检测/大.png'))
    pass


def iconInPic(icon: Image, pic: Image):
    iWidth, iHeight = icon.width, icon.height
    pWidth, pHeight = pic.width, pic.height
    showImg = pic
    for y in range(pHeight - iHeight):
        print(y)
        for x in range(pWidth - iWidth):
            # 地毯式遍历
            TruePixNum = 0
            for ty in range(iHeight):
                for tx in range(iWidth):
                    if isColorSame(pic.getpixel((x + tx, y + ty)), icon.getpixel((tx, ty)), 30):
                        TruePixNum += 1
            if TruePixNum / (iWidth * iHeight) > 0.9:
                print("发现一个", x, y)
                for putX in range(iWidth):
                    showImg.putpixel((x + putX, y), (0, 255, 0))
                for putY in range(iHeight):
                    showImg.putpixel((x, y + putY), (0, 255, 0))
            # addC = (0, int((TruePixNum / (iWidth * iHeight)) * 255), 0)
            # addPixel(showImg, (x, y), addC)
    showImg.show()
    pass


def addPixel(im: Image, loc: tuple, addColor: tuple):
    """往图片上叠加颜色"""
    c = im.getpixel(loc)
    c = min(c[0] + addColor[0], 255), min(c[1] + addColor[1], 255), min(c[2] + addColor[2], 255)
    im.putpixel(loc, c)


def isColorSame(c1, c2, rgbFault):
    return abs(c1[0] + c1[1] + c1[2] - (c2[0] + c2[1] + c2[2])) < rgbFault


if __name__ == '__main__':
    main()
