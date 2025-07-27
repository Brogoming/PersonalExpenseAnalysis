import pandas as pd
import numpy as np
import calendar as cal
from sklearn.linear_model import LinearRegression

def cleanData(originDataFrame):
    """
    Cleans up any null values and incorrect amounts in the data frame
    :param originDataFrame: The frame to clean up
    :return: A modified version of the original data frame
    """
    cleanFrame = originDataFrame.copy()

    for i in cleanFrame.columns.tolist():
        if pd.api.types.is_numeric_dtype(cleanFrame[i]):
            cleanFrame[i] = cleanFrame[i].fillna(0)
        else:
            cleanFrame[i] = cleanFrame[i].fillna('Unknown')

    cleanFrame['Amount'] = originDataFrame['Amount']
    cleanFrame['Amount'] = np.where( originDataFrame['Tag'] == 'Spent', -abs( cleanFrame['Amount'] ), cleanFrame['Amount'] )
    cleanFrame['Amount'] = np.where( originDataFrame['Tag'] == 'Earned', abs( cleanFrame['Amount'] ), cleanFrame['Amount'] )
    return cleanFrame

def getExpenses(originDataFrame):
    """
    Creates Columns Earned, Spent, and Transfer for each account
    :param originDataFrame: The frame where the imported data is coming from
    :return: A data frame with the data spread out into multiple columns
    """
    newFrame = pd.DataFrame( { 'Dates': originDataFrame['Dates'].drop_duplicates().reset_index( drop = True ) } )

    # Get missing dates
    startYear = pd.to_datetime( originDataFrame["Dates"] ).dt.year[0] # gets the year the data started
    endYear = pd.to_datetime( originDataFrame["Dates"] ).dt.year[len(originDataFrame["Dates"]) - 1]  # gets the year the data ended
    missingDates = pd.DataFrame( { 'Dates': pd.date_range( f'01-01-{startYear}', f'12-31-{endYear}').difference(newFrame['Dates']) } )
    missingDates['Dates'] = pd.to_datetime(missingDates['Dates']).dt.date
    newFrame = pd.concat( [newFrame, missingDates] ).sort_values('Dates').reset_index( drop = True )

    tags = ['Earned', 'Spent', 'Transfer']
    locations = originDataFrame['Location'].drop_duplicates()

    for tag in tags:
        for location in locations:
            col = f'{location} {tag}'
            originDataFrame[col] = np.where( (originDataFrame['Tag'] == tag) & (originDataFrame['Location'] == location),
                originDataFrame['Amount'], 0 )
            grouped = originDataFrame.groupby( 'Dates' )[col].sum().reset_index()
            newFrame = newFrame.merge( grouped, on = 'Dates', how = 'left' )

    # Clean up data
    newFrame = newFrame.fillna(0)

    # Account totals per date
    for location in originDataFrame['Location'].drop_duplicates().tolist():
        newFrame[f'{location} Account'] = newFrame[f'{location} Earned'].cumsum() + newFrame[f'{location} Spent'].cumsum() + newFrame[f'{location} Transfer'].cumsum()

    return newFrame

def getAmountData(originDataFrame, amountType):
    """
    Sorts the data by the amount type
    :param originDataFrame: Original data frame before any edits
    :param amountType: Either Spent or Earned
    :return: A new data frame of the amount type
    """
    newFrame = pd.DataFrame( { 'Dates': pd.to_datetime(originDataFrame['Dates']).drop_duplicates() } )
    optionalTags = originDataFrame[originDataFrame['Tag'] == amountType]['Optional Tag'].drop_duplicates()
    for tag in optionalTags:
        newFrame[tag] = np.where((originDataFrame['Tag'] == amountType) & (originDataFrame['Optional Tag'] == tag), originDataFrame['Amount'], 0 )
    return getMonthTotals(newFrame)

def getMonthTotals(originDataFrame):
    """
    Gets the totals of each column per month
    :param originDataFrame: Original data frame before any edits
    :return: A new dataframe with the sum value of amounts per month
    """
    newFrame = pd.DataFrame( { 'Months': pd.to_datetime(originDataFrame['Dates']).dt.month.drop_duplicates().sort_values().reset_index( drop=True ) } )
    for column in originDataFrame.columns.tolist():
        if column != 'Dates':
            newColumn = originDataFrame.groupby( pd.to_datetime( originDataFrame['Dates'] ).dt.month )[column].sum()
            newFrame = pd.merge( newFrame, newColumn, left_on='Months', right_on='Dates', how='left' )
    newFrame['Months'] = newFrame['Months'].apply( lambda x: cal.month_abbr[x] )
    return newFrame.reset_index( drop=True )

def predictNextSixMonths(originDataFrame):
    """
    Predicts a linear expenses for the next 6 months
    :param originDataFrame: Original data frame before any edits
    """
    originDataFrame['Timestamp'] = pd.to_datetime( originDataFrame['Dates'] ).astype( 'int64' ) // 10 ** 9
    allPredictions = []
    accountColumns = []
    last_ts = originDataFrame['Timestamp'].max()
    futureDates = pd.date_range( start=pd.to_datetime( last_ts, unit='s' ) + pd.Timedelta( days=1 ), periods=182, freq='D' )
    futureTimestamps = futureDates.astype( 'int64' ) // 10 ** 9

    for column in originDataFrame.columns.tolist():
        if 'Account' in column:
            model = LinearRegression()
            model.fit( originDataFrame['Timestamp'].values.reshape( -1, 1 ), originDataFrame[column].values )

            # Predict next 31 days
            predictions = model.predict( futureTimestamps.values.reshape( -1, 1 ) )
            allPredictions.append(predictions)
            accountColumns.append(column)

    return [originDataFrame, futureDates, allPredictions, accountColumns]
