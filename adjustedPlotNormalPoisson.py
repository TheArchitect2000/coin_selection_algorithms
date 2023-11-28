#Same as final.py, but added ticks to every subplot
import pickle
import matplotlib.pyplot as plt
import datetime
import numpy as np

with open('var6.pkl', 'rb') as f:
    utxos, balance,  poolSize, numberOfInputs, deposits, targets = pickle.load(f)
# with open('var9_pois.pkl', 'rb') as f:
#     utxosp, balancep,  poolSizep, numberOfInputsp, depositsp, targetsp = pickle.load(f)

with open('var12_pois.pkl', 'rb') as f:
    utxosp, balancep,  poolSizep, numberOfInputsp, depositsp, targetsp = pickle.load(f)


iterations = 10000
print(utxos['LIFO'])

methods = ['FIFO', 'LIFO', 'HVF', 'LVF', 'HPF', 'Greedy', 'Random Draw', 'Random Improve', 'Knapsack', 'Branch and Bound']

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = 1

maxUtxo = 0
maxNumberInputs = 0
maxDeposit = 0
maxTarget = 0
poolSizes_max = []
meth = ['LIFO', 'LVF', 'Greedy', 'Knapsack', 'Branch and Bound']

for m in meth:
    utxos[m].sort(reverse=False)
    utxos[m].pop()

for m in methods:
    if max(utxos[m]) > maxUtxo:
        maxUtxo_old = maxUtxo
        maxUtxo = max(utxos[m])
    if max(numberOfInputs[m]) > maxNumberInputs:
        maxNumberInputs_old = maxNumberInputs
        maxNumberInputs = max(numberOfInputs[m])
    poolSizes_max.append(max(poolSize[m]))
    utxos[m].sort(reverse=True)




maxNumberInputsp = 0
maxDepositp = 0
maxTargetp = 0
poolSizes_maxp = []
maxUtxop = 0

meth = ['LIFO', 'LVF', 'Greedy', 'Knapsack', 'Branch and Bound']

for m in meth:
    utxosp[m].sort(reverse=False)
    utxosp[m].pop()
for m in methods:
    if max(utxosp[m]) > maxUtxop:
        maxUtxo_oldp = maxUtxop
        maxUtxop = max(utxosp[m])
    if max(numberOfInputsp[m]) > maxNumberInputsp:
        maxNumberInputs_oldp = maxNumberInputsp
        maxNumberInputsp = max(numberOfInputsp[m])
    poolSizes_maxp.append(max(poolSizep[m]))
    utxosp[m].sort(reverse=True)



fig = plt.figure(constrained_layout = True, figsize=(6, 8))
fig.supxlabel('UTXO values in UTXO pool')
fig.supylabel('Number of each UTXO value')

ax11 = fig.subfigures(5, 2)
# plt.tight_layout()
title = "UTXO Pool Values"

for i in range(5):
    for j in range(2):
        cond = True
        x = 50
        while cond:
            try:
                bins = int((max(utxos[methods[2*i + j]]) - min(utxos[methods[2*i + j]]))/(maxUtxo/x))
                if methods[2*i + j] == 'HVF':
                    ax1, ax2 = ax11[i, j].subplots(2, 1, gridspec_kw={'height_ratios': [1, 3]})
                    ax1.hist(utxos['HVF'], bins=bins, edgecolor="black",alpha=0.8)
                    ax1.hist(utxosp['HVF'], bins=bins, edgecolor="black",alpha=0.8, linestyle='dashed')
                    ax2.hist(utxos['HVF'], bins=bins, edgecolor="black",alpha=0.8)
                    ax2.hist(utxosp['HVF'], bins=bins, edgecolor="black",alpha=0.8, linestyle='dashed')
                    labels = ["Normal", "Poisson"]
                    ax2.legend(labels, loc='lower right',fontsize=8)
                    ax1.set_ylim(1000, 4000)  # outliers only
                    ax2.set_ylim(0, 80)  # most of the data
                    ax1.set_xlim(0, 2000)
                    ax2.set_xlim(0, 2000)
                    ax2.set_yticks(np.arange(0, 81, 20))
                    ax1.set_yticks(np.arange(1000, 4001, 3000))
                    ax1.set_title('HVF', fontsize=10, fontweight='bold', loc='center')
                    # hide the spines between ax and ax2
                    #ax1.spines.bottom.set_visible(False)
                    #ax2.spines.top.set_visible(False)
                    # ax1.xaxis.tick_top()
                    ax1.tick_params(labeltop=False, labelbottom=False)  # don't put tick labels at the top
                    d = .5  # proportion of vertical to horizontal extent of the slanted line
                    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                                  linestyle="dotted", color='k', mec='k', mew=1, clip_on=False)
                    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
                    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)
                    ax1.grid()
                    ax2.grid()
                else:
                    ax1 = ax11[i,j].subplots(1,1)
                    ax1.clear()
                    ax1.grid()
                    #ax1[i,j].set_axisbelow(True)
                    ax1.hist(utxos[methods[2*i + j]], bins=bins, edgecolor="black",alpha=0.8)
                    ax1.hist(utxosp[methods[2 * i + j]], bins=bins, edgecolor="black",alpha=0.8, linestyle='dashed')
                    labels = ["Normal", "Poisson"]
                    ax1.legend(labels, loc='upper right', fontsize=8)
                    ax1.set_xlim([0, 2000])
                    ax1.set_ylim([0, 120])
                    ax1.set_yticks(np.arange(0, 121, 20))
                    #ax1[i,j].set_ylabel('Frequency')
                    #plt.yticks(np.arange(0, 121, 20))
                    #ax1[i,j].set_xlabel('Values of UTXOs in UTXO Pool')
                    ax1.set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold', loc='center')
                    # if methods[2*i + j] == 'HVF':
                    #     rects = ax1[i,j].patches
                    #     rects[0].set_color('g')
                    #     ax1[i, j].plot(rects[0].xy[0] + rects[0].get_width() / 2, 110, 'y*')
                cond = False

            except:
                x = 2*x

plt.show()
fig.savefig(f'Plots5_merge/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")
