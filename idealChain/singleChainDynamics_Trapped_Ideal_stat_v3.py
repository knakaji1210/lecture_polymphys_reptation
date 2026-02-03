# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# v2 --- 重心を奇跡として描画（240121）
# 管の中のレプテーションを記述できるように修正
# 細い管にしても、理想だと縮んでいってしまう
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更
# 菅更新時間の統計を取るバージョン（試み）

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import animatplot as amp
import singleChainDynamicsFunc_Trapped_Ideal_v3 as scd

try:
    N = int(input('Degree of polymerization (default=5): '))
except ValueError:
    N = 5

try:
    radi = int(input('Radius of Tube (default=3): '))
except ValueError:
    radi = 3

t_max = 1000  # 強制終了させる最大ステップ数
plot_lim = 1.5*N

repeat =0   # 繰り返し数
rep_list = []  # ステップ数（菅更新）を保存するリスト

while repeat < 100:

    rep = 0     # このrepは結果的にステップ数（菅更新）をカウントするための変数になる

    x_list_steps = []
    y_list_steps = []

    #　Random Coilからスタートする場合のみ
    init_coordinate_list = scd.initConfig_Random(N, radi)
    x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)

    # 初期重心位置
    xg = np.mean(x_list)

    # 初期長（重心から最も遠いセグメントの位置）
    xl = np.maximum(abs(np.max(x_list)), abs(np.min(x_list)))
    diffLength = np.abs(xl - xg)

    xg_now = 0

    # ステップごとのセグメントの動作
    # for rep in range(t_max-1):
        
    while not (diffLength < np.abs(xg_now - xg) or rep >= t_max-1):
        # まず両末端を動かす
        coordinate_list = scd.terminalSegment(init_coordinate_list, N, radi, 0)
        coordinate_list = scd.terminalSegment(init_coordinate_list, N, radi, 1)
        # 次に末端以外のセグメントを動かす
        for i in range(N-1):
            coordinate_list = scd.segmentMotion(coordinate_list, radi, i+1)   
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        xg_now = np.mean(x_list)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
        rep += 1
        print("Step: {0}, Abs(xg(t)-xg(0)): {1:.3f}, DiffLength: {2:.3f}".format(rep, np.abs(xg_now - xg), diffLength))

    rep_list.append(rep)
    repeat += 1

tau_list = [x for x in rep_list if x != 0]      # 0を除去
tau_list = [x for x in tau_list if x != 999]    # 最大ステップ数に達したものを除去
print(tau_list)

len_tau = len(tau_list)
mean_tau = np.mean(tau_list)
std_tau = np.std(tau_list)

print("N = {0}, Tube radius {1}:".format(N, radi))
print("Number of samples: {0}".format(len_tau))
print("Mean of tube renewal time τ: {0:.3f} steps".format(mean_tau))
print("Standard deviation of τ: {0:.3f} steps".format(std_tau))