"""
In this simulation
TEMP = 300                                                                         # temperature = 300K
GTX = 14                                                                           # transmitter gain & receiver gain = 14dB
GRX = 14
BANDWIDTH = 10                                                                     # (MHz)
"""

import random
import math
import matplotlib.pyplot as plt 
import numpy as np
import math

"""
This function will draw the map grid for 19 cells
"""
def map_grid(homework = 5):
    assert homework == 5 or homework == 6
    if homework == 6:
        # y = -1000
        hexa_edgeX = [(500 * math.sqrt(3)) / 3, (250 * math.sqrt(3)) / 3, (-250 * math.sqrt(3)) / 3,
        (-500 * math.sqrt(3)) / 3, (-250 * math.sqrt(3)) / 3, (250 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3]
        hexa_edgeY = [-1000, -750, -750, -1000, -1250, -1250, -1000]
        plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')

        # y = -750 to 750
        for i in range(7):
            y = -750 + 250 * i
            x_even = [-250 * math.sqrt(3), 250 * math.sqrt(3)]
            x_odd = [-500 * math.sqrt(3), 0, 500 * math.sqrt(3)]
            if i == 0 or i % 2 == 0:
                # Two base station in this row
                for x in x_even:
                    hexa_edgeX = [(500 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x,
                    (-500 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (500 * math.sqrt(3)) / 3 + x]
                    hexa_edgeY = [0 + y, 250 + y, 250 + y, 0 + y, -250 + y, -250 + y, 0 + y]
                    plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')
                    
            else:
                for x in x_odd:
                    hexa_edgeX = [(500 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x,
                    (-500 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (500 * math.sqrt(3)) / 3 + x]
                    hexa_edgeY = [0 + y, 250 + y, 250 + y, 0 + y, -250 + y, -250 + y, 0 + y]
                    plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')
                    
        # y = 1000
        hexa_edgeX = [(500 * math.sqrt(3)) / 3, (250 * math.sqrt(3)) / 3, (-250 * math.sqrt(3)) / 3,
        (-500 * math.sqrt(3)) / 3, (-250 * math.sqrt(3)) / 3, (250 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3]
        hexa_edgeY = [1000, 1250, 1250, 1000, 750, 750, 1000]
        plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')
    else:
        # y = -500 to 500
        for i in range(5):
            y = -500 + 250 * i
            x_odd = [-250 * math.sqrt(3), 250 * math.sqrt(3)]
            x_even = [0]
            if i == 0 or i % 2 == 0:
                # Two base station in this row
                for x in x_even:
                    hexa_edgeX = [(500 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x,
                    (-500 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (500 * math.sqrt(3)) / 3 + x]
                    hexa_edgeY = [0 + y, 250 + y, 250 + y, 0 + y, -250 + y, -250 + y, 0 + y]
                    plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')
                    
            else:
                for x in x_odd:
                    hexa_edgeX = [(500 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x,
                    (-500 * math.sqrt(3)) / 3 + x, (-250 * math.sqrt(3)) / 3 + x, (250 * math.sqrt(3)) / 3 + x, (500 * math.sqrt(3)) / 3 + x]
                    hexa_edgeY = [0 + y, 250 + y, 250 + y, 0 + y, -250 + y, -250 + y, 0 + y]
                    plt.plot(hexa_edgeX, hexa_edgeY, c = 'black')
                    

"""
Basestation is a dictionary, ex: by calling "Basestation[<a base's id>]", you'll get the created cell object with this base id
homework depends on which homework is writing, the base station power of hw5 & hw6 is different
This function set up 19 cells and give them corresponding id
""" 
def MapSetup(BaseStations, homework):
    assert homework == 5 or homework == 6
    currentID = 1
    # y = -1000
    BaseStations[currentID] = Cell(0, -1000, currentID, homework)
    currentID += 1

    # y = -750 to 750
    for i in range(7):
        y = -750 + 250 * i
        x_even = [-250 * math.sqrt(3), 250 * math.sqrt(3)]
        x_odd = [-500 * math.sqrt(3), 0, 500 * math.sqrt(3)]
        if i == 0 or i % 2 == 0:
            # Two base station in this row
            for x in x_even:
                BaseStations[currentID] = Cell(x, y, currentID, homework)
                currentID += 1
        else:
            # Three base station in this row
            for x in x_odd:
                BaseStations[currentID] = Cell(x, y, currentID, homework)
                currentID += 1
    
    # y = 1000
    BaseStations[currentID] = Cell(0, 1000, currentID, homework)

    # Neighbor setting
    for cell in BaseStations:
        if cell == 1:
            temp = [2, 5, 3, 17, 14, 16]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 2:
            temp = [4, 7, 5, 1, 16, 18]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 4:
            temp = [6, 9, 7, 2, 18, 19]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 3:
            temp = [5, 8, 6, 19, 17, 1]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 5:
            temp = [7, 10, 8, 3, 1, 2]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 6:
            temp = [8, 11, 9, 4, 19, 3]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 7:
            temp = [9, 12, 10, 5, 2, 4]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 8:
            temp = [10, 13, 11, 6, 3, 5]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 9:
            temp = [11, 14, 12, 7, 4, 6]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 10:
            temp = [12, 15, 13, 8, 5, 7]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 11:
            temp = [13, 16, 14, 9, 6, 8]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 12:
            temp = [14, 17, 15, 10, 7, 9]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 13:
            temp = [15, 18, 16, 11, 8, 10]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 14:
            temp = [16, 1, 17, 12, 9, 11]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 15:
            temp = [17, 19, 18, 13, 10, 12]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 16:
            temp = [18, 2, 1, 14, 11, 13]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 17:
            temp = [1, 3, 19, 15, 12, 14]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 18:
            temp = [19, 4, 2, 16, 13, 15]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        elif cell == 19:
            temp = [3, 6, 4, 18, 15, 17]
            for id in temp:
                BaseStations[cell].setNeighbor(BaseStations[id])
        else:
            print("Bug: invalid BS id")

def getGain(homework):
    assert homework == 5 or homework == 6
    if homework == 5:
        return 0
    else:
        return 14
    

"""
This function is used to set up the base station
"""
def getBSpower(homework):
    assert homework == 5 or homework == 6
    if homework == 5:
        return -7
    elif homework == 6:
        return 3
    else:
        print("Invalid homework index (should be 5 or 6), the output is 0 now.")
        return 0

"""
This function is used to set up the mobile station
"""
def getMSpower():
    return -30

"""
Noise power in Watts, bandwidth in MHz
"""
def getNoise():
    # BOLTZMANS_CONST * temp * (bandwidth * (10 ** 6))
    return 1.38 * (10 ** (-23)) * 300 * (10 * (10 ** 6))

def Watts2dB(target):
    return 10 * math.log10(target)

def dB2Watts(target):
    return 10 ** (target / 10)

"""
This function can test whether the point is out of the boundary of the center cell
"""
def hexagon_tester(x, y):
    ans = True
    if ((math.sqrt(3) * x - y) < -500) or ((math.sqrt(3) * x + y) < -500) or ((math.sqrt(3) * x + y) > 500) or ((math.sqrt(3) * x - y) > 500):
        ans = False
    return ans

"""
Class Packet, object for transmitting and save in the buffer
Attribute:
dataSize    Size of packet
des         Destination MS
"""
class Packet:
    def __init__(self, size = 0, target = None):
        self.dataSize = size
        self.des = target

"""
Class Buffer, owned by both devices and cells
Attribute:
capacity    Maximum size of buffer, (bits)
occupied    Used buffer
packet      Packet info, a dictionary, MS.id -> [<undelivered packet>]
"""
class Buffer:
    # The default constructor is a buffer of a device
    def __init__(self, cap = 0.5 * (10**6)):
        self.capacity = cap
        self.occupied = 0
        self.packet = {}

"""
Class Cell
Attribute:
x           x position
y           y position
neighbor    Neighbor cell
buffer      Buffer
id          Name/Identifier
homework    The homework you are working on
"""
class Cell:
    def __init__(self, x = 0, y = 0, id = 0, homework = 5):
        self.x = x  # x position
        self.y = y  # y position
        self.neighbor = {}  # Neighbor cell
        assert homework == 5 or homework == 6
        self.__power = getBSpower(homework)  # Power (dB)
        self.buffer = Buffer(15 * (10 ** 6))   # Buffer
        self.id = id    # Id, initially set to 0
        self.__height = 51.5 # Height (m)
        self.homework = homework
        self.shan = 0

    def getPower(self):
        return self.__power

    def getHeight(self):
        return self.__height

    def setNeighbor(self, cell):
        self.neighbor[cell.id] = cell

    def getNeighbor(self, id):
        if id in self.neighbor:
            return self.neighbor[id]
        else:
            print("The input id is not neighbor cell")
            return None

    def setId(self, id):
        self.id = id

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def UPSINR(self, MS):
        assert MS != None

        # Calculating path loss gain
        dx = self.x - MS.x
        dy = self.y - MS.y 
        distance = math.sqrt(dx ** 2 + dy ** 2)

        num = (self.__height * MS.getHeight()) ** 2
        den = distance ** 4
        PLG = 10 * math.log10(num / den)

        # Receive power calculation
        PR = MS.getPower() + PLG + 2 * getGain(self.homework)

        noise = getNoise()
        return Watts2dB(dB2Watts(PR) / noise)

    def UPShan(self, MS, divider):
        assert MS != None
        SINR = dB2Watts(self.UPSINR(MS))

        # Bits/s
        Shan = ((10 ** 7)/divider) * math.log2(1 + SINR)
        self.shan = Shan
        return Shan
    
    # Return loss packet
    def bufferUpdate(self, updateBits = 0, MS = None):
        assert MS != None

        if self.buffer.occupied + updateBits <= self.buffer.capacity:
            self.buffer.occupied += updateBits
            temp = Packet(updateBits, MS)
            if MS.id in self.buffer.packet:
                self.buffer.packet[MS.id].append(temp)
            else:
                self.buffer.packet[MS.id] = [temp]
            return 0
        # Full
        elif self.buffer.occupied == self.buffer.capacity:
            return updateBits
        # Cannot store full packet
        else:
            retainCap = self.buffer.capacity - self.buffer.occupied
            lossPacket = updateBits - retainCap
            self.buffer.occupied += retainCap
            temp = Packet(retainCap, MS)
            if MS.id in self.buffer.packet:
                self.buffer.packet[MS.id].append(temp)
            else:
                self.buffer.packet[MS.id] = [temp]
            return lossPacket
    
    # Return remaining capacity to transmit packet
    def bufferPop(self, MS = None):
        assert MS != None

        ShannonCap = MS.shan
        if MS.id in self.buffer.packet:
            while len(self.buffer.packet[MS.id]) != 0:
                if ShannonCap >= self.buffer.packet[MS.id][0].dataSize:
                    poppedPack = self.buffer.packet[MS.id].pop(0)
                    self.buffer.occupied -= poppedPack.dataSize
                    ShannonCap -= poppedPack.dataSize
                else:
                    self.buffer.packet[MS.id][0].dataSize -= ShannonCap
                    self.buffer.occupied -= ShannonCap
                    ShannonCap = 0
                    return ShannonCap
            assert len(self.buffer.packet[MS.id]) == 0
            del self.buffer.packet[MS.id]
            return ShannonCap
        else:
            return ShannonCap


"""
Class MS (Mobile Station)
Attribute:
x           x position
y           y position
cell        Handling cell
id          Name / Identifier
shan        Shannon capacity
partner     MS in the same pair
type        0 -> receiver, 1 -> transmitter
homework    which homework are you working on?
buffer      Packet buffer
"""
class MS:
    def __init__(self, x = 0, y = 0, id = 0, homework = 5):
        self.x = x
        self.y = y
        self.__power = getMSpower()
        self.id = id
        self.cell = None
        self.partner = None
        self.type = 0
        self.__height = 1.5 # Height (m)
        self.shan = 0
        self.buffer = Buffer()
        assert homework == 5 or homework == 6
        self.homework = homework

    def getPower(self):
        return self.__power

    def getHeight(self):
        return self.__height

    def setPartner(self, partner, type):
        if type == 0:
            partner.type = 1
            self.partner = partner
            partner.partner = self
            self.type = type
        elif type == 1:
            partner.type = 0
            partner.partner = self
            self.partner = partner
            self.type = type
        else:
            print("Invalid type")


    def setCell(self, cell):
        self.cell = cell
        self.setPos(self.x + cell.x, self.y + cell.y)

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def setId(self, id):
        self.id = id

    # Receive power (dB)
    def signal(self, target):
        assert target != None

        # Calculating path loss gain
        dx = self.x - target.x
        dy = self.y - target.y 
        distance = math.sqrt(dx ** 2 + dy ** 2)

        num = (self.__height * target.getHeight()) ** 2
        den = distance ** 4
        PLG = 10 * math.log10(num / den)

        # Receive power calculation
        PR = target.getPower() + PLG + 2 * getGain(self.homework)
        return PR

    # Calculate SINR between the MS and specified BS, in (dB)
    # transmitters are other devices that are transmitter type, which is a dictionary
    def SINR(self, target, transmitters = None):
        assert target != None
        if type(target) == Cell:
            assert transmitters == None
            sigpow = dB2Watts(self.signal(target))
            noise = getNoise()
            interference = 0

            if target.id in self.cell.neighbor:
                for n in self.cell.neighbor:
                    if target.id != n:
                        interference += dB2Watts(self.signal(self.cell.neighbor[n]))
                interference += dB2Watts(self.signal(self.cell))
            elif target.id == self.cell.id:
                for n in self.cell.neighbor:
                    interference += dB2Watts(self.signal(self.cell.neighbor[n]))
            else:
                for n in self.cell.neighbor:
                    interference += dB2Watts(self.signal(self.cell.neighbor[n]))
                interference += dB2Watts(self.signal(self.cell))
            return Watts2dB(sigpow / (interference + noise))
        elif type(target) == MS:
            assert transmitters != None
            sigpow = dB2Watts(self.signal(target))
            noise = getNoise()
            interference = 0

            for id in transmitters:
                if id != target.id:
                    assert transmitters[id].type == 1
                    interference += dB2Watts(self.signal(transmitters[id]))

            return Watts2dB(sigpow / (noise + interference))
        else:
            print("Error: SINR target is neither a cell nor a MS")
            return 0

    def Shannon(self, target, transmitters = None, divider = 1):
        assert target != None
        SINR = 0

        # Means the data is passed from a base station
        if type(target) == Cell:
            assert transmitters == None
            SINR = dB2Watts(self.SINR(target))
        
        # Means the data is passed from a transmitter
        elif type(target) == MS:
            assert transmitters != None
            SINR = dB2Watts(self.SINR(target, transmitters))

        # Bits/s, here I thought bandwidth do not need to share with others, but I still give a divider
        Shan = ((10 ** 7)/divider) * math.log2(1 + SINR)
        self.shan = Shan
        return Shan

    def bufferUpdate(self, updateBits = 0, target = None):
        assert target != None

        if self.buffer.occupied + updateBits <= self.buffer.capacity:
            self.buffer.occupied += updateBits
            temp = Packet(updateBits, target)
            if target.id in self.buffer.packet:
                self.buffer.packet[target.id].append(temp)
            else:
                self.buffer.packet[target.id] = [temp]
            return 0
        # Full
        elif self.buffer.occupied == self.buffer.capacity:
            return updateBits
        # Cannot store full packet
        else:
            retainCap = self.buffer.capacity - self.buffer.occupied
            lossPacket = updateBits - retainCap
            self.buffer.occupied += retainCap
            temp = Packet(retainCap, target)
            if target.id in self.buffer.packet:
                self.buffer.packet[target.id].append(temp)
            else:
                self.buffer.packet[target.id] = [temp]
            return lossPacket
    
    # Return remaining capacity to transmit packet
    def bufferPop(self, MS = None):
        assert MS != None

        ShannonCap = MS.shan
        if MS.id in self.buffer.packet:
            while len(self.buffer.packet[MS.id]) != 0:
                if ShannonCap >= self.buffer.packet[MS.id][0].dataSize:
                    poppedPack = self.buffer.packet[MS.id].pop(0)
                    self.buffer.occupied -= poppedPack.dataSize
                    ShannonCap -= poppedPack.dataSize
                else:
                    self.buffer.packet[MS.id][0].dataSize -= ShannonCap
                    self.buffer.occupied -= ShannonCap
                    ShannonCap = 0
                    return ShannonCap
            assert len(self.buffer.packet[MS.id]) == 0
            del self.buffer.packet[MS.id]
            return ShannonCap
        else:
            return ShannonCap

    def SFN_SINR(self, BaseStations):
        assert BaseStations != None
        innerIndex = [5, 8, 15, 13, 12, 7, 10]
        outerIndex = [1, 3, 6, 11, 16, 18, 19, 17, 14, 9, 4, 2]
        signal = 0
        interference = 0
        noise = getNoise()

        for index in innerIndex:
            signal += dB2Watts(self.signal(BaseStations[index]))
        for index in outerIndex:
            interference += dB2Watts(self.signal(BaseStations[index]))

        return Watts2dB(signal / (interference + noise))

    def SFN_Shan(self, BaseStations, divider):
        assert BaseStations != None
        SINR = dB2Watts(self.SFN_SINR(BaseStations))

        Shan = ((10 ** 7)/divider) * math.log2(1 + SINR)
        self.shan = Shan
        return Shan


if __name__ == "__main__":
    """
    MS set up
    """
    num = 76
    # while num <= 101:
    receivers = {}
    for i in range(1, num):
        x = random.uniform((-500 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3)
        y = random.uniform(-250, 250)
        while not hexagon_tester(x, y):
            x = random.uniform((-500 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3)
            y = random.uniform(-250, 250)

        receivers[i] = MS(x, y, i)

    transmitters = {}
    for i in range(1, num):
        x = random.uniform((-500 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3)
        y = random.uniform(-250, 250)
        while not hexagon_tester(x, y):
            x = random.uniform((-500 * math.sqrt(3)) / 3, (500 * math.sqrt(3)) / 3)
            y = random.uniform(-250, 250)

        transmitters[i] = MS(x, y, i)

    for i in range(1, num):
        receivers[i].setPartner(transmitters[i], 0)
        transmitters[i].setPartner(receivers[i], 1)

    shansum = 0
    for i in range(1, num):
        SINR = receivers[i].SINR(receivers[i].partner, transmitters)
        Shannon = receivers[i].Shannon(receivers[i].partner, transmitters)
        shansum += Shannon
        print("Distance: ", math.sqrt((receivers[i].x - receivers[i].partner.x)**2 + (receivers[i].y - receivers[i].partner.y)**2), "\tSINR", SINR, "\tShannon", Shannon)
        plt.scatter(SINR, Shannon, c = "blue")
    # shansum /= num
    # plt.scatter(num, shansum, c = "blue")
    num += 5

    plt.show()