import numpy as np
import matplotlib.pyplot as plt

def random_gen():
    x, y = np.random.uniform(-500 / 3 ** 0.5, 289), np.random.uniform(-250, 251)
    if x > 500 / 3 ** 0.5 or y > 250 or (abs(3 ** 0.5 * x) + abs(y) > 500):
        return random_gen()
    else:
        return x, y

def random_arr_gen():
    x = np.empty(50)
    y = np.empty(50)
    for i in range(50):
        x[i], y[i] = random_gen()
    return x, y

temp = 27 + 273.15
bw = 10 * 10 ** 6
P_T = 33
P_R = 23
G_T = G_R = 14
h_t = 51.5
h_r = 1.5
x_interval = 1.5 * 500 / 3 ** 0.5
y_interval = 500
CBS = {"Xl": 0.4e6, "Xm": 0.7e6, "Xh": 1e6}
Poisson = {"lamda_l": 0.4e6, "lamda_m": 0.7e6, "lamda_h": 1e6}
T = 1000

x_boud = np.array([x_interval / 3, x_interval / 1.5, x_interval / 3, -x_interval / 3, 
                    -x_interval / 1.5, -x_interval / 3, x_interval / 3])
y_boud = np.array([y_interval / 2, 0, -y_interval / 2, -y_interval / 2, 0, y_interval / 2, y_interval / 2])

BS_x_coord = np.array([-2 * x_interval, -2 * x_interval, -2 * x_interval, -x_interval, -x_interval, 
            -x_interval, -x_interval, 0, 0, 0, 0, x_interval, x_interval, x_interval, x_interval, 
            2 * x_interval, 2 * x_interval, 2 * x_interval, 0])
BS_y_coord = np.array([-y_interval, 0, y_interval, -1.5 * y_interval, -0.5 * y_interval, 0.5 * y_interval,
            1.5 * y_interval, -2 * y_interval, -y_interval, y_interval, 2 * y_interval, 
            -1.5 * y_interval, -0.5 * y_interval, 0.5 * y_interval, 1.5 * y_interval, -y_interval, 0,
            y_interval, 0])

x_coord, y_coord = random_arr_gen()

receivedPower = np.zeros(50) + P_T - 30 + G_T + G_R
g = np.ones(50) * ((h_r * h_t) ** 2)
dist = np.sqrt(x_coord ** 2 + y_coord ** 2)
noise = np.ones(50) * 1.38 * 10 ** -23 * temp * bw
for i in range(50):
    g[i] /= dist[i] ** 4
receivedPower += 10 * np.log10(g)
interference = np.zeros(50)
interferenceGain = 10 ** ((P_T - 30) / 10) * 10 ** (G_T / 10) * 10 ** (G_R / 10)
for i in range(50):
    for j in range(18):
        interference[i] += interferenceGain * (h_r * h_t) ** 2 / ((x_coord[i] - BS_x_coord[j]) ** 2 + \
            (y_coord[i] - BS_y_coord[j]) ** 2) ** 2
IN = 10 * np.log10(interference + noise)
SINR = 10 ** ((receivedPower - IN) / 10)
ShannonCapacity = np.ones(50) * bw / 50
for i in range(50):
    ShannonCapacity[i] *= np.log2(1 + SINR[i])
# buffer = np.ones((3, 50)) * 6e6
buffer = np.ones(3) * 6e6
# loss = np.zeros((3, 50))
loss = np.zeros(3)
bufferRecord = np.zeros(50)
for idx, rate in enumerate(CBS.values()):
    for i in range(T):
        for j in range(50):
            if buffer[idx] == 6e6:
                if rate <= ShannonCapacity[j]:
                    continue
                else:
                    buffer[idx] -= int(rate - ShannonCapacity[j]) + 1
                    bufferRecord[j] += int(rate - ShannonCapacity[j]) + 1
                    if buffer[idx] < 0:
                        loss[idx] += -buffer[idx]
                        bufferRecord[j] += buffer[idx]
                        buffer[idx] = 0  
            else:
                if bufferRecord[j] <= ShannonCapacity[j]:
                    # temp = 6e6 - buffer[idx]
                    buffer[idx] += bufferRecord[j]                                       
                    if rate + bufferRecord[j] <= ShannonCapacity[j]:
                        bufferRecord[j] = 0
                    else:
                        buffer[idx] -= int(rate + bufferRecord[j] - ShannonCapacity[j]) + 1
                        bufferRecord[j] = int(rate + bufferRecord[j] - ShannonCapacity[j]) + 1
                        if buffer[idx] < 0:
                            loss[idx] += -buffer[idx]
                            bufferRecord[j] += buffer[idx]
                            buffer[idx] = 0                                
                else:
                    bufferRecord[j] -= int(ShannonCapacity[j])
                    buffer[idx] += int(ShannonCapacity[j])
                    bufferRecord[j] += rate
                    buffer[idx] -= rate
                    if buffer[idx] < 0:
                        loss[idx] += -buffer[idx]
                        bufferRecord[j] += buffer[idx]
                        buffer[idx] = 0 
lossProbability = loss / (np.array(list(CBS.values())) * 50 * T)

# plt.figure(1)
plt.subplot(2, 3, 1)
plt.scatter(x_coord, y_coord)
plt.scatter(0, 0, color='red')
plt.plot(x_boud, y_boud, color='black')
plt.title('Problem 1-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)

# plt.figure(2)
plt.subplot(2, 3, 2)
plt.scatter(dist, ShannonCapacity)
plt.title('Problem 1-2')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('Shannon Capacity of the mobile device (bits/s)')
plt.grid(True)

# plt.figure(3)
plt.subplot(2, 3, 3)
x = np.arange(len(lossProbability))
plt.bar(x, lossProbability)
plt.title('Problem 1-3')
plt.xticks(x, ['${X_l}$', '${X_m}$', '${X_h}$'])
plt.xlabel('The traffic load (bits/s)')
plt.ylabel('Bits loss probability')
plt.grid(True)
# plt.show()

x_coord, y_coord = random_arr_gen()

receivedPower = np.zeros(50) + P_T - 30 + G_T + G_R
g = np.ones(50) * ((h_r * h_t) ** 2)
dist = np.sqrt(x_coord ** 2 + y_coord ** 2)
noise = np.ones(50) * 1.38 * 10 ** -23 * temp * bw
for i in range(50):
    g[i] /= dist[i] ** 4
receivedPower += 10 * np.log10(g)
interference = np.zeros(50)
interferenceGain = 10 ** ((P_T - 30) / 10) * 10 ** (G_T / 10) * 10 ** (G_R / 10)
for i in range(50):
    for j in range(18):
        interference[i] += interferenceGain * (h_r * h_t) ** 2 / ((x_coord[i] - BS_x_coord[j]) ** 2 + \
            (y_coord[i] - BS_y_coord[j]) ** 2) ** 2
IN = 10 * np.log10(interference + noise)
SINR = 10 ** ((receivedPower - IN) / 10)
ShannonCapacity = np.ones(50) * bw / 50
for i in range(50):
    ShannonCapacity[i] *= np.log2(1 + SINR[i])
# buffer = np.ones((3, 50)) * 6e6
buffer = np.ones(3) * 6e6
# loss = np.zeros((3, 50))
loss = np.zeros(3)
# totalBits = 0
bufferRecord = np.zeros(50)
for idx, lam in enumerate(Poisson.values()):
    totalBits = 0
    for i in range(T):
        rate = np.random.poisson(lam, size=50)
        totalBits += np.sum(rate, dtype=np.int64)
        for j in range(50):
            if buffer[idx] == 6e6:
                if rate[j] <= ShannonCapacity[j]:
                    continue
                else:
                    buffer[idx] -= int(rate[j] - ShannonCapacity[j]) + 1
                    bufferRecord[j] += int(rate[j] - ShannonCapacity[j]) + 1
                    if buffer[idx] < 0:
                        loss[idx] += -buffer[idx]
                        bufferRecord[j] += buffer[idx]
                        buffer[idx] = 0  
            else:
                if bufferRecord[j] <= ShannonCapacity[j]:
                    # temp = 6e6 - buffer[idx]
                    buffer[idx] += bufferRecord[j]                                       
                    if rate[j] + bufferRecord[j] <= ShannonCapacity[j]:
                        bufferRecord[j] = 0
                    else:
                        buffer[idx] -= int(rate[j] + bufferRecord[j] - ShannonCapacity[j]) + 1
                        bufferRecord[j] = int(rate[j] + bufferRecord[j] - ShannonCapacity[j]) + 1
                        if buffer[idx] < 0:
                            loss[idx] += -buffer[idx]
                            bufferRecord[j] += buffer[idx]
                            buffer[idx] = 0                                
                else:
                    bufferRecord[j] -= int(ShannonCapacity[j])
                    buffer[idx] += int(ShannonCapacity[j])
                    bufferRecord[j] += rate[j]
                    buffer[idx] -= rate[j]
                    if buffer[idx] < 0:
                        loss[idx] += -buffer[idx]
                        bufferRecord[j] += buffer[idx]
                        buffer[idx] = 0 
    lossProbability[idx] = loss[idx] / totalBits
# lossProbability = loss / totalBits

# plt.figure(4)
plt.subplot(2, 3, 4)
plt.scatter(x_coord, y_coord)
plt.scatter(0, 0, color='red')
plt.plot(x_boud, y_boud, color='black')
plt.title('Problem B-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)

# plt.figure(5)
plt.subplot(2, 3, 5)
plt.scatter(dist, ShannonCapacity)
plt.title('Problem B-2')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('Shannon Capacity of the mobile device (bits/s)')
plt.grid(True)

# plt.figure(6)
plt.subplot(2, 3, 6)
x = np.arange(len(lossProbability))
plt.bar(x, lossProbability)
plt.title('Problem B-3')
plt.xticks(x, ['${𝜆_l}$', '${𝜆_m}$', '${𝜆_h}$'])
plt.xlabel('The traffic load (bits/s)')
plt.ylabel('Bits loss probability')
plt.grid(True)

plt.tight_layout()
plt.show()