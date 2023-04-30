# -*- encoding: utf-8 -*-
"""
自动截取战斗中的卡牌图片
2021年2月2日
by littlefean
"""
from PIL import Image
from PIL import ImageGrab
import keyboard
import time
from winsound import Beep

# x y w h
p1 = (762, 904, 762 + 96, 904 + 120)
p2 = (872, 904, 872 + 96, 904 + 120)
p3 = (982, 904, 982 + 96, 904 + 120)
p4 = (1092, 904, 1092 + 96, 904 + 120)


def main():
    while True:
        keyboard.wait('q')
        grabCard()
    pass


def grabCard():
    im = ImageGrab.grab()
    im.crop(p1).save(f"D:\\桌面\\out\\{time.time()}.png")
    time.sleep(0.1)
    im.crop(p2).save(f"D:\\桌面\\out\\{time.time()}.png")
    time.sleep(0.1)
    im.crop(p3).save(f"D:\\桌面\\out\\{time.time()}.png")
    time.sleep(0.1)
    im.crop(p4).save(f"D:\\桌面\\out\\{time.time()}.png")
    Beep(1000, 500)


if __name__ == '__main__':
    main()
