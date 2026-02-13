# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# v2 --- 重心を奇跡として描画（240121）
# 管の中のレプテーションを記述できるように修正
# 細い管にしても、理想だと縮んでいってしまう
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更
# 菅更新時間の統計を取るバージョン（試み）
# SAW鎖の拡張で生じた変更で妥当なものをこちらでも修正（260213）
# 末端以外のセグメントを動かす順番をランダムに変更（260208）

# import sys
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import animatplot as amp
import singleChainDynamicsFunc_Trapped_Ideal_v3 as scd

try:
    N = int(input('Degree of polymerization (default=5): '))
except ValueError:
    N = 5

try:
    radi = int(input('Radius of Tube (default=3): '))
except ValueError:
    radi = 3

# 強制終了させる最大ステップ数
try:
    t_max = int(input('Maximum steps for forced quit (default=1000): '))
except ValueError:
    t_max = 1000

plot_lim = 1.5*N

repeat =0   # 繰り返し数
rep_list = []  # ステップ数（菅更新）を保存するリスト

while repeat < 500:  # 元は100

    x_list_steps = []
    y_list_steps = []

    #　Fully Extendedからスタートする
    coordinate_list = scd.initConfig_FullExted(N)
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)

    # 初期重心位置
    xg0 = np.mean(x_list)

    # 初期長（重心から最も遠いセグメントの位置）
    tubeLength = (np.max(x_list) - np.min(x_list))/2

    rep = 0     # このrepは結果的にステップ数（菅更新）をカウントするための変数になる
    xg = xg0

    orderedArray = np.arange(1,N)   # 260208追加

    # ステップごとのセグメントの動作
    # for rep in range(t_max-1):
        
    while not (tubeLength < np.abs(xg - xg0) or rep >= t_max-1):
        # まず両末端を動かす
        coordinate_list = scd.terminalSegment(coordinate_list, N, radi, 0)
        coordinate_list = scd.terminalSegment(coordinate_list, N, radi, 1)
        # 次に末端以外のセグメントを動かす
        shuffledArray = np.random.permutation(orderedArray)   # 260208追加
        for i in range(N-1):
#            coordinate_list = scd.segmentMotion(coordinate_list, radi, i+1)                   # こちらが元々
            coordinate_list = scd.segmentMotion(coordinate_list, radi, shuffledArray[i])      # 260208変更 
        x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
        xg = np.mean(x_list)
        diffLength = np.abs(xg - xg0)
        x_list_steps.append(x_list)
        y_list_steps.append(y_list)
        rep += 1
#        print("Step: {0}, Diffusion Distance: {1:.3f}, Tube Length: {2:.3f}".format(rep, diffLength, tubeLength))

    rep_list.append(rep)
    repeat += 1

tau_list = [x for x in rep_list if x != 0]      # 0を除去
tau_list = [x for x in tau_list if x != t_max - 1]    # 最大ステップ数に達したものを除去
print(tau_list)

len_tau = len(tau_list)
mean_tau = np.mean(tau_list)
std_tau = np.std(tau_list)

logtau_list = [ np.log10(tau) for tau in tau_list ]
mean_logtau = np.mean(logtau_list)
std_logtau = np.std(logtau_list)

print("N = {0}, Tube Radius = {1}, Max Steps = {2}".format(N, radi, t_max))
print("Number of Successful Events: {0}".format(len_tau))
# print("Mean of tube renewal time τ: {0:.0f}".format(mean_tau))
# print("STD of τ: {0:.0f}".format(std_tau))
print("Mean of tube renewal time log(τ): {0:.2f}".format(mean_logtau))
print("STD of log(τ): {0:.2f}".format(std_logtau))