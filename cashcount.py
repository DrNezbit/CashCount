import os
from datetime import timezone,datetime,timedelta

line1="#"*38 ; line2="="*38
header="#\t   Drawer Count   \t     #"
help_str="(x) or (q) to quit \t\t     #\n(+) or (enter) for next \t     #\n(-) or (space) for back \t     #\n(clear) to clear \t\t     #"
class RegCount():
	def __init__(self):
		self.index=0
		self.do_change=True
		self.do_rolls=False
		self.do_bundles=False
		self.chart= {
			"pennies\t" : 1 , "penny rolls" : 50, 
			"nickles\t" : 5 , "nickle rolls" : 200,
			"dimes  \t" : 10 , "dime rolls" : 500,
			"quarters\t" : 25 , "quarter rolls" : 1000,
			"ones    \t" : 100 , "ones bundle": 2000 ,
			"fives    \t" : 500 , "fives bundle": 10000 ,
			"tens    \t" : 1000 , "tens bundle": 20000 ,
			"twenties\t" : 2000 , "twentys bundle": 40000 ,
			"fiftys  \t" : 5000 , "fiftys bundle": 100000 ,
			"hundreds\t" : 10000 , "hundreds bundle": 200000 }
		self.currency=[(k,v,0) for k,v in self.chart.items()]
		
	def setup_count(self):
		os.system("clear")
		change=input("Count coins (y/n) (y)?: ")
		if change.lower()=="n": self.do_change=False
		else: self.do_change=True
		rolls=input("Count rolls (y/n) (n)?: ")
		if rolls.lower()=="y": self.do_rolls=True
		else: self.do_rolls=False
		bundles=input("Count bundles of 20 (y/n) (n)?: ")
		if bundles.lower()=="y": self.do_bundles=True
		else: self.do_bundles=False
		if not self.do_change:
			self.currency=[x for x in self.currency if x[0].rstrip() not in ["pennies","nickles","dimes","quarters"]]
		if not self.do_rolls:
			self.currency=[x for x in self.currency if "rolls" not in x[0]]
		if not self.do_bundles:
			self.currency=[x for x in self.currency if "bundle" not in x[0]]
		
	def show_current(self):
		os.system("clear")
		now=datetime.now().strftime(
			"#\t%A, %b %d %Y\t     #\n#\t      %I:%M %p\t\t     #")
		show_list=[
			f"#    {x.capitalize()} \t{z} \t${y*z*.01:.2f}" for x,y,z in self.currency]
		print(line1,header,now,line1,
			*show_list,line1,self.get_total(),line1,sep="\n")
		
	def get_total(self):
		total = sum([x*y for d,x,y in self.currency])
		total=f"##\t\tTotal: \t${total*.01:.2f}"
		return total
		
	def get_input(self,retry=False):
		denom,value,amount=self.currency[self.index]
		show=f"{denom.capitalize()} \t{amount} \t${value*amount*.01:.2f}"
		if not retry: print(help_str)
		print(line2,show,line2,sep="\n")
		if retry: print("not a number!".upper())
		user_in=input(f"Enter # of {denom.rstrip().capitalize()}: ")
		return user_in
		
	def run(self):
		self.setup_count()
		while self.index < len(self.currency):
			self.show_current()
			denom,value,amount=self.currency[self.index]
			amount=self.get_input()
			if amount.lower() in ["x","q"]: break
			elif amount.lower() in [" ","-","space"]: self.index-=1
			elif amount.lower() in ["","+","enter"]: self.index+=1
			elif amount.lower() in ["clear"]:
				self.currency=[(k,v,0) for k,v in self.chart.items()] ; self.index=0
				self.setup_count() ; continue
			else:
				while not amount.isdecimal(): 
					self.show_current()
					amount=self.get_input(True)
					if amount.lower() in ["x","q"]:  
						self.index=len(self.currency)+2 ; break
				if self.index==len(self.currency)+2: continue
				self.currency[self.index]=denom,value,int(amount)
				self.index+=1
			if self.index==len(self.currency): self.index=0
			elif self.index==-1: self.index=len(self.currency)-1
		self.show_current()

if __name__=="__main__":	
	RegCount=RegCount()
	RegCount.run()
