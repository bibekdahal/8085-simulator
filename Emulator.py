#!/usr/bin/python3
from gi.repository import Gtk, GObject, Gdk, GLib, Pango, Pango

from ALU import ALU
from CU import CU
from RAM import RAM
from Bus import Bus
from PPI import PPI
from Assembler import Assembler

from HexEntry import HexEntry

from threading import Thread
from functools import partial
import re
import time
from enum import Enum

bus = Bus()
ram = RAM(0x0, 64)
ppi = PPI(0x40)
bus.AddMemoryPeripheral(ram, 0x0, 0x0+64*1024-1)
bus.AddIOPeripheral(ppi, 0x40, 0x40+3)

alu = ALU()
cu = CU(alu, bus)

ppi.SetInterruptCallPA(partial(cu.RST, 5.5, ppi))
ppi.SetInterruptCallPB(partial(cu.RST, 6.5, ppi))
 
cu.Reset()
cu.SetPC(0x8000)

alu = ALU()
cu = CU(alu, bus)

ppi.SetInterruptCallPA(partial(cu.RST, 5.5, ppi))
ppi.SetInterruptCallPB(partial(cu.RST, 6.5, ppi))

class State(Enum):
    none = 0
    exam_mem = 1
    exam_reg = 2
    go = 3
    executing = 4


def WriteMemData(addr, data):
    bus.WriteMemory(addr, data)
def GetMemData(addr):
    return bus.ReadMemory(addr)
def GetRegData(reg):
    return alu.registers[reg]

reglist = [ 'A', 'B', 'C', 'D', 'E', 'H', 'L', 'F' ]
def NextReg(reg):
    return reglist[(reglist.index(reg)+1)%len(reglist)]

def PrevReg(reg):
    id = reglist.index(reg)-1
    if id == -1:
        id = len(reglist) - 1
    return reglist[id]

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="8085 Emulator")
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        vm_box=Gtk.Box(spacing=10)
        self.add(vm_box)
        
        verh1_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        verh2_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
        
        self.entry_addr=Gtk.Entry()
        self.entry_addr.set_max_length(4)
        self.entry_addr.set_alignment(1)
        
        self.entry_hex=Gtk.Entry()
        self.entry_hex.set_max_length(2)
        self.entry_hex.set_alignment(1)

        self.entry_addr.connect('focus-in-event', self.addr_focus)
        self.entry_hex.connect('focus-in-event', self.hex_focus)
        
        KeyPadGrid=Gtk.Grid()
        KeyPadGrid.set_row_spacing(7)
        KeyPadGrid.set_column_spacing(7)
            
        button0=Gtk.Button(label='0')
        button0.connect('clicked',self.on_botton_click)
        button1=Gtk.Button(label='1')
        button1.connect('clicked',self.on_botton_click)
        button2=Gtk.Button(label='2')
        button2.connect('clicked',self.on_botton_click)
        button3=Gtk.Button(label='3')
        button3.connect('clicked',self.on_botton_click)
        button4=Gtk.Button(label='4')
        button4.connect('clicked',self.on_botton_click)
        button5=Gtk.Button(label='5')
        button5.connect('clicked',self.on_botton_click)
        button6=Gtk.Button(label='6')
        button6.connect('clicked',self.on_botton_click)
        button7=Gtk.Button(label='7')
        button7.connect('clicked',self.on_botton_click)
        button8=Gtk.Button(label='8')
        button8.connect('clicked',self.on_botton_click)
        button9=Gtk.Button(label='9')
        button9.connect('clicked',self.on_botton_click)
        buttonA=Gtk.Button(label='A')
        buttonA.connect('clicked',self.on_botton_click)
        buttonB=Gtk.Button(label='B')
        buttonB.connect('clicked',self.on_botton_click)
        buttonC=Gtk.Button(label='C')
        buttonC.connect('clicked',self.on_botton_click)
        buttonD=Gtk.Button(label='D')
        buttonD.connect('clicked',self.on_botton_click)
        buttonE=Gtk.Button(label='E')
        buttonE.connect('clicked',self.on_botton_click)
        buttonF=Gtk.Button(label='F')
        buttonF.connect('clicked',self.on_botton_click)
        buttonH=Gtk.Button(label='H')
        buttonH.connect('clicked',self.on_botton_click)
        buttonL=Gtk.Button(label='L')
        buttonL.connect('clicked',self.on_botton_click)
        button_next=Gtk.Button(label='Next')
        button_next.connect('clicked',self.on_botton_click)
        button_prev=Gtk.Button(label='Prev')
        button_prev.connect('clicked',self.on_botton_click)
        button_reg=Gtk.Button(label='Exam reg')
        button_reg.connect('clicked',self.on_botton_click)
        button_mem=Gtk.Button(label='Exam mem')
        button_mem.connect('clicked',self.on_botton_click)
        button_rst=Gtk.Button(label='Reset')
        button_rst.connect('clicked',self.on_botton_click)
        button_ss=Gtk.Button(label='Single step')
        button_ss.connect('clicked',self.on_botton_click)       
        button_go=Gtk.Button(label='Go')
        button_go.connect('clicked',self.on_botton_click)
        button_exe=Gtk.Button(label='Exec')
        button_exe.connect('clicked',self.on_botton_click)              


        self.pc_text = Gtk.Label('PC: 0000')
        self.sp_text = Gtk.Label('SP: FFFF')
        self.flags_text = Gtk.Label('FLAGS: 00000000')
        
        KeyPadGrid.add(button0)
        KeyPadGrid.attach_next_to(button1,button0,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button2,button1,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button3,button2,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button4,button0,Gtk.PositionType.BOTTOM,1,1)
        KeyPadGrid.attach_next_to(button5,button4,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button6,button5,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button7,button6,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(button8,button4,Gtk.PositionType.BOTTOM,1,1)
        KeyPadGrid.attach_next_to(button9,button8,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonA,button9,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonB,buttonA,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonC,button8,Gtk.PositionType.BOTTOM,1,1)
        KeyPadGrid.attach_next_to(buttonD,buttonC,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonE,buttonD,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonF,buttonE,Gtk.PositionType.RIGHT,1,1)
        KeyPadGrid.attach_next_to(buttonH,buttonC,Gtk.PositionType.BOTTOM,2,1)
        KeyPadGrid.attach_next_to(buttonL,buttonH,Gtk.PositionType.RIGHT,2,1)

        KeyPadGrid.attach_next_to(self.pc_text, buttonH, Gtk.PositionType.BOTTOM, 2, 1)
        KeyPadGrid.attach_next_to(self.sp_text, self.pc_text, Gtk.PositionType.RIGHT, 2, 1)
        KeyPadGrid.attach_next_to(self.flags_text, self.pc_text, Gtk.PositionType.BOTTOM, 4, 1)

        KeyPadGrid.attach_next_to(button_prev,self.flags_text,Gtk.PositionType.BOTTOM,2,1)
        KeyPadGrid.attach_next_to(button_next,button_prev,Gtk.PositionType.RIGHT,2,1)       
        KeyPadGrid.attach_next_to(button_reg,button_prev,Gtk.PositionType.BOTTOM,2,1)
        KeyPadGrid.attach_next_to(button_mem,button_reg,Gtk.PositionType.RIGHT,2,1)     
        KeyPadGrid.attach_next_to(button_rst,button_reg,Gtk.PositionType.BOTTOM,2,1)
        KeyPadGrid.attach_next_to(button_ss,button_rst,Gtk.PositionType.RIGHT,2,1)              
        KeyPadGrid.attach_next_to(button_go,button_rst,Gtk.PositionType.BOTTOM,2,1)
        KeyPadGrid.attach_next_to(button_exe,button_go,Gtk.PositionType.RIGHT,2,1)              
        
        verh1_box.pack_start(self.entry_addr,True,True,0)
        verh1_box.pack_start(self.entry_hex,True,True,0)
        verh1_box.pack_start(KeyPadGrid,True,True,0)
        vm_box.pack_start(verh1_box,False,True,0)
 
        strip = Gtk.Box(spacing=10)
        box1 = Gtk.Box(spacing=10)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.textEditor = Gtk.TextView()
        self.textEditor.set_left_margin(20)
        self.textEditor.override_font(Pango.font_description_from_string("Dejavu Sans Mono 10"))
        scrolledwindow.add(self.textEditor)

        fileButton = Gtk.Button("Load File")
        fileButton.connect('clicked', self.file_button)

        loadLbl = Gtk.Label("Load Address: ")
        self.loadaddr = Gtk.Entry()
        self.loadaddr.set_max_length(4)
        self.loadaddr.set_alignment(1)
        self.loadaddr.set_text('8000')

        scrolledwindow1 = Gtk.ScrolledWindow()
        scrolledwindow1.set_min_content_width(200)
        self.lblLabel = Gtk.Label("Labels From The Program")
        scrolledwindow1.add(self.lblLabel)

        loadButton = Gtk.Button("Load to Memory")
        loadButton.connect('clicked', self.load_button)

        strip.add(fileButton)
        strip.add(loadLbl)
        strip.add(self.loadaddr)
        strip.add(loadButton)

        box1.pack_start(scrolledwindow, True, True, 0)
        box1.pack_start(scrolledwindow1, False, True, 0)

        verh2_box.pack_start(box1, True, True, 0)
        verh2_box.pack_start(strip, False, True, 0)
        vm_box.pack_start(verh2_box,True,True,0)
        
        self.resize(800, 400)

        self.focus_box = 0
        self.reset()

    def file_button(self, w):
        dialog = Gtk.FileChooserDialog("Open File", self, Gtk.FileChooserAction.OPEN, 
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        res = dialog.run()
        if res == Gtk.ResponseType.OK:
            fp = open(dialog.get_filename(), 'r')
            string = fp.read()
            fp.close()
            self.textEditor.get_buffer().set_text(string)
        elif res == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    def load_button(self, w):
        tb = self.textEditor.get_buffer()
        string = tb.get_text(tb.get_start_iter(), tb.get_end_iter(), False)
        asm = Assembler()
        asm.Lex(string)
        asm.Parse()
        addr = int(self.loadaddr.get_text(), 16)
        i = 0
        for byte in asm.bytes:
            ram.Write(addr+i, byte)
            i += 1
        
        strlbl = ""
        for lbl in asm.labels:
            strlbl += "\n" + lbl + " : " + hex(asm.labels[lbl])
        self.lblLabel.set_text(strlbl)
    
    def addr_focus(self, w, e):
        self.focus_box = 0

    def hex_focus(self, w, e):
        self.focus_box = 1

    def on_botton_click(self,widget,data=1):
            input=widget.get_label()
            box = self.entry_addr
            if self.state != State.go and self.focus_box == 1:
                box = self.entry_hex
            
            if input == "Next" or input == "Prev":
                if self.state == State.exam_mem:
                    if self.focus_box == 1:
                        addr = int(self.entry_addr.get_text(),16)
                        offset = 0
                        if input == "Next":
                            WriteMemData(addr, int(self.entry_hex.get_text(),16))
                            offset = 1
                        else:
                            WriteMemData(addr, int(self.entry_hex.get_text(),16))
                            if addr != 0:
                                offset = -1

                        newaddr = '{:04x}'.format(addr+offset)
                        self.entry_addr.set_text(newaddr)
                        self.change_data()
                    self.entry_hex.grab_focus()
                elif self.state == State.exam_reg:
                    curreg = self.entry_addr.get_text()
                    if input == "Next":
                        reg = NextReg(curreg)
                    else:
                        reg = PrevReg(curreg)
                    self.entry_addr.set_text(reg)
                self.change_data()


            elif input == "Exam mem":
                self.exam_mem()
            elif input == "Reset":
                self.reset()
            elif input == "Exam reg":
                self.exam_reg()
            elif input == "Go":
                self.go()

            elif input == "Single step":
                global cu
                if self.executing:
                    if self.state != State.go:
                        self.state = State.go
                        self.entry_hex.set_editable(False)
                        self.entry_addr.set_text(self.lastAddr)
                    cu.SetPC(int(self.entry_addr.get_text(), 16))
                    cu.SingleStep()
                    self.entry_addr.set_text('{:04x}'.format(cu.GetPC()))
                    self.change_data()
            elif input == "Exec":
                if self.executing:
                    self.state = State.executing
                    cu.SetPC(int(self.entry_addr.get_text(), 16))
                    thread = Thread(target=cu.Run)
                    thread.start()
                    thread1 = Thread(target=self.on_executing)
                    thread1.daemon = True
                    thread1.start()
            else:
                if self.state == State.none:
                    self.exam_mem()
                elif self.state == State.exam_reg:
                    if input in reglist:
                        self.entry_addr.set_text(input)
                        self.change_data()
                    return
                if box.get_text_length()==box.get_max_length():
                    box.set_text(box.get_text()[1:4]+input)
                else:
                    box.set_text(box.get_text()+input)
    
    def on_executing(self):
        Gdk.threads_enter()
        self.executing = True
        self.entry_addr.set_text("----")
        self.entry_hex.set_text("--")
        Gdk.threads_leave()
        while cu.running:
            pass
        Gdk.threads_enter()
        self.reset()
        self.executing = True
        self.entry_addr.set_text('{:04x}'.format(cu.GetPC()))
        self.change_data()
        self.executing = False
        Gdk.threads_leave()

    def exam_mem(self):
        if self.state == State.executing:
            return
        if self.executing:
            self.lastAddr = self.entry_addr.get_text()
        self.entry_addr.grab_focus()
        self.state = State.exam_mem
        self.entry_addr.set_text("0000")
        self.change_data()
        self.entry_hex.set_editable(True)

    def exam_reg(self):
        if self.state == State.executing:
            return
        if self.executing:
            self.lastAddr = self.entry_addr.get_text()
        self.state = State.exam_reg
        self.entry_addr.set_text("A")
        self.change_data()
        self.entry_hex.set_editable(False)

    def reset(self):
        self.state = State.none
        self.entry_addr.set_text("-UPS")
        self.entry_hex.set_text("85")
        self.entry_hex.set_editable(False)
        self.executing = False
        self.entry_addr.grab_focus()
        self.change_data()
        cu.Reset()

    def go(self):
        if self.state == State.executing:
            return
        self.state = State.go
        self.entry_addr.set_text("0000")
        self.entry_hex.set_text("00")
        self.entry_hex.set_editable(False)
        self.executing = True

    def change_data(self):
        if self.state == State.exam_reg:
            reg = self.entry_addr.get_text()
            data = '{:02x}'.format(GetRegData(reg))
            self.entry_hex.set_text(data.upper())
        elif self.state == State.exam_mem or self.executing:
            addr = int(self.entry_addr.get_text(),16)
            data = '{:02x}'.format(GetMemData(addr))
            self.entry_hex.set_text(data.upper())
        
        self.pc_text.set_text('PC: ' + '{:04x}'.format(alu.registers['PC']))
        self.sp_text.set_text('SP: ' + '{:04x}'.format(alu.registers['SP']))
        self.flags_text.set_text('FLAGS: ' + '{:08b}'.format(alu.registers['F']))

GObject.threads_init()
Gdk.threads_init()
win=Window()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
