#!/usr/bin/env python

class Gantry():
	def __init__(self, speed_factor = 1, xResolution = 64, yResolution = 64):
		"""
		Pin Definitions:
		
		XDIR is the pin that sends pulses to the driver controlling the
		direction of the X axis motor
		YDIR is the pin that sends pulses to the driver controlling the
		direction of the Y axis motor
		
		XSTEP is the pin that sends pulses to the driver controlling the X
		axis motor to make it move
		YSTEP is the pin that sends pulses to the driver controlling the Y 
		axis motor to make it move 
		
		readX is the pin that reads the XSTEP pin to keep track of the
		number of pulses being sent
		readY is the pin that reads the YSTEP pin to keep track of the 
		number of pulses being sent
		"""
		
		self.XDIR = 20
		self.XSTEP = 12
		self.YDIR = 19
		self.YSTEP = 13
		self.readX = 24
		self.readY = 21
		
		"""
		These variables will hold the directions 
		CW = Clockwise
		CCW = Counter Clockwise
		"""
		self.CW = 1
		self.CCW = 0
		
		"""
		These variables will keep track of the current position of the Gantry
		They default to 0 each time an instance of this class is declared
		"""
		
		self.currentX = 0.
		self.currentY = 0.
		self.currentPos = (self.currentX, self.currentY)
		
		"""
		These variables will be used to hold the locations of the head and tails of the fish
		"""
		self.xHead = 0.
		self.xTail = 0.
		self.yHead = 0.
		self.yTail = 0.
		
		"""
		These variables will store the current direction of the X and Y motors
		They will both default to clockwise
		"""
		self.xdir_curr = 1
		self.ydir_curr = 1 
		
		"""
		This variable will store the resolution of the motors
		They will default to 64 steps per full revolution which requires 12800 pulses
		according to the manual tha can be found at https://github.com/JorgeG30/gantry_control

		The resolution can be changed through the motors driver

		"""
		self.xResolution = xResolution
		self.yResolution = yResolution
		
		"""
		These variables will store the number of total pulses sent to both the X and Y motors
		Based on theses values, the current X and Y position of the motor is calculated.
		Pulses would be added or subtracted according to the direction. (See callback functions)
		"""
		self.xPulses = 0
		self.yPulses = 0
		
		"""
		Create resetable pulse counters to be used in Autonomous Control
		"""
		self.xPulseReset = 0
		self.yPulseReset = 0
	

		"""
		The number of pulses needed to travel 1 mm
		200 is the number of steps for this type of step motor
		"""
		self.xPulse_perRev = self.xResolution * 200
		self.yPulse_perRev = self.yResolution * 200

		self.xPulse_1mm = self.xPulse_perRev / 70. 
		self.yPulse_1mm = self.yPulse_perRev / 54.

		"""
		This variable will keep track of the user defined speed
		Speed will be a multiplier that you multiply the delay by
		The speed will be set using the getSpeed function from within the class
		The variable speed will default to 1
		"""
		# Default
		# X axis speed = 1mm / s = xPulse_1mm / s
		# Y axis speed = 1mm / s = yPulse_1mm / s

		self.speed_factor = speed_factor



	# ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ ------ 
	"""
	This function updates the current position of the gantry based on the number of pulses sent.
	This should be called everytime a pulse is sent either in the CW or CCW direction.
	"""
	def getPos(self):
		self.currentX = self.xPulses / self.xPulse_1mm
		self.currentY = self.yPulses / self.xPulse_1mm
		print('The number of X pulses: ', self.xPulses)
		#print 'Current Position: (%f, %f)' % (self.currentX, self.currentY)
		
	"""
	These functions will be called everytime it detects a pulse sent.
	They will serve as the callback functions
	"""
	def xPulseCount(self, channel):
		self.xPulseReset += 1
		if self.xdir_curr == 0:
			self.xPulses -= 1
		elif self.xdir_curr == 1:
			self.xPulses += 1
		self.getPos()
	
	def yPulseCount(self, channel):
		self.yPulseReset += 1
		if self.ydir_curr == 0:
			self.yPulses -= 1
		elif self.ydir_curr == 1:
			self.yPulses += 1
		self.getPos()
		
	"""
	This function is the callback that will receive the TTL pulse 
	from neural data collection hardware
	"""
	
	def TTLPulse(self, channel):
		pass
	
	"""
	These functions will be used to set the direction of the motor
	They will take in the difference in between the current coordinate 
	and the next coordinate
	"""
	
	def setXCurrDir(self, distance):
		if distance < 0:
			self.xdir_curr = 0
		elif distance > 0:
			self.xdir_curr = 1
	
	def setYCurrDir(self, distance):
		if distance < 0:
			self.ydir_curr = 0
		elif distance > 0:
			self.ydir_curr = 1

	
	
		
		
		
	
	
