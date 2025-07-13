import pandas as pd
import numpy as np
import calendar as cal

def cleanData(originFrame):
    """
    Cleans up any null values and incorrect amounts in the data frame
    :param originFrame: The frame to clean up
    :return: A modified version of the original data frame
    """
    cleanFrame = originFrame.copy()
    for i in cleanFrame.columns.tolist():
        if pd.api.types.is_numeric_dtype(cleanFrame[i]):
            cleanFrame[i] = cleanFrame[i].fillna(0)
        else:
            cleanFrame[i] = cleanFrame[i].fillna('')

    cleanFrame['Amount'] = originFrame['Amount']
    cleanFrame['Amount'] = np.where( originFrame['Tag'] == 'Spent', -abs( cleanFrame['Amount'] ), cleanFrame['Amount'] )
    cleanFrame['Amount'] = np.where( originFrame['Tag'] == 'Earned', abs( cleanFrame['Amount'] ), cleanFrame['Amount'] )
    return cleanFrame

def getExpenses(originFrame):
    """
    Creates Columns Earned, Spent, and Transfer for each account
    :param originFrame: The frame where the imported data is coming from
    :return: A data frame with the data spread out into multiple columns
    """
    newFrame = pd.DataFrame( { 'Dates': originFrame['Dates'].drop_duplicates().reset_index( drop = True ) } )

    tags = ['Earned', 'Spent', 'Transfer']
    locations = originFrame['Location'].drop_duplicates()

    for tag in tags:
        for location in locations:
            col = f'{location} {tag}'
            originFrame[col] = np.where( (originFrame['Tag'] == tag) & (originFrame['Location'] == location),
                originFrame['Amount'], 0 )
            grouped = originFrame.groupby( 'Dates' )[col].sum().reset_index()
            newFrame = newFrame.merge( grouped, on = 'Dates', how = 'left' )

    # Accounts totals per date
    for location in originFrame['Location'].drop_duplicates().tolist():
        newFrame[f'{location} Account'] = newFrame[f'{location} Earned'].cumsum() + newFrame[f'{location} Spent'].cumsum() + newFrame[f'{location} Transfer'].cumsum()
    return newFrame

def getMonthlyExpenses(originFrame):
    """
    Group data by month
    :param originFrame: The frame data is coming from
    :return: New monthly expense data frame
    """
    months = pd.DataFrame({'Month': pd.to_datetime(originFrame['Dates']).dt.month.drop_duplicates().sort_values().reset_index(drop=True)})
    for i in originFrame.columns.tolist():
        if i != 'Dates':
            if "Account" in i:
                newColumn = originFrame.groupby(pd.to_datetime(originFrame['Dates']).dt.month)[i].last()
            else:
                newColumn = originFrame.groupby(pd.to_datetime(originFrame['Dates']).dt.month)[i].sum()
            months = pd.merge(months, newColumn, left_on='Month', right_on='Dates', how='left')
    months['Month'] = months['Month'].apply(lambda x: cal.month_abbr[x])
    return months.reset_index(drop=True)