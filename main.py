#!/usr/bin/python3

from gi.repository import Gtk
class DemoWindow(Gtk.Window):
	def __init__(self):
		self.search_string=''
		self.dicto={'This':00,
					'Is':'01',
					'So':10,
					'Cool':11,
					'Right':20,
					'It':21,
					'can':22,
					'even':23,
					'filter':24,
					'The':25,
					'codes':26,
					'to':27,
					'locate':28,
					'your':29,
					'query':30}	
		self.mnem=list(self.dicto.keys())
		Gtk.Window.__init__(self,title="Demo example")
		self.set_border_width(10)
		vm_box=Gtk.Box(spacing=10)
		self.add(vm_box)
		
		#subh_box=Gtk.Box(oriention=Gtk.Orientation.VERTICAL,spacing=6)
		verh1_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
		verh2_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=1)
		
		self.entry_addr=Gtk.Entry()
		self.entry_addr.set_text('')
		self.entry_addr.set_max_length(4)
		self.entry_addr.set_alignment(1)
		
		self.entry_hex=Gtk.Entry()
		self.entry_hex.set_text('')
		self.entry_hex.set_max_length(2)
		self.entry_hex.set_alignment(1)
		
		vscroll_window=Gtk.ScrolledWindow()
		vscroll_window.set_min_content_height(400)
		vscroll_window.set_min_content_width(50)
		self.codes_list=Gtk.ListBox()
		self.codes_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
		self.codes_list.connect('row-selected',self.on_list_selection)
		self.organize_codes()
		vscroll_window.add_with_viewport(self.codes_list)
		
		self.query=Gtk.Entry()
		self.query.set_alignment(1)
		self.query.connect('key-press-event',self.key_pressed)
		
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
		KeyPadGrid.attach_next_to(button_prev,buttonH,Gtk.PositionType.BOTTOM,2,1)
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
		
		verh2_box.pack_start(vscroll_window,True,True,0)
		verh2_box.pack_start(self.query,True,True,0)
		
		vm_box.pack_start(verh1_box,True,True,0)
		vm_box.pack_start(verh2_box,True,True,0)
		
	def on_botton_click(self,widget,data=1):
			input=widget.get_label()
			if self.entry_addr.get_text_length()==self.entry_addr.get_max_length():
				self.entry_addr.set_text(self.entry_addr.get_text()[1:4]+input)
			else:
				self.entry_addr.set_text(self.entry_addr.get_text()+input)

	def organize_codes(self):
		for key,value in self.dicto.items():
			row=Gtk.ListBoxRow()
			hbox=Gtk.Box(spacing=10)
			mnem=Gtk.Label(label=key)
			code=Gtk.Label(label=value)
			hbox.pack_start(mnem,True,True,0)
			hbox.pack_start(code,True,True,0)
			row.add(hbox)
			self.codes_list.add(row)
	
	def on_list_selection(self,x,y):
		selection=self.codes_list.get_selected_row().get_index()
		self.entry_hex.set_text(str(self.dicto[self.mnem[selection]]))
	
	def key_pressed(self,widget,event):
		if(event.hardware_keycode==ord('\b')):
			self.search_string=self.search_string[:-1]
		else:
			self.search_string+=event.string
		self.codes_list.set_filter_func(self.filter_code,self.search_string)
		
	def filter_code(self,row,data):
		if data in self.mnem[row.get_index()]:
			return True
		else:
			return False
		
win=DemoWindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
