import pandas as pd
from sklearn.linear_model import LinearRegression
from plotData import plotNextSixMonths

def predictNextSixMonths(originFrame):
	"""
	Predicts a linear expenses for the next 6 months
	:param originFrame: Frame to get predictions
	"""
	originFrame['Timestamp'] = pd.to_datetime( originFrame['Dates'] ).astype( 'int64' ) // 10 ** 9

	model = LinearRegression()
	model.fit( originFrame['Timestamp'].values.reshape( -1, 1 ), originFrame['Savings Account'].values )

	# Predict next 31 days
	last_ts = originFrame['Timestamp'].max()
	futureDates = pd.date_range( start=pd.to_datetime( last_ts, unit='s' ) + pd.Timedelta( days=1 ), periods=182, freq='D' )
	futureTimestamps = futureDates.astype( 'int64' ) // 10 ** 9
	predictions = model.predict( futureTimestamps.values.reshape( -1, 1 ) )
	plotNextSixMonths(originFrame, futureDates, predictions)
