import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle

mc = 1
f = 0
costPerOutput = 0
costPerInput = 0
costOfHeader = 0
matchRange = costPerInput + costPerOutput
def BnBRecursion(d,currentSelection, rounds):
    rounds = rounds - 1
    currSel = currentSelection.copy()
    utxosSorted = [u for u in utxos[m] if u not in currSel or currSel.remove(u)]
    utxosSorted.sort(reverse=False)
    if sum(currentSelection) > t:
        return currentSelection
    elif sum(currentSelection) > t + matchRange:
        return []
    elif rounds <= 0:
        return []
    elif d >= len(utxosSorted):
        return []

    randInt = np.random.randint(0, 2)
    randBool = bool(randInt)
    if randBool:
        currentSelection.append(utxosSorted[d])
        withThis = BnBRecursion(d+1, currentSelection, rounds)
        if len(withThis)>0:
            return withThis
        else:
            currentSelection.pop()
            withoutThis = BnBRecursion(d+1, currentSelection, rounds)
            if len(withoutThis) > 0:
                return withoutThis


    else:
        withoutThis = BnBRecursion(d + 1, currentSelection, rounds)
        if len(withoutThis) > 0:
            return withoutThis
        else:
            currentSelection.append(utxosSorted[d])
            withThis = BnBRecursion(d+1, currentSelection, rounds)
            if len(withThis) > 0:
                return withThis

    return currentSelection



N = 100000
iterations = 10000
numDeposits = 3
targets = []
deposits = []



#methods = ['FIFO', 'LIFO','HVF', 'LVF', 'HPF', 'Greedy', 'Random Draw', 'Random Improve', 'Knapsack', 'Branch and Bound']

methods = ['FIFO', 'LIFO', 'HVF', 'LVF', 'HPF', 'Greedy', 'Random Draw', 'Random Improve', 'Knapsack', 'Branch and Bound']
utxos = {}
balance = {}
numberOfInputs = {}
poolSize = {}


for m in methods:
    utxos[m] = [N]
    balance[m] = []
    numberOfInputs[m] = []
    poolSize[m] = []

for it in range(0, iterations):
    print(str(it) + f'/{iterations}')

    deposit = np.random.poisson(1000, numDeposits)
    for j in range(numDeposits):
        while deposit[j] < 0:
            deposit[j] = abs(np.random.poisson(1000, 1))[0]
        deposits.append(deposit[j])

    minBalance = 100000000
    for m in methods:
        balance[m].append(sum(utxos[m]))
        poolSize[m].append(len(utxos[m]))
        if balance[m][-1] < minBalance:
            minBalance = balance[m][-1]


    # Uniform
    # t = np.random.uniform(1, 1000)

    # Poisson
    # t = np.random.poisson(lam=1000,size=1)[0]

    # Normal
    t = abs(np.random.poisson(3000,1))[0]
    while t < 0 or t > minBalance:
        t = abs(np.random.poisson(3000, 1))[0]
    targets.append(t)

    #################### FIFO Algorithm ####################
    m = 'FIFO'
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        num = num + 1
        pay = pay + utxos[m].pop()

    change = pay - t
    if change != 0:
        utxos[m].insert(0, change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### LIFO Algorithm ####################
    m = 'LIFO'
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        num = num + 1
        pay = pay + utxos[m].pop()

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### HVF Algorithm ####################
    m = 'HVF'
    utxos[m].sort(reverse=False)
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        num = num + 1
        pay = pay + utxos[m].pop()

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### LVF Algorithm ####################
    m = 'LVF'
    utxos[m].sort(reverse=True)
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        num = num + 1
        pay = pay + utxos[m].pop()

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### HPF Algorithm ####################
    m = 'HPF'
    priority = []

    # Sort utxo[m] by priority
    for i in range(len(utxos[m])):
        priority.append(utxos[m][i] * i)
    for k in range(len(utxos[m])):
        for j in range(len(utxos[m]) - 1):
            if priority[j] > priority[j+1]:
                utxos[m][j], utxos[m][j + 1] = utxos[m][j + 1], utxos[m][j]
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        num = num + 1
        pay = pay + utxos[m].pop()

    change = pay - t
    if change != 0:
        utxos[m].insert(0, change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### Greedy Algorithm ####################
    m = 'Greedy'
    rem = t
    utxos[m].sort(reverse=False)
    pay = 0
    num = 0
    Selected = []
    for i in range(len(utxos[m]) - 1, -1, -1):
        if utxos[m][i] <= rem and rem > 0:
            num = num + 1
            pay = pay + utxos[m][i]
            Selected.append(utxos[m][i])
            rem = rem - utxos[m][i]
        if rem <= 0:
            break

    utxos[m] = [u for u in utxos[m] if u not in Selected or Selected.remove(u)]
    utxos[m].sort(reverse=True)
    while rem > 0:
        num = num + 1
        minUtxo = utxos[m].pop()
        pay = pay + minUtxo
        rem = rem - minUtxo

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### Random Draw Algorithm ####################
    m = 'Random Draw'
    rem = t
    pay = 0
    num = 0
    while rem - pay > 0:
        idx = np.random.randint(0, len(utxos[m]))
        num = num + 1
        val = utxos[m][idx]
        del utxos[m][idx]
        pay = pay + val

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### Random Improve Algorithm ####################
    m = 'Random Improve'
    rem = t
    pay = 0
    pay2 = 0
    num = 0
    Selected = []
    bestSet = []
    while rem - sum(Selected) > 0:
        rand = np.random.choice(utxos[m])
        num = num + 1
        Selected.append(rand)
        utxos[m].remove(rand)

    # Improve Phase:
    #utxos[m] = [u for u in utxos[m] if u not in Selected or Selected.remove(u)]
    cond = True
    while cond:
        bestSet = Selected.copy()
        if len(utxos[m]) == 0:
            cond = False
            break
        rand = np.random.choice(utxos[m])
        Selected.append(rand)
        num = num + 1
        if abs(2 * t - sum(Selected)) > abs(2 * t - sum(bestSet)) or sum(Selected) > 3 * t:
            cond = False
            num = num - 1
            break
        utxos[m].remove(rand)

    change = sum(bestSet) - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### Knapsack Algorithm ####################
    m = 'Knapsack'
    utxos[m].sort(reverse=True)
    rem = t
    pay = 0
    num = 0
    targetReached = False
    Selected = []
    bestSet = []
    bestVal = 10000000000
    for j in range(2):
        if not targetReached:
            for u in utxos[m]:
                randInt = np.random.randint(0, 2)
                randBool = bool(randInt)
                if (j == 0 and randBool) or (j == 1 and u not in Selected):
                    num = num + 1
                    Selected.append(u)
                    if sum(Selected) == t:
                        targetReached = True
                        bestSet = Selected.copy()
                        break
                    if sum(Selected) > t:
                        targetReached = True
                        if sum(Selected) < bestVal:
                            bestVal = sum(Selected)
                            bestSet = Selected.copy()
                            Selected.pop()
                            num = num - 1
    if len(Selected) < len(bestSet):
        num = num + 1
    bS = bestSet.copy()
    utxos[m] = [u for u in utxos[m] if u not in bS or bS.remove(u)]
    pay = sum(bestSet)

    change = pay - t
    if change != 0:
        utxos[m].append(change)

    numberOfInputs[m].append(num)
    #######################################################
    #################### Branch and Bound Algorithm ####################
    m = 'Branch and Bound'
    utxos[m] = [u-f for u in utxos[m]]
    t = t + costOfHeader + costPerOutput
    rem = t
    rounds = 1000
    d = 0
    currentSelection = []

    currentSelection = BnBRecursion(d, currentSelection, rounds)

    if len(currentSelection) == 0:
        while rem - sum(currentSelection) > 0:
            rand = np.random.choice(utxos[m])
            currentSelection.append(rand)
            utxos[m].remove(rand)

    change = sum(currentSelection) - t
    if change != 0:
        utxos[m].append(change-f)
    currSel = currentSelection.copy()
    utxos[m] = [u for u in utxos[m] if u not in currSel or currSel.remove(u)]

    numberOfInputs[m].append(len(currentSelection))
    #######################################################

    ## Add deposits to utxo pools:
    for m in methods:
        if m == "FIFO" or m == "HPF":
            for j in range(numDeposits):
                utxos[m].insert(0, deposit[j])
        elif m == "Branch and Bound":
            for j in range(numDeposits):
                utxos[m].append(deposit[j]-f)
        else:
            for j in range(numDeposits):
                utxos[m].append(deposit[j])

for m in methods:
    print(m + " utxo_max: " + str(max(utxos[m])))
    print(m + ":  pool_size_max: " + str(max(poolSize[m])))
    print(m + ":  inputs_max: " + str(max(numberOfInputs[m])))

plt.rcParams['axes.titley'] = 1.0    # y is in axes-relative coordinates.
plt.rcParams['axes.titlepad'] = -13

fig1, ax1 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "UTXO Pool Values"


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

poolSizes_max.sort(reverse=False)


# Saving the objects:
with open('var12_pois.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([utxos, balance, poolSize, numberOfInputs, deposits, targets], f)

# # Getting back the objects:
# with open('var.pkl') as f:  # Python 3: open(..., 'rb')
#     utxos, poolSize, numberOfInputs, deposits, targets = pickle.load(f)

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
                ax1[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold')
                cond = False
            except:
                x = 2*x
plt.tight_layout()
plt.show()
fig1.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


fig2, ax2 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "Number of Input UTXOs"

numberOfInputs['HVF'].pop()
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
                ax2[i,j].set_xlim([0, maxNumberInputs])
                ax2[i,j].set_ylabel('Frequency')
                ax2[i,j].set_xlabel('Number of Input UTXOs')
                ax2[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold')
                cond = False
            except:
                x = 2*x
plt.tight_layout()
plt.show()
fig2.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")
print(f"max number of inputs is: {maxNumberInputs}")

fig3, ax3 = plt.subplots(5, 2, figsize=(6, 8), sharey=True)
title = "UTXO Pool Size"


for i in range(5):
    for j in range(2):
        ax3[i,j].clear()
        ax3[i,j].grid()
        ax3[i,j].plot(poolSize[methods[2*i + j]])
        ax3[i,j].set_xlim([0, iterations])
        ax3[i, j].set_ylim([0, poolSizes_max[-2]])
        ax3[i,j].set_ylabel('UTXO Pool Size')
        ax3[i,j].set_xlabel('Iterations')
        ax3[i,j].set_title(f'{methods[2*i + j]}', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.show()
fig3.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")

fig33, ax33 = plt.subplots(1, 1, figsize=(5,4), sharey=True)
title = "UTXO Pool Size"
ax33.clear()
ax33.grid()
ax33.plot(poolSize['HVF'])
ax33.set_xlim([0, iterations])
ax33.set_ylabel('UTXO Pool Size')
ax33.set_xlabel('Iterations')
ax33.set_title('HVF', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.show()
fig3.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


fig4, ax4 = plt.subplots(1, 1, figsize=(5, 4), sharey=True)
title = "UTXO Pool Balance"


ax4.clear()
ax4.grid()
ax4.plot(balance[methods[2*i + j]])
ax4.set_xlim([0, iterations])
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
plt.legend()
plt.tight_layout()
plt.show()
fig5.savefig(f'Plots_EqualDepositTarget2/{title}_{iterations}_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")





#fig.savefig(f'Plots/Normal_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")
