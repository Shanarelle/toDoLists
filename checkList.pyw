from Tkinter import *
import tkFileDialog
import sys
import os

'''
  will hopefully be a list making program
  should diplay checkboxes next to lines of text and allow them to be checked
'''

def toggleCheck():
	for i in range(len(checkvariables)):
		if checkvariables[i].get() == 1:
			textlist[i].tag_add('fade', '1.0', '2.11')
			textlist[i].tag_config('fade', background='grey', overstrike=1)
		else:
			textlist[i].tag_config('fade', background='white', overstrike=0)

# saves data in specific format, using given file path
def save(filename):
	global rownumber
	if filename != '':
		data = str(rownumber) + "\n"
		for i in range(len(checkvariables)):
			data += str(i) + ": "
			data += str(checkvariables[i].get()) + ", "
			data += str(textlist[i].get('1.0', '2.11')) + "\n"
		file = open(filename, 'w')
		file.write(data)
		file.close()

#will open a dialogue box asking the user where to save the file
#will then save it in a specific format it will decipher later
def saveAsText():
	#print "save"
	'''
	file = open('list.txt', 'w')
	pickle.dump(checkvariables[i].get(), file)
	pickle.dump(textlist[i].get('1.0', '2.11'), file)
	file.close()
	'''
	global currentsave
	filename = tkFileDialog.asksaveasfilename(defaultextension='.ckl', initialfile="to-do.ckl", title="Save")
	currentsave = filename
	save(filename)
	
def saveText(event=None):
	global currentsave
	if currentsave != None:
		save(currentsave)
	else:
		saveAsText()
	
# will open and parse a given file
def openFile(filename):
	global currentsave
	currentsave = filename
	file = open(filename)
	for line in file:
		if line.isspace():
			continue
		if line.find(':') == -1:
			continue
		part = line.partition(': ')
		part2 = part[2].partition(', ')
		i = int(part[0])
		textlist[i].insert('1.0', part2[2])
		if int(part2[0]) == 1:
			checklist[i].invoke()
	file.close()
	
# will open a dialogue box asking the user what file to open
# will check that the file is in the correct format
# will recreate the state of the widgets as the file dictates
def loadText():
	#print "load"
	filename = tkFileDialog.askopenfilename(defaultextension=".ckl", title="Open")
	openFile(filename)
	
def addLine(event=None):
	global rownumber, checkvariables, checklist, textlist
	x = IntVar()				# create a variable to contain the state of the corresponding
	checkvariables.append(x)	# ... checkbutton
	y = Checkbutton(screen, text = '', variable = checkvariables[rownumber], command = toggleCheck)
	checklist.append(y)
	b = Text(screen, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
	textlist.append(b)
	checklist[rownumber].grid(row=rownumber, column=0)
	textlist[rownumber].grid(row=rownumber, column=1, sticky=W+E+N+S, padx=2)
	screen.rowconfigure(rownumber, weight=1)
	rownumber += 1
	
def removeLine(event=None):
	global rownumber, checkvariables, checklist, textlist
	checkvariables.pop()
	checklist.pop().grid_forget()
	textlist.pop().grid_forget()
	rownumber -= 1

# gives the next widget focus - called when tab is pressed
def nextWidget(event):
	currentFocus = screen.focus_get()
	newFocus = currentFocus.tk_focusNext()
	newFocus.focus_set()
	
#sys.stdout = open(os.devnull, 'w')
screen = Tk()


# create a menu attached to the top of the window
top = screen.winfo_toplevel()
menuBar = Menu(top)
top["menu"] = menuBar

# create the drop down and add items to it
dropMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=dropMenu)
dropMenu.add("command", label="save - Ctrl+s", command=saveText)
dropMenu.add("command", label="save as", command=saveAsText)
dropMenu.add("command", label="load", command=loadText)
dropMenu.add("command", label="add line - Ctrl+shift+n", command=addLine)
dropMenu.add("command", label="remove line - Ctrl+shift+d", command=removeLine)


# create a grid of checkboxes followed by text boxes
# when you select the checkbox it changes the formattting of the
#  text in the adjacent textbox
checklist = []
checkvariables = []
textlist = []
rownumber = 5
currentsave = None
# if opened from file determine number of rows
if len(sys.argv) > 1:
	file = sys.argv[1]
	openfile = open(file)
	string = openfile.readline()
	string.strip(' \n.')
	rownumber = int(string)
	#print repr(rownumber)
	openfile.close()
	

for i in range(rownumber):
	x = IntVar()				# create a variable to contain the state of the corresponding
	checkvariables.append(x)	# ... checkbutton
	y = Checkbutton(screen, text = '', variable = checkvariables[i], command = toggleCheck)
	checklist.append(y)
	b = Text(screen, height = 2, width = 30, wrap = WORD)		# add a textbox where the user can write their goal
	textlist.append(b)
	checklist[i].grid(row=i, column=0)
	textlist[i].grid(row=i, column=1, sticky=W+E+N+S, padx=2, pady=1)
	screen.rowconfigure(i, weight=1)
screen.columnconfigure(1, weight=1)
	
# load in data from the file
if len(sys.argv) > 1:
	file = sys.argv[1]
	openFile(file)

# bind events to the application
screen.unbind_class('Text', '<Tab>')	#override standard tab effect
screen.bind_all('<Tab>', nextWidget)	# move to next widget when tab is pressed
screen.bind_all('<Control-KeyPress-s>', saveText)	# save when control s is pressed
screen.bind_all('<Control-KeyPress-N>', addLine)	# shortcut to add an extra line
screen.bind_all('<Control-KeyPress-D>', removeLine)	# shortcut to remove the last line

screen.mainloop()




