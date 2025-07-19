import pandas as pd
import numpy as np
import calendar as cal
from datetime import datetime

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
            cleanFrame[i] = cleanFrame[i].fillna('Unknown')

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

    # Get missing dates
    startYear = pd.to_datetime( originFrame["Dates"] ).dt.year[0] # gets the year the data started
    endYear = pd.to_datetime( originFrame["Dates"] ).dt.year[len(originFrame["Dates"]) - 1]  # gets the year the data ended
    missingDates = pd.DataFrame( { 'Dates': pd.date_range( f'01-01-{startYear}', f'12-31-{endYear}').difference(newFrame['Dates']) } )
    missingDates['Dates'] = pd.to_datetime(missingDates['Dates']).dt.date
    newFrame = pd.concat( [newFrame, missingDates] ).sort_values('Dates').reset_index( drop = True )

    tags = ['Earned', 'Spent', 'Transfer']
    locations = originFrame['Location'].drop_duplicates()

    for tag in tags:
        for location in locations:
            col = f'{location} {tag}'
            originFrame[col] = np.where( (originFrame['Tag'] == tag) & (originFrame['Location'] == location),
                originFrame['Amount'], 0 )
            grouped = originFrame.groupby( 'Dates' )[col].sum().reset_index()
            newFrame = newFrame.merge( grouped, on = 'Dates', how = 'left' )

    # Clean up data
    newFrame = newFrame.fillna(0)

    # Account totals per date
    for location in originFrame['Location'].drop_duplicates().tolist():
        newFrame[f'{location} Account'] = newFrame[f'{location} Earned'].cumsum() + newFrame[f'{location} Spent'].cumsum() + newFrame[f'{location} Transfer'].cumsum()

    return newFrame

def getIncomeData(originFrame):
    """
    Gets the different types of income earned
    :param originFrame: The frame where the imported data is coming from
    :return: A new dataframe with the different types of income spread out
    """
    newFrame = pd.DataFrame( { 'Dates': originFrame['Dates'].drop_duplicates().reset_index( drop = True ) } )
    filteredRows = originFrame[originFrame['Tag'] == 'Income']
    optionalTags = filteredRows['Optional Tag'].drop_duplicates()
    for tag in optionalTags:
        newFrame[tag] = np.where((originFrame['Tag'] == 'Income') & (filteredRows['Optional Tag'] == tag), originFrame['Amount'], 0 )

    return newFrame

def getSpentData(originFrame):
    """
    Gets the different types of expenditures
    :param originFrame: The frame where the imported data is coming from
    :return: A new dataframe with the different types of expenditures spread out
    """
    newFrame = pd.DataFrame( { 'Dates': originFrame['Dates'].drop_duplicates().reset_index( drop = True ) } )
    filteredRows = originFrame[originFrame['Tag'] == 'Spent']
    optionalTags = filteredRows['Optional Tag'].drop_duplicates()
    for tag in optionalTags:
        newFrame[tag] = np.where((originFrame['Tag'] == 'Spent') & (originFrame['Optional Tag'] == tag), originFrame['Amount'], 0 )

    return newFrame
