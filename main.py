import pandas as pd
import os
from formatData import getMonthlyExpenses, cleanData, getExpenses

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

def main():
    while True:
        fileName = promptForDataFile()

        try:
            expensesFile = pd.read_csv( fileName, engine = 'pyarrow', dtype_backend = 'pyarrow' )
            expensesFile['Dates'] = pd.to_datetime( expensesFile['Dates'] ).dt.date
            expensesFile = cleanData( expensesFile )
        except Exception as e:
            print( f"Failed to load and clean file: {e}" )
            continue

        expenses = getExpenses(expensesFile)
        monthlyExpenses = getMonthlyExpenses(expenses)
        print(monthlyExpenses)

        userInput = input('Do you want to analyze another file (yes/no)? ').lower()
        while userInput not in ['yes', 'no']:
            userInput = input(f'Invalid Response, try again: ')

        if 'no' == userInput:
            print('Have a nice day!')
            break

if __name__ == "__main__":
    main()