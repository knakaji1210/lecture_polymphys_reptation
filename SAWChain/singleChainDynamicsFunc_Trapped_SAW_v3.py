# Functions of Single Chain Dynamics (2d Square Lattice model)
# v2 --- 重心を奇跡として描画、重心位置の時間変化を追加（240121）
# 管の中のレプテーションを記述できるように修正
# Rep_v2 --- 両側に出口がある状態に変更
# Rev_v3 --- 初期配置のランダムコイル生成も管の半径の制約を考慮
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更
# SAW鎖への拡張（260202開始）

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
    num_step = 0
    theta_s = np.array([0,0.5*np.pi, np.pi, 1.5*np.pi])

    while num_step < N:
        num_step = 0
        num_rep = 0         # 袋小路に入ったときに繰り返す試行回数
        x, y = 0, 0
        x_list = [0]
        y_list = [0]
        init_coordinate_list = [[0,0]]   # 通過した点の記録
        num_step_list = []
        while num_rep < 20 and num_step < N:        # 試行は20回までで諦める
            theta = np.random.choice(theta_s)
            x_temp = x + np.rint(np.cos(theta))     # 一致不一致をチェックするため、整数化を行う
            num_rep_y = 0
            while num_rep_y < 20:  # y方向が管の外に出てしまう場合はやり直し
                y_temp2 = y + np.rint(np.sin(theta))
                if np.abs(y_temp2) >= radi:
                    num_rep_y += 1
                else:
                    y_temp = y_temp2
                    break
            coordinate_temp = [x_temp, y_temp]      # まず仮の新座標を設定
            if coordinate_temp in init_coordinate_list:  # もし新座標が既に占有されていたらという条件
                num_step = num_step
                num_step_list.append(num_step)
                num_rep = num_step_list.count(num_step_list[-1])  
            else:                                   # もし新座標が非占有だったらという条件
                x = x + np.rint(np.cos(theta))
                y = y + np.rint(np.sin(theta))
                x_list.append(x)
                y_list.append(y)
                coordinate = [x, y]
                init_coordinate_list.append(coordinate)  # 新座標を登録
                num_step += 1

    return init_coordinate_list

# 末端の動き・・・隣を中心に回転できることをプログラム
def terminalSegment(coordinate_list, N, radi, p):
    if p == 0:  # N=0側
        direction_list = [0, 1, 2, 3]
        x1 = coordinate_list[1][0]
        y1 = coordinate_list[1][1]
        x2 = coordinate_list[2][0]
        y2 = coordinate_list[2][1]
        dx = x2 - x1
        dy = y2 - y1
        theta2 = np.degrees(np.arctan2(dy,dx))  # NG（来た方に戻る）方向
        ng_direction = int(np.mod(theta2/90,4)) # NG方向をdirection_listの要素と合わせるため
        direction_list.remove(ng_direction)
        theta3 = rd.choice(direction_list)*90.0
#        print("p=0: {}".format(theta3))
        xi = x1 + int(np.cos(np.radians(theta3)))
        yi = y1 + int(np.sin(np.radians(theta3)))
        if np.abs(yi) >= radi:
            updated_coordinate = [x1, y1]               # 菅の外なら位置更新しない
        else:
            updated_coordinate = [xi, yi]               # 菅の内側なら位置更新
        if updated_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
            pass                                        # 座標を更新しない
        else:                                           # もし新座標が非占有だったらという条件
            coordinate_list[0] = updated_coordinate     # 新座標を登録
    if p == 1:  # N=N側
        direction_list = [0, 1, 2, 3]
        xpp = coordinate_list[N-2][0]
        ypp = coordinate_list[N-2][1]
        xp = coordinate_list[N-1][0]
        yp = coordinate_list[N-1][1]
        dx = xp - xpp
        dy = yp - ypp
        theta2 = np.degrees(np.arctan2(dy,dx)) + 180.0  # NG（来た方に戻る）方向
        ng_direction = int(np.mod(theta2/90,4)) # NG方向をdirection_listの要素と合わせるため
        direction_list.remove(ng_direction)
        theta3 = rd.choice(direction_list)*90.0
#        print("p=1: {}".format(theta3))
        xe = xp + int(np.cos(np.radians(theta3)))
        ye = yp + int(np.sin(np.radians(theta3)))
        if np.abs(ye) >= radi:
            updated_coordinate = [xp, yp]               # 菅の外なら位置更新しない
        else:
            updated_coordinate = [xe, ye]               # 菅の内側なら位置更新
        if updated_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
            pass                                        # 座標を更新しない
        else:                                           # もし新座標が非占有だったらという条件
            coordinate_list[N] = updated_coordinate     # 新座標を登録
    return coordinate_list

# 末端以外のセグメントの動き
# 安定バージョンとして利用するこのバージョンではcoordinate_listを返り値とする
def segmentMotion(coordinate_list, radi, i):
    updated_coordinate_list = coordinate_list.copy()    # coordinate_listを変更しないようにするため
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
    else:   # 「L」字型のとき（振る舞いによって２通りあるので分けている）
        if (xp == xi) and ((xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1)):
#            print("c")
            onoff = rd.choice(onoff_list)
#            print(onoff)
            if onoff == "on":
                xnew = xn
                ynew = yp
            if onoff == "off":
                xnew = xi
                ynew = yi
            if np.abs(ynew) >= radi:
                updated_coordinate = [xi, yi]             # 菅の外なら位置更新しない
            else:
                updated_coordinate = [xnew, ynew]         # 菅の内側なら位置更新
            if updated_coordinate in coordinate_list: 
                pass
            else:
                updated_coordinate_list[i] = updated_coordinate # coordinate_listを変更しないようにするため
        else:
            if (xn == xi) and ((xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1)):
#                 print("d")
                onoff = rd.choice(onoff_list)
#                 print(onoff)
                if onoff == "on":
                    xnew = xp
                    ynew = yn
                if onoff == "off":
                    xnew = xi
                    ynew = yi   
                if np.abs(ynew) >= radi:
                    updated_coordinate = [xi, yi]          # 菅の外なら位置更新しない
                else:
                    updated_coordinate = [xnew, ynew]      # 菅の内側なら位置更新
                if updated_coordinate in coordinate_list: 
                    pass
                else:
                    updated_coordinate_list[i] = updated_coordinate # coordinate_listを変更しないようにするため
    coordinate_list = updated_coordinate_list   # updated_coordinate_listをcoordinate_listに戻す（ここは.copy()は不要？）
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