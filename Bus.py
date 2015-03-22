
class Bus:
    def __init__(self):
        self.mem_peripherals = {}
        self.io_peripherals = {}

    def AddMemoryPeripheral(self, peripheral, startAddr, endAddr):
        self.mem_peripherals[peripheral] = (startAddr, endAddr)

    def ReadMemory(self, addr):
        for k,v in self.mem_peripherals.items():
            if addr >= v[0] and addr <= v[1]:
                return k.Read(addr)
        raise Exception("Invalid address to read: " + hex(addr))

    def WriteMemory(self, addr, value):
        for k,v in self.mem_peripherals.items():
            if addr >= v[0] and addr <= v[1]:
                k.Write(addr, value)

    def AddIOPeripheral(self, peripheral, startAddr, endAddr):
        self.io_peripherals[peripheral] = (startAddr, endAddr)

    def RemoveIOPeripheral(self, peripheral):
        if peripheral in self.io_peripherals:
            del self.io_peripherals[peripheral]

    def ReadIO(self, addr):
        for k,v in self.io_peripherals.items():
            if addr >= v[0] and addr <= v[1]:
                return k.Read(addr)
        raise Exception("Invalid address to write: " + hex(addr))

    def WriteIO(self, addr, value):
        for k,v in self.io_peripherals.items():
            if addr >= v[0] and addr <= v[1]:
                k.Write(addr, value)

