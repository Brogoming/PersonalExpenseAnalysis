import pandas as pd
import os
from formatData import cleanData, getExpenses, getEarnedData, getSpentData
from linearPredictions import predictNextSixMonths
from plotData import pieBar, plotAccounts

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
    """
    Prompts the user for options to view the data
    :param originFrame: The frame where the imported data is coming from
    """
    print('\nPlot Data: \nAccounts Overtime = 0\nIncome Overtime = 1\nSpent Overtime = 2\nPredict next month\'s expenses = 3')
    userInput = input( 'Type index number: ' )

    while not userInput.isdigit() or not (0 <= int( userInput ) < 4):
        userInput = input( f'Invalid Response, try again: ' )

    userInput = int(userInput)
    try:
        if userInput == 0:  # Accounts Overtime
            expenses = getExpenses( originFrame )  # formats and cleans the expenses table
            plotAccounts( expenses )
        elif userInput == 1:  # Income Overtime
            earnedDate = getEarnedData(originFrame) # formats and cleans the income table
            pieBar( earnedDate, 'Income' )
        elif userInput == 2:  # Spent Overtime
            spentData = getSpentData(originFrame) # formats and cleans the spent table
            pieBar( spentData, 'Spent' )
        elif userInput == 3: # Predictions
            expenses = getExpenses( originFrame )  # formats and cleans the expenses table
            predictNextSixMonths(expenses)
            pass
    except Exception as e:
        print( f"Failed to load and plot the data: {e}" )

def main():
    """
    Runs the main process
    """
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