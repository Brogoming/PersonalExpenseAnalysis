import pandas as pd
from sklearn.linear_model import LinearRegression
from plotData import plotNextSixMonths

def predictNextSixMonths(originFrame):
	"""
	Predicts a linear expenses for the next 6 months
	:param originFrame: Frame to get predictions
	"""
	originFrame['Timestamp'] = pd.to_datetime( originFrame['Dates'] ).astype( 'int64' ) // 10 ** 9
	allPredictions = []
	accountColumns = []
	last_ts = originFrame['Timestamp'].max()
	futureDates = pd.date_range( start=pd.to_datetime( last_ts, unit='s' ) + pd.Timedelta( days=1 ), periods=182, freq='D' )
	futureTimestamps = futureDates.astype( 'int64' ) // 10 ** 9

	for column in originFrame.columns.tolist():
		if 'Account' in column:
			model = LinearRegression()
			model.fit( originFrame['Timestamp'].values.reshape( -1, 1 ), originFrame[column].values )

			# Predict next 31 days
			predictions = model.predict( futureTimestamps.values.reshape( -1, 1 ) )
			allPredictions.append(predictions)
			accountColumns.append(column)

	return [originFrame, futureDates, allPredictions, accountColumns]

