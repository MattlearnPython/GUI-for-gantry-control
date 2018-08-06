from GantryControl_Class import Gantry

from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import keyboard
from time import sleep
import csv

'''
import RPi.GPIO as GPIO
import pigpio
'''

class Application():
	def __init__(self, root, gantry):
		self.gantry = gantry
		self.root = root

		# Gantry setup
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
		'''
		self.pi = pigpio.pi()

		# Set the GPIO mode for RPi.GPIO
		GPIO.setmode(GPIO.BCM)

		# Set readX and readY as inputs
		GPIO.setup(self.gantry.readX, GPIO.IN)
		GPIO.setup(self.gantry.readY, GPIO.IN)

		# Create callbacks for these pins
		GPIO.add_event_detect(self.gantry.readX, GPIO.RISING, callback = self.gantry.xPulseCount)
		GPIO.add_event_detect(self.gantry.readY, GPIO.RISING, callback = self.gantry.yPulseCount)
		'''

		# GUI widgets	
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

		"""
		# Left region: Keyboard Control
		# Right region: Autonomous Control
		"""
		left = Frame(self.root, borderwidth = 2, relief="solid")
		left.pack(side = "left", expand = True, fill = "both")

		right = Frame(self.root, borderwidth = 2, relief="solid")
		right.pack(side = "right", expand = True, fill = "both")

		right_top = Frame(right, borderwidth = 2, relief = "solid")
		right_top.pack(side = "top", expand = False, fill = "both")

		right_bottom = Frame(right, borderwidth = 2, relief = "solid")
		right_bottom.pack(side = "bottom", expand = False, fill = "both")

		"""
		Widgets on Right-top 
		"""
		selected_files = Button(right_top, text = 'Select Files to Open', width = 25, command = self.select_files)
		selected_files.pack()

		execute_files = Button(right_top, text = 'Start Movement', width = 25, command = self.execute_files)
		execute_files.pack()

		stop = Button(right_top, text = 'Pause Movement', width = 25, command = self.pause_execution)
		stop.pack()

		continue_butt = Button(right_top, text = 'Continue Movement', width = 25, command = self.continue_execution)
		continue_butt.pack()

		abort = Button(right_top, text = 'Abort', width = 25, command = self.abort)
		abort.pack()


		"""
		Widgets on Left
		"""

		# Current
		# 1.Label
		x_label = Label(left, fg = "dark green", text = "Current X Position: ")
		x_label.place(x = 90, y = 70)

		y_label = Label(left, fg = "dark green", text = "Current Y Position: ")
		y_label.place(x = 90, y = 90)

		# 2.Value: need to be updated
		self.xlabel_value = Label(left, fg = "dark green", text = str(gantry.currentX), width = 20)
		self.xlabel_value.place(x = 210, y = 70)

		self.ylabel_value = Label(left, fg = "dark green", text = str(gantry.currentY), width = 20)
		self.ylabel_value.place(x = 210, y = 90)

		# Head and tail
		# 1.Label
		xhead_label = Label(left, fg = "dark green", text = 'Current X Head Coordinate:')
		xhead_label.place(x = 34, y = 120)

		yhead_label = Label(left, fg = "dark green", text = 'Current Y Head Coordinate: ')
		yhead_label.place(x = 34, y = 140)

		xtail_label = Label(left, fg = "dark green", text = 'Current X Tail Coordinate: ')
		xtail_label.place(x = 46, y = 170)

		ytail_label = Label(left, fg = "dark green", text = 'Current Y Tail Coordinate: ')
		ytail_label.place(x = 46, y = 190)

		# 2.Vaule: need to be updates
		self.xhead_value = Label(left, fg = "dark green", text = str(gantry.xHead), width = 20)
		self.xhead_value.place(x = 210, y = 120)

		self.yhead_value = Label(left, fg = "dark green", text = str(gantry.yHead), width = 20)
		self.yhead_value.place(x = 210, y = 140)

		self.xtail_value = Label(left, fg = "dark green", text = str(gantry.xTail), width = 20)
		self.xtail_value.place(x = 210, y = 170)

		self.ytail_value = Label(left, fg = "dark green", text = str(gantry.yTail), width = 20)
		self.ytail_value.place(x = 210, y = 190)

		# Buttons
		keyboard_button = Button(left, text = 'Start Manual Control', width = 25, command = self.keyboard_control)
		keyboard_button.place(x = 100, y = 0)

		end_keyboard_button = Button(left, text = 'End Manual Control', width = 25, command = self.sendEnd)
		end_keyboard_button.place(x = 100, y = 25)

		up_button = Button(left, text = 'UP', width = 10, command = self.sendUp)
		up_button.place(x = 170, y = 300)

		down_button = Button(left, text = 'DOWN', width = 10, command = self.sendDown)
		down_button.place(x = 170, y = 350)

		left_button = Button(left, text = 'LEFT', width = 10, command = self.sendLeft)
		left_button.place(x = 80, y = 325)

		right_button = Button(left, text = 'RIGHT', width = 10, command = self.sendRight)
		right_button.place(x = 260, y = 325)

		head_button = Button(left, text = 'Record Head', width = 15, command = self.recordHead)
		head_button.place(x = 145, y = 230)

		tail_button = Button(left, text = 'Record Tail', width = 15, command =self.recordTail)
		tail_button.place(x = 145, y = 260)


		# Variables for keyboard control
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

		# These variables will be updated with the current state of the arrow buttons
		self.right_pressed = 0
		self.up_pressed = 0
		self.down_pressed = 0
		self.left_pressed = 0

		# Variable that will be checked to end keyboard control
		self.end_keyboard = 0

		# Variables that will be checked to determine head and tail position
		self.head_button_press = 0
		self.tail_button_press = 0

		# Arrays that will store the coordinates and reverse coordinates
		self.x_coordinate = []
		self.y_coordinate = []


	# Keyboard control functions
	# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

	"""
	These functions will be used to send keyboard commands via onscreen GUI buttons.
	"""
	def sendUp(self):
		self.up_pressed = True

	def sendDown(self):
		self.down_pressed = True

	def sendLeft(self):
		self.left_pressed = True

	def sendRight(self):
		self.right_pressed = True

	def sendEnd(self):
		self.end_key = True
	
	def recordHead(self):
		self.gantry.xHead = self.gantry.currentX
		self.gantry.yHead = self.gantry.currentY
		self.xhead_value.config(text = str(self.gantry.xHead), width = 20)
		self.yhead_value.config(text = str(self.gantry.yHead), width = 20)
		self.xhead_value.update()
		self.yhead_value.update()

	def recordTail(self):
		self.gantry.xTail = self.gantry.currentX
		self.gantry.yTail = self.gantry.currentY
		self.xtail_value.config(text = str(self.gantry.xTail), width = 20)
		self.ytail_value.config(text = str(self.gantry.yTail), width = 20)
		self.xtail_value.update()
		self.ytail_value.update()	

	def keyboard_control(self):
		'''
		Initialize the press variables to 0 each time keyboard control is called
		'''
		self.right_pressed = 0
		self.up_pressed = 0
		self.down_pressed = 0
		self.left_pressed = 0
		
		while True:

				self.xlabel_value.config(text = str(self.gantry.currentX))
				self.ylabel_value.config(text = str(self.gantry.currentY))
				self.xlabel_value.update()
				self.ylabel_value.update()
							
				if keyboard.is_pressed('d') or self.right_pressed:
					self.gantry.xdir_curr = self.gantry.CW
					self.pi.write(self.gantry.XDIR, self.gantry.xdir_curr)
					self.pi.write(self.gantry.XSTEP, 1)
					#sleep(.0001)
					self.pi.write(self.gantry.XSTEP, 0)
					#sleep(.0001)
					 
				if keyboard.is_pressed('a') or self.left_pressed:
					self.gantry.xdir_curr = self.gantry.CCW
					self.pi.write(self.gantry.XDIR, self.gantry.xdir_curr)
					self.pi.write(self.gantry.XSTEP, 1)
					#sleep(.0001)
					self.pi.write(self.gantry.XSTEP, 0)
					#sleep(.0001)
					
				if keyboard.is_pressed('s') or self.down_pressed:
					self.gantry.ydir_curr = self.gantry.CCW
					self.pi.write(self.gantry.YDIR, self.gantry.ydir_curr)
					self.pi.write(self.gantry.YSTEP, 1)
					#sleep(.0001)
					self.pi.write(self.gantry.YSTEP, 0)
					#sleep(.0001)
					
				if keyboard.is_pressed('w') or self.up_pressed:
					self.gantry.ydir_curr = self.gantry.CW
					self.pi.write(self.gantry.YDIR, self.gantry.ydir_curr)
					self.pi.write(self.gantry.YSTEP, 1)
					#sleep(.0001)
					self.pi.write(self.gantry.YSTEP, 0)
					#sleep(.0001)
					
				if keyboard.is_pressed('esc') or self.end_keyboard:
					break
				
				# reset and wait for mouse or keyboard input
				self.right_pressed = 0
				self.up_pressed = 0
				self.down_pressed = 0
				self.left_pressed = 0
		self.end_key = 0
			

	# Autonomous control functions
	# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

	def select_files(self):
		self.files = askopenfilenames(parent = self.root, title = 'Choose files')

	def execute_files(self):
		# TEST
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
		# read one file
		i = 0
		with open(self.files[i], 'r') as f:
			reader = csv.reader(f, delimiter = ',')
			for row in reader:
				self.x_set.append(row[0])
				self.y_set.append(row[1])

		self.autonomous_control()

	def pause_execution(self):
		self.is_pause = True

	def continue_execution(self):
		self.is_continue = True

	def abort(self):
		self.is_abort = True

	def autonomous_control(self):
		# Flags
		self.is_abort = False
		
		# Get the length of the coordinates of the current path
		num_points = len(self.x_set)
		
		# Control the speed
		#self.speed_factor = 1
		delay = .0001

		for i in range(num_points):
			# Update current position of the gantry
			self.gantry.getPos()

			cur_x = self.gantry.currentX
			cur_Y = self.gantry.currentY
			next_x = self.x_set[i]
			next_y = self.y_set[i]
			dist_x = next_x - cur_x
			dist_y = next_y - cur_y

			# Change the current direction based on the signs of the distance
			self.gantry.setXCurrDir()
			self.gantry.setYCurrDir()

			# Write the direction into pi
			self.pi.write(gantry.XDIR, gantry.xdir)	
			self.pi.write(gantry.YDIR, gantry.ydir)

			# Pulses needed to reach destination
			x_pulse_req = abs(dist_x * self.gantry.xPulse_1mm)
			y_pulse_req = abs(dist_y * self.gantry.yPulse_1mm)

			while True:
				# Approaching both
				if self.gantry.xPulseReset < x_pulse_req and self.gantry.xPulseReset < x_pulse_req:
					pi.set_bank_1((1<<gantry.XSTEP) | (1<<gantry.YSTEP))
					sleep(delay * self.speed_factor)
					pi.clear_bank_1((1<<gantry.XSTEP) | (1<<gantry.YSTEP))
					sleep(delay * self.speed_factor)

				# Approaching x, reached y
				elif self.gantry.xPulseReset < x_pulse_req:
					pi.write(self.gantry.XSTEP, 1)
					sleep(delay * self.speed_factor)
					pi.write(self.gantry.XSTEP, 0)
					sleep(delay * self.speed_factor)
					
				# Approaching y, reached x
				elif self.gantry.yPulseReset < y_pulse_req:
					pi.write(self.gantry.YSTEP, 1)
					sleep(delay * self.speed_factor)
					pi.write(self.gantry.YSTEP, 0)
					sleep(delay * self.speed_factor)

				# Pause execution
				elif self.is_pause is True:
					root.update() 
					root.update_idletasks()
					while True:
						if self.is_continue is True:
							break
					self.is_continue = False
					self.is_pause = False

				# Abort execution			
				elif self.is_abort is True:
					print('Aborting Movement')
					self.root.update() 
					self.root.update_idletasks()
					self.is_abort = False
					return None

				# Reached both
				else:
					break

				self.gantry.getPos()	
				xlabel.config(text = str(gantry.currentX))
				ylabel.config(text = str(gantry.currentY))
				xlabel.update()
				ylabel.update()

			# Reset Pulse Counters for next coordinate use
			self.gantry.xPulseReset = 0
			self.gantry.yPulseReset = 0




if __name__ == "__main__":
	# Create an instance of the Gantry Class
	gantry = Gantry()

	# GUI 
	# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
	root = Tk()
	root.title('GUI for Gantry Control')
	root.geometry('1000x500')

	app = Application(root, gantry)
	root.mainloop()
