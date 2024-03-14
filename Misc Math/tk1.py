import customtkinter as ctk
from tkinter import *





root = Tk()

root.geometry('500x900')

class CB():
	def __init__(self,master,values=[],height=25,width=200,max_values_displayed=10):
		self.height = height
		self.width = width
		self.max_values_displayed = max_values_displayed
		self.values = values
		self.scrollable_frame = ctk.CTkScrollableFrame(master=master,height = height, width = width-20)
		self.scrollable_frame._scrollbar.configure(height=0)
		self.entry_sv = StringVar()
		self.entry_sv.trace('w',lambda var, index, mode: self.filter_display_items(self.entry.get()))
		self.entry = ctk.CTkEntry(master=master,height=height,width=width,textvariable=self.entry_sv)
		self.display_items = []
		self.entry.bind('<FocusIn>',self.post_frame)
		self.entry.bind('<FocusOut>',self.unpost_frame)
		self.filter_display_items('')
	def filter_display_items(self,term):
		matched_items = [item for item in self.values if term.lower() in item.lower()]
		[item.destroy() for item in self.display_items]
		self.display_items = []
		if len(matched_items) <= self.max_values_displayed:
			self.display_items = [ctk.CTkButton(master=self.scrollable_frame,height=self.height,width=self.width,text=item,command = lambda item=item: self.set_entry(item)) for item in ['']+matched_items]
		if len(matched_items)==1: self.set_entry(matched_items[0])
		self.post_frame(None)
	def set_entry(self,new_val):
		self.entry.delete(0,END)
		self.entry.insert(0,new_val)
	def place(self,x=0,y=0):
		self.entry.place(x=x,y=y)
		self.x = x
		self.y = y
	def unpost_frame(self,e):
		self.scrollable_frame.place_forget()
		[display_item.pack_forget() for display_item in self.display_items]
		
	def post_frame(self,e):
		print(self.display_items)
		if len(self.display_items) <=2: self.unpost_frame(None)
		else:
			[display_item.pack() for display_item in self.display_items]
			self.scrollable_frame.configure(height=self.height*min(5,len(self.display_items)))
			self.scrollable_frame.place(x=self.x,y=self.y)
			

alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

vals = [alph[:i+1] for i in range(len(alph))]
c = CB(root,vals,25,200)
c.place(x=250,y=250)

b = ctk.CTkEntry(master=root)
b.place(x=0,y=0)
"""
class C(ctk.CTkComboBox):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.bind('<FocusIn>',lambda e: self._open_dropdown_menu())
		self.
c = C(master=root,values = [f'Value {i}' for i in range(1,6)])
c.place(x=250,y=250)
"""


root.mainloop()