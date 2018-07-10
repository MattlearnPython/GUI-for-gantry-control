from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename

class Application():
	def __init__(self, master):
		self.frame = Frame(master)
		self.frame.pack()
		self.frame.configure(background = "blue")
		self.create_widgets()

	def create_widgets(self):
		Label(self.frame, text = "This is a testing version!").grid(row = 0, columnspan = 3)

		#Label(self.frame, text = "Mouse control", fg = "black").grid(row = 1)
		# Mouse control
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
		self.up_arrow = PhotoImage(file = "up_arrow.gif")
		Button(self.frame, image = self.up_arrow, fg = "black", command = self.click_up).grid(row = 2, column = 1)

		self.left_arrow = PhotoImage(file = "left_arrow.gif")
		Button(self.frame, image = self.left_arrow, fg = "black", command = self.click_left).grid(row = 3, column = 0, sticky = W)
		self.right_arrow = PhotoImage(file = "right_arrow.gif")
		Button(self.frame, image = self.right_arrow, fg = "black", command = self.click_right).grid(row = 3, column = 2, sticky = E)

		self.down_arrow = PhotoImage(file = "down_arrow.gif")
		Button(self.frame, image = self.down_arrow, fg = "black", command = self.click_down).grid(row = 4, column = 1)


		#Label(self.frame, text = "This is a testing version!", fg = "black").grid(row = 5)
		# Keyboard control
		# ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
		Button(self.frame, text = "Keyboard Control", fg = "black", command = self.keyboard_control).grid(row = 6, columnspan = 3)
		Button(self.frame, text = "Autonomous Control", fg = "black", command = self.autonomous_control).grid(row = 7, columnspan = 3)


		Button(self.frame, text = "Quit", fg = "red", background = "blue", command = self.frame.quit).grid(row = 8, columnspan = 3)

	def keyboard_control(self):
		print("keyboard control")
	def autonomous_control(self):
		input_file = askopenfilename()
		print("autonomous control")

	def click_left(self):

		if key or left
			execute()

		print("left")
	def click_right(self):
		print("right")	
	def click_up(self):
		print("up")	
	def click_down(self):
		print("down")

	def execute
		
		
if __name__ == "__main__":
	window = Tk()
	app = Application(window)

	window.mainloop()