# 重心の拡散係数の重合度依存性

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

DP_val = input('Enter DP values separated by comma: ')
DC_val = input('Enter DC values separated by comma: ')

DP_val = DP_val.split(',')
DP_list = [ float(val) for val in DP_val ]
logDP_list = [ np.log10(DP) for DP in DP_list ]

DC_val = DC_val.split(',')
DC_list = [ float(val) for val in DC_val ]
logDC_list = [ np.log10(DC) for DC in DC_list ]

def loglogFit(x, a, b):
    return  a*x + b

param, cov = curve_fit(loglogFit, logDP_list, logDC_list)
slope = param[0]
err_slope = np.sqrt(cov[0][0])
logDC_fit_list = [ loglogFit(logDP, param[0], param[1]) for logDP in logDP_list ]

resultText = "$D$  ∝ $N^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(slope, err_slope)

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, title='Scaling of Diffusion Const, $D$', 
            xlabel='Log($N$)', ylabel='Log($D$)')
ax.grid(visible=True, which='major', color ='#666666', linestyle='--')

ax.scatter(logDP_list, logDC_list, marker='o', s=50, c='red')
ax.plot(logDP_list, logDC_fit_list,  c='blue')

fig.text(0.35, 0.70, resultText)

savefile = "./png/Scaling_DiffusionConst"
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()