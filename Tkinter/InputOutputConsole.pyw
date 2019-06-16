from tkinter import *

class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		self.display_label = Label(self, text="Enter value to square:")
		self.display_label.grid(row=0, column=0)
		
		self.input_field = Entry(self, bd = 5)	
		self.input_field.grid(row=0,column=1)	
		
		self.result_label = Label(self, text="Result will be here:")
		self.result_label.grid(row=1, column=0)
		
		self.calculation_button = Button(self, text="Square!", command=self.calculation)
		self.calculation_button.grid(row=3,column=3)
		
		self.quit_button = Button(self, text="Quit", command=self.master.destroy)
		self.quit_button.grid(row=4,column=10)			
		
	def calculation(self):
		new_val = int(self.input_field.get())**2
		self.result_label['text'] = new_val		
		self.input_field.delete('0', 'end')
		self.input_field.insert('0', str(new_val))

if __name__ == "__main__":
	app = Application()
	app.mainloop()