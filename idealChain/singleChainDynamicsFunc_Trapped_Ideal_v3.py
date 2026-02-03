# Functions of Single Chain Dynamics (2d Square Lattice model)
# v2 --- 重心を奇跡として描画、重心位置の時間変化を追加（240121）
# 管の中のレプテーションを記述できるように修正
# Rep_v2 --- 両側に出口がある状態に変更
# Rev_v3 --- 初期配置のランダムコイル生成も管の半径の制約を考慮
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更

import random as rd
import numpy as np
from math import *

def initConfig_FullExted(N):
    x, y = -N/2, 0
    init_coordinate_list = [[x,y]]
    for i in range(N):
        x = x + 1
#        y = y + 1
        coordinate = [x, y]
        init_coordinate_list.append(coordinate)
    return init_coordinate_list

def initConfig_Random(N, radi):
    x, y = 0, 0
    init_coordinate_list = [[x,y]]
    angle_list = (0, 90, 180, 270)
    for i in range(N):
        angle = rd.choice(angle_list)
        x = x + int(np.cos(np.radians(angle)))
        num_rep = 0
        while num_rep < 20:  # y方向が管の外に出てしまう場合はやり直し
            y_temp = y + int(np.sin(np.radians(angle)))
            if np.abs(y_temp) >= radi:
                num_rep += 1
            else:
                y = y_temp
                break
        coordinate = [x, y]
        init_coordinate_list.append(coordinate)
    return init_coordinate_list

# 末端の動き・・・隣を中心に回転できることをプログラム
def terminalSegment(coordinate_list, N, radi, p):
    angle_list = (0, 90, 180, 270)
    angle = rd.choice(angle_list)
    if p == 0:
        x0 = coordinate_list[0][0]  # 末端座標
        y0 = coordinate_list[0][1]
        x1 = coordinate_list[1][0]  # その隣
        y1 = coordinate_list[1][1]
        x_temp = x1 + int(np.cos(np.radians(angle)))    # 末端座標の次の候補
        y_temp = y1 + int(np.sin(np.radians(angle)))
        if np.abs(y_temp) >= radi:
            updated_coordinate = [x0, y0]             # 菅の外なら位置更新しない
        else:
            updated_coordinate = [x_temp, y_temp]         # 菅の内側なら位置更新
        coordinate_list[0] = updated_coordinate
    if p == 1:
        xe = coordinate_list[N][0]  # 末端座標
        ye = coordinate_list[N][1]
        xp = coordinate_list[N-1][0]  # その隣
        yp = coordinate_list[N-1][1]
        x_temp = xp + int(np.cos(np.radians(angle)))    # 末端座標の次の候補
        y_temp = yp + int(np.sin(np.radians(angle)))
        if np.abs(y_temp) >= radi:
            updated_coordinate = [xe, ye]             # 菅の外なら位置更新しない
        else:
            updated_coordinate = [x_temp, y_temp]         # 菅の内側なら位置更新
        coordinate_list[N] = updated_coordinate
    return coordinate_list

def segmentMotion(coordinate_list, radi, i):
    angle_list = (0, 90, 180, 270)
    onoff_list = ("on", "off")
    xp = coordinate_list[i-1][0] # p = previous
    yp = coordinate_list[i-1][1]
    xi = coordinate_list[i][0]
    yi = coordinate_list[i][1]
    xn = coordinate_list[i+1][0] # n = next
    yn = coordinate_list[i+1][1]
    # o---o---oの形になっているときは何も動けない
    if (yp == yn and int(np.abs(xn - xp)) == 2) or (xp == xn and int(np.abs(yn - yp)) == 2):
#        print("a")
        xi = xi
        yi = yi
        updated_coordinate = [xi, yi]
        coordinate_list[i] = updated_coordinate
    else:
        # oo===oの形になっているときは[xp, yp]を中心に回転できる
        if xp == xn and yp == yn:
#            print("b")
            angle = rd.choice(angle_list)
#            print("angle = {}".format(angle))
            x_temp = xp + int(np.cos(np.radians(angle)))
            y_temp = yp + int(np.sin(np.radians(angle)))
            if np.abs(y_temp) >= radi:
                updated_coordinate = [xi, yi]             # 菅の外なら位置更新しない
            else:
                updated_coordinate = [x_temp, y_temp]         # 菅の内側なら位置更新
            coordinate_list[i] = updated_coordinate
        else:     # 「L」字型のとき（振る舞いによって２通りあるので分けている）
            if (xp == xi) and ((xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1)):
#                print("c")
                onoff = rd.choice(onoff_list)
#                print(onoff)
                if onoff == "on":
                    x_temp = xn
                    y_temp = yp
                if onoff == "off":
                    x_temp = xi
                    y_temp = yi
                if np.abs(y_temp) >= radi:
                    updated_coordinate = [xi, yi]             # 菅の外なら位置更新しない
                else:
                    updated_coordinate = [x_temp, y_temp]         # 菅の内側なら位置更新
                coordinate_list[i] = updated_coordinate
            else:
                if (xn == xi) and ((xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1)):
#                    print("d")
                    onoff = rd.choice(onoff_list)
#                    print(onoff)
                    if onoff == "on":
                        x_temp = xp
                        y_temp = yn
                    if onoff == "off":
                        x_temp = xi
                        y_temp = yi   
                    if np.abs(y_temp) >= radi:
                        updated_coordinate = [xi, yi]          # 菅の外なら位置更新しない
                    else:
                        updated_coordinate = [x_temp, y_temp]      # 菅の内側なら位置更新
                    coordinate_list[i] = updated_coordinate

    return coordinate_list

def coordinateList2xyList(coordinate_list, N):
    x_list = [ coordinate_list[i][0] for i in range(N+1) ]
    y_list = [ coordinate_list[i][1] for i in range(N+1) ]
    return x_list, y_list

# 末端間距離
def end2endDist(x_list_steps, y_list_steps, N, t_max):
    R_list = []
    for i in range(t_max):
        x0 = x_list_steps[i][0]
        y0 = y_list_steps[i][0]
        xe = x_list_steps[i][N]
        ye = y_list_steps[i][N]
        R = np.sqrt((x0 - xe)**2 + (y0 - ye)**2)
        R_list.append(R)
    R_list_steps = [ R_list[:i] for i in range(t_max+1) ]
    R_list_steps = R_list_steps[1:]
    return R_list, R_list_steps

# 重心位置
def centerOfMass(x_list_steps, y_list_steps, t_max):
    cx_list = []
    cy_list = []
    for i in range(t_max):
        xg = np.mean(x_list_steps[i])
        yg = np.mean(y_list_steps[i])
        cx_list.append(xg)
        cy_list.append(yg)
    cx_list_steps = [ cx_list[:i] for i in range(t_max+1) ]
    cy_list_steps = [ cy_list[:i] for i in range(t_max+1) ]
    cx_list_steps = cx_list_steps[1:]
    cy_list_steps = cy_list_steps[1:]
    return cx_list, cy_list, cx_list_steps, cy_list_steps

# 重心移動距離（初期ステップ位置を0に）
def centerOfMassDist(cx_list, cy_list, t_max):
    Dc2_list = []
    for i in range(t_max):
        cx0 = cx_list[0]
        cy0 = cy_list[0]
        cx = cx_list[i]
        cy = cy_list[i]
        Dc2 = (cx0 - cx)**2 + (cy0 - cy)**2
        Dc2_list.append(Dc2)
    Dc2_list_steps = [ Dc2_list[:i] for i in range(t_max+1) ]
    Dc2_list_steps = Dc2_list_steps[1:]
    return Dc2_list, Dc2_list_steps

def timeStep(t):
    time_steps = [ t[:i].tolist() for i in range(len(t)+1) ]
    time_steps = time_steps[1:]
    return time_steps

def calcMean(Data_list_repeat, t_max, M):
    Data_mean_list = []
    for i in range(t_max):
        Data_rep_list = [ Data_list_repeat[j][i] for j in range(M) ]
        Data_mean = np.mean(Data_rep_list)
        Data_mean_list.append(Data_mean)
    return Data_mean_list