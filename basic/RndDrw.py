import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

N = 100000
iterations = 20000
utxos = [N]

fig, ax = plt.subplots(3,2, figsize=(14,9), sharey=False)
poolsize = [len(utxos)]
numberOfInputs = []
balance = []

targets = []
deposits = []

for i in range(1,iterations):

    balance.append(sum(utxos))
    # Uniform
    # t = np.random.uniform(1, 1000)

    # Poisson
    # t = np.random.poisson(lam=1000,size=1)[0]

    # Normal
    t = abs(np.random.normal(3000,500,1))[0]
    while t<0 or t>balance[-1]:
        t = abs(np.random.normal(3000, 500, 1))[0]
    targets.append(t)
    rem = t
    pay = 0
    num = 0
    while rem-pay > 0:
        idx = np.random.randint(0,len(utxos))
        num = num + 1
        val = utxos[idx]
        del utxos[idx]
        pay = pay + val

    change = pay - t
    if change != 0:
        utxos.append(change)

    deposit = np.random.normal(1000, 250, 3)
    for j in range(3):
        while deposit[j] < 0:
            deposit[j] = abs(np.random.normal(1000, 250, 1))[0]
        deposits.append(deposit[j])
        utxos.append(deposit[j])
    poolsize.append(len(utxos))
    numberOfInputs.append(num)




ax[0,0].clear()
ax[0,0].grid()
ax[0,0].hist(utxos, bins=20, edgecolor="black")
ax[0,0].set_xlim([0,max(utxos)])
ax[0,0].set_ylabel('Frequency')
ax[0,0].set_xlabel('Values of UTXOs in UTXO Pool')


ax[0,1].clear()
ax[0,1].grid()
ax[0,1].hist(numberOfInputs, bins=20, edgecolor="black")
ax[0,1].set_xlim([0,max(numberOfInputs)])
ax[0,1].set_ylim([0, iterations])
ax[0,1].set_ylabel('Frequency')
ax[0,1].set_xlabel('Number of Input UTXOs')

ax[1,0].clear()
ax[1,0].grid()
ax[1,0].plot(poolsize)
ax[1,0].set_xlim([0,iterations])
ax[1,0].set_ylabel('UTXO Pool Size')
ax[1,0].set_xlabel('Iterations')


ax[1,1].clear()
ax[1,1].grid()
ax[1,1].plot(balance)
ax[1,1].set_xlim([0,iterations])
ax[1,1].set_ylabel('UTXO Pool Balance')
ax[1,1].set_xlabel('Iterations')


ax[2,0].clear()
ax[2,0].grid()
ax[2,0].hist(deposits, bins=20, edgecolor="black")
ax[2,0].set_xlim([0,max(deposits)])
ax[2,0].set_ylabel('Frequency')
ax[2,0].set_xlabel('Values of Deposits')

ax[2,1].clear()
ax[2,1].grid()
ax[2,1].hist(targets, bins=20, edgecolor="black")
ax[2,1].set_xlim([0,max(targets)])
ax[2,1].set_ylabel('Frequency')
ax[2,1].set_xlabel('Values of Payments')


plt.show()
fig.savefig(f'Plots/Normal-RandomDraw_{datetime.datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.jpg', format="jpg")


print(sum(utxos))
utxos.sort(reverse=False)
print(utxos)
