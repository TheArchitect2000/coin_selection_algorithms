import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 100000
iterations = 100000
utxos = [N]

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(8, 8), sharey=False)
poolsize = [len(utxos)]
numberOfInputs = []
balance = []

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

    rem = t
    utxos.sort(reverse=False)
    pay = 0
    num = 0
    while rem-pay > 0:
            num = num + 1
            pay = pay + utxos.pop()

    change = pay - t
    if change != 0:
        utxos.append(change)

    deposit = np.random.normal(1000, 250, 3)
    for j in range(3):
        while deposit[j] < 0 or deposit[j] > N:
            deposit[j] = abs(np.random.normal(1000, 250, 1))[0]
        utxos.append(deposit[j])
    poolsize.append(len(utxos))
    numberOfInputs.append(num)


ax1.clear()
ax1.hist(utxos)
ax1.set_xlim([0,2*max(utxos)])
ax1.set_ylabel('Frequency')
ax1.set_xlabel('Values of UTXOs in UTXO Pool')

ax2.clear()
ax2.plot(poolsize)
ax2.set_xlim([0,iterations])
ax2.set_ylabel('UTXO Pool Size')
ax2.set_xlabel('Iterations')

# ax22 = ax2.twinx()
# ax22.clear()
# ax22.plot(balance, 'r')
# ax22.set_xlim([0,iterations])
# ax22.set_ylim([0,1300000])
# ax22.set_ylabel('UTXO Pool Balance')
# ax22.set_xlabel('Iterations')

ax3.clear()
ax3.plot(balance)
ax3.set_xlim([0,iterations])
ax3.set_ylabel('UTXO Pool Balance')
ax3.set_xlabel('Iterations')

ax4.clear()
ax4.hist(numberOfInputs)
ax4.set_xlim([0,30])
ax4.set_ylim([0, iterations])
ax4.set_ylabel('Frequency')
ax4.set_xlabel('# Input UTXOs')
plt.show()

print(sum(utxos))
utxos.sort(reverse=False)
print(utxos)
