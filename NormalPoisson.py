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



fig3, ax3 = plt.subplots(5, 2, figsize=(6, 8))
title = "UTXO Pool Size"

poolSizes_max.remove(max(poolSizes_max))
for i in range(5):
    for j in range(2):
        ax3[i,j].clear()
        ax3[i,j].grid()
        ax3[i,j].plot(poolSize[methods[2*i + j]])
        ax3[i, j].plot(poolSizep[methods[2 * i + j]])
        labels = ["Normal", "Poisson"]
        if methods[2 * i + j] == 'FIFO' or methods[2 * i + j] == 'LIFO' or methods[2 * i + j] == 'HPF' or methods[2 * i + j] == 'Random Draw':
            ax3[i, j].legend(labels, loc='lower right', fontsize=8)
        elif methods[2 * i + j] == 'Knapsack':
            ax3[i, j].legend(labels, loc='upper left', fontsize=8)
        else:
            ax3[i, j].legend(labels, loc='upper right', fontsize=8)
        ax3[i, j].set_xlim([0, iterations])
        #ax3[i, j].set_ylim([0, max(poolSizes_max)])
        ax3[i, j].set_ylim([0, 250])
        ax3[i, j].set_yticks(np.arange(0, 251, 50))
        #ax3[i,j].set_ylabel('UTXO Pool Size')
        #ax3[i,j].set_xlabel('Iterations')
        ax3[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold')
fig3.supxlabel('Iteration number')
fig3.supylabel('UTXO pool size')
plt.tight_layout()
plt.show()
fig3.savefig(f'Plots_merge/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")

