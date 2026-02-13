# Functions of Single Chain Dynamics (2d Square Lattice model)
# v2 --- 重心を奇跡として描画、重心位置の時間変化を追加（240121）
# 管の中のレプテーションを記述できるように修正
# Rep_v2 --- 両側に出口がある状態に変更
# Rev_v3 --- 初期配置のランダムコイル生成も管の半径の制約を考慮
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更
# SAW鎖への拡張（260203一旦完了）
# 諸々のデバッグ（260213）

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
        num_step = 0        # 重合度Nのカウント
        num_rep = 0         # 袋小路に入ったときに繰り返す試行回数
        x, y = 0, 0
        x_list = [0]
        y_list = [0]
        init_coordinate_list = [[0,0]]   # 通過した点の記録
        num_step_list = []
        while num_rep < 20 and num_step < N:        # 試行は20回までで諦める
            theta = np.random.choice(theta_s)
            x_temp = x + np.rint(np.cos(theta))     # 一致不一致をチェックするため、整数化を行う
            num_rep_y = 0           # y方向が管の外に出てしまう場合の試行回数
            while num_rep_y < 20:   # y方向が管の外に出てしまう場合はやり直し
                y_temp_trial = y + np.rint(np.sin(theta))
                if np.abs(y_temp_trial) >= radi:
                    num_rep_y += 1
                else:
                    y_temp = y_temp_trial
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
        x0 = coordinate_list[0][0]
        y0 = coordinate_list[0][1]
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
        x_temp = x1 + int(np.cos(np.radians(theta3)))
        y_temp = y1 + int(np.sin(np.radians(theta3)))
        if np.abs(y_temp) >= radi:
            updated_coordinate = [x0, y0]                # [x0, y0]は元々存在できる場所なので自動的にこれで登録 
        else:
            temp_coordinate = [x_temp, y_temp]           # 菅の内側なら位置更新
            if temp_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
                updated_coordinate = [x0, y0]                                        # 座標を更新しない
            else:                                        # もし新座標が非占有だったらという条件
                updated_coordinate = temp_coordinate
        coordinate_list[0] = updated_coordinate          # 新座標を登録
    elif p == 1:  # N=N側
        direction_list = [0, 1, 2, 3]
        xpp = coordinate_list[N-2][0]
        ypp = coordinate_list[N-2][1]
        xp = coordinate_list[N-1][0]
        yp = coordinate_list[N-1][1]
        xe = coordinate_list[N][0]
        ye = coordinate_list[N][1]
        dx = xp - xpp
        dy = yp - ypp
        theta2 = np.degrees(np.arctan2(dy,dx)) + 180.0  # NG（来た方に戻る）方向
        ng_direction = int(np.mod(theta2/90,4)) # NG方向をdirection_listの要素と合わせるため
        direction_list.remove(ng_direction)
        theta3 = rd.choice(direction_list)*90.0
#        print("p=1: {}".format(theta3))
        x_temp = xp + int(np.cos(np.radians(theta3)))
        y_temp = yp + int(np.sin(np.radians(theta3)))
        if np.abs(y_temp) >= radi:                       # 菅の外なら位置更新しない
            updated_coordinate = [xe, ye]                # [xe, ye]は元々存在できる場所なので自動的にこれで登録
        else:
            temp_coordinate = [x_temp, y_temp]           # 菅の内側なら位置更新
            if temp_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
                updated_coordinate = [xe, ye]            # 座標を更新しない
            else:                                        # もし新座標が非占有だったらという条件
                updated_coordinate = temp_coordinate
        coordinate_list[N] = updated_coordinate 
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
        updated_coordinate = [xi, yi]                   # 要するに何もしない
        updated_coordinate_list[i] = updated_coordinate # coordinate_listを変更しないようにするため 
    else:     # 「L」字型のとき（振る舞いによって２通りあるので分けている）
        if (xp == xi) and ((xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1)):
#            print("c")
            onoff = rd.choice(onoff_list)
#            print(onoff)
            if onoff == "on":                                # 対角線側に移動
                x_temp = xn
                y_temp = yp
            elif onoff == "off":                             # 動かない
                x_temp = xi
                y_temp = yi               
            if np.abs(y_temp) >= radi:                       # 菅の外なら位置更新しない
                updated_coordinate = [xi, yi]                # [xe, ye]は元々存在できる場所なので自動的にこれで登録
            else:
                temp_coordinate = [x_temp, y_temp]           # 菅の内側なら位置更新
                if temp_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
                    updated_coordinate = [xi, yi]            # 座標を更新しない
                else:
                    updated_coordinate = temp_coordinate     # もし新座標が非占有だったらという条件
            updated_coordinate_list[i] = updated_coordinate 
        elif (xn == xi) and ((xn == xp - 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp + 1) or (xn == xp + 1 and yn == yp - 1) or (xn == xp - 1 and yn == yp - 1)):
#            print("d")
            onoff = rd.choice(onoff_list)
#            print(onoff)
            if onoff == "on":                                # 対角線側に移動
                x_temp = xp
                y_temp = yn
            elif onoff == "off":                               # 動かない
                x_temp = xi
                y_temp = yi   
            if np.abs(y_temp) >= radi:                       # 菅の外なら位置更新しない
                updated_coordinate = [xi, yi]                # [xe, ye]は元々存在できる場所なので自動的にこれで登録
            else:
                temp_coordinate = [x_temp, y_temp]           # 菅の内側なら位置更新
                if temp_coordinate in coordinate_list:       # もし新座標が既に占有されていたらという条件
                    updated_coordinate = [xi, yi]            # 座標を更新しない
                else:                                        # もし新座標が非占有だったらという条件
                    updated_coordinate = temp_coordinate
            updated_coordinate_list[i] = updated_coordinate  # ここがcoordinate_list[i] = updated_coordinateとなっていたのがミス
    coordinate_list = updated_coordinate_list                    # updated_coordinate_listをcoordinate_listに戻す（ここは.copy()は不要？）       
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