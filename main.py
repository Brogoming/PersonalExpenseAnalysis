import pandas as pd
import numpy as np
import calendar as cal

pd.set_option('display.max_rows', None)        # Show all rows
pd.set_option('display.max_columns', None)     # Show all columns
pd.set_option('display.width', None)           # Don't wrap lines
pd.set_option('display.max_colwidth', None)    # Show full content in cells

def accountColumns(originFrame, newFrame):
    for tag in originFrame['Tag'].drop_duplicates().tolist():
        for location in originFrame['Location'].drop_duplicates().tolist():
            originFrame[f'{location} {tag}'] = np.where(originFrame['Tag'] == tag, np.where(originFrame['Location'] == location, originFrame['Amount'], 0), 0)
            spent = originFrame.groupby('DateOnly')[f'{location} {tag}'].sum().reset_index()
            newFrame = newFrame.merge(spent, left_on='Dates', right_on='DateOnly', how='left')
        originFrame[tag] = np.where(originFrame['Tag'] == tag, originFrame['Amount'], 0)
        newFrame = newFrame.drop(columns=['DateOnly_x', 'DateOnly_y'])
    return newFrame

def main():
    expensesFile = pd.read_csv('./data/expensesV2.csv')
    expensesFile['Dates'] = pd.to_datetime(expensesFile['Dates'])
    expensesFile['DateOnly'] = expensesFile['Dates'].dt.date
    expenses = pd.DataFrame({'Dates': expensesFile['DateOnly'].drop_duplicates().reset_index(drop=True)})

    expenses = accountColumns(expensesFile, expenses)

    # Accounts
    for location in expensesFile['Location'].drop_duplicates().tolist():
        expenses[f'{location} Account'] = expenses[f'{location} Earned'].cumsum() + expenses[f'{location} Spent'].cumsum() + expenses[f'{location} Transfer'].cumsum()

    print(expenses)

if __name__ == "__main__":
    main()