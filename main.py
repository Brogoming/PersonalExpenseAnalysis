import os
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from formatData import cleanData, getExpenses, predictNextSixMonths, getAmountData
from plotData import tableView, plotNextSixMonths, barPieCharts

def getFileData(uploadedFilePath):
	"""
	Gathers and cleans data based in the file imported
	:param uploadedFilePath: Path to the imported file
	:return: Cleaned up data frame
	"""
	try:
		expensesFile=pd.read_csv(uploadedFilePath, engine='pyarrow', dtype_backend='pyarrow')
		expensesFile['Dates']=pd.to_datetime(expensesFile['Dates']).dt.date
		expensesFile=cleanData(expensesFile)
		return expensesFile
	except Exception as e:
		print(f"Failed to load and clean file: {e}")

def createTab(notebook, title, contentFunc, *args):
	"""
	Creates a tab and the contents of the tab
	:param notebook: Notebook to make a frame from
	:param title: Name of the tab
	:param contentFunc: Plot function
	:param args: Arguments to feed in to the plot function
	:return: A new frame
	"""
	frame=Frame(notebook)
	contentFunc(*args, frame)  # Inject content into the frame
	notebook.add(frame, text=title)
	return frame

def categoryTabs(tabFrame, uploadedFilePath):
	"""
	Creates Original Table, Modified Table, Accounts Overview, Spent Overview, and Earned Overview tabs
	:param tabFrame: Tab of the file imported
	:param uploadedFilePath: Path to the imported file
	"""
	cateTabs=ttk.Notebook(tabFrame)
	cateTabs.pack(expand=True, fill="both")

	# Original Table
	expensesFile=getFileData(uploadedFilePath)
	createTab(cateTabs, 'Original Table', tableView, expensesFile)

	# Modified Table
	expenses=getExpenses(expensesFile)
	createTab(cateTabs, 'Modified Table', tableView, expenses)

	# Accounts Overview
	expenses, futureDates, allPredictions, accountColumns=predictNextSixMonths(expenses)
	createTab(cateTabs, 'Accounts Overview', plotNextSixMonths, expenses, futureDates, allPredictions, accountColumns)

	# Spent and Earned Tabs
	for label in ['Spent', 'Earned']:
		amountData=getAmountData(expensesFile, label)
		createTab(cateTabs, f'{label} Overview', barPieCharts, amountData, label)

	root.update_idletasks()

def addFilePath():
	"""
	Add a file tab for every file imported. This then creates our category tabs for each file
	"""
	uploadedFilePath=filedialog.askopenfilename(title="Select a file", filetypes=[("CSV Files", "*.csv")])
	if not uploadedFilePath:
		return

	fileName=os.path.basename(uploadedFilePath)
	existingTabs=[fileTabs.tab(tabId, "text") for tabId in fileTabs.tabs()]

	if fileName in existingTabs:
		print(f"Tab '{fileName}' already exists.")
		return

	tabFrame=Frame(fileTabs)
	closeButton=ttk.Button(tabFrame, text="x", command=lambda: fileTabs.forget(tabFrame))
	closeButton.pack(anchor='nw')

	fileTabs.add(tabFrame, text=fileName)
	categoryTabs(tabFrame, uploadedFilePath)
	root.update_idletasks()

def menuBar():
	"""
	Creates the menu bar for importing and exiting
	"""
	menubar=Menu(root)

	# Adding File Menu and commands
	file=Menu(menubar, tearoff=0)
	menubar.add_cascade(label='File', menu=file)
	file.add_command(label='Import', command=addFilePath)
	file.add_separator()
	file.add_command(label='Exit', command=onClose)

	# display Menu
	root.config(menu=menubar)

def onClose():
	"""
	Closes the window properly
	"""
	# Explicit cleanup
	root.quit()  # Exit the mainloop
	root.destroy()  # Destroy the root window

root=Tk()
root.title("Personal Expense Analysis")
root.state('zoomed')

menuBar()

fileTabs=ttk.Notebook(root)
fileTabs.pack(expand=True, fill="both")

# Proper close handling
root.protocol("WM_DELETE_WINDOW", onClose)

root.mainloop()
