from Tkinter import *
from checkListclass import *
import tkFileDialog
import sys
import os

'''### declarations ###########################'''
ACTIVE_COLOR = '#a0a0a0'
INACTIVE_COLOR = '#e0e0e0'
'''############################################'''

def change_tab():
	slaves = root.grid_slaves(row=1)
	slaves[0].grid_remove()
	focus = tab_focus.get()
	framelist[focus].grid(row=1, sticky=N+S+E+W)
	dropMenu.entryconfigure(3, command=framelist[focus].addLine)
	dropMenu.entryconfigure(4, command=framelist[focus].removeLine)
	
	root.bind_all('<Tab>', framelist[focus].nextWidget)	# move to next widget when tab is pressed
	root.bind_all('<Control-KeyPress-N>', framelist[focus].addLine)	# shortcut to add an extra line
	root.bind_all('<Control-KeyPress-D>', framelist[focus].removeLine)	# shortcut to remove the last line
	

	
def saveText(filename, event=None):
	file = open(filename, 'w')
	file.write("Header ")
	for i in range(len(framelist)):
		if i != 0:
			file.write(",")
		data = framelist[i].rownumber
		file.write(str(data))
	file.write("\n")
	for frame in framelist:
		file.write("\r\nNewTab\r\n")
		file.write(frame.save())
	file.close()

#will open a dialogue box asking the user where to save the file
#will then save it in a specific format it will decipher later
def saveAs(event=None):
	global currentsave
	filename = tkFileDialog.asksaveasfilename(defaultextension='.ckl', initialfile="to-do.ckl", title="Save")
	currentsave = filename
	saveText(filename)
	
	
def save(event=None):
	global currentsave
	if currentsave == None:
		saveAs()
	else:
		saveText(currentsave)



# will recreate the state of the widgets as the file dictates
def openFile(filename, event=None):
	global currentsave
	currentsave = filename
	index = -1
	file = open(filename)
	for line in file:
		if line.find('Header') != -1:	#not data
			continue
		if line.find('NewTab') != -1:
			index+= 1
		else:
			framelist[index].parseLine(line)
	
	
# will open a dialogue box asking the user what file to open
def load(event=None):
	#print "load"
	filename = tkFileDialog.askopenfilename(defaultextension=".ckl", title="Open")
	self.openFile(filename)
	

	
root = Tk()

# create the tab labels
tab_container = Frame(root)
tab_container.grid(row=0, ipady=2, sticky=E+W)

tab_focus = IntVar()
imm_tab = Radiobutton(tab_container, text='Immediate Goals', variable=tab_focus, value=0, command=change_tab, indicatoron=0, selectcolor=ACTIVE_COLOR)
imm_tab.pack(side=LEFT, padx=1)
med_tab = Radiobutton(tab_container, text='Medium-Term Goals', variable=tab_focus, value=1, command=change_tab, indicatoron=0, selectcolor=ACTIVE_COLOR)
med_tab.pack(side=LEFT, padx=1)
long_tab = Radiobutton(tab_container, text='Big Picture', variable=tab_focus, value=2, command=change_tab, indicatoron=0, selectcolor=ACTIVE_COLOR)
long_tab.pack(side=LEFT, padx=1)

currentsave = None
framelist = []

# if opened from file determine number of rows for each tab
if len(sys.argv) > 1:
	file = sys.argv[1]
	openfile = open(file)
	string = openfile.readline()
	string = string.strip('Header \n.')
	split = string.partition(',')
	while split[2] != '':
		framelist.append(CheckList(root, rows=split[0]))
		split = split[2].partition(',')
	else:
		framelist.append(CheckList(root, rows=split[0]))
	openfile.close()
else:
	for i in range(3):
		framelist.append(CheckList(root))


framelist[0].grid(row=1, sticky=N+S+E+W)

# load in data from file if present
if len(sys.argv) > 1:
	file = sys.argv[1]
	openFile(file)



# create a menu attached to the top of the window
top = root.winfo_toplevel()
menuBar = Menu(top)
top["menu"] = menuBar

		
# create the drop down menu and add items to it
dropMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=dropMenu)
dropMenu.add("command", label="load", command=load)
dropMenu.add("command", label="save - Ctrl+s", command=save)
dropMenu.add("command", label="save as", command=saveAs)
dropMenu.add("command", label="add line - Ctrl+shift+n", command=framelist[0].addLine)
dropMenu.add("command", label="remove line - Ctrl+shift+d", command=framelist[0].removeLine)


# bind events to the application
root.unbind_class('Text', '<Tab>')	#override standard tab effect
root.bind_all('<Control-KeyPress-s>', save)	# save when control s is pressed
# the bindings that are active panel specific
root.bind_all('<Tab>', framelist[0].nextWidget)	# move to next widget when tab is pressed
root.bind_all('<Control-KeyPress-N>', framelist[0].addLine)	# shortcut to add an extra line
root.bind_all('<Control-KeyPress-D>', framelist[0].removeLine)	# shortcut to remove the last line


root.mainloop()
# video.attach_window(frame.window_id())


