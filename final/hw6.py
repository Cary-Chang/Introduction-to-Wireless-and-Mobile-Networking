from numpy.core.records import array
from numpy.lib.function_base import append
from modules import *

def random_gen():
    x, y = np.random.uniform(-500 / 3 ** 0.5, 289), np.random.uniform(-250, 251)
    if x > 500 / 3 ** 0.5 or y > 250 or (abs(3 ** 0.5 * x) + abs(y) > 500):
        return random_gen()
    else:
        return x, y

def random_arr_gen(N):
    x = np.empty(N)
    y = np.empty(N)
    for i in range(N):
        x[i], y[i] = random_gen()
    return x, y

def genMobileStations(MobileStations):
    for idx in [5, 7, 8, 10, 12, 13, 15]:
        N = np.random.randint(5, 16)
        x_coord, y_coord = random_arr_gen(N)
        MobileStations[idx] = []
        for i in range(N):
            MobileStations[idx].append(MS(x_coord[i], y_coord[i], i, 6))
            MobileStations[idx][i].setCell(BaseStations[idx])
    return MobileStations


BaseStations = {}
MobileStations = {}
MapSetup(BaseStations, 6)
MobileStations = genMobileStations(MobileStations)

# Problem 1-1
plt.figure(1)
# for values in MobileStations.values():
#     for value in values:
#         plt.scatter(value.x, value.y, c="red")
for key, value in BaseStations.items():
    plt.scatter(value.x, value.y, c="blue")
    plt.annotate(f'{key}', (value.x, value.y), xytext=(-10, 5), textcoords='offset points')
plt.title('Problem 1-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)
map_grid(6)
# plt.show()

# Problem 1-2
# downSINR = []
poorSINR = np.empty(7)
for i, (idx, values) in enumerate(MobileStations.items()):
    temp = []
    for ms in values:
        temp.append(ms.SINR(BaseStations[idx]))
    # downSINR.append(temp)
    poorSINR[i] = min(temp)
poorSINR = np.sort(poorSINR)
cdfOfpoorSINR = np.arange(len(poorSINR)) / float(len(poorSINR) - 1)
plt.figure(2)
plt.plot(poorSINR, cdfOfpoorSINR, "-o")
plt.title('Problem 1-2')
plt.xlabel('SINR (dB)')
plt.ylabel('CDF')
plt.grid(True)
# plt.show()

# Problem 1-3
averageDataRate = np.empty(7)
resourceEfficiency = np.empty(7)
for i, (idx, values) in enumerate(MobileStations.items()):
    temp = []
    for ms in values:
        temp.append(ms.Shannon(BaseStations[idx]))
    averageDataRate[i] = min(temp)
    resourceEfficiency[i] = averageDataRate[i] * len(temp) / 10e6
print('Problem 1-3:')
print('The average data rate:')
for i , idx in enumerate(MobileStations.keys()):
    print(f'\tBaseStations[{idx}]: {averageDataRate[i]} bits/s')
print('The resource efficiency:')
for i , idx in enumerate(MobileStations.keys()):
    print(f'\tBaseStations[{idx}]: {resourceEfficiency[i]} bits/s/Hz')

# Problem 2-1
poorSINR = np.empty(100)
for i in range(100):
    poorTemp = np.empty(7)
    for j, (idx, values) in enumerate(MobileStations.items()):
        temp = []
        for ms in values:
            temp.append(ms.SFN_SINR(BaseStations))
        poorTemp[j] = min(temp)
    poorSINR[i] = min(poorTemp)
poorSINR = np.sort(poorSINR)
cdfOfpoorSINR = np.arange(len(poorSINR)) / float(len(poorSINR) - 1)
plt.figure(3)
plt.plot(poorSINR, cdfOfpoorSINR, "-o")
plt.title('Problem 2-1')
plt.xlabel('SINR (dB)')
plt.ylabel('CDF')
plt.grid(True)

# Problem 2-2
MSNum = 0
for values in MobileStations.values():
    MSNum += len(values)
averageDataRate = np.empty(100)
resourceEfficiency = np.empty(100)
temp = []
for i in range(100):
    for idx, values in MobileStations.items():
        for ms in values:
            temp.append(ms.SFN_Shan(BaseStations, MSNum))
    averageDataRate[i] = min(temp)
    resourceEfficiency[i] = averageDataRate[i] * len(temp) / 10e6
print(sum(averageDataRate))
print('Problem 2-2:')
print(f'The average data rate: {np.average(averageDataRate)} bits/s')
print(f'The resource efficiency: {np.average(resourceEfficiency)} bits/s/Hz')

plt.show()