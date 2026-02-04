# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# v2 --- 重心を奇跡として描画（240121）
# 管の中のレプテーションを記述できるように修正
# 細い管にしても、理想だと縮んでいってしまう
# Rev_v3 --- x方向の管の長さ制限を停止、長い管の中を動くような挙動に変更

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
    radi = int(input('Radius of Tube (default=2): '))
except ValueError:
    radi = 2

# 強制終了させる最大ステップ数
try:
    t_max = int(input('Maximum steps for forced quit (default=1000): '))
except ValueError:
    t_max = 1000

plot_lim = 1.5*N

x_list_steps = []
y_list_steps = []

try:
    initConfig = input('Initial Configuration (Fully Extended (F) or Random Coil (R)): ')
    if initConfig == "":
        raise ValueError
except ValueError:
    initConfig = "R"

try:
    centerConfig = input('with center of gravity (W) or without it (O)): ')
    if centerConfig == "":
        raise ValueError
except ValueError:
    centerConfig = "W"

if initConfig == "F": # Fully Extendedからスタートする場合
    init_coordinate_list = scd.initConfig_FullExted(N)
    x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
else: #　Random Coilからスタートする場合
    init_coordinate_list = scd.initConfig_Random(N, radi)
    x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)

# 初期重心位置
xg0 = np.mean(x_list)

# 初期長（x方向の鎖の広がり）
tubeLength = (np.max(x_list) - np.min(x_list))/2

rep = 0
xg = xg0

# ステップごとのセグメントの動作
# for rep in range(t_max-1):
while not (tubeLength < np.abs(xg - xg0) or rep >= t_max-1):
    # まず両末端を動かす
    coordinate_list = scd.terminalSegment(init_coordinate_list, N, radi, 0)
    coordinate_list = scd.terminalSegment(init_coordinate_list, N, radi, 1)
    # 次に末端以外のセグメントを動かす
    for i in range(N-1):
        coordinate_list = scd.segmentMotion(coordinate_list, radi, i+1)   
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    xg = np.mean(x_list)
    diffLength = np.abs(xg - xg0)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
    rep += 1
    print("Step: {0}, Diffusion Distance: {1:.3f}, Tube Length: {2:.3f}".format(rep, diffLength, tubeLength))

# 最大ステップ数を超えたら強制終了させる
if rep == t_max - 1:
    print("Maximum step reached.")
    sys.exit()

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の２行
x_list_steps = np.asanyarray(x_list_steps, dtype=object)
y_list_steps = np.asanyarray(y_list_steps, dtype=object)

# 重心位置
cx_list, cy_list, cx_list_steps, cy_list_steps = scd.centerOfMass(x_list_steps, y_list_steps, rep+1)
cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

fig_title = "Dynamics of a Single Polymer Chain Trapped in a Tube ($N$ = {0}, $D$ = {1})".format(N,2*radi)

# うまく終了した場合には、repは菅更新時間になる
result_text = "$τ$ = {}".format(rep)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, title=fig_title, xlabel='$X$', ylabel='$Y$',
        xlim=[-plot_lim, plot_lim], ylim=[-plot_lim , plot_lim])
ax.grid(axis='both', color="gray", lw=0.5)

rect_u = patches.Rectangle(xy=(-plot_lim, radi), width=2*plot_lim, height=plot_lim - radi, fc="grey", fill=True)
rect_d = patches.Rectangle(xy=(-plot_lim, -plot_lim), width=2*plot_lim, height=plot_lim - radi, fc="grey", fill=True)
rect_orig = patches.Rectangle(xy=(xg0-tubeLength, -radi), width=2*tubeLength, height=2*radi, fc="yellow", fill=True)
ax.add_patch(rect_u)
ax.add_patch(rect_d)
ax.add_patch(rect_orig)

fig.text(0.70, 0.80, result_text)

singleChainDynamics_c = amp.blocks.Line(cx_list_steps, cy_list_steps, ax=ax, ls='-', marker="o", markersize=20/plot_lim, color='red')
singleChainDynamics = amp.blocks.Line(x_list_steps, y_list_steps, ax=ax, ls='-', marker="o", markersize=100/plot_lim, color='blue')

t = np.linspace(0, rep, rep+1)
timeline = amp.Timeline(t, units=' steps', fps=5)

if rep <= 2:
    print("Too few steps to animate.")
    sys.exit()
else:
    if centerConfig == "O": # 重心描画なし
        anim = amp.Animation([singleChainDynamics], timeline)
    if centerConfig == "W": # 重心描画あり
        anim = amp.Animation([singleChainDynamics_c, singleChainDynamics], timeline)
    anim.controls()

    if initConfig == "F": # Fully Extendedからスタートする場合
        savefile = "./gif/SingleChain_Dynamics_Ideal_N{0}_T{1}_FE_in_D{2}-Tube".format(N, rep, 2*radi)
    if initConfig == "R": # Random Coilからスタートする場合
        savefile = "./gif/SingleChain_Dynamics_Ideal_N{0}_T{1}_RC_in_D{2}-Tube".format(N, rep, 2*radi)
    anim.save_gif(savefile)
    plt.show()
    plt.close()
