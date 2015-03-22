#!/usr/bin/python3

######
# IGNORE THIS FILE
# THIS IS NOT PART OF FINAL PROJECT
# JUST A TEST PROGRAM
#####

from ALU import ALU
from CU import CU
from RAM import RAM
from Bus import Bus
from PPI import PPI
from threading import Thread
from functools import partial
import re
import time

def openFile():
    filep = open("random.bin", "r")
    global words
    asm = filep.read()
    filep.close()
    asm = re.sub(re.compile(";.*?\n"), "", asm)
    words = bytearray.fromhex("".join(asm.split()))

def execute():
    try:
        cu.Run()
    except Exception as ex:
        print()
        print ("Error: ")
        print ("=======")
        print(ex)
        print("\tat address: " + hex(alu.registers['PC']))
        print()
        cu.Reset()

def main():
    global bus, ram, ppi, alu, cu
    bus = Bus()
    ram = RAM(0x0, 64)
    ppi = PPI(0x40)
    bus.AddMemoryPeripheral(ram, 0x0, 0x0+64*1024-1)
    bus.AddIOPeripheral(ppi, 0x40, 0x40+3)
    
    
    alu = ALU()
    cu = CU(alu, bus)
    
    ppi.SetInterruptCallPA(partial(cu.RST, 5.5, ppi))
    ppi.SetInterruptCallPB(partial(cu.RST, 6.5, ppi))
    
    openFile()
    i = 0
    for wd in words:
        ram.Write(0x8000+i, wd)
        i += 1
    
    
    #ram.Write(0x002C, 0x6F)
    #ram.Write(0x002D, 0xC9)
    ram.Write(0x002c, 0xdb)
    ram.Write(0x002d, 0x40)
    ram.Write(0x002e, 0xc9)
    cu.Reset()
    cu.SetPC(0x8000)
    
    thread = Thread(target=execute)
    thread.start()
    
    ppi.a = 0xbb
    while cu.running:
        pass
#        cmd = input("Enter a command: ")
#        if cmd == "quit":
#            cu.running = False
#        elif cmd == "stba":
#            ppi.StrobeA()
#        elif cmd == "stbb":
#            ppi.StrobeB()
#        elif cmd == "show":
#            print("")
#            alu.Show()
#            #print("\n")
#            #ram.Show()
#            print("\n")
#            ppi.Show()

    ram.ShowRange(parser.labels["TABLE"], parser.labels["TABLE"]+0x63)
    alu.Show()


from Assembler import Assembler
parser = Assembler()
try:
    #main()
    filep = open("samples/testlbl.asm", "r")
    asm = filep.read()
    filep.close()
    parser.Lex(asm)
    parser.Parse()
    
    #filep = open("random.bin", "w")
    for bytes in parser.bytes_list:
        print(hex(bytes["address"]))
        for byte in bytes["bytes"]:
            print(hex(byte))
    #    filep.write('{0:02x}'.format(byte) + "\n")
    #filep.close()

    #main()

except (KeyboardInterrupt, SystemExit):
    print("")

except Exception as ex:
    print()
    print ("Error: ")
    print ("=======")
    print(ex)
    print("at line: \n\t" + parser.line + "\nline no.: " + str(parser.line_no))
    print()
