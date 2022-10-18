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

plt.figure(1)
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
plt.scatter(dist, receivedPower)
plt.title('Problem 1-2')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('Received power of the mobile device (dB)')
plt.grid(True)

# plt.figure(3)
plt.subplot(2, 3, 3)
plt.scatter(dist, receivedPower - IN)
plt.title('Problem 1-3')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('SINR of the mobile device (dB)')
plt.grid(True)


x_coord, y_coord = random_arr_gen()
receivedPower = np.zeros(50) + P_R - 30 + G_T + G_R
g = np.ones(50) * ((h_r * h_t) ** 2)
dist = np.sqrt(x_coord ** 2 + y_coord ** 2)
for i in range(50):
    g[i] /= dist[i] ** 4
receivedPower += 10 * np.log10(g)
interference = np.zeros(50)
interferenceGain = 10 ** ((P_R - 30) / 10) * 10 ** (G_T / 10) * 10 ** (G_R / 10)
for i in range(50):
    for j in range(50):
        if i != j:
            interference[i] += interferenceGain * (h_r * h_t) ** 2 / (x_coord[j] ** 2 + \
                y_coord[j] ** 2) ** 2
IN = 10 * np.log10(interference + noise)

# plt.figure(4)
plt.subplot(2, 3, 4)
plt.scatter(x_coord, y_coord)
plt.scatter(0, 0, color='red')
plt.plot(x_boud, y_boud, color='black')
plt.title('Problem 2-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)

# plt.figure(5)
plt.subplot(2, 3, 5)
plt.scatter(dist, receivedPower)
plt.title('Problem 2-2')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('Received power of the central BS (dB)')
plt.grid(True)

# plt.figure(6)
plt.subplot(2, 3, 6)
plt.scatter(dist, receivedPower - IN)
plt.title('Problem 2-3')
plt.xlabel('Distance from central BS (m)')
plt.ylabel('SINR of the central BS (dB)')
plt.grid(True)

plt.tight_layout()
# plt.show()

x_coord = []
y_coord = []
dist = np.empty(50 * 19)
for i in range(19):
    x, y = random_arr_gen()
    x_coord.append(x)
    y_coord.append(y)
# x_coord, y_coord = random_arr_gen()
receivedPower = np.zeros(50 * 19) + P_R - 30 + G_T + G_R
g = np.ones(50 * 19) * ((h_r * h_t) ** 2)
noise = np.ones(50 * 19) * 1.38 * 10 ** -23 * temp * bw
# dist[18] = np.sqrt(x_coord ** 2 + y_coord ** 2)
for i in range(19):
    for j in range(50):
        dist[i * 50 + j] = np.sqrt(x_coord[i][j] ** 2 + y_coord[i][j] ** 2)
    # dist[i] = np.sqrt(x_coord[j] ** 2 + y_coord[j] ** 2)
for i in range(50 * 19):
    g[i] /= dist[i] ** 4
receivedPower += 10 * np.log10(g)
interference = np.zeros(50 * 19)
interferenceGain = 10 ** ((P_R - 30) / 10) * 10 ** (G_T / 10) * 10 ** (G_R / 10)
for i in range(19):
    for j in range(50):
        for k in range(50):
            for l in range(19):
                if not((i, j) == (l, k)):
                    interference[i * 50 + j] += interferenceGain * (h_r * h_t) ** 2 / ((x_coord[l][k] + BS_x_coord[l] - BS_x_coord[i]) ** 2 + \
                        (y_coord[l][k] + BS_y_coord[l] - BS_y_coord[i]) ** 2) ** 2
            # if j != k:
            #     interference[i * 50 + j] += interferenceGain * (h_r * h_t) ** 2 / ((x_coord[i][j] - x_coord[i][k]) ** 2 + \
            #         (y_coord[i][j] - y_coord[i][k]) ** 2) ** 2
IN = 10 * np.log10(interference + noise)
print(IN)
plt.figure(2)
# plt.figure(7)
plt.subplot(2, 2, 1)
plt.scatter(x_coord[18], y_coord[18])
plt.scatter(0, 0, color='black')
plt.plot(x_boud, y_boud, color='black')
plt.scatter(BS_x_coord, BS_y_coord, color='black')
for i in range(18):
    # x_coord, y_coord = random_arr_gen()
    plt.scatter(x_coord[i] + BS_x_coord[i], y_coord[i] + BS_y_coord[i])
    plt.plot(x_boud + BS_x_coord[i], y_boud + BS_y_coord[i], color='black')
plt.title('Problem B-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)
# plt.show()

# plt.figure(8)
plt.subplot(2, 2, 3)
plt.scatter(dist, receivedPower)
plt.title('Problem B-2')
plt.xlabel('Distance from the BS (m)')
plt.ylabel('Received power of the BS (dB)')
plt.grid(True)
# plt.show()

# plt.figure(9)
plt.subplot(2, 2, 4)
plt.scatter(dist, receivedPower - IN)
plt.title('Problem B-3')
plt.xlabel('Distance from the BS (m)')
plt.ylabel('SINR of the BS (dB)')
plt.grid(True)

plt.tight_layout()
plt.show()