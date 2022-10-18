from modules import *

def random_gen():
    x, y = np.random.uniform(-500 / 3 ** 0.5, 289), np.random.uniform(-250, 251)
    if x > 500 / 3 ** 0.5 or y > 250 or (abs(3 ** 0.5 * x) + abs(y) > 500):
        return random_gen()
    else:
        return x, y

def random_arr_gen(N, paired=False, pairs=None):
    x = np.empty(N)
    y = np.empty(N)
    if (paired):
        for i in range(N):
            x[i], y[i] = random_gen()
            while ((x[i] - pairs[i][0]) ** 2 + (y[i] - pairs[i][1]) ** 2 > 20 ** 2):
                x[i], y[i] = random_gen()
        return x, y
    for i in range(N):
        x[i], y[i] = random_gen()
    return x, y

def genPairs(MobileStations, N):
    x_coord, y_coord = random_arr_gen(N)
    for i in range(N):
        MobileStations[i] = [MS(x_coord[i], y_coord[i], id=i)]
    x_coord, y_coord = random_arr_gen(N, True, list(zip(x_coord, y_coord)))
    for i in range(N):
        MobileStations[i].append(MS(x_coord[i], y_coord[i], id=i))
        MobileStations[i][0].setPartner(MobileStations[i][1], 1)
        MobileStations[i][1].setPartner(MobileStations[i][0], 0)
        MobileStations[i][0].setCell(BaseStations[10])
        MobileStations[i][1].setCell(BaseStations[10])
    return MobileStations

BaseStations = {}
MobileStations = {}
MapSetup(BaseStations, 5)
for i in [5, 7, 8, 12, 13, 15]:
    BaseStations[10].setNeighbor(BaseStations[i])
MobileStations = genPairs(MobileStations, 75)
# x_coord, y_coord = random_arr_gen()
# for i in range(75):
#     MobileStations[i] = [MS(x_coord[i], y_coord[i], id=i)]
# x_coord, y_coord = random_arr_gen(True, list(zip(x_coord, y_coord)))
# for i in range(75):
#     MobileStations[i].append(MS(x_coord[i], y_coord[i], id=i))
#     MobileStations[i][0].setPartner(MobileStations[i][1], 1)
#     MobileStations[i][1].setPartner(MobileStations[i][0], 0)
#     MobileStations[i][0].setCell(BaseStations[10])
#     MobileStations[i][1].setCell(BaseStations[10])

# Problem 1-1
plt.figure(1)
for value in BaseStations.values():
    if value.id in [5, 7, 8, 10, 12, 13, 15]:
        p1 = plt.scatter(value.x, value.y, c="blue")
for value in MobileStations.values():
    p2 = plt.scatter(value[0].x, value[0].y, c="red")
    p3 = plt.scatter(value[1].x, value[1].y, c="green")
plt.legend([p1, p2, p3], ["Base stations.", "D2D transmitters", "D2D receivers"], loc="upper right")
# plt.subplot(2, 3, 1)
plt.title('Problem 1-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)
map_grid(5)
# plt.show()

# Problem 1-2
# upSINR = np.empty(150)
upSINR = np.empty(75)
for i, ms in enumerate(MobileStations.values()):
    upSINR[i] = BaseStations[10].UPSINR(ms[0])
    # upSINR[i + 75] = BaseStations[10].UPSINR(ms[1])
upSINR = np.sort(upSINR)
# cdfOfupSINR = np.cumsum(upSINR)
cdfOfupSINR = np.arange(len(upSINR)) / float(len(upSINR) - 1)
plt.figure(2)
plt.plot(upSINR, cdfOfupSINR)
plt.title('Problem 1-2-1')
plt.xlabel('Uplink SINR (dB)')
plt.ylabel('CDF')
plt.grid(True)
# plt.show()

# downSINR = np.empty(150)
downSINR = np.empty(75)
for i, ms in enumerate(MobileStations.values()):
    # downSINR[i] = ms[0].SINR(BaseStations[10])
    # downSINR[i + 75] = ms[1].SINR(BaseStations[10])
    downSINR[i] = ms[1].SINR(BaseStations[10])
downSINR = np.sort(downSINR)
cdfOfdownSINR = np.arange(len(downSINR)) / float(len(downSINR) - 1)
plt.figure(3)
plt.plot(downSINR, cdfOfdownSINR)
plt.title('Problem 1-2-2')
plt.xlabel('Downlink SINR (dB)')
plt.ylabel('CDF')
plt.grid(True)
# plt.show()

# Problem 1-3
# ShannonCapacity = np.empty(150)
ShannonCapacity = np.empty(75)
for i, ms in enumerate(MobileStations.values()):
    # ShannonCapacity[i] = ms[0].Shannon(BaseStations[10], divider=150)
    # ShannonCapacity[i + 75] = ms[1].Shannon(BaseStations[10], divider=150)
    ShannonCapacity[i] = ms[1].Shannon(BaseStations[10], divider=75)
throughput = np.sum(ShannonCapacity)
print('Problem 1-3: throughput =', throughput, 'Bits/s')

# Problem 1-4
D2DSINR = np.empty(75)
transmitters = {}
for i, ms in enumerate(MobileStations.values()):
    transmitters[i] = ms[0]
for i, ms in enumerate(MobileStations.values()):
    D2DSINR[i] = ms[1].SINR(ms[0], transmitters=transmitters)
D2DSINR = np.sort(D2DSINR)
cdfOfD2DSINR = np.arange(len(D2DSINR)) / float(len(D2DSINR) - 1)
plt.figure(4)
plt.plot(D2DSINR, cdfOfD2DSINR)
plt.title('Problem 1-4')
plt.xlabel('D2D SINR (dB)')
plt.ylabel('CDF')
plt.grid(True)
# plt.show()

# Problem 1-5
ShannonCapacity = np.empty(75)
for i, ms in enumerate(MobileStations.values()):
    # ms[0]:D2D transmitter; ms[1]:D2D receiver
    ShannonCapacity[i] = ms[1].Shannon(ms[0], transmitters=transmitters, divider=1)
throughput = np.sum(ShannonCapacity)
print('Problem 1-5: throughput =', throughput, 'Bits/s')

# Problem 1-6
temp = MobileStations
# -----------------------------------------------------
throughputs = [throughput]
transmitters = {}
for j in range(1, 10):
    MobileStations = genPairs({}, 75 + 75 * j)
    for i, ms in enumerate(MobileStations.values()):
        transmitters[i] = ms[0]
    # x_coord, y_coord = random_arr_gen()
    # for i in range(75):
    #     MobileStations[i + 75 * j] = [MS(x_coord[i], y_coord[i], id=i + 75 * j)]
    #     transmitters[i + 75 * j] = MobileStations[i + 75 * j][0]
    # x_coord, y_coord = random_arr_gen(True, list(zip(x_coord, y_coord)))
    # for i in range(75):
    #     MobileStations[i + 75 * j].append(MS(x_coord[i], y_coord[i], id=i + 75 * j))
    #     MobileStations[i + 75 * j][0].setPartner(MobileStations[i + 75 * j][1], 1)
    #     MobileStations[i + 75 * j][1].setPartner(MobileStations[i + 75 * j][0], 0)
    #     MobileStations[i + 75 * j][0].setCell(BaseStations[10])
    #     MobileStations[i + 75 * j][1].setCell(BaseStations[10])
    ShannonCapacity = np.empty(75 + 75 * j)
    for i, ms in enumerate(MobileStations.values()):
        ShannonCapacity[i] = ms[1].Shannon(ms[0], transmitters=transmitters, divider=1)
    throughputs.append(np.sum(ShannonCapacity))
numOfD2DPairs = [75 * (i + 1) for i in range(10)]
plt.figure(5)
plt.plot(numOfD2DPairs, throughputs)
plt.title('Problem 1-6')
plt.xlabel('Number of D2D pairs')
plt.ylabel('System throughput (Bits/s)')
plt.grid(True)
# plt.show()
# ----------------------------------------------------------

# Problem 2-1
T = 1000
MobileStations = temp
del temp
lossProbability = []
lamdas = np.array([100e3, 500e3, 1e6, 1.5e6, 2e6])
# ----------------------------------------------------------
# ShannonCapacity = np.empty(75)
# for i, ms in enumerate(MobileStations.values()):
#     # ms[0]:D2D transmitter; ms[1]:D2D receiver
#     ShannonCapacity[i] = ms[1].Shannon(ms[0], transmitters=transmitters, divider=1)
# FDD
for idx, lam in enumerate(lamdas):
    totalBits = 0
    lossBits = 0
    for i in range(T):
        speed = np.random.poisson(lam, size=75)
        totalBits += np.sum(speed, dtype=np.int64)
        for i, ms in enumerate(MobileStations.values()):
            BaseStations[10].UPShan(ms[0], 150)
            ShanCap = ms[0].bufferPop(BaseStations[10])
            if ShanCap > 0:
                if ShanCap > speed[i]:
                    ShanCap -= speed[i]
                    speed[i] = BaseStations[10].shan - ShanCap
                else:
                    remainData = speed[i] - ShanCap
                    lossBits += ms[0].bufferUpdate(remainData, BaseStations[10])
                    speed[i] = BaseStations[10].shan
            else:
                remainData = -ShanCap + speed[i]
                lossBits += ms[0].bufferUpdate(remainData, BaseStations[10])
                speed[i] = BaseStations[10].shan                
            ms[1].Shannon(BaseStations[10], divider=150)
            ShanCap = BaseStations[10].bufferPop(ms[1])
            if ShanCap > 0:
                if ShanCap > speed[i]:
                    ShanCap -= speed[i]
                else:
                    remainData = speed[i] - ShanCap
                    lossBits += BaseStations[10].bufferUpdate(remainData, ms[1])
            else:
                remainData = -ShanCap + speed[i]
                lossBits += BaseStations[10].bufferUpdate(remainData, ms[1])
    lossProbability.append(lossBits / totalBits)
plt.figure(6)
x = np.arange(len(lossProbability))
plt.bar(x, lossProbability)
plt.title('Problem 2-1')
plt.xticks(x, lamdas)
plt.xlabel('Arrival rate (bits/s)')
plt.ylabel('Bits loss probability')
plt.grid(True)
# ---------------------------------------------------------------
# plt.show()

# Problem 2-2
lossProbability = []
transmitters = {}
for i, ms in enumerate(MobileStations.values()):
    transmitters[i] = ms[0]
for lam in lamdas:
    totalBits = 0
    lossBits = 0
    for i in range(T):
        speed = np.random.poisson(lam, size=75)
        totalBits += np.sum(speed, dtype=np.int64)
        for i, ms in enumerate(MobileStations.values()):
            ms[1].Shannon(ms[0], transmitters=transmitters, divider=1)
            ShanCap = ms[0].bufferPop(ms[1])
            if ShanCap > 0:
                if ShanCap > speed[i]:
                    ShanCap -= speed[i]
                else:
                    remainData = speed[i] - ShanCap
                    lossBits += ms[0].bufferUpdate(remainData, ms[1])
            else:
                remainData = -ShanCap + speed[i]
                lossBits += ms[0].bufferUpdate(remainData, ms[1])
    lossProbability.append(lossBits / totalBits)
plt.figure(7)
x = np.arange(len(lossProbability))
plt.bar(x, lossProbability)
plt.title('Problem 2-2')
plt.xticks(x, lamdas)
plt.xlabel('Arrival rate (bits/s)')
plt.ylabel('Bits loss probability')
plt.grid(True)
plt.show()