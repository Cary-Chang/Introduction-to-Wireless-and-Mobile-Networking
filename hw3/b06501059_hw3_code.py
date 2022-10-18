import numpy as np
import matplotlib.pyplot as plt
import csv

TIMES = 0
class MobileDevice:
    global TIMES
    def __init__(self, x, y, cell_id):
        self.x = x
        self.y = y
        self.cell_id = cell_id
        self.time = 0
        self.direction = 0.0
        self.velocity = 0
        self.loc_id = cell_id
        self.SINR = 0.0
        self.out = False
    def calParameters(self):
        self.time = np.random.randint(1, 7)
        self.direction = np.random.uniform(0, 2 * np.pi)
        self.velocity = np.random.randint(1, 16)
    def move(self):
        if self.time == 0:
            self.calParameters()
        self.x += self.velocity * np.cos(self.direction)
        self.y += self.velocity * np.sin(self.direction)
        self.time -= 1
    def calReceivedPower(self, BS):
        P_T = 23
        G_T = G_R = 14
        h_t = 51.5
        h_r = 1.5
        dist = (self.x - BS[0]) ** 2 + (self.y - BS[1]) ** 2
        receivedPower = P_T - 30 + G_T + G_R + 10 * np.log10((h_r * h_t) ** 2 / dist ** 2)
        return receivedPower
    def calSINR(self, mobileDevices, BS, noise, interferenceGain, nearCells, BSs):
        h_t = 51.5
        h_r = 1.5
        interference = 0.0
        if self.out and (self.cell_id in nearCells[self.loc_id].keys()) and (nearCells[self.loc_id][self.cell_id] is not None):
            BS = list(BS)
            BS[0] += nearCells[self.loc_id][self.cell_id][0]
            BS[1] += nearCells[self.loc_id][self.cell_id][1]
        for device in mobileDevices:
            if device != self and device.loc_id in nearCells[self.loc_id].keys():
                if nearCells[self.loc_id][device.loc_id] is None:
                    interference += interferenceGain * (h_r * h_t) ** 2 / ((device.x - BS[0]) ** 2\
                        + (device.y - BS[1]) ** 2) ** 2
                else:
                    interference += interferenceGain * (h_r * h_t) ** 2 / (((device.x + \
                        nearCells[self.loc_id][device.loc_id][0]) - BS[0]) ** 2\
                        + ((device.y + nearCells[self.loc_id][device.loc_id][1]) - BS[1]) ** 2) ** 2
        SINR = self.calReceivedPower(BS) - 10 * np.log10(interference + noise)
        self.SINR = SINR
        return SINR
    def distFromBS(self, BS):
        return (self.x - BS[0]) ** 2 + (self.y - BS[1]) ** 2
    def detectOutOfBound(self, BS):
        x = self.x - BS[0]
        y = self.y - BS[1]
        if abs(x) > 500 / 3 ** 0.5 or abs(y) > 250 or (abs(3 ** 0.5 * x) + abs(y) > 500):
            return True
        else:
            return False
    def findLocation(self, BSs):
        dist = (self.x - BSs[self.loc_id - 1][0]) ** 2 + (self.y - BSs[self.loc_id - 1][1]) ** 2
        if (dist > 250 ** 2):
            x_interval = 1.5 * 500 / 3 ** 0.5
            y_interval = 500   
            if self.x > 0 and self.y > 0:
                idx = [10, 11, 12, 15, 16, 18, 19]
                d = [self.distFromBS((BSs[i - 1][0], BSs[i - 1][1])) for i in idx]
                self.loc_id = idx[min(range(len(d)), key=d.__getitem__)]
                if self.loc_id in [12, 16, 18, 19]:                    
                    if self.detectOutOfBound((BSs[self.loc_id - 1][0], BSs[self.loc_id - 1][1])):
                        self.out = True
                        if self.loc_id == 12:
                            dist_1 = self.distFromBS((BSs[12 - 1][0], BSs[12 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[16 - 1][0], BSs[16 - 1][1] + y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 17
                                self.x = self.x - BSs[12 - 1][0] + BSs[17 - 1][0]
                                self.y = self.y - (BSs[12 - 1][1] + y_interval) + BSs[17 - 1][1]
                            else:
                                self.loc_id = 1
                                self.x = self.x - BSs[16 - 1][0] + BSs[1 - 1][0]
                                self.y = self.y - (BSs[16 - 1][1] + y_interval) + BSs[1 - 1][1]
                        elif self.loc_id == 16:
                            dist_1 = self.distFromBS((BSs[16 - 1][0], BSs[16 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[19 - 1][0], BSs[19 - 1][1] + y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 1
                                self.x = self.x - BSs[16 - 1][0] + BSs[1 - 1][0]
                                self.y = self.y - (BSs[16 - 1][1] + y_interval) + BSs[1 - 1][1]
                            else:
                                self.loc_id = 4
                                self.x = self.x - BSs[19 - 1][0] + BSs[4 - 1][0]
                                self.y = self.y - (BSs[19 - 1][1] + y_interval) + BSs[4 - 1][1]
                        elif self.loc_id == 18:
                            self.loc_id = 3
                            self.x = self.x - (BSs[18 - 1][0] + x_interval) + BSs[3 - 1][0]
                            self.y = self.y - (BSs[18 - 1][1] + y_interval / 2) + BSs[3 - 1][1]
                        else:
                            dist_1 = self.distFromBS((BSs[19 - 1][0], BSs[19 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[19 - 1][0] + x_interval, BSs[19 - 1][1] + y_interval / 2))
                            dist_3 = self.distFromBS((BSs[19 - 1][0] + x_interval, BSs[19 - 1][1] - y_interval / 2))
                            if dist_1 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 4
                                self.x = self.x - BSs[19 - 1][0] + BSs[4 - 1][0]
                                self.y = self.y - (BSs[19 - 1][1] + y_interval) + BSs[4 - 1][1]
                            elif dist_2 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 8
                                self.x = self.x - (BSs[19 - 1][0] + x_interval) + BSs[8 - 1][0]
                                self.y = self.y - (BSs[19 - 1][1] + y_interval / 2) + BSs[8 - 1][1]
                            else:
                                self.loc_id = 3
                                self.x = self.x - (BSs[19 - 1][0] + x_interval) + BSs[3 - 1][0]
                                self.y = self.y - (BSs[19 - 1][1] - y_interval / 2) + BSs[3 - 1][1]
            elif self.x < 0 and self.y > 0:
                idx = [2, 3, 6, 7, 10, 11, 12]
                d = [self.distFromBS((BSs[i - 1][0], BSs[i - 1][1])) for i in idx]
                self.loc_id = idx[min(range(len(d)), key=d.__getitem__)]
                if self.loc_id in [2, 3, 7, 12]:
                    if self.detectOutOfBound((BSs[self.loc_id - 1][0], BSs[self.loc_id - 1][1])):
                        self.out = True
                        if self.loc_id == 12:
                            dist_1 = self.distFromBS((BSs[12 - 1][0], BSs[12 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[7 - 1][0], BSs[7 - 1][1] + y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 17
                                self.x = self.x - BSs[12 - 1][0] + BSs[17 - 1][0]
                                self.y = self.y - (BSs[12 - 1][1] + y_interval) + BSs[17 - 1][1]
                            else:
                                self.loc_id = 13
                                self.x = self.x - BSs[7 - 1][0] + BSs[13 - 1][0]
                                self.y = self.y - (BSs[7 - 1][1] + y_interval) + BSs[13 - 1][1]
                        elif self.loc_id == 7:
                            dist_1 = self.distFromBS((BSs[7 - 1][0], BSs[7 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[3 - 1][0], BSs[3 - 1][1] + y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 13
                                self.x = self.x - BSs[7 - 1][0] + BSs[13 - 1][0]
                                self.y = self.y - (BSs[7 - 1][1] + y_interval) + BSs[13 - 1][1]
                            else:
                                self.loc_id = 8
                                self.x = self.x - BSs[3 - 1][0] + BSs[8 - 1][0]
                                self.y = self.y - (BSs[3 - 1][1] + y_interval) + BSs[8 - 1][1]
                        elif self.loc_id == 2:
                            self.loc_id = 18
                            self.x = self.x - (BSs[2 - 1][0] - x_interval) + BSs[18 - 1][0]
                            self.y = self.y - (BSs[2 - 1][1] + y_interval / 2) + BSs[18 - 1][1]
                        else:
                            dist_1 = self.distFromBS((BSs[3 - 1][0], BSs[3 - 1][1] + y_interval))
                            dist_2 = self.distFromBS((BSs[3 - 1][0] - x_interval, BSs[3 - 1][1] + y_interval / 2))
                            dist_3 = self.distFromBS((BSs[3 - 1][0] - x_interval, BSs[3 - 1][1] - y_interval / 2))
                            if dist_1 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 8
                                self.x = self.x - BSs[3 - 1][0] + BSs[8 - 1][0]
                                self.y = self.y - (BSs[3 - 1][1] + y_interval) + BSs[8 - 1][1]
                            elif dist_2 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 19
                                self.x = self.x - (BSs[3 - 1][0] - x_interval) + BSs[19 - 1][0]
                                self.y = self.y - (BSs[3 - 1][1] + y_interval / 2) + BSs[19 - 1][1]
                            else:
                                self.loc_id = 18
                                self.x = self.x - (BSs[3 - 1][0] - x_interval) + BSs[18 - 1][0]
                                self.y = self.y - (BSs[3 - 1][1] - y_interval / 2) + BSs[18 - 1][1]
            elif self.x < 0 and self.y < 0:
                idx = [1, 2, 4, 5, 8, 9, 10]
                d = [self.distFromBS((BSs[i - 1][0], BSs[i - 1][1])) for i in idx]
                self.loc_id = idx[min(range(len(d)), key=d.__getitem__)]
                if self.loc_id in [1, 2, 4, 8]:
                    if self.detectOutOfBound((BSs[self.loc_id - 1][0], BSs[self.loc_id - 1][1])):
                        self.out = True
                        if self.loc_id == 8:
                            dist_1 = self.distFromBS((BSs[8 - 1][0], BSs[8 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[4 - 1][0], BSs[4 - 1][1] - y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 3
                                self.x = self.x - BSs[8 - 1][0] + BSs[3 - 1][0]
                                self.y = self.y - (BSs[8 - 1][1] - y_interval) + BSs[3 - 1][1]
                            else:
                                self.loc_id = 19
                                self.x = self.x - BSs[4 - 1][0] + BSs[19 - 1][0]
                                self.y = self.y - (BSs[4 - 1][1] - y_interval) + BSs[19 - 1][1]
                        elif self.loc_id == 4:
                            dist_1 = self.distFromBS((BSs[4 - 1][0], BSs[4 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[1 - 1][0], BSs[1 - 1][1] - y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 19
                                self.x = self.x - BSs[4 - 1][0] + BSs[19 - 1][0]
                                self.y = self.y - (BSs[4 - 1][1] - y_interval) + BSs[19 - 1][1]
                            else:
                                self.loc_id = 16
                                self.x = self.x - BSs[1 - 1][0] + BSs[16 - 1][0]
                                self.y = self.y - (BSs[1 - 1][1] - y_interval) + BSs[16 - 1][1]
                        elif self.loc_id == 2:
                            self.loc_id = 17
                            self.x = self.x - (BSs[2 - 1][0] - x_interval) + BSs[17 - 1][0]
                            self.y = self.y - (BSs[2 - 1][1] - y_interval / 2) + BSs[17 - 1][1]
                        else:
                            dist_1 = self.distFromBS((BSs[1 - 1][0], BSs[1 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[1 - 1][0] - x_interval, BSs[1 - 1][1] + y_interval / 2))
                            dist_3 = self.distFromBS((BSs[1 - 1][0] - x_interval, BSs[1 - 1][1] - y_interval / 2))
                            if dist_1 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 16
                                self.x = self.x - BSs[1 - 1][0] + BSs[16 - 1][0]
                                self.y = self.y - (BSs[1 - 1][1] - y_interval) + BSs[16 - 1][1]
                            elif dist_2 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 17
                                self.x = self.x - (BSs[1 - 1][0] - x_interval) + BSs[17 - 1][0]
                                self.y = self.y - (BSs[1 - 1][1] + y_interval / 2) + BSs[17 - 1][1]
                            else:
                                self.loc_id = 12
                                self.x = self.x - (BSs[1 - 1][0] - x_interval) + BSs[12 - 1][0]
                                self.y = self.y - (BSs[1 - 1][1] - y_interval / 2) + BSs[12 - 1][1]
            elif self.x > 0 and self.y < 0:
                idx = [8, 9, 10, 13, 14, 17, 18]
                d = [self.distFromBS((BSs[i - 1][0], BSs[i - 1][1])) for i in idx]
                self.loc_id = idx[min(range(len(d)), key=d.__getitem__)]
                if self.loc_id in [8, 13, 17, 18]:
                    if self.detectOutOfBound((BSs[self.loc_id - 1][0], BSs[self.loc_id - 1][1])):
                        self.out = True
                        if self.loc_id == 8:
                            dist_1 = self.distFromBS((BSs[8 - 1][0], BSs[8 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[13 - 1][0], BSs[13 - 1][1] - y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 3
                                self.x = self.x - BSs[8 - 1][0] + BSs[3 - 1][0]
                                self.y = self.y - (BSs[8 - 1][1] - y_interval) + BSs[3 - 1][1]
                            else:
                                self.loc_id = 7
                                self.x = self.x - BSs[13 - 1][0] + BSs[7 - 1][0]
                                self.y = self.y - (BSs[13 - 1][1] - y_interval) + BSs[7 - 1][1]
                        elif self.loc_id == 13:
                            dist_1 = self.distFromBS((BSs[13 - 1][0], BSs[13 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[17 - 1][0], BSs[17 - 1][1] - y_interval))
                            if dist_1 <= dist_2:
                                self.loc_id = 7
                                self.x = self.x - BSs[13 - 1][0] + BSs[7 - 1][0]
                                self.y = self.y - (BSs[13 - 1][1] - y_interval) + BSs[7 - 1][1]
                            else:
                                self.loc_id = 12
                                self.x = self.x - BSs[17 - 1][0] + BSs[12 - 1][0]
                                self.y = self.y - (BSs[17 - 1][1] - y_interval) + BSs[12 - 1][1]
                        elif self.loc_id == 18:
                            self.loc_id = 2
                            self.x = self.x - (BSs[18 - 1][0] + x_interval) + BSs[2 - 1][0]
                            self.y = self.y - (BSs[18 - 1][1] - y_interval / 2) + BSs[2 - 1][1]
                        else:
                            dist_1 = self.distFromBS((BSs[17 - 1][0], BSs[17 - 1][1] - y_interval))
                            dist_2 = self.distFromBS((BSs[17 - 1][0] + x_interval, BSs[17 - 1][1] + y_interval / 2))
                            dist_3 = self.distFromBS((BSs[17 - 1][0] + x_interval, BSs[17 - 1][1] - y_interval / 2))
                            if dist_1 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 12
                                self.x = self.x - BSs[17 - 1][0] + BSs[12 - 1][0]
                                self.y = self.y - (BSs[17 - 1][1] - y_interval) + BSs[12 - 1][1]
                            elif dist_2 == min(dist_1, dist_2, dist_3):
                                self.loc_id = 2
                                self.x = self.x - (BSs[17 - 1][0] + x_interval) + BSs[2 - 1][0]
                                self.y = self.y - (BSs[17 - 1][1] + y_interval / 2) + BSs[2 - 1][1]
                            else:
                                self.loc_id = 1
                                self.x = self.x - (BSs[17 - 1][0] + x_interval) + BSs[1 - 1][0]
                                self.y = self.y - (BSs[17 - 1][1] - y_interval / 2) + BSs[1 - 1][1]
    def checkHandoff(self, mobileDevices, BSs, noise, interferenceGain, time, nearCells, threshold=-15):
        global TIMES
        if self.SINR <= threshold:
            TIMES += 1
            result = [time, self.cell_id]
            self.cell_id = self.loc_id
            result.append(self.cell_id)
            with open('results.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(result)
    def updateLocation(self, BSs):
        self.move()
        self.findLocation(BSs)
    def updateSINR(self, BSs, mobileDevices, noise, interferenceGain, nearCells):
        self.calSINR(mobileDevices, (BSs[self.cell_id - 1][0], BSs[self.cell_id - 1][1]), noise, interferenceGain, nearCells, BSs)
    def updateHandoff(self, BSs, mobileDevices, noise, interferenceGain, time, nearCells):
        self.checkHandoff(mobileDevices, BSs, noise, interferenceGain, time, nearCells)
        self.out = False

temp = 27 + 273.15
bw = 10 * 10 ** 6
P_T = 33
P_R = 23
G_T = G_R = 14
h_t = 51.5
h_r = 1.5
x_interval = 1.5 * 500 / 3 ** 0.5
y_interval = 500
noise = 1.38 * 10 ** -23 * temp * bw
interferenceGain = 10 ** ((P_R - 30) / 10) * 10 ** (G_T / 10) * 10 ** (G_R / 10)

x_boud = np.array([x_interval / 3, x_interval / 1.5, x_interval / 3, -x_interval / 3, 
                    -x_interval / 1.5, -x_interval / 3, x_interval / 3])
y_boud = np.array([y_interval / 2, 0, -y_interval / 2, -y_interval / 2, 0, y_interval / 2, y_interval / 2])

BS_x_coord = np.array([-2 * x_interval, -2 * x_interval, -2 * x_interval, -x_interval, -x_interval, 
            -x_interval, -x_interval, 0, 0, 0, 0, 0, x_interval, x_interval, x_interval, x_interval, 
            2 * x_interval, 2 * x_interval, 2 * x_interval])
BS_y_coord = np.array([-y_interval, 0, y_interval, -1.5 * y_interval, -0.5 * y_interval, 0.5 * y_interval,
            1.5 * y_interval, -2 * y_interval, -y_interval, 0, y_interval, 2 * y_interval, 
            -1.5 * y_interval, -0.5 * y_interval, 0.5 * y_interval, 1.5 * y_interval, -y_interval, 0,
            y_interval])
BSs = list(zip(BS_x_coord, BS_y_coord))
nearCells = {1:{17:(-5 * x_interval, y_interval / 2), 12:(-3 * x_interval, -3.5 * y_interval), 16:(-3 * x_interval, -3.5 * y_interval), 2:None, 4:None, 5:None}, 
             2:{1:None, 3:None, 5:None, 6:None, 17:(-5 * x_interval, y_interval / 2), 18:(-5 * x_interval, y_interval / 2)}, 
             3:{2:None, 6:None, 7:None, 18:(-5 * x_interval, y_interval / 2), 19:(-5 * x_interval, y_interval / 2), 8:(-2 * x_interval, 4 * y_interval)}, 
             4:{1:None, 5:None, 8:None, 9:None, 16:(-3 * x_interval, -3.5 * y_interval), 19:(-3 * x_interval, -3.5 * y_interval)},
             5:{1:None, 2:None, 4:None, 6:None, 9:None, 10:None}, 
             6:{2:None, 3:None, 5:None, 7:None, 10:None, 11:None}, 
             7:{3:None, 6:None, 11:None, 12:None, 8:(-2 * x_interval, 4 * y_interval), 13:(-2 * x_interval, 4 * y_interval)}, 
             8:{4:None, 9:None, 13:None, 19:(-3 * x_interval, -3.5 * y_interval), 3:(2 * x_interval, -4 * y_interval), 7:(2 * x_interval, -4 * y_interval)},
             9:{4:None, 5:None, 8:None, 10:None, 13:None, 14:None}, 
             10:{5:None, 6:None, 9:None, 11:None, 14:None, 15:None}, 
             11:{6:None, 7:None, 10:None, 12:None, 15:None, 16:None}, 
             12:{7:None, 11:None, 16:None, 13:(-2 * x_interval, 4 * y_interval), 17:(-2 * x_interval, 4 * y_interval), 1:(-3 * x_interval, -3.5 * y_interval)},
             13:{8:None, 9:None, 14:None, 17:None, 7:(2 * x_interval, -4 * y_interval), 12:(2 * x_interval, -4 * y_interval)}, 
             14:{9:None, 10:None, 13:None, 15:None, 17:None, 18:None}, 
             15:{10:None, 11:None, 14:None, 16:None, 18:None, 19:None}, 
             16:{11:None, 12:None, 15:None, 19:None, 1:(3 * x_interval, 3.5 * y_interval), 4:(3 * x_interval, 3.5 * y_interval)},
             17:{13:None, 14:None, 18:None, 12:(2 * x_interval, -4 * y_interval), 1:(5 * x_interval, -0.5 * y_interval), 2:(5 * x_interval, -0.5 * y_interval)}, 
             18:{14:None, 15:None, 17:None, 19:None, 2:(5 * x_interval, -0.5 * y_interval), 3:(5 * x_interval, -0.5 * y_interval)}, 
             19:{15:None, 16:None, 18:None, 4:(3 * x_interval, 3.5 * y_interval), 8:(3 * x_interval, 3.5 * y_interval), 3:(5 * x_interval, -0.5 * y_interval)}}

def random_gen():
    offset = np.random.randint(0, 19)
    x, y = np.random.uniform(-500 / 3 ** 0.5, 289), np.random.uniform(-250, 251)
    if x > 500 / 3 ** 0.5 or y > 250 or (abs(3 ** 0.5 * x) + abs(y) > 500):
        return random_gen()
    else:
        return x + BS_x_coord[offset], y + BS_y_coord[offset], offset + 1

def random_arr_gen():
    x = np.empty(100)
    y = np.empty(100)
    idx = np.empty(100, dtype=int)
    for i in range(100):
        x[i], y[i], idx[i] = random_gen()
    return x, y, idx

x_coord, y_coord, cell_id = random_arr_gen()

plt.figure(1)
plt.scatter(BS_x_coord, BS_y_coord)
for i, pos in enumerate(zip(BS_x_coord, BS_y_coord)):
    plt.plot(x_boud + pos[0], y_boud + pos[1], color='black')
    plt.annotate(f'{i + 1}', (pos[0], pos[1]), xytext=(-10, 5), textcoords='offset points')
plt.title('Problem B-1')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)

plt.figure(2)
plt.scatter(x_coord, y_coord)
for i, pos in enumerate(zip(BS_x_coord, BS_y_coord)):
    plt.plot(x_boud + pos[0], y_boud + pos[1], color='black')
plt.title('Problem B-2')
plt.xlabel('Distance (m)')
plt.ylabel('Distance (m)')
plt.grid(True)


with open('results.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Time(s)', 'Source cell ID', 'Destination cell ID'])

mobileDevices = []
for x, y, idx in zip(x_coord, y_coord, cell_id):
    mobileDevices.append(MobileDevice(x, y, idx))

for i in range(900):
    for ms in mobileDevices:
        ms.updateLocation(BSs)
    for ms in mobileDevices:
        ms.updateSINR(BSs, mobileDevices, noise, interferenceGain, nearCells)
    for ms in mobileDevices:
        ms.updateHandoff(BSs, mobileDevices, noise, interferenceGain, i + 1, nearCells)

with open('results.csv', mode='a', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow([])
    writer.writerow(['Total handoff events:', TIMES])

plt.show()