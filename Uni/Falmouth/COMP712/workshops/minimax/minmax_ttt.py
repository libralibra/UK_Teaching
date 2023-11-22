import tkinter as tk
import random
from turtle import color
import numpy as np
import math
import tkinter.messagebox

# -------------------------------------------------定制棋盘---------------------------------------------------------------
root = tk.Tk()
root.title("少年子律的井字棋")
root.geometry('600x600')
frame = tk.Frame(root)
frame.pack()
paint = tk.Canvas(frame, width=600, height=600, background='white')
paint.pack()
for i in range(4):
    paint.create_line(40 + i * 180, 40, 40 + i * 180, 580)
    paint.create_line(40, 40 + i * 180, 580, 40 + i * 180)


# 游戏开始
def game_start(event):
    global chess_background
    global player
    global chess_blank
    # player为0时机器下棋，player为1时你开始下棋
    if player == 0:
        chess_background, player, chess_blank = AI_play(
            player, chess_background, chess_blank)
        player = 1
    else:
        for i in [0, 1, 2]:
            for j in [0, 1, 2]:
                if 40 + i * 180 < event.x and event.x < 220 + i * 180 and 40 + j * 180 < event.y and event.y < 220 + j * 180:
                    if chess_background[j, i] == 0:
                        chess_background[j, i] = 2
                        chess_blank.pop(getwhere(chess_blank, i + j * 3))
                        player = 0
                    else:
                        player = 1
                        wrong()
    # 每次下完棋更新棋盘UI
    chess(chess_background)
    # 判断是否结束，谁胜谁负
    flag, over = game_over(chess_background)
    # 如果游戏结束，更新棋盘并且提示胜负关系
    if over == 1:
        result(flag)
        if flag == 1:
            print("AI赢了")

        elif flag == 2:
            print("人赢了")

        elif flag == 3:
            print("和棋")
        chess_background[:, :] = 0
        chess_blank = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        chess(chess_background)


# 建立棋局评价函数value = inf*F3（AI）+3*F2（AI）+F1（AI）-inf*F3（人）-3*F2（人）-F1（人）
def value(chess_background):
    score = 0
    chess_reorder = np.zeros([8, 3])
    chess_reorder[0:3, :] = chess_background
    chess_reorder[3:6, :] = np.transpose(chess_background)
    chess_reorder[6, :] = np.array(
        [chess_background[0, 0], chess_background[1, 1], chess_background[2, 2]])
    chess_reorder[7, :] = np.array(
        [chess_background[2, 0], chess_background[1, 1], chess_background[0, 2]])
    for i in range(8):
        if sum(chess_reorder[i, :]) == 1:
            score = score + 1
            score = score + 1
        if np.all(chess_reorder[i, :] == [0, 1, 1]) or np.all(chess_reorder[i, :] == [1, 0, 1]) or np.all(chess_reorder[i, :] == [1, 1, 0]):
            score = score + 3
        if product(chess_reorder[i]) == 1:
            score = np.inf
        if np.all(chess_reorder[i, :] == [0, 0, 2]) or np.all(chess_reorder[i, :] == [0, 2, 0]) or np.all(chess_reorder[i, :] == [2, 0, 0]):
            score = score - 1
        if sum(chess_reorder[i, :]) == 4:
            score = score - 3
        if product(chess_reorder[i]) == 8:
            score = -(np.inf)
    return score


# 利用maxmin对抗搜索来判断下一步AI走棋的位置，为了降低搜索量，搜索深度为2
def AI_play(player, chess_background, chess_blank):
    m = len(chess_blank)
    value_step = np.zeros(9)
    max_value = -(1000)
    max_step = chess_blank[0]
    # 拓展当前节点
    for step in chess_blank:
        value_step[:] = 1000
        background = chess_background.copy()
        blank = chess_blank.copy()
        background[step // 3, step % 3] = 1
        blank.pop(getwhere(blank, step))
        min_value = np.inf
        # 拓展子节点，并计算深度为2的子节点value值
        for k in range(len(blank)):
            temp = background.copy()
            temp[blank[k] // 3, blank[k] % 3] = 2
            value_step[k] = value(temp)
            # 取子节点的后继节点中的最小值
            if min_value > value_step[k] or value_step[k] == -(np.inf):
                min_value = value_step[k]
                min_step = blank[k]
        # 取当前节点后继节点中的最大值
        if min_value > max_value:
            max_value = min_value
            max_step = step
    max_chess_y = max_step // 3
    max_chess_x = max_step % 3
    chess_background[max_chess_y, max_chess_x] = 1
    chess_blank.pop(getwhere(chess_blank, max_chess_x + max_chess_y * 3))
    player = 1
    return chess_background, player, chess_blank


# 判定游戏结束
def game_over(chess_background):
    over = 0
    flag = 0
    if product(chess_background[:, 0]) == 1 or product(chess_background[:, 1]) == 1 or product(chess_background[:, 2]) == 1 or product(chess_background[0, :]) == 1 or product(chess_background[1, :]) == 1 or product(chess_background[2, :]) == 1 or (
            chess_background[0, 0] == 1 and chess_background[1, 1] == 1 and chess_background[2, 2] == 1) or (chess_background[2, 0] == 1 and chess_background[1, 1] == 1 and chess_background[0, 2] == 1):
        flag = 1
        over = 1
    elif product(chess_background[:, 0]) == 8 or product(chess_background[:, 1]) == 8 or product(chess_background[:, 2]) == 8 or product(chess_background[0, :]) == 8 or product(chess_background[1, :]) == 8 or product(chess_background[2, :]) == 8 or (
            chess_background[0, 0] == 2 and chess_background[1, 1] == 2 and chess_background[2, 2] == 2) or (chess_background[2, 0] == 2 and chess_background[1, 1] == 2 and chess_background[0, 2] == 2):
        flag = 2
        over = 1
    elif chess_background.all() != 0:
        flag = 3
        over = 1
    else:
        over = 0
        flag = 0
    return flag, over


# 更行棋局UI
def chess(chess_background):
    global c
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if chess_background[i, j] == 0:
                paint.create_rectangle(
                    40 + 180 * j, 40 + 180 * i, 40 + 180 * (j + 1), 40 + 180 * (i + 1), fill="white")
            if chess_background[i, j] == 1:
                paint.create_oval(40 + 180 * j, 40 + 180 * i,
                                  40 + 180 * (j + 1), 40 + 180 * (i + 1))
            if chess_background[i, j] == 2:
                paint.create_line(110 + 180 * j - 45 * math.sqrt(2), 110 + 180 * i - 45 * math.sqrt(
                    2), 110 + 180 * j + 45 * math.sqrt(2), 110 + 180 * i + 45 * math.sqrt(2))
                paint.create_line(110 + 180 * j + 45 * math.sqrt(2), 110 + 180 * i - 45 * math.sqrt(
                    2), 110 + 180 * j - 45 * math.sqrt(2), 110 + 180 * i + 45 * math.sqrt(2))


# 两个小工具
def getwhere(a, b):
    m = len(a)
    for i in range(m):
        if a[i] == b:
            return i
        else:
            if i > m:
                print("出界")


def product(a):
    return a[0] * a[1] * a[2]


# 弹出messagebox提示胜负
def result(flag):
    context = ""
    if flag == 1:
        context = "AI赢了"
    elif flag == 2:
        context = "你赢了"
    elif flag == 3:
        context = "和棋"
    tk.messagebox.askokcancel(title="结果", message=context)


# 人走棋出错，弹出出错界面
def wrong():
    tk.messagebox.askokcancel(title="错误", message="重新选择下一步位置")


# 判定谁是第一个下棋者
def firstplayer(a):
    if a == 0:
        tk.messagebox.askokcancel(title="先手", message="机器先手")
    else:
        tk.messagebox.askokcancel(title="先手", message="你先手")


# 主函数
# 初始化棋盘
chess_blank = [0, 1, 2, 3, 4, 5, 6, 7, 8]
chess_background = np.zeros((3, 3))
player = random.randint(0, 1)
if player == 0:
    print("AI先手")
else:
    print("人先手")
# 游戏正式开始
firstplayer(player)
paint.bind("<Button -1>", game_start)
# game_start(tk.Menubutton)
root.mainloop()
