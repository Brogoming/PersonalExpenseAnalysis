import pandas as pd
import os
from formatData import cleanData, getExpenses, getIncomeData, getSpentData
from plotData import plotAccounts

pd.set_option('display.max_rows', None)        # Show all rows
pd.set_option('display.max_columns', None)     # Show all columns
pd.set_option('display.width', None)           # Don't wrap lines
pd.set_option('display.max_colwidth', None)    # Show full content in cells

dataDir = './data'

def promptForDataFile():
    """
    Prompts the user for the file they want analyzed
    :return: the correct file path
    """
    all_entries = os.listdir(dataDir)

    dataFiles = [entry for entry in all_entries if os.path.isfile(os.path.join(dataDir, entry))]
    print('What file do you want to analyze?')
    for i, fileName in enumerate( dataFiles ):
        print( f'{i}: {fileName}' )
    userInput = input(f'Type index number: ')

    while not userInput.isdigit() or not (0 <= int(userInput) < len(dataFiles)):
        userInput = input(f'Invalid Response, try again: ')

    return os.path.join(dataDir, dataFiles[int(userInput)])

def plotOptions(originFrame):
    print('\nPlot Data: \nAccounts Overtime = 0\nIncome Overtime = 1\nSpent Overtime = 2')
    userInput = input( 'Type index number: ' )

    while not userInput.isdigit() or not (0 <= int( userInput ) < 3):
        userInput = input( f'Invalid Response, try again: ' )

    userInput = int(userInput)
    if userInput == 0:  # Accounts Overtime
        expenses = getExpenses( originFrame )  # formats and cleans the expenses table
        plotAccounts( expenses )
    elif userInput == 1:  # Income Overtime
        incomeDate = getIncomeData(originFrame) # formats and cleans the income table
        pass
    elif userInput == 2:  # Spent Overtime
        spentData = getSpentData(originFrame) # formats and cleans the spent table
        pass

def main():
    while True:
        fileName = promptForDataFile()

        try:
            expensesFile = pd.read_csv( fileName, engine = 'pyarrow', dtype_backend = 'pyarrow' )
            expensesFile['Dates'] = pd.to_datetime( expensesFile['Dates']).dt.date
            expensesFile = cleanData( expensesFile )
        except Exception as e:
            print( f"Failed to load and clean file: {e}" )
            continue

        plotOptions(expensesFile)

        userInput = input('\nDo you want to analyze another file (yes/no)? ').lower()
        while userInput not in ['yes', 'no']:
            userInput = input(f'Invalid Response, try again: ')

        if 'no' == userInput:
            print('Have a nice day!')
            break

if __name__ == "__main__":
    main()