
class RAM:
    def __init__(self, baseAddr, sizeInK):
        self.baseAddr = baseAddr
        self.data = [0]*sizeInK*1024

    def Read(self, addr):
        return self.data[addr-self.baseAddr]

    def Write(self, addr, data):
        self.data[addr-self.baseAddr] = data


    def Show(self):
        addr = self.baseAddr
        for i in self.data:
            if i!=0:
                print(hex(addr)+": "+hex(i))
            addr+=1

    def ShowRange(self, start, end):
        addr = start
        while addr <= end:
            print(hex(addr)+": "+hex(self.Read(addr)))
            addr+=1

