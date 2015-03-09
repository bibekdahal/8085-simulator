
class ALU:
    def __init__(self):
        self.registers = { 'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'H':0, 'L':0, 'F':0, 'PC':0, 'SP':0xFF }
        self.CheckAll()

    def SetCarry(self, toSet=True):
        if toSet:
            self.registers['F'] |= 0x01
        else:
            self.registers['F'] &= ~0x01

    def SetAuxCarry(self, toSet=True):
        if toSet:
            self.registers['F'] |= 0x08
        else:
            self.registers['F'] &= ~0x08

    def SetZero(self, toSet=True):
        if toSet:
            self.registers['F'] |= 0x40
        else:
            self.registers['F'] &= ~0x40

    def SetSign(self, toSet=True):
        if toSet:
            self.registers['F'] |= 0x80
        else:
            self.registers['F'] &= ~0x80

    def SetParity(self, toSet=True):
        if toSet:
            self.registers['F'] |= 0x04
        else:
            self.registers['F'] &= ~0x04



    def CheckForCarry(self):
        self.SetCarry(self.registers['A'] > 0xFF)
        if self.registers['A'] > 0xFF:
            self.registers['A'] -= 0xFF + 0x01
    
    def CheckForBurrow(self):
        self.SetCarry(self.registers['A'] < 0x00)
        if self.registers['A'] < 0x00:
            self.registers['A'] += 0xFF + 0x1

    def CheckForZero(self, val=0xFFFFFFF):
        if val == 0xFFFFFFF:
            val = self.registers['A']
        self.SetZero(val==0)
    
    def CheckForSign(self, val=0xFFFFFFF):
        if val == 0xFFFFFFF:
            val = self.registers['A']
        self.SetSign(val & 0x80 == 0x80)

    def CheckForParity(self, val=0xFFFFFFF):
        if val == 0xFFFFFFF:
            val = self.registers['A']
        p = 0
        while val:
            p = ~p
            val = val & (val - 1)
        self.SetParity(p==0)


    def CheckAll(self, val=0xFFFFFFF):
        self.CheckForZero(val)
        self.CheckForSign(val)
        self.CheckForParity(val)


    def Add(self, val, carry=False):
        res = self.registers['A'] + val
        if carry:
            c = self.registers['F'] & 0x01
            res += c
        self.registers['A'] = res
        self.CheckForCarry()
        self.CheckAll()
                
    def Sub(self, val, burrow=False):
        res = self.registers['A'] - val
        if (burrow):
            c = self.registers['F'] & 0x01
            res -= c
        self.registers['A'] = res
        self.CheckForBurrow()

    def And(self, val):
        self.registers['A'] &= val
        self.CheckAll()

    def Or(self, val):
        self.registers['A'] |= val
        self.CheckAll()

    def Xor(self, val):
        self.registers['A'] ^= val
        self.CheckAll()

    def Not(self):
        self.Xor(0xFF)
        self.CheckAll()

    def Compare(self, val):
        temp = self.registers['A']
        self.Subtract(val)
        self.registers['A'] = temp

    def DecimalAdjust(self):
        #TODO
        pass

    def DoubleAddition(self, val):
        c = 0x00
        self.registers['L'] += val & 0xFF
        if self.registers['L'] > 0xFF:
            self.registers['L'] -= 0xFF + 0x01
            c = 0x01
        val = val >> 8
        self.registers['H'] += val + c
        self.SetCarry(self.registers['H'] > 0xFF)
        if self.registers['H'] > 0xFF:
            self.registers['H'] -= 0xFF + 0x01
        self.CheckAll(self.GetHL())


    def GetBC(self):
        return (self.registers['B'] << 8) | self.registers['C']

    def GetDE(self):
        return (self.registers['D'] << 8) | self.registers['E']
   
    def GetHL(self):
        return (self.registers['H'] << 8) | self.registers['L']
    
    def GetPSW(self):
        return (self.registers['A'] << 8) | self.registers['F']

    def SetBC(self, val):
        self.registers['C'] = val & 0xFF
        self.registers['B'] = (val >> 8)

    def SetDE(self, val):
        self.registers['E'] = val & 0xFF
        self.registers['D'] = (val >> 8)

    def SetHL(self, val):
        self.registers['L'] = val & 0xFF
        self.registers['H'] = (val >> 8)

    def SetAF(self, val):
        self.registers['F'] = val & 0xFF
        self.registers['A'] = (val >> 8)


    def Show(self):
        for k in sorted(self.registers):
            print(k+": "+hex(self.registers[k]))
