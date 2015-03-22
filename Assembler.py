
import re

regOffset = [ 'B', 'C', 'D', 'E', 'H', 'L', 'M', 'A' ]
regPair = { 'H':'L', 'B':'C', 'D':'E', 'A':'F' }

mvi_map = { 'A':0x3E, 'B':0x06, 'C':0x0E, 'D':0x16, 'E':0x1E, 'H':0x26, 'L':0x2E, 'M':0x36 }
lxi_map = { 'B':0x01, 'D':0x11, 'H':0x21, 'SP':0x31 }
mov_map = { 'A':0x78, 'B':0x40, 'C':0x48, 'D':0x50, 'E':0x58, 'H':0x60, 'L':0x68, 'M':0x70 }
push_map = { 'B':0xC5, 'D':0xD5, 'H':0xE5, 'PSW':0xF5 }
pop_map = { 'B':0xC1, 'D':0xD1, 'H':0xE1, 'PSW':0xF1 }
rst_map = [ 0xC7, 0xCF, 0xD7, 0xDF, 0xE7, 0xEF, 0xF7, 0xFF ]
cnd_map = { 'NZ':0xC2, 'Z':0xCA, 'NC':0xD2, 'C':0xDA, 'PO':0xE2, 'P':0xF2, 'M':0xFA }

ins_len2 = [ 'MVI', 'ADI', 'ACI', 'SUI', 'SBI', 'ANI', 'XRI', 'ORI', 'CPI',
             'OUT', 'IN' ]

ins_len3 = [ 'LXI', 'JMP', 'JNZ', 'JZ', 'JNC', 'JC', 'JPO', 'JPE', 'JP', 'JM',
                    'CALL', 'CNZ', 'CZ', 'CNC', 'CC', 'CPO', 'CPE', 'CP', 'CM',
                    'LHLD', 'LDA', 'STA', 'SHLD', 'LDA', 'STA' ]

imm_opcodes = { 'ADI':0xC6, 'ACI':0xCE, 'SUI':0xD6, 'SBI':0xDE, 'ANI':0xE6, 'XRI':0xEE, 'ORI':0xF6, 'CPI':0xFE, 'OUT':0xD3, 'IN':0xDB }
addr_opcodes = { 'LDA': 0x3A, 'STA':0x32, 'JMP':0xC3, 'CALL':0xCD }

singlebytereg_opcodes = { 'ADD':0x80, 'ADC':0x88, 'SUB':0x90, 'SBB':0x98, 'ANA':0xA0, 'XRA':0xA8, 'ORA':0xB0, 'CMP':0xB8 } 
singlebyte_opcodes = { 'RET':0xC9, 'HLT':0x76, 'RLC':0x07, 'RRC':0x0F, 'RAL':0x17, 'RAR':0x1F, 'CMA':0x2E, 'DDA':0x27, 'CMC':0x3F,
                        'STC':0x37, 'EI':0xFB, 'DI':0xFB, 'NOP':0x00, 'XTHL':0xE3, 'SPHL':0xF9, 'SIM':0x30, 'RIM':0x20, 'XCHG':0xEB }

misc_opcodes = [ 'MOV', 'INX', 'DCX', 'INR', 'DCR', 'PUSH', 'POP', 'DAD', 'RST' ]

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

class Assembler:
    
    def __init__(self):
        self.asm = []
        self.bytes_list = []
        self.labels = {}

    def IsIns(self, opcode):
        if opcode in ins_len2:
            return True
        elif opcode in ins_len3:
            return True
        elif opcode in singlebytereg_opcodes:
            return True
        elif opcode in singlebyte_opcodes:
            return True
        elif opcode in misc_opcodes:
            return True
        return False

    def GetInsLen(self, opcode):
        if opcode in ins_len2:
            return 2
        elif opcode in ins_len3:
            return 3
        return 1

    def Lex(self, asmString):
        asms = asmString.split('\n')
        lastLabel = ""
        lineno = 0
        for asm in asms:
            lineno += 1
            line = re.sub(re.compile(";.*$"), "", asm)
            self.line_no = lineno
            self.line = line
            s = {}
            tokens = re.findall("\s*(\w+|.)", line)
            tokens = [ t for t in tokens if t.strip() ]
            if len(tokens) >= 2 and tokens[1] == ':':
                lastLabel = tokens[0].upper()
                if self.IsIns(lastLabel):
                    raise Exception("Invalid label: "+ lastLabel)
                tokens = tokens[2:]
                for x in self.asm:
                    if lastLabel == x["label"]:
                        lastLabel = ""
                        raise Exception("Error: duplicate label name, previously defined at:\n\t"+x["line"]) 
                        break
            if len(tokens) == 0:
                if lastLabel != "":
                    s = {}
                    s["data"] = [ 0 ]
                    s["opcode"] = "00"
                    s["type"] = "HEX"
                    s["line_no"] = lineno
                    s["line"] = line
                    s["label"] = lastLabel
                    self.asm.append(s)
                continue
            s["opcode"] = tokens[0].upper()
            s["op1"] = None
            s["op2"] = None
            s["line"] = line
            s["line_no"] = lineno
            s["label"] = ""
            s["type"] = "ASM"
            if (is_hex(s["opcode"]) and s["opcode"]!="ADD" and s["opcode"]!='DAA' and s["opcode"]!='DAD'):
                s["type"] = "HEX"
                s["data"] = []
                for t in tokens:
                    s["data"].append(int(t,16))
            elif len(tokens) > 1:
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
        if byte > 0xFF:
            raise Exception("Expected byte value: " + hex(byte))
        self.bytes.append(byte)
    
    def AddHexByte(self, num):
        self.AddByte(int(num, 16))

    def AddHexWord(self, word):
        if is_hex(word):
            num = int(word, 16)
            if num > 0xFFFF:
                raise Exception("Expected word value: " + hex(num))
            self.AddByte(num & 0xFF)
            self.AddByte((num >> 8) & 0xFF)
        else:
            if word not in self.labels:
                self.ErrorInvalidLabel()
            self.AddHexWord(hex(self.labels[word]))

    def ErrorFirstOperand(self):
        raise Exception("Invalid first operand for " + self.opcode + ": " + str(self.op1))

    def ErrorSecondOperand(self):
        raise Exception("Invalid second operand for " + self.opcode + ": " + self.op2)

    def ErrorUnexpectedFirstOperand(self):
        raise Exception("Unexpected first operand for " + self.opcode + ": " + self.op1)

    def ErrorUnexpectedSecondOperand(self):
        raise Exception("Unexpected second operand for " + self.opcode + ": " + self.op2)

    def ErrorInvalidLabel(self):
        raise Exception("Invalid label for " + self.opcode + ": " + self.op1)

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
            self.ErrorFirstOperand()
            return
        if self.op2 is None:
            self.ErrorSecondOperand()
            return
        self.AddByte(mvi_map[self.op1])
        self.AddHexByte(self.op2)
    
    def InrDcr(self, offset=-2):
        if not self.op1 in mvi_map:
            self.ErrorFirstOperand()
            return
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(mvi_map[self.op1]+offset)

    def InxDcx(self, offset=2):
        if not self.op1 in lxi_map:
            self.ErrorFirstOperand()
            return
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(lxi_map[self.op1]+offset)

    def Push(self):
        if not self.op1 in push_map:
            self.ErrorFirstOperand()
            return
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(push_map[self.op1])

    def Pop(self):
        if not self.op1 in pop_map:
            self.ErrorFirstOperand()
            return
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(pop_map[self.op1])
    
    def Rst(self):
        if self.op1 is None or not is_hex(self.op1) or int(self.op1) > 7:
            self.ErrorFirstOperand()
        if self.op2:
           self.ErrorUnexpectedSecondOperand()
        self.AddByte(rst_map[int(self.op1)])

    def Dad(self):
        dad_map = { 'B':0x09, 'D':0x19, 'H':0x29, 'SP':0x39 }
        if self.op1 is None or not self.op1 in dad_map:
            self.ErrorFirstOperand()
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
        self.AddByte(dad_map[self.op1])

    def Lxi(self):
        if not self.op1 in lxi_map:
            self.ErrorFirstOperand()
            return
        if self.op2 is None:
            self.ErrorSecondOperand()
            return
        self.AddByte(lxi_map[self.op1])
        self.AddHexWord(self.op2)

    def SingleByteRegParamInstruction(self):
        if not self.op1 in regOffset:
            self.ErrorFirstOperand()
            return
        if self.op2:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddByte(singlebytereg_opcodes[self.opcode] + regOffset.index(self.op1))

    def ImmediateInstruction(self):
        if self.op1 is None:
            self.ErrorFirstOperand()
            return
        self.AddByte(imm_opcodes[self.opcode])
        self.AddHexByte(self.op1)
    
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
        self.AddressInstruction(cnd_map[cnd]+offset)

    def AddressInstruction(self, opcode):
        self.AddByte(opcode)
        if self.op1 is None:
            self.ErrorFirstOperand()
            return
        if not self.op2 is None:
            self.ErrorUnexpectedSecondOperand()
            return
        self.AddHexWord(self.op1)

    def CollectLabels(self, addr_base):
        addr = addr_base
        for s in self.asm:
            if s["label"] != "":
                if is_hex(s["label"]):
                    addr = int(s["label"], 16)
                else:
                    self.labels[s["label"]] = addr
            if s["type"] == "ASM":
                addr += self.GetInsLen(s["opcode"])
            else:
                addr += len(s["data"])
#        for k in self.labels:
#            print(k, hex(self.labels[k]))

    def Parse(self, addr_base=0x8000):
        self.CollectLabels(addr_base)
        addr = addr_base
        for s in self.asm:
            if s["label"] != "" and is_hex(s["label"]):
                addr = int(s["label"], 16)
            byte_list = {}
            byte_list["address"] = addr
            byte_list["bytes"] = []
            byte_list["line_no"] = s["line_no"]
            byte_list["asm"] = s["line"]
            self.bytes = byte_list["bytes"]
             
            if s["type"] == "ASM":
                oc = s["opcode"]
                self.opcode = oc
                self.op1 = s["op1"]
                self.op2 = s["op2"]
                self.line = s["line"]
                self.line_no = s["line_no"]
                if oc == "MVI":
                    self.Mvi()
                elif oc == "LXI":
                    self.Lxi()
                elif oc == "MOV":
                    self.Mov()
                elif oc == "INR":
                    self.InrDcr()
                elif oc == "DCR":
                    self.InrDcr(-1)
                elif oc == "INX":
                    self.InxDcx()
                elif oc == "DCX":
                    self.InxDcx(0xA)
                elif oc == "PUSH":
                    self.Push()
                elif oc == "POP":
                    self.Pop()
                elif oc == "RST":
                    self.Rst()
                elif oc == "DAD":
                    self.Dad()
                elif oc in addr_opcodes:
                    self.AddressInstruction(addr_opcodes[oc])
                elif oc in imm_opcodes:
                    self.ImmediateInstruction()
                elif oc in singlebytereg_opcodes:
                    self.SingleByteRegParamInstruction()
                elif oc in singlebyte_opcodes:
                    self.SingleByteInstruction()
                elif oc[1:] in cnd_map:
                    if oc[:1] == 'J':
                        self.Cnd()
                    elif oc[:1] == 'C':
                        self.Cnd(2)
                    elif oc[:1] == 'R':
                        self.Cnd(-2, False)
                else:
                    raise Exception("Invalid assembly instruction")
            else:
                for t in s["data"]:
                    while t > 0xFF:
                        self.AddByte(t&0xFF)
                        t = t >> 8
                    self.AddByte(t)
            
            if s["type"] == "ASM":
                addr += self.GetInsLen(s["opcode"])
            else:
                addr += len(s["data"])
            self.bytes_list.append(byte_list)

