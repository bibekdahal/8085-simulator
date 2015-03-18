
import re

regOffset = [ 'B', 'C', 'D', 'E', 'H', 'L', 'M', 'A' ]
regPair = { 'H':'L', 'B':'C', 'D':'E', 'A':'F' }

mvi_map = { 'A':0x3E, 'B':0x06, 'C':0x0E, 'D':0x16, 'E':0x1E, 'H':0x26, 'L':0x2E, 'M':0x36 }
lxi_map = { 'B':0x01, 'D':0x11, 'H':0x21, 'SP':0x31 }
mov_map = { 'A':0x78, 'B':0x40, 'C':0x48, 'D':0x50, 'E':0x58, 'H':0x60, 'L':0x68, 'M':0x70 }
push_map = { 'B':0xC5, 'D':0xD5, 'H':0xE5, 'A':0xF5 }
pop_map = { 'B':0xC1, 'D':0xD1, 'H':0xE1, 'A':0xF1 }
rst_map = [ 0xC7, 0xCF, 0xD7, 0xDF, 0xE7, 0xEF, 0xF7, 0xFF ]
cnd_map = { 'NZ':0xC2, 'Z':0xCA, 'NC':0xD2, 'C':0xDA, 'PO':0xE2, 'P':0xF2, 'M':0xFA }

ins_len2 = [ 'MVI', 'ADI', 'ACI', 'SUI', 'SBI', 'ANI', 'XRI', 'ORI', 'CPI',
             'OUT', 'IN' ]

ins_len3 = [ 'LXI', 'JMP', 'JNZ', 'JZ', 'JNC', 'JC', 'JPO', 'JPE', 'JP', 'JM',
                    'CALL', 'CNZ', 'CZ', 'CNC', 'CC', 'CPO', 'CPE', 'CP', 'CM',
                    'LHLD', 'LDA', 'STA', 'SHLD' ]

imm_opcodes = { 'ADI':0xC6, 'ACI':0xCE, 'SUI':0xD6, 'SBI':0xDE, 'ANI':0xE6, 'XRI':0xEE, 'ORI':0xF6, 'CPI':0xFE }
immword_opcodes = { 'JMP':0xC3, 'CALL':0xCD }

singlebytereg_opcodes = { 'ADD':0x80, 'ADC':0x88, 'SUB':0x90, 'SBB':0x98, 'ANA':0xA0, 'XRA':0xA8, 'ORA':0xB0, 'CMP':0xB8 } 
singlebyte_opcodes = { 'RET':0xC9 }

class Parser:
    
    def __init__(self):
        self.asm = []
        self.bytes = []
        self.labels = {}

    def GetInsLen(self, opcode):
        if opcode in ins_len2:
            return 2
        elif opcode in ins_len3:
            return 3
        return 1

    def Lex(self, asmString):
        asms = asmString.split('\n')
        lastLabel = ""
        for asm in asms:
            line = re.sub(re.compile(";.*$"), "", asm)
            s = {}
            tokens = re.findall("\s*(\d+|\w+|.)", line)
            if len(tokens) >= 2 and tokens[1] == ':':
                lastLabel = tokens[0]
                tokens = tokens[2:]
                for x in self.asm:
                    if lastLabel == x["label"]:
                        lastLabel = ""
                        print("Error: duplicate label name at lines:\n\t"+line+"\n\t"+x["line"]) 
                        break

            if len(tokens) == 0:
                continue
            s["opcode"] = tokens[0].upper()
            s["op1"] = None
            s["op2"] = None
            s["line"] = line
            s["label"] = ""
            if len(tokens) > 1:
                s["op1"] = tokens[1].upper()
                if len(tokens) > 2:
                    if len(tokens) < 4 or tokens[2] != ",":
                        print("Error: expected operand separated by comma\n\t"+line)
                        return False
                    s["op2"] = tokens[3].upper()
                s["label"] = lastLabel
                lastLabel = ""
            self.asm.append(s)
        return True
    
    def AddByte(self, byte):
        self.bytes.append(byte)
    
    def AddHexByte(self, num):
        self.AddByte(int(num, 16))

    def AddHexWord(self, word):
        num = int(word, 16)
        self.AddByte(num & 0xFF)
        self.AddByte((num >> 8) & 0xFF)

    def ErrorFirstOperand(self):
        print("Invalid first operand for " + self.opcode + ": " + self.op1 + "\n\t"+self.line)

    def ErrorSecondOperand(self):
        print("Invalid second operand for " + self.opcode + ": " + self.op2 + "\n\t"+self.line)

    def ErrorUnexpectedFirstOperand(self):
        print("Unexpected first operand for " + self.opcode + ": " + self.op1 + "\n\t"+self.line)

    def ErrorUnexpectedSecondOperand(self):
        print("Unexpected second operand for " + self.opcode + ": " + self.op2 + "\n\t"+self.line)

    def Mov(self):
        if not self.op1 in mov_map:
            self.ErrorFirstOperand()
            return
        if not self.op2 in regOffset:
            self.ErrorSecondOperand()
            return
        self.AddByte(mov_map[self.op1] + regOffset.index(self.op2))

    def Mvi(self):
        if not self.op1 in mvi_map:
            ErrorFirstOperand()
            return
        if self.op2 is None:
            ErrorSecondOperand()
            return
        self.AddByte(mvi_map[self.op1])
        self.AddHexByte(self.op2)

    def Lxi(self):
        if not self.op1 in lxi_map:
            ErrorFirstOperand()
            return
        if self.op2 is None:
            ErrorSecondOperand()
            return
        self.AddByte(lxi_map[self.op1])
        self.AddHexWord(self.op2)

    def SingleByteRegParamInstruction(self):
        if not self.op1 in regOffset:
            self.ErrorFirstOperand()
            return
        if not self.op2 is None:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(singlebytereg_opcodes[self.opcode] + regOffset.index(self.op1))

    def ImmediateInstruction(self):
        if self.op1 is None:
            self.ErrorFirstOperand()
            return
        self.AddByte(imm_opcodes[self.opcode])
        self.AddHexByte(self.op1)
    
    def ImmediateWordInstruction(self):
        if self.op1 is None:
            self.ErrorFirstOperand()
            return
        self.AddByte(immword_opcodes[self.opcode])
        self.AddHexWord(self.op1)

    def SingleByteInstruction(self):
        if not self.op1 is None:
            self.ErrorUnexpectedFirstOperand()
            return
        self.AddByte(singlebyte_opcodes[self.opcode])

    def Cnd(self, offset=0, operand=True):
        cnd = self.opcode[1:]
        if operand and self.op1 is None:
            self.ErrorFirstOperand()
            return
        elif not operand and not self.op1 is None:
            self.ErrorUnexpectedFirstOperand()
            return
        self.AddByte(cnd_map[cnd]+offset)
        if operand:
            self.AddHexWord(self.op1)

    def CollectLabels(self, addr_base):
        addr = addr_base
        for s in self.asm:
            if s["label"] != "":
                self.labels[s["label"]] = addr
            addr += self.GetInsLen(s["opcode"])
        for k in self.labels:
            print(k, hex(self.labels[k]))

    def Parse(self, addr_base=0x8000):
        self.CollectLabels(addr_base)
        for s in self.asm:
            oc = s["opcode"]
            self.opcode = oc
            self.op1 = s["op1"]
            self.op2 = s["op2"]
            self.line = s["line"]
            if oc == "MVI":
                self.Mvi()
            elif oc == "LXI":
                self.Lxi()
            elif oc == "MOV":
                self.Mov()
            elif oc in imm_opcodes:
                self.ImmediateInstruction()
            elif oc in singlebytereg_opcodes:
                self.SingleByteRegParamInstruction()
            elif oc in immword_opcodes:
                self.ImmediateWordInstruction()
            elif oc in singlebyte_opcodes:
                self.SingleByteInstruction()
            elif oc[1:] in cnd_map:
                if oc[:1] == 'J':
                    self.Cnd()
                elif oc[:1] == 'C':
                    self.Cnd(2)
                elif oc[:1] == 'R':
                    self.Cnd(-2, False)

