from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from pathlib import Path
import shutil
import os

uploadedFilePath = ''

def uploadFile():
	global uploadedFilePath
	uploadedFilePath = filedialog.askopenfilename( title="Select a file",filetypes=[("CSV Files", "*.csv")] )
	if uploadedFilePath:
		print( "Uploaded file:", uploadedFilePath )
		saveButton.configure(state='active', bg='green')
	root.update_idletasks()

def saveFile():
	global uploadedFilePath
	if uploadedFilePath:
		try:
			# Copy the file
			shutil.copy( uploadedFilePath, './data' )
			print( f"File '{os.path.basename( uploadedFilePath )}' copied successfully to './data'" )
		except FileNotFoundError:
			print( f"Error: Source file '{uploadedFilePath}' not found." )
		except Exception as e:
			print( f"An error occurred: {e}" )

def selectFileFnc(*args):
	global uploadedFilePath
	print(f'./data/{selectFile.get()}')

root = Tk()
root.title("Personal Expense Analysis")
root.geometry('800x900')

Button(root, text='Upload File', border=4, bg='red', command=uploadFile).grid(row=0, column=0, sticky = 'E', padx = 2, pady =2)
saveButton = Button(root, text='Save File', border=4, bg='green', state='disabled', command=saveFile)
saveButton.grid(row=0, column=1, sticky = 'W', padx = 2, pady =2)
Label(root, text='Select File:').grid(row=1, column=0, sticky = 'E', padx = 2, pady =2)
Label(root, text='Account:').grid(row=0, column=3, sticky = 'E', padx = 2, pady =2)
Label(root, text='Amount:').grid(row=1, column=3, sticky = 'E', padx = 2, pady =2)

currentDir = Path(__file__).parent
dataDir = currentDir / 'data'
dataDir.mkdir(exist_ok=True)  # Make sure the folder exists

fileList = [f.name for f in dataDir.glob('*.csv')]
selectFile = Combobox(root, values=fileList)
selectFile.set("")
selectFile.bind("<<ComboboxSelected>>", selectFileFnc)

accountOptions = ["Savings Account", "Checking Account"] # temp until we read the file
selectAccount = Combobox(root, values=accountOptions)
selectAccount.set("")
# selectFile.bind("<<ComboboxSelected>>")

amountVar = IntVar(name="amountVar")
# messageVar.trace_add("write", disableDecoder)
amountEntry = Entry(root, width=20, textvariable=amountVar)

# Place widgets
selectFile.grid(row=1, column=1, sticky = 'W', padx = 2, pady =2)
selectAccount.grid(row=0, column=4, sticky = 'W', padx = 2, pady =2)
amountEntry.grid(row=1, column=4, sticky = 'W', padx = 2, pady =2)

Frame(root, height=60, width=1, relief='sunken', bg='black').grid(row=0, column=2, rowspan=2)
Frame(root, height=1, width=800, bd=1, relief='sunken', bg='black').grid(row=2, column=0, columnspan=5)

root.mainloop()