# -*- encoding: utf-8 -*-
"""
自动玩皇室战争的程序
保证雷电模拟器整个是竖屏的，左侧边缘举例屏幕左侧有629个像素的距离
2020年7月27日
by littlefean
"""
from time import sleep
import time
import win32clipboard
import win32con
import pyautogui
from random import randint
from random import choice
from random import uniform
import VisionUtils

# todo 判断双方比分
COUNT = 0  # 对战场数


def main():
    while True:
        open_box()
        press_match()
        press_pass()
        if uniform(0, 1) < 0.01:
            send_emoj()
            pass
        if is_water_full(7):
            four_cards = get_card(cards)
            # 完全随机放牌
            # put_card(randint(1, 4), randint(769, 1130), randint(509, 821))
            # 矿桶套
            choose_and_put_card(four_cards)
            # 偷塔套
            # put_double_tong(four_cards)
            # 炸塔套
            # put_center(four_cards)
        press_continue()
        sleep(0.75)
    pass


def press_match():
    """点击按钮：开始游戏"""
    # if get_sec_color(752, 699) == (255, 184, 0):    # 正常的按钮
    # if get_sec_color(865, 697) == (255, 187, 0):  # 赏金活动的按钮
    if VisionUtils.isColorSimilar(VisionUtils.getColorByPixel((865, 697)), (255, 187, 0), 10):
        print("检测到开始游戏的按钮，可以点击了")
        pyautogui.click(865, 697)
        print("点击了开始游戏按钮")
    pass


def open_box():
    """解锁主界面的宝箱功能"""
    boxLeftBars = [
        VisionUtils.Rectangle((646, 820), 5, 137),
        VisionUtils.Rectangle((791, 820), 5, 137),
        VisionUtils.Rectangle((938, 820), 5, 137),
        VisionUtils.Rectangle((1081, 820), 5, 137)
    ]
    # 判断是否是主界面
    if VisionUtils.isColorSimilar(VisionUtils.getColorByPixel((865, 697)), (255, 187, 0), 10):
        # 这些位置分别表示每个宝箱方框左侧的一个小细条区域
        # 需要等待金币和奖杯飞出的动画以免干扰屏幕判断
        sleep(5)

        # 先判断是否有解锁好了的宝箱，它是闪着金色的
        for i in range(len(boxLeftBars)):
            if VisionUtils.isColorHRangeInScr(boxLeftBars[i], (30, 60)):
                # 开始解锁这个宝箱
                pyautogui.click(697 + i * 140, 889)
                sleep(5)
                while True:
                    if VisionUtils.isColorSimilar(VisionUtils.getColorByPixel((865, 697)), (255, 187, 0), 10):
                        break
                    else:
                        pyautogui.click(697 + i * 140, 889)
                        sleep(1)
                log("解锁了一个宝箱")
                sleep(5)
        # 是主界面，判断是否有宝箱正在解锁
        # 绿色的H值：135~150度内说明有宝箱正在解锁
        for i in range(len(boxLeftBars)):
            if VisionUtils.isColorHRangeInScr(boxLeftBars[i], (135, 150)):
                break
        else:
            # 有可能是有宝箱，但是都没在解锁状态；也有可能全是空的
            # 横着一条线判断是否存在“点击解锁”按钮的浅蓝色，若有则返回数字，判断这个数字的位置来判断解锁的按点
            im = VisionUtils.getScreen()
            position = None
            for x in range(560):
                if VisionUtils.isColorSimilar(im.load()[641 + x, 795], (112, 208, 252), 20):
                    position = 641 + x
                    break
            canUnlockBox = []
            if position is not None:
                if position in range(640, 778):
                    canUnlockBox.append(0)
                elif position in range(779, 923):
                    canUnlockBox.append(1)
                elif position in range(924, 1066):
                    canUnlockBox.append(2)
                elif position in range(1067, 1205):
                    canUnlockBox.append(3)
                # 开始解锁其中一个宝箱
                log(f"开始解锁第{canUnlockBox[0]}个宝箱")
                pyautogui.click(697 + canUnlockBox[0] * 140, 889)
                sleep(1)
                pyautogui.click(977, 726)
                sleep(1)


def is_water_full(over):
    """判断圣水是否n了"""
    if over == 9:
        return VisionUtils.getColorByPixel((1128, 1057)) == (196, 31, 203)
    if over == 7:
        return VisionUtils.isColorSimilar(VisionUtils.getColorByPixel((1053, 1055)), (203, 33, 209), 30)


def press_continue():
    """判断是不是游戏结束了，并按确定"""
    global COUNT
    if VisionUtils.getColorByPixel((968, 962)) == (78, 175, 255):
        print("检测到游戏里出现了结束按钮")
        # todo 检测是胜利还是失败
        pyautogui.click(881, 945)
        print("按了游戏的结束按钮")
        COUNT += 1
        log(f"{time.asctime(time.localtime(time.time()))}打了第{COUNT}场")
        # while True:
        #     if is_similar(rbtEye.getColorByPixel((865, 697)), (255, 187, 0), 10):
        #         # 开始去战队里随机发一个表情
        #         pyautogui.click(1057, 1023)
        #         sleep(3)
        #         # 判断战队界面是不是聊天界面
        #         if not rbtEye.isColorInScr(rbtEye.Rectangle((831, 903), 1, 1), (192, 120, 252)):
        #             sleep(5)
        #             pyautogui.click(1152, 89)
        #             sleep(1)

        #         def sendEmoji():
        #             """发送表情"""
        #             # 按表情打开面板的按钮
        #             sleep(0.5)
        #             pyautogui.click(992, 910)
        #             sleep(1)
        #             # 随机发一个表情
        #             x = 697 + randint(0, 4) * 110
        #             y = 722 + randint(0, 1) * 93
        #             pyautogui.click(x, y)
        #             sleep(1)
        #             # 回到主菜单
        #             pyautogui.click(864, 910)

        #         def sendText():
        #             """发送文字"""

        #             def send_msg_to_clip(type_data, msg):
        #                 """
        #                 操作剪贴板分四步：
        #                 1. 打开剪贴板：OpenClipboard()
        #                 2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
        #                 3. 往剪贴板写入数据：SetClipboardData()
        #                 4. 关闭剪贴板：CloseClipboard()

        #                 :param type_data: 数据的格式，
        #                 unicode字符通常是传 win32con.CF_UNICODETEXT
        #                 :param msg: 要写入剪贴板的数据
        #                 """
        #                 win32clipboard.OpenClipboard()
        #                 win32clipboard.EmptyClipboard()
        #                 win32clipboard.SetClipboardData(type_data, msg)
        #                 win32clipboard.CloseClipboard()

        #             # 随机输入一句话
        #             sleep(1)
        #             pyautogui.click(1127, 910)
        #             sleep(5)
        #             arr = open("皇室战争随机发送语句.txt").readlines()
        #             content = choice(arr)
        #             send_msg_to_clip(win32con.CF_UNICODETEXT, content)
        #             sleep(0.5)
        #             pyautogui.hotkey("ctrl", 'v')
        #             sleep(0.5)
        #             pyautogui.hotkey('enter')
        #             sleep(1)

        #         # sendText()
        #         sleep(1)
        #         # 回到主菜单
        #         pyautogui.click(864, 910)
        #         break
        #     else:
        #         pass
        return True
    else:
        return False


def get_card(cardsArray):
    """获取当前游戏的卡牌，并返回一个Card类型 列表"""
    c1 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((766, 907), 90, 86))
    c2 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((876, 907), 90, 86))
    c3 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((986, 907), 90, 86))
    c4 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((1096, 907), 90, 86))
    print(f"颜色提取：第一张牌{c1}，第二张牌{c2}，第三章牌{c3}，第四章牌{c4}")

    cardArray = []
    bo = False
    for i in cardsArray:
        # 遍历卡牌库数组
        if VisionUtils.isColorSimilar(c1, i.color, 2):
            cardArray.append(i)
            # print(f"第一张卡牌添加了：{i.name}")
            bo = True
            break
    if not bo:
        print("第一张卡牌没能成功添加")
        cardArray.append(error)
    bo = False
    for i in cardsArray:
        # 遍历卡牌库数组
        if VisionUtils.isColorSimilar(c2, i.color, 2):
            cardArray.append(i)
            # print(f"第二张卡牌添加了：{i.name}")
            bo = True
            break
    if not bo:
        print("第2张卡牌没能成功添加")
        cardArray.append(error)

    bo = False
    for i in cardsArray:
        # 遍历卡牌库数组
        if VisionUtils.isColorSimilar(c3, i.color, 2):
            cardArray.append(i)
            # print(f"第三张卡牌添加了：{i.name}")
            bo = True
            break
    if not bo:
        print("第3张卡牌没能成功添加")
        cardArray.append(error)
    bo = False
    for i in cardsArray:
        # 遍历卡牌库数组
        if VisionUtils.isColorSimilar(c4, i.color, 2):
            cardArray.append(i)
            # print(f"第四张卡牌添加了：{i.name}")
            bo = True
            break
    if not bo:
        print("第4张卡牌没能成功添加")
        cardArray.append(error)
    print(f"{cardArray[0].name} | {cardArray[1].name} | {cardArray[2].name} | {cardArray[3].name}")
    return cardArray


def put_card(c, x, y):
    """将第 card_id 张卡牌放到屏幕上的 x, y位置"""
    card_1_x, card_1_y = 811, 957
    card_2_x, card_2_y = 924, 961
    card_3_x, card_3_y = 1038, 959
    card_4_x, card_4_y = 1118, 968
    if c == 1:
        pyautogui.click(card_1_x, card_1_y)
    elif c == 2:
        pyautogui.click(card_2_x, card_2_y)
    elif c == 3:
        pyautogui.click(card_3_x, card_3_y)
    else:
        pyautogui.click(card_4_x, card_4_y)
    pyautogui.click(x, y)


def get_score():
    """获取当前打掉了对方几个塔，返回0，1，2"""

    # 如果零中间的圈圈里全是黑色(<70)的，那么就是零
    def is_dark(color):
        if color[0] < 80 and color[1] < 90 and color[2] < 90:
            return True
        else:
            return False

    # color0 = get_average_color(1183, 578, 1183+3-1, 578+7-1)
    color0 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((1183, 578), 3, 7))
    # 0
    if is_dark(color0):
        print("0塔打掉")
        return 0
    else:
        # color1 = get_average_color(1190, 567, 1190+3-1, 567+28-1)
        color1 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((1190, 567), 3, 28))
        # 1
        if is_dark(color1):
            print("现在打掉了对方两个塔")
            return 1
        else:
            # 2
            # color2 = get_average_color(1176, 582, 1176+2-1, 582+10-1)
            color2 = VisionUtils.getColorByAverage(VisionUtils.Rectangle((1176, 582), 2, 10))
            if is_dark(color2):
                return 0
            else:
                print("现在打掉了对放三个塔")
                return 2


def choose_and_put_card(cardList):
    """将四槽卡牌列表里的卡牌，打出去"""

    def rand_put_card():
        pcd = randint(0, 3)
        pp = choice(cardList[pcd].put_array)
        px = pp[0]
        py = pp[1]
        # print(f"{cardList[pcd].name}被放了出去~~~~~~~~~~")
        put_card(pcd + 1, px, py)

    indexTong = 1
    indexKuang = 1
    for i in range(len(cardList)):
        if cardList[i].name == "飞桶":
            indexTong = i + 1
        elif cardList[i].name == "矿工":
            indexKuang = i + 1
    if (feiTong in cardList) and (kuangGong in cardList):
        """飞桶和矿工同时在手牌中"""
        if get_score() == 0:
            # 右飞桶，左矿工
            if randint(0, 1) == 1:
                # 先扔桶
                put_card(indexTong, throw_position[1][0], throw_position[1][1])
                # 隔一段时间
                sleep(0.2)
                # 在下矿
                put_card(indexKuang, 816, 259)
            # 同时右边
            else:
                # 先扔桶
                put_card(indexTong, throw_position[1][0], throw_position[1][1])
                # 隔一段时间
                sleep(0.2)
                # 在下矿
                p = choice(kw_position_r)
                put_card(indexKuang, p[0], p[1])
        elif get_score() == 1:
            # 先扔桶
            put_card(indexTong, throw_position[0][0], throw_position[0][1])
            # 隔一段时间
            sleep(0.2)
            # 在下矿
            p = choice(kw_position_l)
            put_card(indexKuang, p[0], p[1])
        else:
            # 先扔桶
            put_card(indexTong, 923 + randint(-10, 10), 181 + randint(-10, 10))
            # 隔一段时间
            sleep(0.2)
            # 在下矿
            put_card(indexKuang, 923 + randint(-10, 10), 181 + randint(-10, 10))
        return
    elif feiTong in cardList:
        if uniform(0, 1) < 0.35:
            for i in range(len(cardList)):
                if cardList[i].name == "飞桶":
                    # 判定右塔在的条件
                    if get_score() == 0:
                        # 右塔在
                        put_card(i + 1, 1070 + randint(-10, 10), 261 + randint(-10, 10))
                    # 判定右塔不在的条件
                    elif get_score() == 1:
                        # 右塔不在，左塔在
                        put_card(i + 1, 768 + randint(-10, 10), 269 + randint(-10, 10))
                    else:
                        # 直接去打主塔
                        put_card(i + 1, 923 + randint(-10, 10), 181 + randint(-10, 10))
                    print(f"飞桶优先扔出！，{cardList[i].name}")
                    break
        else:
            rand_put_card()
        # 没有飞桶
    elif kuangGong in cardList:
        if uniform(0, 1) < 0.35:
            for i in range(len(cardList)):
                if cardList[i].name == "矿工":
                    if get_score() == 0:
                        # 右塔在
                        p = choice(kw_position_r)
                        put_card(i + 1, p[0], p[1])
                    elif get_score() == 1:
                        # 右塔不在，左塔在
                        p = choice(kw_position_l)
                        put_card(i + 1, p[0], p[1])
                    else:
                        # 直接去打主塔
                        put_card(i + 1, 923 + randint(-10, 10), 181 + randint(-10, 10))
                    print(f"人群当中钻出了一个光头！，{cardList[i].name}")
                    break
        else:
            rand_put_card()
    else:
        rand_put_card()


def put_center():
    """直接塔"""
    x = 1122 + randint(-10, 10)
    y = 259 + randint(-10, 10)
    if get_score() == 0:
        put_card(randint(1, 4), x, y)
    elif get_score() == 1:
        x = 714 + randint(-10, 10)
        y = 259 + randint(-10, 10)
        put_card(randint(1, 4), x, y)
    else:
        put_card(randint(1, 4), 923 + randint(-10, 10), 181 + randint(-10, 10))
    pass


def put_double_tong(cardList):
    """镜子桶直接偷主塔的策略"""
    # 判定手牌是不是都是 飞桶，镜子，克隆，冰冻
    indexTong = -1
    indexKeLong = -1
    indexBingDong = -1
    for i in range(len(cardList)):
        if cardList[i].name == "飞桶":
            indexTong = i + 1
        elif cardList[i].name == "克隆":
            indexKeLong = i + 1
        elif cardList[i].name == "冰冻":
            indexBingDong = i + 1

    def isAllReady():
        return (feiTong in cardList) and (keLong in cardList) and (bingDong in cardList)

    if isAllReady():
        put_card(indexTong, 923 + randint(-10, 10), 181 + randint(-10, 10))
        # put_card(indexTong, 923+randint(-10, 10), 181+randint(-10, 10))  # 镜子
        sleep(2.5)
        put_card(indexBingDong, 923 + randint(-10, 10), 181 + randint(-10, 10))  # 冰冻
        put_card(indexKeLong, 923 + randint(-10, 10), 181 + randint(-10, 10))  # 克隆
        pass
    else:
        def indexDel(num, array):
            """删除列表中的某一个数"""
            for n in range(len(array) - 1):
                if array[n] == num:
                    array.pop(n)
                break

        indexArray = [1, 2, 3, 4]
        i = 0
        while i < len(indexArray):
            if len(indexArray) != 0:
                if i == indexKeLong:
                    indexDel(indexKeLong, indexArray)
                if i == indexBingDong:
                    indexDel(indexBingDong, indexArray)
                if i == indexTong:
                    indexDel(indexTong, indexArray)
            i += 1
        pcd = choice(indexArray)
        pp = choice(cardList[pcd].put_array)
        px = pp[0]
        py = pp[1]
        print(f"{cardList[pcd].name}被放了出去~~~~~~~~~~")
        put_card(pcd + 1, px, py)
    pass


def send_emoj():
    """发送表情"""
    if VisionUtils.getColorByPixel((676, 892)) == (255, 255, 255):
        pyautogui.click(676, 892)
        # pyautogui.click(993, 730)  # 发哭表情
        pyautogui.click(779 + randint(0, 3) * 100, 729 + randint(0, 1) * 80)
    pass


def press_pass():
    """
    跳过界面：
        天梯界面
        今日不再有奖励的警告界面
        模拟器的xxx应用已经停止运行
        连接中断重新登陆界面
        天梯最顶端界面
    :return:
    """
    if VisionUtils.getColorByPixel((712, 1031)) == (52, 67, 84):
        if VisionUtils.getColorByPixel((799, 956)) == (97, 97, 199):
            pyautogui.click(911, 1021)
            log(f"{time.asctime(time.localtime(time.time()))}检测到了被跳过的天梯1界面并pass")
    if VisionUtils.isColorSimilar(VisionUtils.getColorByPixel((878, 704)), (78, 175, 255), 30):
        pyautogui.click(878, 704)
    if VisionUtils.isColorAllScr(VisionUtils.Rectangle((675, 561), 413, 51), (238, 238, 238)):
        # xxx应用已经停止运行
        pyautogui.click(1146, 591)
        log(f"{time.asctime(time.localtime(time.time()))}检测到了xxx应用已经停止运行并pass")
    if VisionUtils.isColorAllScr(VisionUtils.Rectangle((780, 492), 396, 132), (66, 66, 66)):
        # 连接中断
        log(f"{time.asctime(time.localtime(time.time()))}检测到了连接中断")
        sleep(5)
        pyautogui.click(693, 600)
    if VisionUtils.isColorAllScr(VisionUtils.Rectangle((753, 567), 427, 57), (66, 66, 66)):
        # 另一台设备连接了
        log(f"{time.asctime(time.localtime(time.time()))}检测到了另外设备连接")
        sleep(5)
        pyautogui.click(693, 600)
    if VisionUtils.getColorByPixel((963, 1027)) == (78, 175, 255):
        if VisionUtils.getColorByPixel((1200, 959)) == (97, 97, 199):
            if VisionUtils.getColorByPixel((787, 958)) == (97, 97, 199):
                # 天梯界面
                log(f"{time.asctime(time.localtime(time.time()))}检测到了天梯2顶端界面并pass")
                pyautogui.click(917, 1029)
    pass


class Card:
    def __init__(self, name, color, put_array):
        """
        卡牌类的构造方法
        :param name: 卡牌名称
        :param color: 卡牌平均颜色值
        :param put_array: 可以在屏幕上放置的位置
        """
        self.name = name
        self.color = color
        self.put_array = put_array


def log(text):
    """
    生成txt文件，文件末尾追加写入一行日志信息
    :param text: 日志信息
    :return: none
    """
    with open("对战日志.txt", mode='a') as f:
        f.write(str(text))
        f.write("\n")


if __name__ == '__main__':
    # 前置位房子
    room_back_position = [(932, 599), (889, 599), (961, 593)]
    # 中层房子位置
    room_center_position = [(889, 663), (961, 663)]
    # 后置位房子位置
    room_inter_position = [(1128, 776), (1018, 776), (821, 776), (710, 776)]
    # 冲锋位置
    dash_position = [(769, 508), (1070, 513)]
    # 丢桶位置
    throw_position = [(786, 259), (1070, 261)]  # left, right
    # 中间位置
    center_position = [(921, 602), (919, 821)]
    # 矿工位置
    kw_position_l = [(765, 304), (712, 280), (796, 197), (819, 284)]  # left
    kw_position_r = [(1071, 305), (1127, 281), (1097, 193), (1019, 236)]  # right

    feiTong = Card("飞桶", (152, 156, 99), throw_position)
    huoYanJingLing = Card("火焰精灵", (193, 136, 93), dash_position + room_inter_position)
    touMaoXiaoWu = Card("哥布林小屋", (150, 131, 107), room_center_position + room_back_position)
    geBuLinDaDui = Card("哥布林大队", (120, 127, 76), center_position)
    zhaDanRen2 = Card("攻城炸弹人", (101, 104, 99), dash_position)
    YeManRenFang = Card("野蛮人房子", (150, 141, 119), room_inter_position + room_center_position)
    jingRui = Card("野蛮人精锐", (115, 109, 98), center_position + dash_position)
    huoLu = Card("烈焰熔炉", (119, 112, 97), room_center_position + room_back_position)
    kuangGong = Card("矿工", (124, 111, 106), kw_position_l + kw_position_r)
    # jingZi = Card("镜子", )
    keLong = Card("克隆", (73, 144, 147), throw_position)
    bingJing = Card("冰晶", (106, 149, 194), throw_position)
    xiaoShan = Card("小闪", (109, 155, 186), throw_position)
    bingDong = Card("冰冻", (167, 212, 226), throw_position)
    zhiYu = Card("治愈", (232, 168, 69), throw_position)
    xiaoKuLou = Card("小骷髅", (119, 138, 140), throw_position)

    # (186, 183, 158)火箭
    # (153, 180, 223)大山
    # 每增加一种卡牌，需要手动添加到下面的列表中
    error = Card("未识别", (0, 0, 0), room_back_position + room_center_position)
    cards = [
        feiTong, huoYanJingLing, touMaoXiaoWu, geBuLinDaDui, zhaDanRen2, YeManRenFang, jingRui, huoLu, kuangGong,
        keLong, bingJing, bingDong, xiaoShan, zhiYu, xiaoKuLou
    ]
    main()
