title="""Cash Counter v2 by DrNezbit"""
from tkinter import *
from tkinter import messagebox

BS = 20 # BS = BUNDLE SIZE = # of bills in bundles

"""" chart = { "name" : (single value, roll/bundle value) } """
chart = {"pennies" : (1 ,50) , "nickles" : (5 , 200) ,
				"dimes" : (10 , 500) , "quarters" : (25 ,1000) ,
				"ones" : (100 , 100*BS) , "fives" : (500 , 500*BS) ,
				"tens" : (1000 , 1000*BS) , "twenties" : (2000 , 2000*BS) ,
				"fiftys" : (5000 , 5000*BS) , "hundreds" : (10000 , 10000*BS) }

class GUI(Tk): # GUI CLASS

	class Row: # ROW CLASS
		"""Build with (name, singles_entry, rolls_entry, and total_label)"""
		def __init__(self, name: str, singles: Entry, rolls: Entry, total: Label):
			self.singles = singles ; self.rolls = rolls ; self.total = total
			self.single_val, self.roll_val = chart[name]
		def get_total(self) -> int:
			"""Calculate row total and set row total label"""
			singles_in, rolls_in= self.singles.get(), self.rolls.get()
			singles= int(singles_in) if singles_in.isdigit() else 0
			rolls= int(rolls_in) if rolls_in.isdigit() else 0
			row_total = singles*self.single_val + rolls * self.roll_val
			self.total.configure(text=f"$ {(row_total*0.01):.2f}")
			return row_total
	
	def __init__(self): 
		super().__init__() ; self.bg_color = "gray60"
		self.title(title) ; self.geometry("1000x1200")
		self.resizable(False,False)
		self.configure(background=self.bg_color)
		self.column=(0,250,475,700)
		self.row=tuple([100+80*x for x in range(11)])
		self.singles_list, self.roll_list= [] , []
		self.currency_list=[self.build_row(name,x+1) for x,name in enumerate(chart.keys())]
		self.total_count=self.setup_frame()
		self.TAB_ORDER=[w.lift() for w in self.singles_list+self.roll_list]
		
	def setup_frame(self) -> Label:
		"""Add header, total label, and buttons to frame, return total label"""
		header_font = ("MS Sans Serif", 16, "bold")
		self.add_label(text="Cash Count", coords=( 200,0),font=header_font)
		self.add_label(text="Single", coords=(200,self.row[0]+15))
		self.add_label(text="Roll/Bundle" ,coords=(430,self.row[0]+15))
		self.add_label(text="Total", coords=(700,self.row[0]+15))
		total_lbl=self.add_label("", coords=(self.column[2],1000), width=19, show_relief=True)
		Button(text="Clear", bg="gray80", fg="black", width=14, command=self.clear).place(x=10, y= 1100)
		Button(text="Exit", bg="red", fg="black", width=16, command=self.exit).place(x=475, y= 1100)
		self.singles_list[0].focus()
		return total_lbl
		
	def add_label(self, text:str, coords:tuple=(0,0), width:int=10, height:int=1, font:tuple= ("MS Sans Serif", 8, "bold"), show_relief=False) -> Label:
		"""Create and return a label"""
		relief = "raised" if show_relief else "flat"
		lbl=Label(self, text=text, width=width, height=height, font=font, background=self.bg_color, justify="center", bd=5, relief=relief)
		lbl.place(x=coords[0],y=coords[1]) # x = horizontal / y = vertical
		return lbl
			
	def add_input(self, coords:tuple=(0,0)) -> Entry:
		"""Create and return an entry box"""
		entry=Entry(self, width=6, justify="center", bd=5, relief="ridge")
		entry.place(x=coords[0], y=coords[1])
		entry.bind("<FocusIn>", self.show_totals)
		entry.bind("<Return>", lambda entry: entry.widget.tk_focusNext().focus())
		return entry
	
	def build_row(self, row_name: str, num: int) -> Row:
		"""Construct a row from name and row number"""
		row=self.row[num]
		self.add_label(row_name.capitalize(), coords=(self.column[0],row))
		singles=self.add_input(coords=(self.column[1],row))
		rolls=self.add_input(coords=(self.column[2],row))
		total=self.add_label("",coords=(self.column[3],row),show_relief=True)
		self.singles_list.append(singles) ; self.roll_list.append(rolls)
		built_row=self.Row(row_name, singles, rolls, total)
		return built_row

	def show_totals(self, _: None) -> None:
		"""Show total count on total label"""
		counted=sum([c.get_total() for c in self.currency_list])
		self.total_count.configure(text=f"Total: $ {(counted*0.01):.2f}")

	def clear(self) -> None:
		"""Confirm, clear all entry boxes, and set focus to beginning"""
		c=messagebox.askokcancel("Confirm","Clear?", icon="warning")
		if c is None: return # User clicked "Cancel"
		elif c: # User clicked "Ok"
			_ = [x.delete(0,END) for x in self.singles_list+self.roll_list]
			self.singles_list[0].focus()
			
	def exit(self) -> None:
		"""Confirm and exit GUI"""
		c=messagebox.askokcancel("Confirm","Exit?", icon="warning")
		if c is None: return # User clicked "Cancel"
		elif c: self.destroy() # User clicked "Ok"
		
if __name__ == "__main__": GUI().mainloop()