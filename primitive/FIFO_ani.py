import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 10000
iterations = 500
utxos = [N]
#fig, ax = plt.subplots()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8, 8), sharey=False)
poolsize = [len(utxos)]
numberOfInputs = []
balance = []

def animate(i):
    ax1.clear()
    ax1.hist(utxos)
    ax1.set_xlim([0, N])
    ax1.set_ylabel('UTXOs')

    ax2.clear()
    ax2.plot(poolsize)
    ax2.set_xlim([0, iterations])
    ax2.set_ylabel('UTXO Pool Size')

    ax3.clear()
    ax3.plot(balance)
    ax3.set_xlim([0, iterations])
    ax3.set_ylabel('UTXO Pool Balance')

    ax4.clear()
    ax4.hist(numberOfInputs)
    ax4.set_xlim([0, 30])
    ax4.set_ylim([0, iterations])
    ax4.set_ylabel('# Input UTXOs')

    # Uniform
    t = np.random.uniform(1, 1000)

    # Poisson
    # t = np.random.poisson(lam=1000,size=1)[0]

    # Normal
    # t = abs(np.random.normal(3000,1000,1))[0]
    # while t<0 or t>N:
    #     t = abs(np.random.normal(3000, 1000, 1))[0]

    rem = t
    pay = 0
    num = 0
    while rem-pay > 0:
        num = num + 1
        pay = pay + utxos.pop()

    change = pay - t
    if change != 0:
        utxos.insert(0, change)
    balance.append(sum(utxos))
    utxos.insert(0, t)
    poolsize.append(len(utxos))
    numberOfInputs.append(num)

ani = FuncAnimation(fig, animate, frames=iterations, interval=1, repeat=False)
plt.show()

print(sum(utxos))
utxos.sort(reverse=False)
print(utxos)