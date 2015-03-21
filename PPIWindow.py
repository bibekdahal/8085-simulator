#!/usr/bin/python3
from gi.repository import Gtk
import math
import time

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="8255 PPI")
        main_vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox=Gtk.Box(spacing=7)
        self.add(hbox)
        
        self.ports=[['0' for x in range(8)] for x in range(3)]
        self.drawing_area=Gtk.DrawingArea()
        self.drawing_area.set_size_request(200,20)
        self.drawing_area.connect('draw',self.expose_handler)
        
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        entry1=Gtk.Entry()
        entry1.set_name('Entry1')
        entry2=Gtk.Entry()
        entry2.set_name('Entry2')
        entry3=Gtk.Entry()
        entry3.set_name('Entry3')
        entry1.connect('changed',self.post_input)
        entry2.connect('changed',self.post_input)
        entry3.connect('changed',self.post_input)

        vbox.pack_start(entry1,True,True,0)
        vbox.pack_start(entry2,True,True,0)
        vbox.pack_start(entry3,True,True,0)

        strb1=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        strb2=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        label1=Gtk.Label('Strobe A')
        label2=Gtk.Label('Strobe B')
        
        switch1=Gtk.Button('S1')
        switch2=Gtk.Button('S2')
        #switch1.set_name('SWITCHA')
        #switch2.set_name('SWITCHB')
        #switch1.set_active(False)
        #switch2.set_active(False)
        
        #switch1.connect('notify::active',self.on_switch_activated)
        #switch2.connect('notify::active',self.on_switch_activated)

        switch1.connect('clicked', self.on_switch_activated)
        switch2.connect('clicked', self.on_switch_activated)
        
        strb1.pack_start(label1,True,True,0)
        strb1.pack_start(switch1,True,True,0)
        
        strb2.pack_start(label2,True,True,0)
        strb2.pack_start(switch2,True,True,0)
        
        mini=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        mini.pack_start(strb1,True,True,0)
        mini.pack_start(strb2,True,True,0)
        
        hbox.pack_start(self.drawing_area,True,True,0)
        hbox.pack_start(vbox,True,True,0)
        hbox.pack_start(mini,True,True,0)

        
    def expose_handler(self,widget,cr):
        x=0
        for j in range(3):
            for i in range(8):
                
                if self.ports[j][i]=='1':
                    cr.set_source_rgb(1,0,0)
                else:
                    cr.set_source_rgb(0,0,0)
                cr.arc(20*(i+1),11*(j+1)+x,7, 0, 2*math.pi)
                cr.fill()
            x+=17
        
    def post_input(self,widget):
        input=widget.get_text()
        if not is_hex(input):
            input = '0'
        if widget.get_name()=='Entry1':
            self.ports[0]="{0:8b}".format(int(input,16))
        elif widget.get_name()=='Entry2':
            self.ports[1]="{0:8b}".format(int(input,16))
        elif widget.get_name()=='Entry3':
            self.ports[2]="{0:8b}".format(int(input,16))
        self.drawing_area.queue_draw()
    
    def on_switch_activated(self,switch):
        print('switch '+switch.get_label()+' was clicked')
        
win = MyWindow()
win.set_border_width(4)
win.set_size_request(200,60)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
