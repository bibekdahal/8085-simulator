
class PPI:
    def __init__(self, baseAddr):
        self.baseAddr = baseAddr
        self.cr = 0x0
        self.a = 0x0
        self.b = 0x0
        self.c = 0x0
        self.interruptA = None
        self.interruptB = None

        self.changedHandler = None

    def Change(self):
        if self.changedHandler:
            self.changedHandler()

    def Write(self, addr, value):
        t = addr - self.baseAddr
        if t == 0x3:
            self.cr = value
            if self.cr & 0x80 != 0x80:
                self.BSR()
        elif self.cr & 0x80 != 0x80:
            return
        elif t == 0x0:
            self.OutA(value)
        elif t == 0x1:
            self.OutB(value)
        elif t == 0x2:
            self.OutC(value)
    
    def Read(self, addr):
        t = addr - self.baseAddr
        if self.cr & 0x80 != 0x80:
            return 0x0
        if t == 0x3:
            return 0x0
        elif t == 0x0:
            return self.InA()
        elif t == 0x1:
            return self.InB()
        elif t == 0x2:
            return self.InC()


    def BSR(self):
        bit = self.cr & 0x0E
        bit = bit >> 1
        data = self.cr & 0x01
        data = data << bit
        self.c = (self.c & ~data)|data
        self.Change()

    def InA(self):
        if self.cr & 0x10 == 0x00:
            return 0
        return self.a

    def InB(self):
        if self.cr & 0x02 == 0x00:
            return 0
        return self.b

    def InC(self):
        byte = 0x0
        if self.cr & 0x08 == 0x08:
            byte |= self.c & 0xF0
        if self.cr & 0x01 == 0x01:
            byte |= self.c & 0x0F
        return byte

    def OutA(self, value):
        if (self.cr & 0x10 == 0x10) and (self.cr & 0x60 != 0x60):
            return
        self.a = value
        self.Change()

    def OutB(self, value):
        if self.cr & 0x02 == 0x02:
            return
        self.b = value
        self.Change()

    def OutC(self, value):
        if self.cr & 0x08 == 0x00:
            self.c = (value & 0xF0) | (self.c & 0x0F)
        if self.cr & 0x01 == 0x00:
            self.c = (self.c & 0xF0) | (value & 0x0F)
        self.Change()


    def SetInterruptCallPA(self, call):
        self.interruptA = call

    def SetInterruptCallPB(self, call):
        self.interruptB = call

    def Inta(self):
        pass

    def StrobeA(self):
        if self.cr & 0x20 == 0x20 and not self.interruptA is None:
            self.interruptA()

    def StrobeB(self):
        if self.cr & 0x04 == 0x04 and not self.interruptB is None:
            self.interruptB()


    def Show(self):
        print ("Port A: " + hex(self.a))
        print ("Port B: " + hex(self.b))
        print ("Port C: " + hex(self.c))
