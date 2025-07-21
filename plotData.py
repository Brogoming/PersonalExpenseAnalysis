import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plotAccounts(originFrame):
	fig, ax = plt.subplots(figsize=(10,5))
	for column in originFrame.columns.tolist():
		if 'Account' in column:
			ax.plot(originFrame['Dates'], originFrame[column], '.-',label=column)

	ax.xaxis.set_major_locator( mdates.MonthLocator() )
	ax.xaxis.set_major_formatter( mdates.DateFormatter( '%b %Y' ) )
	fig.autofmt_xdate()

	plt.title('Accounts Overtime')
	plt.xlabel('Dates')
	plt.ylabel('Amount (usd)')

	plt.legend()
	plt.show()

def pieBar(originFrame, amountType):
	"""
	Shows both a pie chart and a bar chart in one panel
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	fig, ax = plt.subplots(1,2, layout='constrained', figsize=(15,8))
	barChart(ax, originFrame, amountType)
	pieChart( ax, originFrame, amountType )

	plt.show()

def pieChart(ax, originFrame, amountType):
	"""
	Plots the data on a pie chart
	:param ax: axis
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	categories = originFrame.columns.tolist()
	categories.pop(0) # removes the months column
	values = []

	for column in categories:
		values.append(abs(originFrame[column].cumsum().sum()))

	ax[1].pie(values, labels=categories, autopct='%.2f %%')
	ax[1].set_title( f'{amountType} Overall by Category' )

def barChart(ax, originFrame, amountType):
	"""
	Plots the data on a bar chart
	:param ax: axis
	:param originFrame: Data to plot
	:param amountType: Name of the data being plotted
	:return: void
	"""
	labels = originFrame['Months']
	x = np.arange( len( labels ) )  # the label locations
	width = 1 / len( originFrame.columns.tolist() )  # the width of the bars
	multiplier = 0

	for column in originFrame.columns.tolist():
		if column != 'Months':
			offset = width * multiplier
			rects = ax[0].bar( x + offset, abs( originFrame[column] ), width, label=column )
			ax[0].bar_label( rects, padding=3 )
			multiplier += 1

	ax[0].set_ylabel( 'Amounts (usd)' )
	ax[0].set_title( f'{amountType} per Month' )
	ax[0].set_xticks( x + width, labels )
	ax[0].legend()

def plotNextSixMonths(originFrame, futureDates, allPredictions, accountColumns):
	"""
	Plots out what is predicted for the next 6 months
	:param originFrame: The original data
	:param futureDates: The next 6 months
	:param allPredictions: All predicted values
	:param accountColumns: column names of the accounts
	"""
	fig, ax = plt.subplots(figsize=(10, 5))
	for i, column in enumerate(accountColumns):
		ax.plot( originFrame['Dates'], originFrame[column], '.-', label=f'{column} Actual' )
		ax.plot( futureDates, allPredictions[i], '.-', label=f'{column} Prediction' )
	plt.legend()
	plt.xlabel( 'Date' )
	plt.ylabel( f'Account Total' )
	plt.title( f'Account Forecast Over Time' )
	plt.grid( True )
	plt.show()