import pickle
import matplotlib.pyplot as plt
import datetime
import numpy as np

with open('var6.pkl', 'rb') as f:
    utxos, balance,  poolSize, numberOfInputs, deposits, targets = pickle.load(f)

iterations = 10000
print(utxos['LIFO'])

methods = ['FIFO', 'LIFO', 'HVF', 'LVF', 'HPF', 'Greedy', 'Random Draw', 'Random Improve', 'Knapsack', 'Branch and Bound']

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = -13

maxUtxo = 0
maxNumberInputs = 0
maxDeposit = 0
maxTarget = 0
poolSizes_max = []
for m in methods:
    if max(utxos[m]) > maxUtxo:
        maxUtxo_old = maxUtxo
        maxUtxo = max(utxos[m])
    if max(numberOfInputs[m]) > maxNumberInputs:
        maxNumberInputs_old = maxNumberInputs
        maxNumberInputs = max(numberOfInputs[m])
    poolSizes_max.append(max(poolSize[m]))
    utxos[m].sort(reverse=True)


poolSizes_max.sort(reverse=False)






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


fig1, ax1 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "UTXO Pool Values"
for i in range(5):
    for j in range(2):
        cond = True
        x = 50
        while cond:
            try:
                bins = int((max(utxos[methods[2*i + j]]) - min(utxos[methods[2*i + j]]))/(maxUtxo/x))
                ax1[i,j].clear()
                ax1[i,j].grid()
                #ax1[i,j].set_axisbelow(True)
                ax1[i,j].hist(utxos[methods[2*i + j]], bins=bins, edgecolor="black")
                ax1[i,j].set_xlim([0, 2000])
                plt.yticks(np.arange(0, 121, 20))
                ax1[i, j].set_ylim([0, 120])
                ax1[i,j].set_ylabel('Frequency')
                ax1[i,j].set_xlabel('Values of UTXOs in UTXO Pool')
                ax1[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold', loc='right')
                cond = False
            except:
                x = 2*x
plt.tight_layout()
plt.show()
fig1.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")

fig1, ax1 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "UTXO Pool Values"
for i in range(5):
    for j in range(2):
        cond = True
        x = 50
        while cond:
            try:
                bins = int((max(utxos[methods[2*i + j]]) - min(utxos[methods[2*i + j]]))/(maxUtxo/x))
                ax1[i,j].clear()
                ax1[i,j].grid()
                ax1[i,j].set_axisbelow(True)
                ax1[i,j].hist(utxos[methods[2*i + j]], bins=bins, edgecolor="black")
                ax1[i,j].set_xlim([0, maxUtxo])
                ax1[i,j].set_ylabel('Frequency')
                ax1[i,j].set_xlabel('Values of UTXOs in UTXO Pool')
                ax1[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold', loc='right')
                cond = False
            except:
                x = 2*x
plt.tight_layout()
plt.show()
fig1.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}_original.jpg', format="jpg")


fig2, ax2 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "Number of Input UTXOs"


for i in range(5):
    for j in range(2):
        cond = True
        x = 50
        while cond:
            try:
                bins = int((max(numberOfInputs[methods[2*i + j]]) - min(numberOfInputs[methods[2*i + j]]))/(maxNumberInputs/x))
                ax2[i,j].clear()
                ax2[i,j].grid()
                ax2[i,j].hist(numberOfInputs[methods[2*i + j]], bins=bins, edgecolor="black")
                ax2[i,j].set_xlim([0, 40])
                ax2[i, j].set_ylim([0,8000])
                plt.xticks(np.arange(0, 41, 5))
                plt.yticks(np.arange(0, 8001, 2000))
                ax2[i,j].set_ylabel('Frequency')
                ax2[i,j].set_xlabel('Number of Input UTXOs')
                ax2[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold', loc='right')
                cond = False
            except:
                x = 2*x
plt.tight_layout()
plt.show()
print(maxNumberInputs_old)
fig2.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


fig3, ax3 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "UTXO Pool Size"

poolSizes_max.remove(max(poolSizes_max))
for i in range(5):
    for j in range(2):
        ax3[i,j].clear()
        ax3[i,j].grid()
        ax3[i,j].plot(poolSize[methods[2*i + j]])
        ax3[i, j].set_xlim([0, iterations])
        #ax3[i, j].set_ylim([0, max(poolSizes_max)])
        ax3[i, j].set_ylim([0, 250])
        plt.yticks(np.arange(0, 251, 50))
        ax3[i,j].set_ylabel('UTXO Pool Size')
        ax3[i,j].set_xlabel('Iterations')
        ax3[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold', loc='right')
plt.tight_layout()
plt.show()
fig3.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


fig33, ax33 = plt.subplots(1, 1, figsize=(5,4), sharey=True)
title = "UTXO Pool Size HVF"
ax33.clear()
ax33.grid()
ax33.plot(poolSize['HVF'])
ax33.set_xlim([0, iterations])
ax33.set_ylim([0, 2000])
ax33.set_ylabel('UTXO Pool Size')
ax33.set_xlabel('Iterations')
ax33.set_title('HVF', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.show()
fig33.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


fig4, ax4 = plt.subplots(1, 1, figsize=(5, 4), sharey=True)
title = "UTXO Pool Balance"


ax4.clear()
ax4.grid()
ax4.plot(balance[methods[0]])
ax4.set_xlim([0, iterations])
ax4.set_ylim([0, 140000])
plt.yticks(np.arange(0, 140001, 20000))
ax4.set_ylabel('UTXO Pool Balance')
ax4.set_xlabel('Iterations')
plt.tight_layout()
plt.show()
fig4.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")



fig5, ax5 = plt.subplots(1, 1, figsize=(5, 4), sharey=True)
title = "Deposits and Targets"


ax5.clear()
ax5.grid()
ax5.hist(deposits, label="Deposits", bins=20, edgecolor="black")
ax5.hist(targets, label="Targets", bins=20, edgecolor="black")
ax5.set_xlabel('Values of Deposits/Targets')
ax5.set_ylabel('Frequency')
ax5.set_xlim([0, 5000])
ax5.set_ylim([0, 5000])
plt.xticks(np.arange(0, 5001, 1000))
plt.legend()
plt.tight_layout()
plt.show()
fig5.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")

