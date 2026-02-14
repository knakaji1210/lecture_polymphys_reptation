# 菅更新時間（Tube Renewal Time, TRT）の重合度依存性

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

DP_val = input('Enter DP values separated by comma: ')
logTRT_val = input('Enter logTRT values separated by comma: ')          # logTRT
logTRT_std_val = input('Enter logTRT STD values separated by comma: ')  # STD of logTRT

DP_val = DP_val.split(',')
DP_list = [ float(val) for val in DP_val ]
logDP_list = [ np.log10(DP) for DP in DP_list ]

logTRT_val = logTRT_val.split(',')
logTRT_list = [ float(val) for val in logTRT_val ]

logTRT_std_val = logTRT_std_val.split(',')
logTRT_std_list = [ float(val) for val in logTRT_std_val ]

def loglogFit(x, a, b):
    return  a*x + b

param, cov = curve_fit(loglogFit, logDP_list, logTRT_list, sigma=logTRT_std_list, absolute_sigma=True)
slope = param[0]
err_slope = np.sqrt(cov[0][0])
logTRT_fit_list = [ loglogFit(logDP, param[0], param[1]) for logDP in logDP_list ]

resultText = "$τ_{{t}}$  ∝ $N^{{{{{0:.3f}}}±{{{1:.3f}}}}}$".format(slope, err_slope)

fig = plt.figure(figsize=(8,8))

ax = fig.add_subplot(111, title='Scaling of Tube Renewal Time, $τ_{{t}}$', 
            xlabel='Log($N$)', ylabel='Log($τ_{{t}}$)')
ax.grid(visible=True, which='major', color ='#666666', linestyle='--')

ax.errorbar(logDP_list, logTRT_list, yerr = logTRT_std_list, capsize=5, fmt='o', markersize=6, ecolor='black', color='r')
# ax.scatter(logDP_list, logTRT_list, marker='o', s=50, c='red')
ax.plot(logDP_list, logTRT_fit_list,  c='blue')

fig.text(0.35, 0.70, resultText)

savefile = "./png/Scaling_LongestRelaxationTime"
fig.savefig(savefile, dpi=300)

plt.show()
plt.close()