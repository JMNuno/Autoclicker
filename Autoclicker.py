#! python3
# JMN

import tkinter
from tkinter import ttk
import ctypes
import time

# bugs: unable to update values while clicking is happening due to focus_set() but can't delete that without breaking esc hotkey
# bugs: esc hotkey only works when screen is set



class Clicker():
    def __init__(self):
        self.DEFAULT_AMOUNT = 100 # Default amount of clicks
        self.DEFAULT_SPEED = 100 # Default speed in ms
        self.status = False # Test to see whether to continue running or not
        
        # Initialize
        self.root = tkinter.Tk()
        self.mainframe = ttk.Frame(self.root)
        self.mouse = ctypes.windll.user32
        self.root.title('Autoclicker')

        # Set default values
        self.amount = tkinter.StringVar() # number of clicks
        self.amount.set(self.DEFAULT_AMOUNT)
        self.speed = tkinter.StringVar() # click interval in ms
        self.speed.set(self.DEFAULT_SPEED)
    
        # Mainframe labels, entries, and buttons
        self.amount_label = ttk.Label(self.mainframe, text = 'Number of clicks \n (Set to 0 for infinite) \n (Hit esc to stop - Broken)').grid(column = 1, row = 1, sticky = tkinter.W)
        self.speed_label = ttk.Label(self.mainframe, text = 'Click interval \n (in ms)').grid(column = 1, row = 2, stick = tkinter.W)
        self.amount_entry = ttk.Entry(self.mainframe, textvariable = self.amount, width =5).grid(column =2, row = 1)
        self.speed_entry = ttk.Entry(self.mainframe, textvariable = self.speed, width = 5).grid(column = 2, row =2 )
        self.start_button = ttk.Button(self.mainframe, text = 'Start', width = 10, command = self.state_true).grid(column = 1, row =3, columnspan = 2, stick = tkinter.W)
        self.stop_button = ttk.Button(self.mainframe, text = 'Stop', width =10, command = self.state_false).grid(column = 2, row = 3, columnspan = 2, stick=tkinter.E)

        self.progress_text = tkinter.StringVar()
        self.progress_label = ttk.Label(self.mainframe, textvariable = self.progress_text, width = 20).grid(column = 1, row = 4)
        
        # Key Bindings
        self.mainframe.bind('<Escape>', self.clicked_escape)
        
        # Pack and run
        self.mainframe.pack()
        self.run()
        

    def run(self):
        t1 = time.clock() # clocks are used to measure times between clicks; time.sleep() would slow down window updating
        self.counter = 0

        # Main loop
        while True:
            # Update
            self.entered_speed = int(self.speed.get())/1000
            self.entered_amount = int(self.amount.get())
            self.root.update()
            
        
            if self.status == True:
                self.mainframe.pack()
                t2 = time.clock()

                # check if enough time has passed and still need more clicks
                if self.entered_amount == 0 and t2 - t1 > self.entered_speed: # For infinite clicks
                    self.mouse_click()
                    t1 = time.clock()
                elif self.counter < self.entered_amount and t2-t1 > self.entered_speed:
                    self.mouse_click()
                    self.counter += 1
                    t1 = time.clock()
                elif self.counter >= self.entered_amount and t2 - t1 > self.entered_speed: #reset counter once exceeded
                    self.state_false()

                self.mainframe.focus_set() #currently broken but needed to register esc key... 
                    


            
    def state_true(self):
        self.progress_text.set('Running...')       
        self.counter = 0
        self.status = True

    def state_false(self):
        self.progress_text.set('Paused')
        self.counter = 0
        self.status = False
        
    def clicked_escape(self, event):
        print('hit escape')
        self.state_false()
        
    def mouse_click(self):
        # left mouse button down and up
        self.mouse.mouse_event(2, 0, 0, 0, 0) # down
        self.mouse.mouse_event(4, 0, 0, 0, 0) # up

    def bug_check(self, loc='\t'):
        print('loc: ', loc , '\tstatus: ', self.status, 'counter', '\tcounter')


t1 = Clicker()


