import pandas as pd
import calendar as cal

pd.set_option('display.max_columns', None)

def main():
    expenses = pd.read_csv('./data/expenses.csv')
    expenses.fillna(0, inplace=True)
    expenses['Date'] = pd.to_datetime(expenses['Date'])

    # Get account difference
    expenses['Account1'] = expenses['Income1'].cumsum() - expenses['Spent1'].cumsum()
    expenses['Account2'] = expenses['Income2'].cumsum() - expenses['Spent2'].cumsum()

    # Get totals
    expenses['TotalIncome'] = expenses['Income1'] + expenses['Income2']
    expenses['TotalSpent'] = expenses['Spent1'] + expenses['Spent2']
    expenses['TotalAccount'] = expenses['Account1'] + expenses['Account2']

    # Per month
    months = pd.DataFrame({'Month': expenses['Date'].dt.month.drop_duplicates().sort_values().reset_index(drop=True)})
    for i in expenses.columns.tolist():
        if i != 'Date':
            if i in ['TotalAccount','Account1','Account2']:
                newColumn = expenses.groupby(expenses['Date'].dt.month)[i].last()
                months = pd.merge(months, newColumn, left_on='Month', right_on='Date', how='left')
            else:
                newColumn = expenses.groupby(expenses['Date'].dt.month)[i].sum()
                months = pd.merge(months, newColumn, left_on='Month', right_on='Date', how='left')
    months['Month'] = months['Month'].apply(lambda x: cal.month_abbr[x])

if __name__ == "__main__":
    main()