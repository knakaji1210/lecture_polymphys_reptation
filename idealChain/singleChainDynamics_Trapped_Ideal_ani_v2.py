# Animation of Single Chain Dynamics (2d Square Lattice model)
# Flory-Huggins的に分岐数zに対してz-1で対応するようにすることはできていない
# v2 --- 重心を奇跡として描画（240121）
# 管の中のレプテーションを記述できるように修正
# 細い管にしても、理想だと縮んでいってしまう
# ただし、少し飛び出させてradi=1で行うと、管更新が観察される場合もある！

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import animatplot as amp
import singleChainDynamicsFunc_Trapped_Ideal_v2 as scd

try:
    N = int(input('Degree of polymerization (default=10): '))
except ValueError:
    N = 10

length = 3*N/8 

try:
    t_max = int(input('Number of steps (default=100): '))
except ValueError:
    t_max = 100

try:
    radi = int(input('Radius of Tube (default=2): '))
except ValueError:
    radi = 2

t = np.linspace(0, t_max-1, t_max)

x_list_steps = []
y_list_steps = []

try:
    initConfig = input('Initial Configuration (Fully Extended (F) or Random Coil (R)): ')
    if initConfig == "":
        raise ValueError
except ValueError:
    initConfig = "F"

try:
    centerConfig = input('with center of gravity (W) or without it (O)): ')
    if centerConfig == "":
        raise ValueError
except ValueError:
    centerConfig = "O"

if initConfig == "F": # Fully Extendedからスタートする場合
    init_coordinate_list = scd.initConfig_FullExted(N)
    x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
    plot_lim = 1.2*N
else: #　Random Coilからスタートする場合
    init_coordinate_list = scd.initConfig_Random(N)
    x_list, y_list = scd.coordinateList2xyList(init_coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)
#    plot_lim = 3*np.sqrt(N)
#    plot_lim = np.sqrt(30*N)
    plot_lim = 0.8*N

for rep in range(t_max-1):
    coordinate_list = scd.terminalSegment(init_coordinate_list, N, length, radi, 0)
    for i in range(N-1):
        coordinate_list = scd.segmentMotion(coordinate_list, length, radi, i+1)
        coordinate_list = scd.terminalSegment(init_coordinate_list, N, length, radi, 1)
    x_list, y_list = scd.coordinateList2xyList(coordinate_list, N)
    x_list_steps.append(x_list)
    y_list_steps.append(y_list)

# numpyのバージョンアップにより、""ndarray from ragged nested sequences"の制限が厳しくなり、
# animatplotの途中でエラーが出るようになった。そのための修正が以下の２行
x_list_steps = np.asanyarray(x_list_steps, dtype=object)
y_list_steps = np.asanyarray(y_list_steps, dtype=object)

# 重心位置
cx_list, cy_list, cx_list_steps, cy_list_steps = scd.centerOfMass(x_list_steps, y_list_steps, t_max)
cx_list_steps = np.asanyarray(cx_list_steps, dtype=object)
cy_list_steps = np.asanyarray(cy_list_steps, dtype=object)

fig_title = "Dynamics of a Single Polymer Chain ($N$ = {0}, $D$ = {1})".format(N,2*radi)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, title=fig_title, xlabel='$X$', ylabel='$Y$',
        xlim=[-plot_lim, plot_lim], ylim=[-plot_lim , plot_lim])
ax.grid(axis='both', color="gray", lw=0.5)

rect_u = patches.Rectangle(xy=(-length, radi), width=2*length, height=plot_lim - radi, fc="red", fill=True)
rect_d = patches.Rectangle(xy=(-length, -plot_lim), width=2*length, height=plot_lim - radi, fc="red", fill=True)
ax.add_patch(rect_u)
ax.add_patch(rect_d)

singleChainDynamics_c = amp.blocks.Line(cx_list_steps, cy_list_steps, ax=ax, ls='-', marker="o", markersize=20/plot_lim, color='red')
singleChainDynamics = amp.blocks.Line(x_list_steps, y_list_steps, ax=ax, ls='-', marker="o", markersize=100/plot_lim, color='blue')

timeline = amp.Timeline(t, units=' steps', fps=5)

if centerConfig == "O": # 重心描画なし
    anim = amp.Animation([singleChainDynamics], timeline)
if centerConfig == "W": # 重心描画あり
    anim = amp.Animation([singleChainDynamics_c, singleChainDynamics], timeline)
anim.controls()

if initConfig == "F": # Fully Extendedからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_Ideal_N{0}_{1}steps_FE_in_D{2}-Tube".format(N, t_max, 2*radi)
if initConfig == "R": # Random Coilからスタートする場合
    savefile = "./gif/SingleChain_Dynamics_Ideal_N{0}_{1}steps_RC_in_D{2}-Tube".format(N, t_max, 2*radi)
anim.save_gif(savefile)

plt.show()
plt.close()
