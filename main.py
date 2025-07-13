import pandas as pd
import os
from formatData import getMonthlyExpenses, cleanData, getExpenses

pd.set_option('display.max_rows', None)        # Show all rows
pd.set_option('display.max_columns', None)     # Show all columns
pd.set_option('display.width', None)           # Don't wrap lines
pd.set_option('display.max_colwidth', None)    # Show full content in cells

def getFile():
    """
    Prompts the user for the file they want analyzed
    :return: teh correct file path
    """
    all_entries = os.listdir('./data')

    dataFiles = [entry for entry in all_entries if os.path.isfile(os.path.join('./data', entry))]
    print('What file do you want to analyze?')
    [print(f'{i}: {fileName}') for i, fileName in enumerate(dataFiles)]
    userInput = input(f'Type index number: ')

    while not userInput.isdigit() or not (0 <= int(userInput) < len(dataFiles)):
        userInput = input(f'Invalid Response, try again: ')

    return f"data/{dataFiles[int(userInput)]}"

def main():
    while True:
        fileName = getFile()

        expensesFile = pd.read_csv(fileName, engine='pyarrow', dtype_backend='pyarrow')
        expensesFile['Dates'] = pd.to_datetime(expensesFile['Dates']).dt.date
        expensesFile = cleanData(expensesFile)

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