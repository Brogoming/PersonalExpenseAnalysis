from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from pathlib import Path
import shutil
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from formatData import cleanData, getExpenses, getEarnedData, getSpentData
from linearPredictions import predictNextSixMonths
from plotData import plotNextSixMonths, pieBar

uploadedFilePath = ''
selectedFile = ''
accountOptions = []
graphCanvas = None  # Global variable to store current canvas

def plotGraphs(expensesFile):
    global graphCanvas

    if graphCanvas:
        graphCanvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(3,2, layout='constrained', figsize=(7,7))

    # Account totals
    expenses = getExpenses(expensesFile)  # formats and cleans the expenses table
    [expenses, futureDates, allPredictions, accountColumns] = predictNextSixMonths(expenses)
    plotNextSixMonths(expenses, futureDates, allPredictions, accountColumns, ax, fig)

    # TODO fix the other graphs
    # Spent Graph
    spentData = getSpentData(expensesFile)  # formats and cleans the spent table
    pieBar(spentData, 'Spent', ax, fig)

    # Earned Graph
    earnedDate = getEarnedData(expensesFile)  # formats and cleans the income table
    pieBar(earnedDate, 'Income', ax, fig)

    graphCanvas = FigureCanvasTkAgg(fig, master=root)
    graphCanvas.draw()
    graphCanvas.get_tk_widget().grid(row=3, column=0, columnspan=5, padx=5, pady=5)
    root.update_idletasks()

def uploadFile():
    global uploadedFilePath
    global selectedFile
    uploadedFilePath = filedialog.askopenfilename( title="Select a file",filetypes=[("CSV Files", "*.csv")] )
    if uploadedFilePath:
        print( "Uploaded file:", uploadedFilePath )
        try:
            # Copy the file
            shutil.copy(uploadedFilePath, './data')
            print(f"File '{os.path.basename(uploadedFilePath)}' copied successfully to './data'")
        except FileNotFoundError:
            print(f"Error: Source file '{uploadedFilePath}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        selectedFile = f'./data/{os.path.basename(uploadedFilePath)}'
    root.update_idletasks()

def selectFileFnc(*args):
    global selectedFile, accountOptions
    selectedFile = selectFileBox.get()
    if '.csv' in selectedFile:
        try:
            expensesFile = pd.read_csv(f'./data/{selectedFile}', engine='pyarrow', dtype_backend='pyarrow')
            expensesFile['Dates'] = pd.to_datetime(expensesFile['Dates']).dt.date
            expensesFile = cleanData(expensesFile)
            accountOptions = expensesFile['Location'].drop_duplicates().tolist()
            if len(accountOptions) > 0:
                plotGraphs(expensesFile)
                selectAccountBox.configure(state='active', values=accountOptions)
                root.update_idletasks()
        except Exception as e:
            print(f"Failed to load and clean file: {e}")

def selectAccountFnc(*args):
    account = selectAccountBox.get()
    if account != '':
        amountEntry.configure(state='normal')

root = Tk()
root.title("Personal Expense Analysis")
root.geometry('800x900')

Button(root, text='Upload File', border=4, bg='red', command=uploadFile).grid(row=0, column=0, sticky = 'E', padx = 2, pady =2)
Label(root, text='Select File:').grid(row=1, column=0, sticky = 'E', padx = 2, pady =2)
Label(root, text='Account:').grid(row=0, column=3, sticky = 'E', padx = 2, pady =2)
Label(root, text='Amount:').grid(row=1, column=3, sticky = 'E', padx = 2, pady =2)

currentDir = Path(__file__).parent
dataDir = currentDir / 'data'
dataDir.mkdir(exist_ok=True)  # Make sure the folder exists

fileList = [f.name for f in dataDir.glob('*.csv')]
selectFileBox = Combobox(root, values=fileList)
selectFileBox.set("")
selectFileBox.bind("<<ComboboxSelected>>", selectFileFnc)

selectAccountBox = Combobox(root, values=accountOptions, state='disabled')
selectAccountBox.set("")
selectAccountBox.bind("<<ComboboxSelected>>", selectAccountFnc)

amountVar = IntVar(name="amountVar")
# messageVar.trace_add("write", disableDecoder)
amountEntry = Entry(root, width=20, textvariable=amountVar, state='disabled')

# Place widgets
selectFileBox.grid(row=1, column=1, sticky = 'W', padx = 2, pady =2)
selectAccountBox.grid(row=0, column=4, sticky = 'W', padx = 2, pady =2)
amountEntry.grid(row=1, column=4, sticky = 'W', padx = 2, pady =2)

Frame(root, height=60, width=1, relief='sunken', bg='black').grid(row=0, column=2, rowspan=2)
Frame(root, height=1, width=800, bd=1, relief='sunken', bg='black').grid(row=2, column=0, columnspan=5)

root.mainloop()