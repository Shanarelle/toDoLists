from Tkinter import *
import tkFileDialog
import sys
import os

'''
  will hopefully be a list making program
  should diplay checkboxes next to lines of text and allow them to be checked
'''
class DropList( Frame ):
	def __init__( self, parent, **options ):
		if options.has_key('rows'):
			self.rownumber = int(options.get('rows'))
			del options['rows']
		else:
			self.rownumber = 5		#should be specified in the options argument

		Frame.__init__(self, parent, **options)
		
		
		# create a grid of checkboxes followed by text boxes
		# when you select the checkbox it changes the formattting of the
		#  text in the adjacent textbox
		self.checklist = []
		self.checkvariables = []
		self.textlist = []
		self.dropvariables = []
		self.dropbuttons = []
		self.droptext = []
		self.subnumbers = []
		self.currentsave = None

		for j in range(self.rownumber):
			x = IntVar()
			self.dropvariables.append(x)
			y = Button(self, text = '>', variable = self.dropvariables[j], command = self.toggleDrop)
			self.dropbuttons.append(y)
			b = Text(self, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
			self.droptext.append(b)
			self.dropbuttons[j].grid(row=j, column=1)
			self.droptext[j].grid(row=j, column=2, columnspan=2, sticky=W+E+N+S, padx=2, pady=1)
			self.rowconfigure(j, weight=1)
		#fix how to get subnumbers later
			self.subnumbers.append(1)
			
			for i in range(self.subnumbers[j]):
				x = IntVar()				# create a variable to contain the state of the corresponding
				self.checkvariables.append(x)	# ... checkbutton
				y = Checkbutton(self, text = '', variable = self.checkvariables[i], command = self.toggleCheck)
				self.checklist.append(y)
				b = Text(self, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
				self.textlist.append(b)
				self.checklist[i].grid(row=i, column=1)
				self.textlist[i].grid(row=i, column=2, sticky=W+E+N+S, padx=2, pady=1)
				self.rowconfigure(i, weight=1)
			self.columnconfigure(2, weight=1)

		
	def toggleCheck(self):
		for i in range(len(self.checkvariables)):
			if self.checkvariables[i].get() == 1:
				self.textlist[i].tag_add('fade', '1.0', '2.11')
				self.textlist[i].tag_config('fade', background='grey', overstrike=1)
			else:
				self.textlist[i].tag_config('fade', background='white', overstrike=0)

	def toggleDrop(self):
		for i in range(len(self.dropvariables)):
			if self.dropvariables[i].get() == 1:
				print "drop " + repr(i) + " pressed"
			
				
	# saves data in specific format, using given file path
	def save(self):
		data = str(self.rownumber) + "\n"
		for i in range(len(self.checkvariables)):
			data += str(i) + ": "
			data += str(self.checkvariables[i].get()) + ", "
			data += str(self.textlist[i].get('1.0', '2.11')) + "\n"
		return data
		
	# will open and parse a given file
	def parseLine(self,line):
		if line.isspace():
			return
		if line.find(':') == -1:
			return
		part = line.partition(': ')
		part2 = part[2].partition(', ')
		i = int(part[0])
		self.textlist[i].insert('1.0', part2[2])
		if int(part2[0]) == 1:
			self.checklist[i].invoke()
		
	def addLine(self,event=None):
		x = IntVar()				# create a variable to contain the state of the corresponding
		self.checkvariables.append(x)	# ... checkbutton
		y = Checkbutton(self, text = '', variable = self.checkvariables[self.rownumber], command = self.toggleCheck)
		self.checklist.append(y)
		b = Text(self, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
		self.textlist.append(b)
		self.checklist[self.rownumber].grid(row=self.rownumber, column=0)
		self.textlist[self.rownumber].grid(row=self.rownumber, column=1, sticky=W+E+N+S, padx=2)
		self.rowconfigure(self.rownumber, weight=1)
		self.rownumber += 1
		
	def removeLine(self,event=None):
		self.checkvariables.pop()
		self.checklist.pop().grid_forget()
		self.textlist.pop().grid_forget()
		self.rownumber -= 1

	# gives the next widget focus - called when tab is pressed
	def nextWidget(self,event):
		currentFocus = self.focus_get()
		newFocus = currentFocus.tk_focusNext()
		newFocus.focus_set()
	
#sys.stdout = open(os.devnull, 'w')




