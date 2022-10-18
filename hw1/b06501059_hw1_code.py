import numpy as np
import matplotlib.pyplot as plt

# Parameters
temp = 27 + 273.15
bw = 10 * 10 ** 6
P_T = 33
G_T = G_R = 14
h_t = 51.5
h_r = 1.5
sigma = 6
mu = 0

receivedPower = np.zeros(1001) + P_T - 30 + G_T + G_R
g = np.ones(1001) * ((h_r * h_t) ** 2)
dist = np.arange(1001, dtype=np.int32) * 0.1
noise = 10 * np.log10(np.ones(1001) * 1.38 * 10 ** -23 * temp * bw)
S = np.random.normal(mu, sigma, 1001)

g[0] = np.inf
for i in range(len(g) - 1):
    g[i + 1] /= ((i + 1) * 0.1) ** 4
receivedPower += 10 * np.log10(g)

# plt.figure(1)
plt.subplot(2, 2, 1)
plt.plot(dist, receivedPower)
plt.title('Problem 1-1')
plt.xlabel('Distance (m)')
plt.ylabel('Received power of the mobile device (dB)')
plt.xlim(0, 100)
plt.grid(True)

# plt.figure(2)
plt.subplot(2, 2, 2)
plt.plot(dist, receivedPower - noise)
plt.title('Problem 1-2')
plt.xlabel('Distance (m)')
plt.ylabel('SINR of the mobile device (dB)')
plt.xlim(0, 100)
plt.grid(True)

# plt.figure(3)
plt.subplot(2, 2, 3)
plt.plot(dist, receivedPower + S)
plt.title('Problem 2-1')
plt.xlabel('Distance (m)')
plt.ylabel('Received power of the mobile device (dB)')
plt.xlim(0, 100)
plt.grid(True)

# plt.figure(4)
plt.subplot(2, 2, 4)
plt.plot(dist, receivedPower + S - noise)
plt.title('Problem 2-2')
plt.xlabel('Distance (m)')
plt.ylabel('SINR of the mobile device (dB)')
plt.xlim(0, 100)
plt.grid(True)

plt.tight_layout()
plt.show()